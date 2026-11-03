# Subagent: GATE-M2 qa (GATE-M2 qa)

Source: `agent-aa4a52d9261d6e025.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T12:53:42.021Z

You are the QA member of the M2 gate panel in /Users/arsis/zlayt-pm-project, pinned to commit 0c24f5f. Act as a reviewer only: write no product code and edit no tests. You may write only reviews/GATE-M2-qa.md.

Verify the ship bar (docs/CONTRACT.md §8.2 and spec/REQUIREMENTS.md ship-bar rows, with D-046) against the committed evidence: the three live 3-runs evals/reports/20261102T113305Z.md, 115041Z and 120809Z (source 63e18ed, clean tree), plus controls-20261102T123937Z.md (bea3984). Check that each row of the ship bar is met, that each report names its commit with a clean tree, and that the per-run directories exist.

Commits after 63e18ed changed the trim (T-128), lexicon_scan (T-132), lexicon.yaml (T-133) and the export gate (T-134). On a `git archive 0c24f5f` copy, run the fixture eval and the unit suite. Judge whether those changes could move the live ship-bar numbers, and say whether a fresh confirming live 3-run at 0c24f5f is needed before the m2 tag. Also report that evals/reports/calibration.json has only been regenerated on the fixture backend.

Apply the verdict rule exactly: a blocker means fail, a major means changes, otherwise pass. Write reviews/GATE-M2-qa.md with a ```json block of real values: card "GATE-M2", persona qa, model claude-sonnet-5-5, verdict, findings (each with severity and evidence), exercised. Reply in 3 lines.

### User / tool · 2026-11-02T12:53:42.026Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:53:43.990Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git status --short | head && ls evals/reports | tail -30 && grep -n \"8.2\" -A40 docs/CONTRACT.md | head -90"
}
````

### User / tool · 2026-11-02T12:53:44.126Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:53:44.877Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"ship\" spec/REQUIREMENTS.md | head -40; grep -n \"D-046\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -50"
}
````

### User / tool · 2026-11-02T12:53:44.979Z

**tool result**
````
120:| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. No short-cite mode (D-002). | UT: for every statement and amount line in `letter_text`, the quoted excerpt is a substring of the input after normalization (100%, ship bar 1). Headings and the total line are fixed text. | UT + EV `grounding_rate` |
137:| R-CO-3 | **Nothing in the output that is not in the records.** | Ship bar items 1 and 4. On the sample case every `must_not` item in `evals/golden` holds (no fixed range), including: no disc herniation caused by the collision; "may represent degenerative change" not turned into "degenerative" or "traumatic"; no PT total; the two accident dates not merged; "concussion without loss of consciousness" kept as written. Any hit is a blocker. | EV (negative assertions) + PR (claims-adjuster) |
153:| R-SU-3 | One-page product note. Checklist: the 7 required contents are present as headings (problem and user; what was built; what was cut and why; ship bar with 3–5 testable criteria, how tested, what was found; where AI can fail and how design handles it; model/code split; three metrics, each with a "tells you" line); exactly 3 post-launch metrics; renders to 1 page (≤ 650 words). Numbers in the note equal the latest eval report. | Checklist run by the writer self-check, then PR (hiring-panel, product-manager). | PR |
168:**Why not the others.** PDF upload puts unverifiable extraction upstream of the grounding check. The confidence indicator already ships as `verified / needs_review / rejected`. A firm-voice paragraph is generated prose that would need its own verification.
319:## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
321:These five are the product note's "good enough to ship" criteria. Metric names are proposed; qa owns the final names in `evals/run`, and updates this table by card if they differ.
331:Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).
373:| 6 | `docs/CONTRACT.md` §5 M2 | "qa injects 20"; closed as permanent. The ship bar here is a rate over the file and the product note quotes the rate. CONTRACT is never edited. | none | closed |
54:| D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
55-| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
56-| D-048 | Language routing fails safe (2026-11-02, after T-085 r2): a record or line runs as English only when it is **confidently English** (enough English function and clinical words, and no non-English evidence). Everything else is Spanish if confidently Spanish, otherwise LANGUAGE_UNCERTAIN: needs_review, labeled, and never passes on English token checks alone. On mixed lines, the English **and** Spanish token and qualifier checks both run (union), so a dropped 'posible' is caught whichever language leads. Routing gets a held-out measurement set. | Two rounds of heuristic detection let fresh Spanish and other-language lines through as unlabeled English. | T-085 legal-nurse r2 |
57-| D-049 | Billing completeness is decided by a code accounting pass (2026-11-02, after T-083 r3): every money-shaped token in a billing record ($-prefixed, a number with two decimals, or a no-cents figure in an amount column) must be accounted for as a parsed row, an unreconciled line, an excluded rate or an on-row 'unclear'. If any token is unaccounted for, the provider is complete: false and the record is listed. Repeated summary rows (e.g. two balance-forward lines) are all listed, never overwritten. On-row 'unclear' with complete: false is acceptable (nothing is lost). | Three rounds of per-format parsing still let bare figures vanish with complete: true; a token-level accounting pass makes silent loss impossible regardless of format. | T-083 staff r3 |
58-| D-050 | Non-English is never auto-verified (2026-11-02, §7.4 after T-085 r3): every item from a record routed Spanish or LANGUAGE_UNCERTAIN is needs_review with the label 'AI translation — check against the original'. The Spanish code checks and the translation judge still run and their failures are shown, but passing them never yields 'verified'. The paralegal's accept is the gate. English routing keeps its normal ladder. | Three rounds showed heuristic Spanish/Portuguese/Italian routing and cue lists keep leaking (4/41 dropped hedges, 1/27 misroutes on fresh lines); making the human the only verifier for translated text removes the silent-pass risk instead of chasing word lists. | T-085 legal-nurse r3 |
59-| D-051 | Code checks bind accept for **every** item (2026-11-02, T-098 review blocker): an item whose current summary fails any D-034/D-047/D-022 code check (e.g. an AI draft 'Pain 5/10' over a quote without 5/10) cannot be accepted, single or batch (422 with the reason; the paralegal must edit it to match the quote), and the export gate blocks it if such a state exists anyway. Only the judge step is exempt for human wording (D-045b); the code rung never is. | A one-click accept exported an invented number. | T-098 staff r1 F1 |
60-| D-052 | Billing ships as a **cited line listing without provider totals** (2026-11-02, §7.4 as pre-declared on T-083). Each parsed billing line is shown with its verbatim excerpt and classification (charge, adjustment, payment, rate, unclear), and unreconciled lines are listed; no billed/paid/balance totals and no 'complete' badge are computed or shown. The existing case-level charge total (D-019, stated charges only) is unchanged. | Five review rounds kept finding ways a per-provider total could silently omit or overwrite a figure; a listing cannot hide a missing line. | T-083 staff r5 |
61-| D-053 | Nothing the model proposes is silently dropped (2026-11-02, T-094 review blocker). A model-only flag or conflict that the judge rejects, or a model-proposed conflict that no code candidate confirms (the no-candidate rule applies to conflicts only; ADR-020), goes to the **could-not-verify tray** with the judge's reason; it is never a flag and never reaches the letter. The eval scores precision on emitted flags only (tray items are not assertions), and reports tray counts separately; R-CO-7's flag-set signature covers flags, not tray items. Conflict candidates from code (T-094) remain the only path to a conflict *flag*; recall gaps in the code rules are listed in SCOPE_CUTS until covered. | Suppressing rejected items to raise precision hid model output from the paralegal, against R-FL-3 and the ladder. | T-094 staff r1 |
62-| D-054 | Summary clauses the quote does not support are removed by code (2026-11-02, after T-094 r2). Before judging, code splits an AI summary into clauses; a clause is removed only when it adds salient content the excerpt lacks: a number or month, a side or a negation (only in a clause sharing no content word with the excerpt), or a procedure/device/drug, body-part or diagnosis term not covered by a word of the same family in the excerpt (amended T-112 r2: faithful paraphrases and abbreviation expansions stay; whole clauses only, never leaving a fragment; e.g. 'splint fitted' when the excerpt is only the pain sentence is removed), and the removal is shown in the item trace ('removed from the summary: not in the quote'). If nothing supported remains, the item goes to the could-not-verify tray. The judge then checks what is left. No prompt change, no fixture re-record. | Ship-bar item 4 flapped ~1 run in 3 on case_02 because the model sometimes summarized beyond its own excerpt; trimming by code is deterministic and keeps 'every statement traces to a verbatim excerpt'. | T-094 r2 handoff |
63-| D-055 | Gaps never exclude records by guessing (2026-11-02, after T-116 r2). Gap endpoints are computed over all dated records, as before T-116. When a gap starts or ends at a record that looks administrative (intake form, records request, bill, affidavit, by header), the gap carries a visible warning ('this gap ends at an intake form, not a visit; check whether treatment continued') and the paralegal decides. No record is silently dropped from gap math. | Two rounds of label heuristics still excluded real visits (', fax', 'records request' in a visit label), inventing gaps; a warning cannot invent a gap. | T-116 paralegal r2 |
64-| D-056 | Amends D-029 (2026-11-02, T-115): curated fixtures may hand-shape extraction and narrative outputs for the demo, but **judge answers are never scripted**: every judge answer the demo or eval replays is a real recorded model output, and a curated file may never shadow a recording for the same key. tests/unit/test_curated_fixtures.py enforces it (empty allow-list). | Scripted judge answers make the ladder's second check fictional; four had been written by hand, one overriding a real recording. | T-115 staff r1/r2 |
65-| D-057 | Rule-filtered model proposals are listed, not dropped (2026-11-02, after T-113). A model-proposed flag that a code rule filters out (e.g. D-032 `objective_negative`: a normal finding is not a flag) goes to a collapsed, counted "Filtered by rule" group in the could-not-verify tray with the rule named; it is never in the timeline or letter and needs no action. | D-053 says nothing the model proposes is silently dropped; trays full of normal findings would be noise, so they are listed collapsed with a count. | T-113 backend question |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:53:47.229Z

**tool call — Bash**
````
{
 "command": "sed -n 315,335p spec/REQUIREMENTS.md; for r in 20261102T113305Z 20261102T115041Z 20261102T120809Z; do echo \"=== $r\"; cat evals/reports/$r.md | head -120; done"
}
````

### User / tool · 2026-11-02T12:53:47.340Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:53:49.095Z

**tool call — Bash**
````
{
 "command": "sed -n 319,335p spec/REQUIREMENTS.md | cut -c1-900; for r in 20261102T113305Z 20261102T115041Z 20261102T120809Z; do echo \"=== $r\"; wc -c evals/reports/$r.md; head -60 evals/reports/$r.md | cut -c1-300; ls evals/reports/runs | grep -i ${r:0:15}; done"
}
````

### User / tool · 2026-11-02T12:53:49.214Z

**tool result (error)**
````
Exit code 1
## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)

These five are the product note's "good enough to ship" criteria. Metric names are proposed; qa owns the final names in `evals/run`, and updates this table by card if they differ.

| # | Criterion (CONTRACT §8.2) | Number | Measured by | Run with | R-IDs |
|---|---|---|---|---|---|
| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, dates; exported items) + export unit test | `python -m evals.run`; `pytest tests/unit` | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| 2 | **Recall** | ≥ 95% of golden timeline entries and ≥ 95% of golden dollar amounts captured across the eval set | `entry_recall`, `amount_recall` | `python -m evals.run` | R-TL-1, R-TL-7, R-CH-1 |
| 3 | **Flags** | Per flag type (gap, conflict, pre_existing, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% of every item in `hallucinations.jsonl` (today 40, so at least 33). CONTRACT §5 M2 still says "qa injects 20"; the rate governs permanently and the product note quotes the rate. Seeded J3/J4 control sets must also catch every seeded wrong item with 0 false agrees (D-046). | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-TL-10, R-CH-2, R-CH-7, R-CO-3, R-CO-7 |
| 5 | **Reviewability** | Paralegal persona completes the sample case end to end and scores "I could verify every claim quickly" ≥ 4/5. E2E export test green. | `reviews/<card>-paralegal.md`, key `scores.verify_quickly` (1–5, D-015) ≥ 4; `pytest tests/e2e` (letter block holds accepted entries and charges only, no flag content; `needs_review` first; dismissed never exports; edits labeled; decisions survive reload) | persona review + `pytest tests/e2e` | R-RV-1 to R-RV-6, R-RV-8, R-RV-9, R-EX-1 to R-EX-9 |

Other gates (not ship-bar numbers, still required): `python tools/check_secrets.py` clean; `tools/install_test.sh` under 5 minutes (R-CO-4).

Rule for the product note: report what the eval **found**, including misses, not just the targets.

---
=== 20261102T113305Z
   12613 evals/reports/20261102T113305Z.md
# Eval report 2026-11-02T11:33:05Z

**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6`, tree clean.

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (237 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.965 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `claude-cli`, 10 golden cases, source commit `63e18ed413`)

- Verified items matched the record 83/84 times in testing on the claude-cli backend (10 golden cases, small sample).
- Items marked needs review matched the record 9/10 times in testing on the claude-cli backend (10 golden cases, small sample).

| Item type | Verified (matched/seen) | Needs review (matched/seen) |
|---|---|---|
| entry | 53/54 | 2/3 |
| amount | 9/9 | 6/6 |
| flag | 21/21 | 1/1 |


## Judge controls, per item

In-sample controls were written with the prompts 

... [7728 characters truncated] ...

ports/20261102T120809Z.md
# Eval report 2026-11-02T12:08:09Z

**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6`, tree clean.

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (237 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `claude-cli`, 10 golden cases, source commit `63e18ed413`)

- Verified items matched the record 83/84 times in testing on the claude-cli backend (10 golden cases, small sample).
- Items marked needs review matched the record 10/10 times in testing on the claude-cli backend (10 golden cases, small sample).

| Item type | Verified (matched/seen) | Needs review (matched/seen) |
|---|---|---|
| entry | 53/54 | 3/3 |
| amount | 9/9 | 6/6 |
| flag | 21/21 | 1/1 |


## Judge controls, per item

In-sample controls were written with the prompts they test; held-out controls were written before the next prompt edit. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate 

| id | judge | split | kind | pair | origin | expected | verdict per run | ok |
|---|---|---|---|---|---|---|---|---|
| J3R1 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | packet | conflict | conflict / conflict / conflict | yes |
| J3R2 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R3 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R4 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | packet | benign | benign / benign / benign | yes |
| J3V1 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V14 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V2 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V3 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V4 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | variant | conflict | conflict / conflict / conflict | yes |
| J3V5 | j3 | in-sample | wrong | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | benign | benign / benign / benign | yes |
| J3V6 | j3 | in-sample | correct | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | conflict | conflict / conflict / conflict | yes |
| J3V7 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V10 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V15 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V16 | j3 | in-sample | wrong | history_denial:Patient denies any prior injury. | variant | benign | benign / benign / benign | yes |
| J3V11 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | variant | conflict | conflict / conflict / conflict | yes |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:53:53.729Z

**tool call — Bash**
````
{
 "command": "for r in 20261102T113305Z 20261102T115041Z 20261102T120809Z; do echo \"=== $r\"; sed -n 3,5p evals/reports/$r.md|cut -c1-200; grep -E \"^\\| (grounding|entry_recall|amount_recall|hallucination|unsupported|determinism|J3|J4|golden_must|unsplit|case_07)|flag_precision\" evals/reports/$r.md | cut -c1-230; grep -n -i -E \"run dir|runs/|3 runs|repeat\" evals/reports/$r.md | head -8 | cut -c1-250; done; ls evals/reports/runs | head -40; echo; sed -n 1,12p evals/reports/controls-20261102T123937Z.md | cut -c1-400"
}
````

### User / tool · 2026-11-02T12:53:53.865Z

**tool result**
````
=== 20261102T113305Z
**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6`, tree clean.

| grounding_rate | 1.000 (237 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.965 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| J3R1 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | packet | conflict | conflict / conflict / conflict | yes |
| J3R2 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R3 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R4 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | packet | benign | benign / benign / benign | yes |
| J3V1 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V14 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V2 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V3 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V4 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | variant | conflict | conflict / conflict / conflict | yes |
| J3V5 | j3 | in-sample | wrong | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | benign | benign / benign / benign | yes |
| J3V6 | j3 | in-sample | correct | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | conflict | conflict / conflict / conflict | yes |
| J3V7 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V10 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V15 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V16 | j3 | in-sample | wrong | history_denial:Patient denies any prior injury. | variant | benign | benign / benign / benign | yes |
| J3V11 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | variant | conflict | conflict / conflict / conflict | yes |
| J3V12 | j3 | in-sample | correct | history_denial:Patient denies any prior injury. | variant | conflict | conflict / conflict / conflict | yes |
| J4W1 | j4 | in-sample | wrong | P4-neck-history |  | disagree | disagree / disagree / disagree | yes |
| J4C10 | j4 | in-sample | correct | P4-neck-history |  | agree | agree / agree / agree | yes |
| J4W6 | j4 | in-sample | wrong | P4-back-history |  | disagree | disagree / disagree / disagree | yes |
| J4C1 | j4 | in-sample | correct | P4-back-history |  | agree | agree / agree / agree | yes |
| J4W2 | j4 | in-sample | wrong | P4-hedged-findings |  | disagree | disagree / disagree / disagree | yes |
| J4C2 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4C6 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4W3 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4C3 | j4 | in-sample | correct | P4-missed-care |  | agree | agree / agree / agree | yes |
| J4W9 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4W4 | j4 | in-sample | wrong | P4-referral |  | disagree | disagree / disagree / disagree | yes |
| J4C11 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4C8 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4W8 | j4 | in-sample | wrong | P4-mri |  | disagree | disagree / disagree / disagree | yes |
| J4C9 | j4 | in-sample | correct | P4-mri |  | agree | agree / agree / agree | yes |
| J4W7 | j4 | in-sample | wrong | P4-scene |  | disagree | disagree / disagree / disagree | yes |
| J4C7 | j4 | in-sample | correct | P4-scene |  | agree | agree / agree / agree | yes |
| J4W5 | j4 | in-sample | wrong | P4-ct |  | disagree | disagree / disagree / disagree | yes |
| J4C4 | j4 | in-sample | correct | P4-onset |  | agree | agree / agree / agree | yes |
| J4C5 | j4 | in-sample | correct | P4-surgery |  | agree | agree / agree / agree | yes |
19:| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
20:| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
41:In-sample controls were written with the prompts they test; held-out controls were written before the next prompt edit. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at th
118:- per-run artifacts: `evals/reports/runs/20261102T111525Z`
=== 20261102T115041Z
**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6`, tree clean.

| grounding_rate | 1.000 (238 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| J3R1 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | packet | conflict | conflict / conflict / conflict | yes |
| J3R2 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R3 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R4 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | packet | benign | benign / benign / benign | yes |
| J3V1 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V14 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V2 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V3 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V4 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | variant | conflict | conflict / conflict / conflict | yes |
| J3V5 | j3 | in-sample | wrong | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | benign | benign / benign / benign | yes |
| J3V6 | j3 | in-sample | correct | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | conflict | conflict / conflict / conflict | yes |
| J3V7 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V10 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V15 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V16 | j3 | in-sample | wrong | history_denial:Patient denies any prior injury. | variant | benign | benign / benign / benign | yes |
| J3V11 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | variant | conflict | conflict / conflict / conflict | yes |
| J3V12 | j3 | in-sample | correct | history_denial:Patient denies any prior injury. | variant | conflict | conflict / conflict / conflict | yes |
| J4W1 | j4 | in-sample | wrong | P4-neck-history |  | disagree | disagree / disagree / disagree | yes |
| J4C10 | j4 | in-sample | correct | P4-neck-history |  | agree | agree / agree / agree | yes |
| J4W6 | j4 | in-sample | wrong | P4-back-history |  | disagree | disagree / disagree / disagree | yes |
| J4C1 | j4 | in-sample | correct | P4-back-history |  | agree | agree / agree / agree | yes |
| J4W2 | j4 | in-sample | wrong | P4-hedged-findings |  | disagree | disagree / disagree / disagree | yes |
| J4C2 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4C6 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4W3 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4C3 | j4 | in-sample | correct | P4-missed-care |  | agree | agree / agree / agree | yes |
| J4W9 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4W4 | j4 | in-sample | wrong | P4-referral |  | disagree | disagree / disagree / disagree | yes |
| J4C11 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4C8 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4W8 | j4 | in-sample | wrong | P4-mri |  | disagree | disagree / disagree / disagree | yes |
| J4C9 | j4 | in-sample | correct | P4-mri |  | agree | agree / agree / agree | yes |
| J4W7 | j4 | in-sample | wrong | P4-scene |  | disagree | disagree / disagree / disagree | yes |
| J4C7 | j4 | in-sample | correct | P4-scene |  | agree | agree / agree / agree | yes |
| J4W5 | j4 | in-sample | wrong | P4-ct |  | disagree | disagree / disagree / disagree | yes |
| J4C4 | j4 | in-sample | correct | P4-onset |  | agree | agree / agree / agree | yes |
| J4C5 | j4 | in-sample | correct | P4-surgery |  | agree | agree / agree / agree | yes |
19:| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
20:| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
41:In-sample controls were written with the prompts they test; held-out controls were written before the next prompt edit. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at th
118:- per-run artifacts: `evals/reports/runs/20261102T113305Z`
=== 20261102T120809Z
**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6`, tree clean.

| grounding_rate | 1.000 (237 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| J3R1 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | packet | conflict | conflict / conflict / conflict | yes |
| J3R2 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R3 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | packet | conflict | conflict / conflict / conflict | yes |
| J3R4 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | packet | benign | benign / benign / benign | yes |
| J3V1 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V14 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V2 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V3 | j3 | in-sample | wrong | plan_vs_outcome:Plan of care: 12 visits. | variant | benign | benign / benign / benign | yes |
| J3V4 | j3 | in-sample | correct | plan_vs_outcome:Plan of care: 12 visits. | variant | conflict | conflict / conflict / conflict | yes |
| J3V5 | j3 | in-sample | wrong | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | benign | benign / benign / benign | yes |
| J3V6 | j3 | in-sample | correct | plan_vs_outcome:Refer to physical therapy 2x/week for 6 weeks. | variant | conflict | conflict / conflict / conflict | yes |
| J3V7 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V10 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V15 | j3 | in-sample | wrong | history_denial:Patient denies prior neck problems. | variant | benign | benign / benign / benign | yes |
| J3V16 | j3 | in-sample | wrong | history_denial:Patient denies any prior injury. | variant | benign | benign / benign / benign | yes |
| J3V11 | j3 | in-sample | correct | history_denial:Patient denies prior neck problems. | variant | conflict | conflict / conflict / conflict | yes |
| J3V12 | j3 | in-sample | correct | history_denial:Patient denies any prior injury. | variant | conflict | conflict / conflict / conflict | yes |
| J4W1 | j4 | in-sample | wrong | P4-neck-history |  | disagree | disagree / disagree / disagree | yes |
| J4C10 | j4 | in-sample | correct | P4-neck-history |  | agree | agree / agree / agree | yes |
| J4W6 | j4 | in-sample | wrong | P4-back-history |  | disagree | disagree / disagree / disagree | yes |
| J4C1 | j4 | in-sample | correct | P4-back-history |  | agree | agree / agree / agree | yes |
| J4W2 | j4 | in-sample | wrong | P4-hedged-findings |  | disagree | disagree / disagree / disagree | yes |
| J4C2 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4C6 | j4 | in-sample | correct | P4-hedged-findings |  | agree | agree / agree / agree | yes |
| J4W3 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4C3 | j4 | in-sample | correct | P4-missed-care |  | agree | agree / agree / agree | yes |
| J4W9 | j4 | in-sample | wrong | P4-missed-care |  | disagree | disagree / disagree / disagree | yes |
| J4W4 | j4 | in-sample | wrong | P4-referral |  | disagree | disagree / disagree / disagree | yes |
| J4C11 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4C8 | j4 | in-sample | correct | P4-referral |  | agree | agree / agree / agree | yes |
| J4W8 | j4 | in-sample | wrong | P4-mri |  | disagree | disagree / disagree / disagree | yes |
| J4C9 | j4 | in-sample | correct | P4-mri |  | agree | agree / agree / agree | yes |
| J4W7 | j4 | in-sample | wrong | P4-scene |  | disagree | disagree / disagree / disagree | yes |
| J4C7 | j4 | in-sample | correct | P4-scene |  | agree | agree / agree / agree | yes |
| J4W5 | j4 | in-sample | wrong | P4-ct |  | disagree | disagree / disagree / disagree | yes |
| J4C4 | j4 | in-sample | correct | P4-onset |  | agree | agree / agree / agree | yes |
| J4C5 | j4 | in-sample | correct | P4-surgery |  | agree | agree / agree / agree | yes |
19:| J3 judge_conflict_v6 seeded catch rate | 1.000 (16/16 wrong caught x3 runs; in-sample 10/10; held-out 6/6; false agree 0 []; correct accepted 16/16; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
20:| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
41:In-sample controls were written with the prompts they test; held-out controls were written before the next prompt edit. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at th
118:- per-run artifacts: `evals/reports/runs/20261102T115041Z`
20261102T034706Z
20261102T035806Z
20261102T042232Z
20261102T045543Z
20261102T051136Z
20261102T052638Z
20261102T054926Z
20261102T060623Z
20261102T063157Z
20261102T075514Z
20261102T081339Z
20261102T083312Z
20261102T090500Z
20261102T090956Z
20261102T091115Z
20261102T093020Z
20261102T093440Z
20261102T094756Z
20261102T094902Z
20261102T095146Z
20261102T095639Z
20261102T101232Z
20261102T103042Z
20261102T103337Z
20261102T103538Z
20261102T103649Z
20261102T104042Z
20261102T104435Z
20261102T105126Z
20261102T111525Z
20261102T113305Z
20261102T114137Z
20261102T114852Z
20261102T115041Z
20261102T115516Z
20261102T115718Z
20261102T120358Z
20261102T121838Z
20261102T123651Z

# Judge controls 20261102T123937Z

**controls_ok: True**  backend `claude-cli`  prompts `judge_conflict_v6`, `judge_flag_v3` (hashes in the json)
Source commit `bea39845ebb67b4fe0ef207ebed9499cf1e5964b`, tree clean.

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| J3 judge_conflict_v6 seeded catch rate | 1.000 (19/19 wrong caught x3 runs; in-sample 13/13; held-out 6/6; false agree 0 []; correct accepted 18/18; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |

## Judge controls, per item
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:01.750Z

**tool call — Bash**
````
{
 "command": "for d in 20261102T111525Z 20261102T113305Z 20261102T115041Z; do echo $d; ls evals/reports/runs/$d | head; done; git log --oneline 63e18ed..0c24f5f | cat; git log -1 --format=%H%n%s 63e18ed bea3984 | cat; git status --short evals tests app | head; git ls-files evals/reports | grep -E \"1133|1150|1208|123937\" ; echo ---; git diff --stat 63e18ed 0c24f5f -- app evals tests | cat | tail -40"
}
````

### User / tool · 2026-11-02T12:54:01.963Z

**tool result**
````
20261102T111525Z
calibration.json
case_01_date_formats.json
case_02_gap_boundaries.json
case_03_rate_and_ocr.json
case_04_duplicates_no_amounts.json
case_05_provider_conflict.json
case_06_subtle_pre_existing.json
case_07_prompt_injection.json
case_08_diagnosis_temptation.json
case_09_nonvisit_hides_gap.json
20261102T113305Z
calibration.json
case_01_date_formats.json
case_02_gap_boundaries.json
case_03_rate_and_ocr.json
case_04_duplicates_no_amounts.json
case_05_provider_conflict.json
case_06_subtle_pre_existing.json
case_07_prompt_injection.json
case_08_diagnosis_temptation.json
case_09_nonvisit_hides_gap.json
20261102T115041Z
calibration.json
case_01_date_formats.json
case_02_gap_boundaries.json
case_03_rate_and_ocr.json
case_04_duplicates_no_amounts.json
case_05_provider_conflict.json
case_06_subtle_pre_existing.json
case_07_prompt_injection.json
case_08_diagnosis_temptation.json
case_09_nonvisit_hides_gap.json
0c24f5f fix(board): a review with no blocker or major must carry verdict pass (§7.4; lesson T-113 r2)
db1d8d5 fix(backend): T-134 r2 item trace says edited, waiting for your check (not accepted) for an open edit; judges step ignores human-edit re-check gap; mutant-killing tests
128942d docs(orchestrator): scope cut 13d and patient-as-source assumption (T-133 r3)
f3ac48f chore(evals): regenerate calibration.json from a clean worktree of 6fa8ecc (fixture; lexicon.yaml T-133 r3)
671f054 feat(frontend): T-136 read item.edit_to_check and review.counts.edit_to_check; a never records the comparison; dismissed flags and amounts under Dismissed (n); EDIT_NOT_CONFIRMED gate warning
6fa8ecc fix(lexicon): T-133 r3 header guard skips only a bare 'History:' header; qualified past-history headers flag again
abaa14a docs(orchestrator): scope cut 13c informant-reported history in conflict candidates (T-113 F2)
bba9e5c test(backend): T-113 r2 live controls from clean worktree of bea3984, judge_conflict_v6: J3 19/19 x3, 5 clean held-out controls all right, J4 12/12
bea3984 fix(backend): T-113 r2 held-out status derived from git, H3V16/H3V1/H3V3 moved to in_sample, 5 new held-out J3 controls locked before any run, tray reason for model conflicts, list-word and tray-order tests
eef92a7 fix(backend): T-128 fix-up stop splitting clauses at ' with ', drop the by-construction fragment claim
5d7074e fix(backend): T-132 r3 normalize soft wraps, uncapped attribution chains, short vitals labels end the extension
4065ef2 chore(evals): regenerate calibration.json from a clean worktree of f939ccb (fixture; lexicon.yaml T-133 r2)
5fb338d fix(backend): T-134 an edit still Needs review is open: out of the letter, not accepted, gate warns EDIT_NOT_CONFIRMED, notes say second check not available
f939ccb fix(lexicon): T-133 r2 history_significant_for never fires on HPI headers or narratives; deny sourced from pyConText
425095f docs(architect): T-109 r3 ADR-020 item 2 cite _model_conflicts at flags.py:185-209
5f1a7e2 docs(architect): T-109 r3 row 11 J3 controls (no dosage/laterality), row 4 and ADR-020 item 5 suffix-only trim (T-128 r3)
bd8c50e docs(orchestrator): mark D-004, D-031 and scope cut 15 superseded by D-042/D-052 (T-109 r3)
b348221 fix(backend): T-128 r3 trim only a suffix, n't contraction and quote-side tests
c759213 fix(backend): T-132 r2 wrapped attribution phrase, chained attribution clauses, no extension across blank line or section header
b612176 feat(frontend): T-060 r5 + T-131 - dismissed items keep no Accept, edited-needs-review counts as open, focus stays in one list, one need-review count, plain reasons, long dates, Filtered by rule, one-line letter control
1218b2e chore(evals): regenerate calibration.json from a clean worktree of e79c3aa (fixture; lexicon.yaml T-133)
dab3037 docs(orchestrator): D-053 no-candidate rule applies to conflicts only (T-109 r3)
94a135b docs(orchestrator): T-105 accepted-debt row
a27e1d7 docs(architect): T-109 r3 ADR-015/019/020 match HEAD: judge_conflict_v6, model-conflict tray scope, D-057, T-112 shipped, charge wording list, committed ship-bar reports
f8bb674 docs(architect): T-109 r3 LLM_VS_CODE rows 4, 11, 12, 13 match HEAD: T-112 r2 summary trim, candidate drop rules, judge_conflict_v6, tray routes, D-057 filtered group
e79c3aa feat(lexicon): deny/denying as negation words; bare 'History ... notable/significant for' prior-condition entry (T-133)
5dfba88 test(qa): T-113/T-112 three consecutive live 3-runs from clean 63e18ed, ship_bar_met x3
2790918 refactor(backend): summary_trim reads negation and side words from the lexicon (T-105 r2 leftover)
f4d68bb fix(backend): T-132 attribution-only history unit extends to the next clause; MS is not Ms.; pin the history-word gate
1f0a164 fix(backend): T-129 r2 serve unsplit and preamble on GET case; a re-run resets decisions on shifted record numbers
180138c fix(backend): T-128 r2 structural no-fragment rule (first clause kept, 2-word prefix, no dangling joins), inert abbreviations removed
882d4ee chore(evals): regenerate calibration.json from a clean worktree of 97b59a6 (fixture; lexicon.yaml T-105 r2)
97b59a6 fix(backend): T-105 r2 lexicon.yaml is the single source: dropped_qualifiers, quote-side checks, negation/side words and the Spanish helper read it through grounding views; structural no-duplicate-list guard
a44dced fix(backend): T-126 r2 every tray flag stays out of export counts and notes, merge trace, one filtered helper
f7829c1 fix(backend): T-120 r3 history-source skip strips only the attribution phrase and scans what is left (no condition guessing)
93de5f2 feat(backend): T-127 keep gap_change on the gap flag, gap_changes_removed in GET case
3a74f75 fix(backend): T-129 a preamble no longer shifts record numbers
3d53ca5 feat(backend): T-128 summary trim never leaves a fragment, pin r3 mutants
433ac1c test(backend): T-123 pin which record is named as paperwork in either order (kills the provider-ordering mutant)
aa6ae9f feat(backend): T-105 added-qualifier word lists (attribution, hedge, approximation, inability) come from lexicon.yaml code_lists.added_qualifier; curly apostrophes, Spanish-helper negations, faithful paraphrases; lexicon text updated to D-055
4c59fac fix(backend): T-121 r2 one-line style carries the translated summary, whitespace-only quote collapse documented and tested, translation note on its own line
07dbd2b fix(backend): T-120 r2 history-source skip only when the sentence names no condition (colon, year, 'of' keep the flag); per/via only before a person or channel
1a0106b docs(orchestrator): T-112 accepted-debt row (§7.4 after round 3)
c559ce2 test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring
e293daa feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed group, edit re-check notice, typed $ in refusals, readable library titles
6d01774 feat(backend): T-126 rule-filtered model flags (D-032 objective_negative) go to a collapsed Filtered by rule group, never dropped (D-057)
bea39845ebb67b4fe0ef207ebed9499cf1e5964b
fix(backend): T-113 r2 held-out status derived from git, H3V16/H3V1/H3V3 moved to in_sample, 5 new held-out J3 controls locked before any run, tray reason for model conflicts, list-word and tray-order tests
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
evals/reports/20261102T113305Z.md
evals/reports/20261102T115041Z.md
evals/reports/20261102T120809Z.md
evals/reports/controls-20261102T123937Z.json
evals/reports/controls-20261102T123937Z.md
evals/reports/runs/20261102T113305Z/calibration.json
evals/reports/runs/20261102T113305Z/case_01_date_formats.json
evals/reports/runs/20261102T113305Z/case_02_gap_boundaries.json
evals/reports/runs/20261102T113305Z/case_03_rate_and_ocr.json
evals/reports/runs/20261102T113305Z/case_04_duplicates_no_amounts.json
evals/reports/runs/20261102T113305Z/case_05_provider_conflict.json
evals/reports/runs/20261102T113305Z/case_06_subtle_pre_existing.json
evals/reports/runs/20261102T113305Z/case_07_prompt_injection.json
evals/reports/runs/20261102T113305Z/case_08_diagnosis_temptation.json
evals/reports/runs/20261102T113305Z/case_09_nonvisit_hides_gap.json
evals/reports/runs/20261102T113305Z/run1.json
evals/reports/runs/20261102T113305Z/run2.json
evals/reports/runs/20261102T113305Z/run3.json
evals/reports/runs/20261102T113305Z/sample.json
evals/reports/runs/20261102T115041Z/calibration.json
evals/reports/runs/20261102T115041Z/case_01_date_formats.json
evals/reports/runs/20261102T115041Z/case_02_gap_boundaries.json
evals/reports/runs/20261102T115041Z/case_03_rate_and_ocr.json
evals/reports/runs/20261102T115041Z/case_04_duplicates_no_amounts.json
evals/reports/runs/20261102T115041Z/case_05_provider_conflict.json
evals/reports/runs/20261102T115041Z/case_06_subtle_pre_existing.json
evals/reports/runs/20261102T115041Z/case_07_prompt_injection.json
evals/reports/runs/20261102T115041Z/case_08_diagnosis_temptation.json
evals/reports/runs/20261102T115041Z/case_09_nonvisit_hides_gap.json
evals/reports/runs/20261102T115041Z/run1.json
evals/reports/runs/20261102T115041Z/run2.json
evals/reports/runs/20261102T115041Z/run3.json
evals/reports/runs/20261102T115041Z/sample.json
---
 .../case_05_provider_conflict.json                 |  364 +++++
 .../case_06_subtle_pre_existing.json               |  411 ++++++
 .../20261102T115041Z/case_07_prompt_injection.json |  448 ++++++
 .../case_08_diagnosis_temptation.json              |  279 ++++
 .../case_09_nonvisit_hides_gap.json                |  360 +++++
 evals/reports/runs/20261102T115041Z/run1.json      |  974 +++++++++++++
 evals/reports/runs/20261102T115041Z/run2.json      |  974 +++++++++++++
 evals/reports/runs/20261102T115041Z/run3.json      |  974 +++++++++++++
 evals/reports/runs/20261102T115041Z/sample.json    |  974 +++++++++++++
 evals/run.py                                       |   15 +-
 tests/e2e/conftest.py                              |   13 +-
 tests/e2e/test_code_check_refusal.py               |   13 +-
 tests/e2e/test_edit.py                             |    2 +-
 tests/e2e/test_edit_to_check.py                    |  211 +++
 tests/e2e/test_input.py                            |    4 +-
 tests/e2e/test_keyboard_mobile.py                  |    2 +-
 tests/e2e/test_polish_r3.py                        |   22 +-
 tests/e2e/test_polish_r4.py                        |  239 ++++
 tests/e2e/test_polish_r5.py                        |  244 ++++
 tests/e2e/test_rerun_judge.py                      |    2 +-
 tests/e2e/test_suggestions.py                      |    6 +-
 tests/e2e/test_timeline.py                         |    4 +-
 tests/unit/test_conflict_candidates.py             |   30 +
 tests/unit/test_flags_pass.py                      |   29 +-
 tests/unit/test_ingest.py                          |   82 ++
 tests/unit/test_spanish_records.py                 |    3 +
 tests/unit/test_summary_trim.py                    |  242 +++-
 tests/unit/test_t093_j3_controls_reachable.py      |    9 +-
 tests/unit/test_t105_added_qualifier_lexicon.py    |  229 +++
 tests/unit/test_t113_heldout_audit.py              |   84 ++
 tests/unit/test_t120_history_source_sentence.py    |   85 +-
 tests/unit/test_t121_letter_styles.py              |   34 +-
 .../unit/test_t123_baseline_same_day_paperwork.py  |   12 +
 tests/unit/test_t126_filtered_by_rule.py           |  167 +++
 tests/unit/test_t127_gap_change_kept.py            |   66 +
 tests/unit/test_t132_attribution_unit.py           |  232 +++
 tests/unit/test_t133_lexicon.py                    |  342 +++++
 tests/unit/test_t134_unconfirmed_edit.py           |  206 +++
 tests/unit/test_trace.py                           |   31 +-
 120 files changed, 29350 insertions(+), 354 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:06.925Z

**tool call — Bash**
````
{
 "command": "git ls-files evals/reports/runs/20261102T111525Z | wc -l; git ls-files evals/reports/runs/20261102T113305Z | wc -l; git ls-files evals/reports/runs/20261102T115041Z | wc -l; git log --format='%h %ad %s' --date=iso -3 -- evals/reports/runs/20261102T111525Z | cat; git show 5dfba88 --stat | cat | head -50; sed -n 110,125p evals/reports/20261102T113305Z.md | cut -c1-300; git log -1 --format='%h %ad %s' --date=iso 63e18ed | cat"
}
````

### User / tool · 2026-11-02T12:54:07.172Z

**tool result**
````
      14
      14
      14
5dfba88 2026-11-02 06:08:48 -0600 test(qa): T-113/T-112 three consecutive live 3-runs from clean 63e18ed, ship_bar_met x3
commit 5dfba8889b9c5d98b2f29c6cea1fcf5ac23d51a7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 06:08:48 2026 -0600

    test(qa): T-113/T-112 three consecutive live 3-runs from clean 63e18ed, ship_bar_met x3
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 evals/reports/20261102T113305Z.md                  | 138 +++
 evals/reports/20261102T115041Z.md                  | 138 +++
 evals/reports/20261102T120809Z.md                  | 138 +++
 .../reports/runs/20261102T111525Z/calibration.json | 270 ++++++
 .../20261102T111525Z/case_01_date_formats.json     | 459 ++++++++++
 .../20261102T111525Z/case_02_gap_boundaries.json   | 594 +++++++++++++
 .../20261102T111525Z/case_03_rate_and_ocr.json     | 419 +++++++++
 .../case_04_duplicates_no_amounts.json             | 242 +++++
 .../case_05_provider_conflict.json                 | 364 ++++++++
 .../case_06_subtle_pre_existing.json               | 411 +++++++++
 .../20261102T111525Z/case_07_prompt_injection.json | 448 ++++++++++
 .../case_08_diagnosis_temptation.json              | 279 ++++++
 .../case_09_nonvisit_hides_gap.json                | 360 ++++++++
 evals/reports/runs/20261102T111525Z/run1.json      | 974 ++++++++++++++++++++
 evals/reports/runs/20261102T111525Z/run2.json      | 974 ++++++++++++++++++++
 evals/reports/runs/20261102T111525Z/run3.json      | 974 ++++++++++++++++++++
 evals/reports/runs/20261102T111525Z/sample.json    | 974 ++++++++++++++++++++
 .../reports/runs/20261102T113305Z/calibration.json | 270 ++++++
 .../20261102T113305Z/case_01_date_formats.json     | 488 +++++++++++
 .../20261102T113305Z/case_02_gap_boundaries.json   | 590 +++++++++++++
 .../20261102T113305Z/case_03_rate_and_ocr.json     | 419 +++++++++
 .../case_04_duplicates_no_amounts.json             | 246 ++++++
 .../case_05_provider_conflict.json                 | 364 ++++++++
 .../case_06_subtle_pre_existing.json               | 411 +++++++++
 .../20261102T113305Z/case_07_prompt_injection.json | 448 ++++++++++
 .../case_08_diagnosis_temptation.json              | 279 ++++++
 .../case_09_nonvisit_hides_gap.json                | 360 ++++++++
 evals/reports/runs/20261102T113305Z/run1.json      | 974 ++++++++++++++++++++
 evals/reports/runs/20261102T113305Z/run2.json      | 975 +++++++++++++++++++++
 evals/reports/runs/20261102T113305Z/run3.json      | 974 ++++++++++++++++++++
 evals/reports/runs/20261102T113305Z/sample.json    | 974 ++++++++++++++++++++
 .../reports/runs/20261102T115041Z/calibration.json | 265 ++++++
 .../20261102T115041Z/case_01_date_formats.json     | 463 ++++++++++
 .../20261102T115041Z/case_02_gap_boundaries.json   | 590 +++++++++++++
 .../20261102T115041Z/case_03_rate_and_ocr.json     | 419 +++++++++
 .../case_04_duplicates_no_amounts.json             | 242 +++++
 .../case_05_provider_conflict.json                 | 364 ++++++++
 .../case_06_subtle_pre_existing.json               | 411 +++++++++
 .../20261102T115041Z/case_07_prompt_injection.json | 448 ++++++++++
 .../case_08_diagnosis_temptation.json              | 279 ++++++
 .../case_09_nonvisit_hides_gap.json                | 360 ++++++++
 evals/reports/runs/20261102T115041Z/run1.json      | 974 ++++++++++++++++++++
- entry misses: {"case_02_gap_boundaries": [{"entry": "E1", "why": "excerpt misses must_contain_excerpt"}], "case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}
- missed must flags: {}
- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0, "per_case": {"case_02_gap_boundaries": {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0}}}
- flag tray (could-not-verify flags, D-053; not scored, not in the R-CO-7 flag signature): 1 {"LLM_ONLY": 1} by case {"case_05_provider_conflict": 1}
- grounding failures: []
- seeded hallucinations not caught: []
- must_not detail: {}

- per-run artifacts: `evals/reports/runs/20261102T111525Z`

## Prompt and lexicon hashes

- `app/llm/prompts/extract_es_v1.md` 985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb
- `app/llm/prompts/extract_v1.md` 11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2
- `app/llm/prompts/flags_v1.md` d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725
- `app/llm/prompts/judge_amount_class_v1.md` e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8
63e18ed 2026-11-02 05:14:48 -0600 fix(backend): T-112 r3 summary trim keeps abbreviation expansions, no bare-noun fragments
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:11.092Z

**tool call — Bash**
````
{
 "command": "git diff --stat 63e18ed 0c24f5f -- app evals/run.py evals/*.py | cat; git diff --stat 63e18ed 0c24f5f -- app/llm/prompts | cat; git diff 63e18ed 0c24f5f -- evals/run.py | cat"
}
````

### User / tool · 2026-11-02T12:54:11.264Z

**tool result**
````
 app/backend/api.py                 |   6 +-
 app/backend/confidence.py          |   2 +-
 app/backend/conflict_candidates.py |   6 +-
 app/backend/export.py              |  39 +++++++--
 app/backend/flag_templates.py      |  12 +++
 app/backend/flags.py               |  42 ++++++++--
 app/backend/grounding.py           | 159 ++++++++++++++++++++++++++-----------
 app/backend/ingest.py              |  12 ++-
 app/backend/lexicon_scan.py        | 115 ++++++++++++++++++++++++++-
 app/backend/pipeline.py            |  40 +++++++++-
 app/backend/present.py             |  86 +++++++++++++++++---
 app/backend/review.py              |  16 +++-
 app/backend/spanish_text.py        |  64 ++++++---------
 app/backend/store.py               |   7 ++
 app/backend/summary_trim.py        |  77 ++++++------------
 app/backend/trace.py               |  58 +++++++++++---
 app/backend/why.py                 |   7 ++
 app/frontend/api.js                |   2 +-
 app/frontend/app.js                |  14 ++--
 app/frontend/charges.js            |  17 ++--
 app/frontend/dom.js                |  22 +++++
 app/frontend/export.js             |  16 ++--
 app/frontend/flags.js              |  19 ++++-
 app/frontend/judges.js             |  22 ++---
 app/frontend/manual.js             |   4 +-
 app/frontend/mock.js               |   4 +-
 app/frontend/review.css            |   6 ++
 app/frontend/review.js             | 126 ++++++++++++++++++++++++-----
 app/frontend/stepper.js            |  21 +++--
 app/frontend/styles.css            |  25 +++++-
 app/frontend/switcher.js           |   6 +-
 app/frontend/timeline.js           | 122 ++++++++++++++++++++++------
 app/llm/lexicon.yaml               | 134 +++++++++++++++++++++++++++++--
 evals/heldout_audit.py             | 122 ++++++++++++++++++++++++++++
 evals/j3_controls.py               |  42 ++++++++--
 evals/run.py                       |  15 ++--
 36 files changed, 1190 insertions(+), 297 deletions(-)
diff --git a/evals/run.py b/evals/run.py
index c302922..b423865 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -576,7 +576,7 @@ def control_prompt(j):
 
 
 def load_controls(gold=None):
-    """In-sample controls (they share authors and rules with the prompts they test) and the held-out set (written before the next prompt edit)."""
+    """In-sample controls (they share authors and rules with the prompts they test) and the held-out file (separately authored; its status is derived by evals/heldout_audit.py)."""
     gold = pathlib.Path(gold or GOLD)
     rows = []
     for name, split in CONTROL_FILES:
@@ -1014,16 +1014,21 @@ def render_controls(jc):
 
 
 def render_control_items(jc):
-    """Per-item verdict on every repeat. in-sample controls share authors and rules with the prompts (not independent evidence); held-out controls were written
-    before the next prompt edit."""
+    """Per-item verdict on every repeat. in-sample controls share authors and rules with the prompts (not independent evidence); a held-out row is separately authored
+    and its status is derived from git (evals/heldout_audit.py), never taken from the label."""
     if not jc or "rows" not in jc:
         return []
-    L = ["", "## Judge controls, per item", "", "In-sample controls were written with the prompts they test; held-out controls were written before the next prompt edit. "
-         "A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate "
+    L = ["", "## Judge controls, per item", "", "In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says "
+         "whether it is still held out. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate "
          "from a golden or library packet, `variant` is a crafted variant of one (T-093 r4; tests/unit/test_t093_j3_controls_reachable.py).", "", "| id | judge | split | kind | pair | origin | expected | verdict per run | ok |", "|---|---|---|---|---|---|---|---|---|"]
     for r in jc["rows"]:
         ok = (r["verdict"] not in (POSITIVE[r["judge"]], "unavailable")) if r["kind"] == "wrong" else all(v == POSITIVE[r["judge"]] for v in r["verdicts"])
         L.append(f"| {r['id']} | {r['judge']} | {r['split'].replace('_', '-')} | {r['kind']} | {(r.get('pair') or '').replace('|', '/')} | {r.get('origin') or ''} | {r['expected']} | {' / '.join(r['verdicts'])} | {'yes' if ok else 'NO'} |")
+    try:
+        from evals import heldout_audit
+        L += ["", *heldout_audit.summary_lines()]
+    except Exception as e:      # the audit is information about the evidence, never a reason to lose the report
+        L += ["", f"Held-out status could not be computed ({type(e).__name__}); the `held-out` label alone is a claim, not a check."]
     return L + [""]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:18.328Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $S/arch && mkdir -p $S/arch && git archive 0c24f5f | tar -x -C $S/arch && ls $S/arch | head -30 && ls -la .venv/bin/python && cat Makefile | grep -n -E \"^(test|evals)\" -A4"
}
````

### User / tool · 2026-11-02T12:54:18.397Z

**tool result (error)**
````
Permission to use Bash with command S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $S/arch && mkdir -p $S/arch && git archive 0c24f5f has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:22.688Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/arch0c24 && git archive 0c24f5f | tar -x -C $S/arch0c24 && ls $S/arch0c24 | head -30; grep -n -E \"^(test|evals)\" -A4 Makefile"
}
````

### User / tool · 2026-11-02T12:54:23.495Z

**tool result (error)**
````
Exit code 2
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
ugrep: warning: Makefile: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:28.682Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arch0c24; cd $S && ls evals tests | head -40; sed -n 1,40p evals/run.py | cut -c1-200; grep -n \"argparse\\|add_argument\" evals/run.py | head -20"
}
````

### User / tool · 2026-11-02T12:54:28.783Z

**tool result**
````
evals:
__init__.py
adversarial
golden
heldout_audit.py
j3_controls.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py

tests:
__init__.py
conftest.py
e2e
fixtures
unit
"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
    python -m evals.run --write-calibration
                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)
    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk

Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
        entry: record_ids, date, date_status, provider, summary, excerpt, state, reasons, ladder{judge{verdict}}
        amount: record_ids, text, value_cents, kind;  flag: type, evidence[{record_id, excerpt}], computed{from,to,days}
    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
ship_bar_met is false there (R-CO-7). Names mirror REQUIREMENTS section 7.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys

from evals.matching import assign_detail, norm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "evals" / "golden"
REPORTS = ROOT / "evals" / "reports"
REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
LIVE_BACKENDS = ("claude-cli", "anthropic-api")
KNOWN_BACKENDS = ("fixture",) + LIVE_BACKENDS
NOT_MEASURED = {"value": None, "status": "not_measured"}

THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
21:import argparse
1213:    ap = argparse.ArgumentParser(prog="python -m evals.run")
1214:    ap.add_argument("--check-fresh", action="store_true")
1215:    ap.add_argument("--check-spec", action="store_true")
1216:    ap.add_argument("--backend", default=None)
1217:    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
1218:    ap.add_argument("--out", default=str(REPORTS))
1219:    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
1220:    ap.add_argument("--write-calibration", action="store_true",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:35.848Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arch0c24 && ln -sfn /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; LLM_BACKEND=fixture timeout 550 /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --backend fixture --out /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/evalout 2>&1 | tail -30",
 "timeout": 580000
}
````

### User / tool · 2026-11-02T12:54:35.970Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:45.855Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arch0c24 && LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --backend fixture --out ../evalout 2>&1 | tail -30",
 "timeout": 580000
}
````

### User / tool · 2026-11-02T12:54:47.426Z

**tool result**
````
ship_bar_met=False backend=fixture report=../evalout/20261102T125447Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:54.055Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/evalout && sed -n 1,30p 20261102T125447Z.md | cut -c1-260; grep -n -E \"misses|missed|failures|not caught|tray|clauses removed\" 20261102T125447Z.md | cut -c1-300"
}
````

### User / tool · 2026-11-02T12:54:54.151Z

**tool result**
````
# Eval report 2026-11-02T12:54:47Z

**ship_bar_met: False**  backend `fixture`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `unknown`, tree unknown.

Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7); judge_controls (J3/J4 seeded wrong items): not measured

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (241 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | None | 0 | R-TL-4 |
| determinism_3run | None | 1.0 | R-CO-7 |
| judge_controls (J3/J4 seeded) | not_measured | catch every wrong item on every repeat, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `fixture`, 10 golden cases, source commit `unknown`)

- Verified items matched the record 84/85 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).
44:- entry misses: {"case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}
45:- missed must flags: {}
46:- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 0, "clauses_removed": 0, "tray_placeholders": 0, "per_case": {}}
47:- flag tray (could-not-verify flags, D-053; not scored, not in the R-CO-7 flag signature): 5 {"FILTERED_BY_RULE": 4, "LLM_ONLY": 1} by case {"case_01_date_formats": 2, "case_05_provider_conflict": 1, "case_07_prompt_injection": 1, "sample": 1}
48:- grounding failures: []
49:- seeded hallucinations not caught: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:54:58.477Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arch0c24 && LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 580000
}
````

### User / tool · 2026-11-02T12:58:14.949Z

**tool result**
````
........................................................................ [ 74%]
........................................................................ [ 77%]
........................................................................ [ 79%]
........................................................................ [ 81%]
......................ss................................................ [ 83%]
........................................................................ [ 85%]
........................................................................ [ 87%]
........................................................................ [ 89%]
........................................................................ [ 91%]
........................................................................ [ 93%]
........................................................................ [ 95%]
.....................................ss................................. [ 97%]
........................................................................ [ 99%]
..                                                                       [100%]
3450 passed, 8 skipped in 194.89s (0:03:14)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:58:22.903Z

**tool call — Bash**
````
{
 "command": "git diff 63e18ed 0c24f5f -- app/backend/pipeline.py app/backend/flags.py app/backend/confidence.py app/backend/ingest.py app/backend/conflict_candidates.py | cut -c1-220"
}
````

### User / tool · 2026-11-02T12:58:23.009Z

**tool result**
````
diff --git a/app/backend/confidence.py b/app/backend/confidence.py
index ab169fe..a4d542e 100644
--- a/app/backend/confidence.py
+++ b/app/backend/confidence.py
@@ -11,7 +11,7 @@ REASON_CODES = (
     "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
     "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
     "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED", "LANGUAGE_UNCERTAIN",
-    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE",
+    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE",
 )
 REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
 STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}
diff --git a/app/backend/conflict_candidates.py b/app/backend/conflict_candidates.py
index 30f7eeb..cdbcb09 100644
--- a/app/backend/conflict_candidates.py
+++ b/app/backend/conflict_candidates.py
@@ -77,10 +77,8 @@ def _other_person(unit: str) -> bool:
 
 
 def _paperwork(rec: dict) -> bool:
-    """T-116 F3: an intake form, bill or affidavit is not a clinical encounter. The header test is gaps' (conservative: a record with treatment evidence is a visit).
-    T-116 is renaming non_visit_label to admin_label; either answers the same question."""
-    test = getattr(gaps, "admin_label", None) or gaps.non_visit_label
-    return bool(test(rec))
+    """T-116 F3: an intake form, bill or affidavit is not a clinical encounter. The header test is gaps' (conservative: a record with treatment evidence is a visit)."""
+    return bool(gaps.admin_label(rec))
 
 
 def _after(a, b) -> bool:
diff --git a/app/backend/flags.py b/app/backend/flags.py
index 7e5fca9..5b611b7 100644
--- a/app/backend/flags.py
+++ b/app/backend/flags.py
@@ -19,6 +19,7 @@ _NEEDS_LEXICON = ("scene_facts",)
 # against the claimant, so the paralegal must see them first. Detected by credibility.scan (family match + negation), raised under their own
 # category, never folded into a hedge flag. The lexicon's objective_negative hits (incl. the same phrases) stay context only.
 CREDIBILITY_CATEGORY = credibility.CATEGORY
+FILTER_RULES, FILTERED = FT.FILTER_RULES, FT.FILTERED       # D-057 (T-126): data lives in flag_templates so present.py can read it without importing the engines
 JUDGE_PROMPT = {j: AU.PROMPT_OF_STEP[j] for j in ("j3", "j4")}
 
 
@@ -109,18 +110,31 @@ def _overlap(a, b) -> bool:
     return bool(a and b and a[0] < b[1] and b[0] < a[1])
 
 
+def _note_merged(f: dict, lf: dict) -> None:
+    """Other categories the model proposed for the same quote (collapsed into this flag) go in the audit trail: ladder.code_checks.merged_categories."""
+    extra = sorted(c for c in lf.get("_merged", []) if c and c != f["category"])
+    if extra:
+        f["ladder"] = dict(f["ladder"], code_checks=dict(f["ladder"].get("code_checks") or {}, merged_categories=extra))
+
+
 def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
     """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
     (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
     body, out, used = record["excerpt"], [], set()
-    uniq, seen = [], set()
+    uniq, seen, filtered, fseen = [], {}, [], set()
     for lf in llm_flags:
-        if lf.get("category") in _CONTEXT_ONLY:
+        if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
+            k = (lf["type"], lf["category"], grounding.normalize(lf["excerpt"]))
+            if k not in fseen:
+                fseen.add(k)
+                filtered.append(lf)
             continue
         k = (lf["type"], grounding.normalize(lf["excerpt"]))
         if k not in seen:
-            seen.add(k)
+            seen[k] = lf
             uniq.append(lf)
+        elif lf.get("category") != seen[k].get("category") and lf.get("category") not in seen[k].setdefault("_merged", []):
+            seen[k]["_merged"].append(lf.get("category"))       # T-126 r2 / D-053: a second category on the same quote is not silently lost; the kept flag's code_checks names it
     # R-CO-7: the model's flag order must not decide ids or which model flag a lexicon flag pairs with. Sort by position in the record,
     # then type, category and text (code decides what code can decide).
     uniq.sort(key=lambda lf: ((grounding.locate(body, lf["excerpt"]) or (10 ** 9, 0))[0], lf["type"], lf["category"], grounding.normalize(lf["excerpt"])))
@@ -133,6 +147,7 @@ def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False,
             used.add(match)
             lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
             lx["ladder"] = dict(lx["ladder"], judge=None)
+            _note_merged(lx, uniq[match])
             # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
             # only the fallback quote for phrase-list-only flags. A credibility flag is the exception (D-043, T-092): its excerpt is the whole
             # period sentence, so a model clause never replaces it (the positive half of a mixed sentence must stay in the quote).
@@ -154,9 +169,15 @@ def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False,
         if i in used:
             continue
         f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", llm_spans[i], tagged, "llm_only")
+        _note_merged(f, lf)
         if lf.get("category") in _NEEDS_LEXICON:
             f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
         out.append(f)
+    for lf in filtered:
+        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", grounding.locate(body, lf["excerpt"]), tagged, "llm_only")
+        f["_tray"] = FILTERED
+        f["_last"] = True       # after every other tray item, so no recorded judge prompt (it carries the flag id) changes
+        out.append(f)
     for f in out:
         f["_stage"]["injection"] = tagged
         _compose(f)
@@ -182,7 +203,7 @@ def _model_conflicts(proposed: list, record: dict, tagged: bool) -> list:
                 f["title"], f["explanation"] = FT.render("conflict", lf["category"], provider_a=record.get("source"), date_a=record.get("date_iso"),
                                                          quote_a=lf["excerpt"], quote_b=lf["excerpt_b"])
             except KeyError:
-                pass
+                pass        # a category outside the closed list: ground() marks it SCHEMA_INVALID (visible, not dropped); no model text is used as a title
         f["_tray"] = "LLM_ONLY"
         out.append(f)
     return out
@@ -197,7 +218,8 @@ def ground(flags: list, record: dict) -> list:
         elif f["origin"] == "llm" and FT.TYPE_OF.get(f["category"]) != f["type"]:
             fail.append("SCHEMA_INVALID")
         f["_stage"]["grounding_failures"] = fail
-        f["ladder"]["code_checks"] = {"excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
+        f["ladder"]["code_checks"] = {**{k: v for k, v in (f["ladder"].get("code_checks") or {}).items() if k == "merged_categories"},
+                                      "excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
         _compose(f)
     return flags
 
@@ -239,7 +261,8 @@ def run_flag_pass(record: dict, *, call, tagged: bool = False, accident_year=Non
     flags = merge(llm, lexicon_flags(record, accident_year), record, tagged, llm_failed=failed, fixture_miss=miss)
     # tray items go LAST: a flag's id (f_r<n>_<k>) is its position in this list and is part of the judge's prompt, so inserting an item that used to be
     # dropped must not renumber the flags after it (recorded judge answers are keyed on that prompt)
-    flags = [f for f in flags if "_tray" not in f] + [f for f in flags if "_tray" in f] + _model_conflicts(conflicts, record, tagged)
+    last = [f for f in flags if f.pop("_last", False)]
+    flags = [f for f in flags if "_tray" not in f] + [f for f in flags if "_tray" in f and f not in last] + _model_conflicts(conflicts, record, tagged) + last
     ground(flags, record)
     for f in flags:
         code = f.pop("_tray", None)
@@ -332,6 +355,11 @@ def _judge_one(f: dict, i: int, *, call, case_text: str = "") -> None:
 def _to_tray(f: dict, code: str, judge_reason=None) -> None:
     """Move a flag to the could-not-verify tray: state rejected, the reason code first, a fixed sentence (plus the judge's fixed detail sentence)."""
     f["state"] = "rejected"
+    if code == FILTERED:
+        f["_stage"]["judge"] = None
+        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding failure / injection reason (T-126 r2)
+        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERBATIM"))
+        return
     if code == "LLM_ONLY":
         # never sent to a judge by design (model-only, not code-confirmed): it carries its real reason, not the compose default "judge unavailable"
         # (T-122: the eval counted case_05's f_r1_1 as a judge that did not run)
@@ -340,6 +368,8 @@ def _to_tray(f: dict, code: str, judge_reason=None) -> None:
     f["reasons"] = [code] + [r for r in f["reasons"] if r != code]
     detail = why.judge_detail(judge_reason) if judge_reason else ""
     f["why"] = why.why(code) + (" " + detail if detail else "")
+    if code == "LLM_ONLY" and f.get("type") == "conflict":
+        f["why"] = why.MODEL_CONFLICT       # T-113 r2 F5: a conflict is never a phrase-list item; say why it is in the tray
 
 
 def judge_flags(flags: list, *, call, case_text: str = "") -> list:
diff --git a/app/backend/ingest.py b/app/backend/ingest.py
index 0bfb90b..efca1fa 100644
--- a/app/backend/ingest.py
+++ b/app/backend/ingest.py
@@ -126,17 +126,25 @@ def _split(text: str):
         if not f["complete"]:
             method = "ambiguous"
         end = max(e for _, e in cov)
+        f["first"] = min(x for x, _ in cov)             # where the block's own fields start (a block can begin with a preamble line)
         items.append((a, end, f))
     for s, e in _leftovers(text, cov_all):
         items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
         method = "ambiguous"
-    items.sort(key=lambda t: t[0])
+    # T-129: record numbers are the paralegal's citations, so they count only the real records, in paste order. Unsplit text (a preamble, a note between separators) is kept
+    # (D-027: nothing is dropped) but numbered AFTER the real records, so a fax cover sheet on top never shifts "record 1" to "record 2". Text above the first real record
+    # is marked `preamble`.
+    items.sort(key=lambda t: (bool(t[2].get("unsplit")), t[0]))
+    first_real = min((f["first"] for _a, _e, f in items if not f.get("unsplit")), default=None)
+    for _a, e, f in items:
+        if f.get("unsplit") and first_real is not None and e <= first_real:
+            f["preamble"] = True
     return [_record(i + 1, text[a:e], a, e, f) for i, (a, e, f) in enumerate(items)], method
 
 
 def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
     return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
-            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit"))}
+            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit")), "preamble": bool(p.get("preamble"))}
 
 
 class SplitFailed(Exception):
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index a504bf9..d317e06 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -143,13 +143,45 @@ def _store_split_failure(conn, cid: str, reason) -> None:
     DB.update_case(conn, cid, config_json=cfg or None)
 
 
-def _store_records(conn, cid: str, ing: dict) -> None:
+def _store_record_marks(conn, cid: str, ing: dict) -> None:
+    """T-129: which stored records are unsplit text (D-027) and which of those is a preamble, kept in the case config so GET case serves them (record_view)."""
+    marks = {"unsplit_records": [r["id"] for r in ing["records"] if r.get("unsplit")], "preamble_records": [r["id"] for r in ing["records"] if r.get("preamble")]}
+    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
+    if all(cfg.get(k, []) == v for k, v in marks.items()):
+        return
+    for k, v in marks.items():
+        if v:
+            cfg[k] = v
+        else:
+            cfg.pop(k, None)
+    DB.update_case(conn, cid, config_json=cfg or None)
+
+
+def _item_record_ids(item: dict) -> list:
+    return list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
+
+
+def _reset_reviewed_on(conn, cid: str, moved: set, now: float) -> None:
+    """T-129 r2: a record number now names different text (a re-run after the numbering changed, or a model split that moved). A decision the paralegal made on an item
+    that cites such a record was made on other text, so it goes back to pending (the review event keeps what it was); the run then rebuilds or removes the item."""
+    if not moved:
+        return
+    for kind in ("entry", "amount", "flag"):
+        for it in DB.list_items(conn, cid, kind):
+            if it["review_status"] != "pending" and moved & set(_item_record_ids(it)):
+                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
+
+
+def _store_records(conn, cid: str, ing: dict, now: float = 0.0) -> None:
     """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
     or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
     before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
+    _store_record_marks(conn, cid, ing)
     stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
     if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
         return
+    new_spans = {r["id"]: (r["char_start"], r["char_end"]) for r in ing["records"]}
+    _reset_reviewed_on(conn, cid, {i for i, a, b in stored if new_spans.get(i) != (a, b)}, now)
     conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
     try:
         conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
@@ -215,7 +247,7 @@ def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
 def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
     """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
     ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
-    _store_records(conn, cid, ing)
+    _store_records(conn, cid, ing, now)
     _persist(conn, cid, "flag", ing["flags"], now)
     _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
     DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
@@ -284,7 +316,7 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     _store_split_failure(conn, cid, ing.get("split_failure"))
     if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
         errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
-    _store_records(conn, cid, ing)
+    _store_records(conn, cid, ing, clock())
     dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
     entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
     code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
@@ -365,9 +397,9 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
     final_amounts = [_clean(a) for a in final_amounts]
     damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
+    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
     from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
     PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
-    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
     now_t = clock()
     _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
     _persist(conn, cid, "amount", final_amounts, now_t)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:58:23.440Z

**tool call — Bash**
````
{
 "command": "git diff 63e18ed 0c24f5f -- app/llm/lexicon.yaml | cut -c1-240 | head -220"
}
````

### User / tool · 2026-11-02T12:58:23.569Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:58:37.969Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arch0c24 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --check-fresh; echo exit=$?; /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'E'\nimport json\nd=json.load(open('evals/reports/latest.json'))\nprint({k:d.get(k) for k in ('source_commit','backend','ship_bar_met','tree_clean','generated_at')})\nprint(d.get('hashes') or [k for k in d][:30])\nE\ngrep -n \"lexicon.yaml\\|FIXTURE_MISS\" ../evalout/20261102T125447Z.md | head; cd /Users/arsis/zlayt-pm-project; git log -1 --format=%h -- evals/reports/latest.json; git show 63e18ed:app/llm/lexicon.yaml | shasum -a 256; shasum -a 256 app/llm/lexicon.yaml; grep -n lexicon.yaml evals/reports/20261102T120809Z.md | cut -c1-200"
}
````

### User / tool · 2026-11-02T12:58:38.256Z

**tool result**
````
check-fresh: app/llm/lexicon.yaml changed since the report
check-fresh: app/llm/prompts/judge_conflict_v6.md changed since the report
exit=1
{'source_commit': None, 'backend': 'fixture', 'ship_bar_met': False, 'tree_clean': None, 'generated_at': '2026-11-02T09:56:40Z'}
{'app/llm/lexicon.yaml': 'a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263', 'app/llm/prompts/extract_es_v1.md': '985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb', 'app/llm/prompts/extract_v1.md': '11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2', 'app/llm/prompts/flags_v1.md': 'd5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725', 'app/llm/prompts/judge_amount_class_v1.md': 'e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8', 'app/llm/prompts/judge_conflict_v1.md': '10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa', 'app/llm/prompts/judge_conflict_v2.md': '6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6', 'app/llm/prompts/judge_conflict_v4.md': '15df87e8655a014111bbcddb2fee769d01e28149072ceea76f3f9d51fcae4649', 'app/llm/prompts/judge_conflict_v5.md': '90deea934564aa0fda0ad34dc38477104e371c0267259c38c61f58635819dffd', 'app/llm/prompts/judge_faithfulness_es_v1.md': 'd51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898', 'app/llm/prompts/judge_faithfulness_v1.md': '636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b', 'app/llm/prompts/judge_flag_v1.md': '97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432', 'app/llm/prompts/judge_flag_v2.md': '7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe', 'app/llm/prompts/judge_flag_v3.md': '64d65c0182360d4ef84b5f4b62e19a6707ee3f508d975aec4ea6e527c9a5a664', 'app/llm/prompts/narrative_v1.md': '3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac', 'app/llm/prompts/split_v1.md': '9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b'}
71:- `app/llm/lexicon.yaml` c0178e302a6d609202cba813b2e2edf839d9b5ac23835b41bf11febc80524d9a
78450f6
a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263  -
c0178e302a6d609202cba813b2e2edf839d9b5ac23835b41bf11febc80524d9a  app/llm/lexicon.yaml
138:- `app/llm/lexicon.yaml` a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:58:58.086Z

**tool call — Bash**
````
{
 "command": "grep -l \"verify_quickly\" reviews/*.md | head -20; grep -h -o '\"verify_quickly\": *[0-9.]*' reviews/*paralegal*.md | head -20; ls -t reviews | grep -i paralegal | head -8; python3 - <<'E'\nimport json\nd=json.load(open('evals/reports/calibration.json'))\nprint({k:v for k,v in d.items() if not isinstance(v,(list,dict))}); print(list(d)[:12])\nE\ngit log -3 --format='%h %ad %s' --date=iso -- evals/reports/calibration.json | cat; cat .claude/agent-memory/qa/project_calibration_route.md | head -40"
}
````

### User / tool · 2026-11-02T12:58:58.245Z

**tool result**
````
reviews/CONTRACT-M2M3-paralegal.md
reviews/CONTRACT-M2M3-product-manager.md
reviews/T-013-paralegal-r3.md
reviews/T-013-paralegal-r2.md
reviews/T-013-product-manager-r3.md
reviews/T-013-product-manager-r2.md
reviews/T-015-paralegal-r3.md
reviews/T-015-paralegal-r2.md
reviews/T-017-product-manager.md
reviews/T-018-product-manager-r2.md
reviews/T-018-product-manager.md
reviews/T-025-product-manager-r2.md
reviews/T-025-product-manager.md
reviews/T-041-paralegal-r2.md
reviews/T-043-paralegal-r2.md
reviews/T-041-paralegal.md
reviews/T-043-paralegal.md
reviews/T-056-paralegal-r2.md
reviews/T-056-paralegal.md
reviews/T-060-paralegal-pass1.md
"verify_quickly": 3
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 2
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 3
"verify_quickly": 4
"verify_quickly": 4
"verify_quickly": 3
"verify_quickly": 4
"verify_quickly": 3
"verify_quickly": 3
"verify_quickly": 3
"verify_quickly": 3
T-060-paralegal-pass5.md
T-120-paralegal-r4.md
T-114-paralegal-r3.md
T-060-paralegal-pass4.md
T-120-paralegal-r3.md
T-120-paralegal-r2.md
T-123-paralegal.md
T-121-paralegal.md
{'backend': 'fixture', 'case_count': 10, 'generated_at': '2026-11-02T12:48:56Z', 'match_rule': 'entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.', 'schema': 'evals.calibration/1', 'small_sample': True, 'source': 'evals.run over the golden cases; measured counts only (D-042, scope cut 10)', 'source_commit': '6fa8eccdc881d1660c55103534fd7ebd370d545c', 'source_tree': '948eabad4a016f6d0a17826ad896e02caf85289f', 'source_tree_clean': True}
['backend', 'by_state', 'by_type', 'case_count', 'cases', 'generated_at', 'hashes', 'match_rule', 'models', 'not_scored', 'schema', 'sentences']
f3ac48f 2026-11-02 06:49:07 -0600 chore(evals): regenerate calibration.json from a clean worktree of 6fa8ecc (fixture; lexicon.yaml T-133 r3)
4065ef2 2026-11-02 06:34:40 -0600 chore(evals): regenerate calibration.json from a clean worktree of f939ccb (fixture; lexicon.yaml T-133 r2)
1218b2e 2026-11-02 06:16:24 -0600 chore(evals): regenerate calibration.json from a clean worktree of e79c3aa (fixture; lexicon.yaml T-133)
---
name: calibration-route-and-regen
description: How GET /api/calibration decides stale, how calibration.json is regenerated from a clean worktree, and the fixture-dir pitfall in score_unsplit
metadata:
  type: project
---

GET /api/calibration lives in app/backend/calibration_route.py (T-099, stale flag T-102). It serves evals/reports/calibration.json read-only.
`calibration.stale` / `stale_reason` compare the file's recorded `hashes` (prompts + lexicon, sha256) with the same files at HEAD
(`git cat-file blob HEAD:path`, cached per HEAD sha); a checkout-less copy falls back to disk. Hashes are never served.

**Why:** the served numbers must say when they describe older prompts (T-096 shows "numbers from an older version").
**How to apply:** when prompts change, regenerate before the gate. Do it in a clean worktree, not the shared tree:
`git worktree add <scratchpad>/<unique-name> HEAD`, then `.venv/bin/python -m evals.run --write-calibration --backend fixture` from
inside it (the committed file is refused from a dirty tree), copy the file back (`cmp` it), commit it, then `git worktree remove --force`.
Pick a unique worktree name: a `wt` folder already existed in the scratchpad (an old copy of the project with a .env) and was not touched.

Pitfalls:
- evals/run.py `score_unsplit` sets LLM_FIXTURE_DIR to tests/fixtures/llm/split for the unsplit case, and fixture.call does not fall back
  to the default dir when LLM_FIXTURE_DIR is set. The other LLM calls in that case miss (FIXTURE_MISS), judge_unavailable_count > 0, and
  the report shows blocker 4_no_invented_facts. Golden-case calibration counts are unaffected. Open follow-up for qa.
- The count changes between regenerations come from code as well as prompts (T-110 and others), so 83/84 became 84/85 at HEAD.
- git-guard rejects `git add ... && git commit ...` in one Bash call: stage in one call, commit in the next.
- `timeout` is not installed on this Mac; use the Bash tool's timeout parameter.
- The git-guard hook and `git commit -- <paths>` only commit the listed paths; the shared index often holds other workers' staged deletions.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:59:04.364Z

**tool call — Bash**
````
{
 "command": "for f in $(ls -tr reviews/*paralegal*.md | tail -12); do echo \"$f $(stat -f %Sm -t %m%d-%H:%M $f) $(grep -h -o '\"verify_quickly\": *[0-9.]*' $f | tr '\\n' ' ') $(grep -h -o '\"verdict\": *\"[a-z]*\"' $f | head -1)\"; done; ls reviews | grep -i GATE | head; git log -1 --format='%h %ad' --date=iso -- reviews/T-060-paralegal-pass5.md | cat"
}
````

### User / tool · 2026-11-02T12:59:04.718Z

**tool result**
````
reviews/T-116-paralegal-r4.md 1102-04:43  "verdict": "fail"
reviews/T-116-paralegal-r5.md 1102-04:50  "verdict": "changes"
reviews/T-114-paralegal-r2.md 1102-05:00 "verify_quickly": 3  "verdict": "changes"
reviews/T-120-paralegal.md 1102-05:24 "verify_quickly": 2  "verdict": "fail"
reviews/T-121-paralegal.md 1102-05:25 "verify_quickly": 4  "verdict": "pass"
reviews/T-123-paralegal.md 1102-05:25 "verify_quickly": 4  "verdict": "pass"
reviews/T-120-paralegal-r2.md 1102-05:32 "verify_quickly": 3  "verdict": "fail"
reviews/T-120-paralegal-r3.md 1102-05:48 "verify_quickly": 3  "verdict": "fail"
reviews/T-060-paralegal-pass4.md 1102-05:55 "verify_quickly": 4  "verdict": "changes"
reviews/T-114-paralegal-r3.md 1102-05:56 "verify_quickly": 4  "verdict": "pass"
reviews/T-120-paralegal-r4.md 1102-05:58 "verify_quickly": 3  "verdict": "pass"
reviews/T-060-paralegal-pass5.md 1102-06:34 "verify_quickly": 4  "verdict": "changes"
GATE-M0-summary.md
GATE-M1-summary.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:59:11.160Z

**tool call — Bash**
````
{
 "command": "head -30 reviews/T-060-paralegal-pass5.md | cut -c1-300; grep -n -i \"e2e\" memory/STATE.md | head -8 | cut -c1-300; grep -rn \"m2\" memory/STATE.md | head -5 | cut -c1-300"
}
````

### User / tool · 2026-11-02T12:59:11.267Z

**tool result**
````
# T-060 pass 5: paralegal-reviewer (Maria Delgado persona)

Verdict: **changes** (0 blockers, 2 majors, 12 minors, 1 nit). Commit under review: b612176 (HEAD at review start: b6121766039c820e37a2a8df504b693103d89fc2; `git diff --stat b612176 HEAD -- app/frontend` is empty). I ran `git archive b612176` into the scratchpad (`p5-b612176`) and served it on 127.0

The letter is still clean: every quote is verbatim and the $185 rate stays out of the total. The state is still the problem. The edited record 3 can be recorded as compared by one `a` keypress, the row keeps "Needs review" next to "Accepted", and after that the export bar, the header and the copy wa

## Pass-4 majors, re-checked

| Pass-4 item | Status at b612176 | Evidence |
|---|---|---|
| M1: dismissed flag or amount keeps Accept, `a` turns it into Accepted | Mostly fixed. A dismissed flag and a dismissed amount show only Dismissed and Undo (plus Audit and links); `a` on either leaves progress and the row unchanged. Not fixed: they are not collected under "Dismissed (n)" (F2). | `a
| M2: edited entry marked Needs review has no control, counts as decided, export says "Nothing left to decide" | Partly fixed, partly regressed. Mouse path: the header counts the edit as open and the copy warning names it. But "I compared it with the quote" leaves the Needs review chip on the row, a

## Pass-4 minors, re-checked

- m1 (j/k coverage): open, F4.
- m2 (one-line letter has no control): fixed. The export panel has a "One line per entry (date, provider, quote)" radio; output is one line per entry and charge with the `[Ex. __ / Bates __]` placeholder. `p5-13-case1-dismiss-entry-oneline.out.txt`, `p5-13-letter-oneline.txt`.
- m3 (dismissed entry leaves its accepted charge in the letter and total): open, F5.
- m4 (`o` then `a` swallowed): open, F6.
- m5 (batch button, no question, "verified"): open, F7.
- m6 (ISO row dates): fixed. Rows read "January 9, 2026" (`p5-01-body.txt` line 51).
- m7 (dismissed amount not in notes): open, F8.
- m8 (refusal lingers; no live check line): open, F9.
- m9 (rate reads Accepted): open, F10.
- m10 (accuracy figure on case screen): open, F11.
- m11 (phrase list wording): open, F12.
- m12 (lib09 notice drops the record-4 assumption): open, F13.
- n1 (Causation language group): open, F15.

## What I ran
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:59:20.528Z

**tool call — Bash**
````
{
 "command": "git diff 63e18ed 0c24f5f -- app/backend/summary_trim.py | cut -c1-260 | head -170; git log --oneline 63e18ed..0c24f5f -- app/backend/summary_trim.py | cat"
}
````

### User / tool · 2026-11-02T12:59:20.648Z

**tool result**
````
diff --git a/app/backend/summary_trim.py b/app/backend/summary_trim.py
index 548c867..e2bb2fc 100644
--- a/app/backend/summary_trim.py
+++ b/app/backend/summary_trim.py
@@ -6,7 +6,7 @@ Why: the generator sometimes summarizes beyond its own excerpt ('Initial consult
 Judge 1 rightly objects, and a ship bar that depends on the model's luck flaps. Trimming by code is deterministic and keeps 'every statement traces to a quote'.
 
 Rule (T-112 r2: remove only what is demonstrably NEW, never a faithful paraphrase; the judge still checks everything that stays):
- 1. Split the summary into clauses at ';' ',' sentence-ending '.' and the joins ' and ' / ' with ' (no split inside '1,200', '6.5', 'Dr.', 'approx.', 'e.g.').
+ 1. Split the summary into clauses at ';' ',' sentence-ending '.' and the join ' and ' (NOT ' with ': 'Neck pain consistent with sprain.' is ONE clause, so a removed object can never strand its head word) (no split inside '1,200', '6.5', 'Dr.', 'approx.', 'e.
  2. A clause is REMOVED only when it carries salient new content, i.e. at least one of these is not in the quote (the record's source label and parsed date also count
     as present, as in grounding.new_tokens):
       a. a number or a month name (D-034; 'six', 'twice', 'x2' in the quote count as 2, 6 ...);   b. a side (left / right / bilateral; 'L', 'lt', 'both' in the quote count);
@@ -22,9 +22,13 @@ Rule (T-112 r2: remove only what is demonstrably NEW, never a faithful paraphras
     Terms (d-f) are matched by word FAMILY (lexicon below): the quote supports a term when it has a word of the same family (Tylenol~acetaminophen, cervical~neck,
     fingers~digits, prescription~prescribed) or of a family that covers it (a bare 'scan' is covered by MRI or CT; 'spine' by neck or back).
  3. A clause with no salient new content STAYS, whatever its other words ('Dizziness reported.' over 'Pt dizzy since crash.'; 'Walks with a cane' over 'Patient ambulating
-    with cane'); the judge checks it. Whole clauses only: a kept clause is never edited, and when removing a clause would leave a fragment (a kept clause that starts with
-    an article or preposition, or a lone noun left after a removed ' with ' clause: 'Laceration repaired with sutures.' never becomes 'Sutures.') nothing is trimmed.
-    A lone participle before a removed ' with ' clause ('diagnosed' in 'diagnosed with diabetes') is that clause's head word and is removed with it.
+    with cane'); the judge checks it. Whole clauses only: a kept clause is never edited. What code guarantees (T-128 r2/r3, D-054), with no word list. It does NOT guarantee that the kept text reads as a finished sentence: a clause is never
+    edited, a kept ' and ' clause can still be a short phrase, and the judge and the human check the wording:
+      (1) trim only a SUFFIX (T-128 r3): the kept text is always a prefix of whole clauses, and a clause is removed only when every clause after it is removed too,
+          so no kept clause can follow (and depend on) a removed one ('Shoulder pain; surgery performed; due to torn labrum.' keeps both or drops the tail);
+      (2) the FIRST clause is never removed: when it is unsupported nothing is trimmed and the whole summary goes to judge 1 (unless every clause is unsupported: rule 4);
+      (3) the kept prefix has at least 2 content words.
+    When a rule says no, the summary is returned unchanged. ' with ' is not a clause boundary, so 'diagnosed with diabetes' is one clause: removed whole or kept whole.
  4. If every clause is removed, or the clauses left have no content word at all (stopwords and numbers only), `text` is '' and the caller sends the item to the
     could-not-verify tray (D-053/D-054). A summary with no removal is returned unchanged, byte for byte."""
 import re
@@ -74,9 +78,8 @@ for _g in _GROUPS:
         _GROUP_OF.setdefault(_w, set()).update(_g)
 
 _WORD = re.compile(r"[a-z]+")
-_NEG = re.compile(r"\b(?:no|not|none|never|without|denies|denied|deny|negative|neither|nor|absent)\b|n't\b", re.IGNORECASE)
 _SUFFIXES = ("ations", "ation", "ments", "ment", "ness", "ings", "ing", "ied", "ies", "ed", "es", "s", "ly", "al")
-_SPLIT = re.compile(r";|,(?!\d)|(?<!\d),|\s+(?:and|with)\s+|\.(?=\s|$)", re.IGNORECASE)
+_SPLIT = re.compile(r";|,(?!\d)|(?<!\d),|\s+and\s+|\.(?=\s|$)", re.IGNORECASE)
 _STRENGTH = {";": 2, ",": 1, ".": 3}
 
 
@@ -90,15 +93,14 @@ def _stem(w: str) -> str:
 
 
 # Clinical abbreviations are expanded to the words (and family words) they stand for, in the quote AND in the summary, so 'Chin lac.' supports 'Laceration to the chin'
-# and 'Laceration' supports 'lac' alike. Case-sensitive entries are ordinary English words when lower case (US/us, IM/I'm, OA, RA, LE, UE, IV).
+# and 'Laceration' supports 'lac' alike. Case-sensitive entries are ordinary English words when lower case (US/us, IM/I'm, OA, RA, LE, UE). Inert entries (IV, HEP, EKG) were removed: they changed no trim (T-128 r2)..
 _ABBR_CASE = {"US": "ultrasound", "IM": "intramuscular injection", "OA": "osteoarthritis", "RA": "rheumatoid arthritis", "LE": "lower extremity leg",
-              "UE": "upper extremity arm", "IV": "intravenous"}
+              "UE": "upper extremity arm"}
 _ABBR = {"lac": "laceration", "lacs": "laceration", "djd": "degenerative joint disease", "esi": "epidural steroid injection", "tpi": "trigger point injection",
          "rcr": "rotator cuff repair surgery", "tka": "total knee arthroplasty surgery", "tha": "total hip arthroplasty surgery", "orif": "open reduction internal fixation surgery",
          "acdf": "anterior cervical discectomy fusion surgery neck", "apap": "acetaminophen", "abx": "antibiotic", "cp": "chest pain", "cxr": "chest xray",
          "ble": "bilateral lower extremity leg", "lle": "left lower extremity leg", "rle": "right lower extremity leg",
-         "bue": "bilateral upper extremity arm", "lue": "left upper extremity arm", "rue": "right upper extremity arm", "hep": "home exercise program",
-         "ekg": "ecg", "u/s": "ultrasound"}
+         "bue": "bilateral upper extremity arm", "lue": "left upper extremity arm", "rue": "right upper extremity arm", "u/s": "ultrasound"}
 _ABBR_RX = re.compile(r"(?<![a-z0-9/])(" + "|".join(sorted((re.escape(k) for k in _ABBR), key=len, reverse=True)) + r")(?![a-z0-9/])")
 _ABBR_CASE_RX = re.compile(r"(?<![A-Za-z0-9/])(" + "|".join(_ABBR_CASE) + r")(?![A-Za-z0-9/])")
 
@@ -216,7 +218,7 @@ _FAMILIES = [
     ("proc", "mri", r"^mri$|^magnetic$", (), ""), ("proc", "ct", r"^ct$|^cat$|^tomograph", (), ""), ("proc", "xray", r"^xray|^radiograph|^xr$|^films?$", (), ""),
     ("proc", "ultrasound", r"^ultrasound|^sonogra", (), ""), ("proc", "emg", r"^emg$|^electromyo|^ncv$|^ncs$|^conduction$", (), ""),
     ("proc", "imaging", r"^imaging$|^scans?$", ("mri", "ct", "xray", "ultrasound"), ""),
-    ("proc", "surgery", r"surg|^operat|^arthroscop|^fusion$|ectomy$|plasty$", (), ""),
+    ("proc", "surgery", r"surg|^operat|^arthroscop|^fusion$|ectomy$|plasty$", (), r"^reduction$|^fixation$|^arthroplasty|^repair"),     # quote side: ORIF / RCR spelled out
     ("proc", "injection", r"^inject|^epidural|^esi$|^shots?$|^infusion", (), ""),
     ("proc", "therapy", r"^therap|^physio|^rehab|^chiropract|^acupunct|^massage|^traction$|^manipulat", (), r"^pt$"),
     ("proc", "plan", r"^order|^recommend|^advis|^request|^schedul|^arrang|^authori[sz]|^suggest|^propos", (), ""),
@@ -264,8 +266,7 @@ _FAMILIES = [
 ]
 _FAM = [(k, n, re.compile(rx), cov, re.compile(qx) if qx else None) for k, n, rx, cov, qx in _FAMILIES]
 _BODY = frozenset(n for k, n, *_ in _FAMILIES if k == "body")
-_NEG_WORDS = frozenset({"no", "not", "none", "never", "without", "denies", "denied", "negative", "neither", "nor", "absent"})
-_SIDE_WORDS = frozenset({"left", "right", "bilateral", "bilaterally"})
+# Negation and side words are the lexicon's (code_lists.added_qualifier through grounding.view / aq), not lists of this module (T-105 r2, T-128 r2).
 # Quote words that already carry a negation or a negative finding: a summary negation is then not NEW content (the judge decides if it is the right one).
 _QUOTE_NEG = re.compile(r"\b(?:normal|unremarkable|wnl|nl|clear|intact|resolved|resolving|ruled|r/o|free|unable|cannot|persist\w*|unchanged|fail\w*|lack\w*|neg|non\w+|un[a-z]{4,}|"
                         r"nad|nkda|nonspecific)\b|\w+n't\b|\bw/o\b", re.IGNORECASE)
@@ -276,7 +277,6 @@ _NUMWORDS = {"zero": 0, "no": None, "one": 1, "once": 1, "single": 1, "two": 2,
              "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
              "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100, "dozen": 12}
 _MONTHS = grounding._MONTHS
-_LEAD = frozenset("a an the his her their its of to in on at for by from as with without and or but per via".split())
 
 
 def _family_hits(words) -> dict:
@@ -335,11 +335,11 @@ def new_salient(clause: str, quote: dict) -> list:
             out.append(m.lower())
     sw = grounding.side_neg_words(clause, keep_order=True)
     for w in dict.fromkeys(sw):
-        if w in _SIDE_WORDS:
+        if grounding.aq("side").fullmatch(w):
             ok = w in quote["sides"] or (w.startswith("bilateral") and (quote["both"] or {"left", "right"} <= quote["sides"]))
             if not ok:
                 loose.append(w)
-        elif w.endswith("n't") or w in _NEG_WORDS:
+        elif w.endswith("n't") or grounding.is_negation_word(w):
             if not quote["neg"]:
                 loose.append(w)
     toks = re.findall(r"[A-Za-z0-9]+", clause)
@@ -361,7 +361,7 @@ _LABEL_FAMILIES = frozenset({"mri", "ct", "xray", "ultrasound", "emg", "imaging"
 
 def _quote_profile(excerpt: str, label: str, date_iso: str) -> dict:
     ex = excerpt or ""
-    sides = {w for w in grounding.side_neg_words(ex + " " + (label or "")) if w in _SIDE_WORDS}
+    sides = set()          # 'left' / 'right' by the abbreviation-aware patterns below; a quote's 'bilateral' sets "both" (_QUOTE_BOTH), which is how the summary's side is checked
     if _QUOTE_LEFT.search(ex + " " + (label or "")):
         sides.add("left")
     if _QUOTE_RIGHT.search(ex + " " + (label or "")):
@@ -371,28 +371,11 @@ def _quote_profile(excerpt: str, label: str, date_iso: str) -> dict:
     if m:
         month = _MONTHS[int(m.group(1)) - 1]
     low = (ex + " " + (label or "")).lower()
-    neg = bool(_NEG.search(ex) or _QUOTE_NEG.search(ex))
+    neg = bool(grounding.has_negation(ex, extra=True) or _QUOTE_NEG.search(ex))
     return {"nums": _number_set(ex, label or "", date_iso or ""), "low": low, "month": month, "sides": sides, "both": bool(_QUOTE_BOTH.search(ex) or _QUOTE_BOTH.search(_prep(ex))), "neg": neg,
             "forms": _quote_forms(ex + " " + (label or "")), "fams": _quote_families(_words(ex)) | {f for f in _quote_families(_words(label or "")) if f in _LABEL_FAMILIES or f in _BODY}}
 
 
-def _fragment(piece: str) -> bool:
-    first = _WORD.findall(piece.lower())[:1]
-    return bool(first) and first[0] in _LEAD
-
-
-_PARTICIPLE = re.compile(r"^(?:[a-z]+(?:ed|ing)|given|consistent|due|secondary|related|compatible|suggestive|positive)$")
-
-
-def _single_word(piece: str) -> str:
-    w = _WORD.findall(piece.lower())
-    return w[0] if len(w) == 1 else ""
-
-
-def _joined_by_with(sep: str) -> bool:
-    return sep.strip().lower() == "with"
-
-
 def trim(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> dict:
     """See the module docstring. Never edits a kept clause's words; only whole clauses are dropped, or nothing is."""
     clauses = split_clauses(summary or "")
@@ -402,27 +385,19 @@ def trim(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> dic
     unchanged = {"text": summary, "removed": [], "kept": [c[0] for c in clauses], "supported": bool(summary), "notes": [], "changed": False}
     if not any(drop):
         return unchanged
-    # 'diagnosed with diabetes': the lone participle left of a removed ' with ' clause is its head word, not a clause of its own: it goes with it (one removal, one note).
-    merged = {}
-    for i in range(len(clauses) - 1):
-        if not drop[i] and drop[i + 1] and _joined_by_with(clauses[i][1]) and _PARTICIPLE.match(_single_word(clauses[i][0])):
-            drop[i] = True
-            merged[i] = i + 1
-    removed = []
-    for i, (c, d) in enumerate(zip(clauses, drop)):
-        if not d or i - 1 in merged:
-            continue
-        text = c[0].rstrip(" .;,")
-        removed.append(f"{text} with {clauses[i + 1][0].rstrip(' .;,')}" if i in merged else text)
+    removed = [c[0].rstrip(" .;,") for c, d in zip(clauses, drop) if d]
     notes = [NOTE.format(r) for r in removed]
     left = [c[0] for c, d in zip(clauses, drop) if not d]
     if not left or not any(content_words(c) for c in left):
         return {"text": "", "removed": removed, "kept": [], "supported": False, "notes": notes, "changed": True}
-    if any(_fragment(c) for c in left):             # removing would leave 'A cane.'-style fragments: trim nothing, the judge checks the whole summary
+    # T-128 r2/r3 (D-054 'never leave a fragment'), structural, no word list:
+    if drop[0]:                                      # (2) the first clause is never removed: an unsupported first clause means the whole summary goes to judge 1
+        return unchanged
+    first_cut = drop.index(True)
+    if not all(drop[first_cut:]):                    # (1) SUFFIX ONLY (T-128 r3): a clause is removed only when every clause after it is removed too, so no kept clause can depend on a removed one
+        return unchanged
+    if len(content_words(" ".join(c[0] for c in clauses[:first_cut]))) < 2:       # (3) the kept prefix must carry at least 2 content words ('Pain.' alone is not a summary)
         return unchanged
eef92a7 fix(backend): T-128 fix-up stop splitting clauses at ' with ', drop the by-construction fragment claim
b348221 fix(backend): T-128 r3 trim only a suffix, n't contraction and quote-side tests
2790918 refactor(backend): summary_trim reads negation and side words from the lexicon (T-105 r2 leftover)
180138c fix(backend): T-128 r2 structural no-fragment rule (first clause kept, 2-word prefix, no dangling joins), inert abbreviations removed
3d53ca5 feat(backend): T-128 summary trim never leaves a fragment, pin r3 mutants
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:59:27.144Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/evals/reports/runs && grep -l \"removed from the summary\" 20261102T111525Z/* 20261102T113305Z/* 20261102T115041Z/* | head; grep -h -o \".\\{200\\}removed from the summary.\\{200\\}\" 20261102T111525Z/case_02_gap_boundaries.json | head -3"
}
````

### User / tool · 2026-11-02T12:59:27.239Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:59:31.522Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/evals/reports/runs && grep -l -i \"not in the quote\\|SUMMARY_NOT_IN_QUOTE\\|trim\" 2026110*/* 2>/dev/null | head; python3 - <<'E'\nimport json\nd=json.load(open('20261102T111525Z/case_02_gap_boundaries.json'))\nprint(list(d)[:20])\nE"
}
````

### User / tool · 2026-11-02T12:59:31.652Z

**tool result**
````
['backend', 'case', 'errors', 'items', 'models', 'run', 'schema', 'signature_parts', 'status', 'tray_flag_count', 'warning_codes']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:59:34.776Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/evals/reports && grep -h \"summary clauses removed\" 20261102T113305Z.md 20261102T115041Z.md 20261102T120809Z.md | cut -c1-260; grep -c . /dev/null; grep -n \"T-128\\|trim\" /Users/arsis/zlayt-pm-project/memory/SCOPE_CUTS.md | head -5 | cut -c1-250"
}
````

### User / tool · 2026-11-02T12:59:34.898Z

**tool result**
````
- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0, "per_case": {"case_02_gap_boundaries": {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0}}}
- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 0, "clauses_removed": 0, "tray_placeholders": 0, "per_case": {}}
- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 0, "clauses_removed": 0, "tray_placeholders": 0, "per_case": {}}
0
78:| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; the D-054 trimmer is vocabulary-bound, so it misses some abbreviations (fresh probes: 12/43 faithful pairs over-trimmed to the tray, 9/30 unsupported clauses kept). Bo
79:| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | memory/SCOPE_CUTS.md T-112 row; follow-up T-128 | see card | M2 |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:59:58.313Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport json,hashlib,subprocess\nd=json.load(open('evals/reports/calibration.json'))\nbad=[]\nfor p,h in d['hashes'].items():\n    try: b=subprocess.check_output(['git','cat-file','blob','HEAD:'+p])\n    except Exception: bad.append((p,'missing')); continue\n    if hashlib.sha256(b).hexdigest()!=h: bad.append(p)\nprint('stale vs HEAD:',bad)\nprint(d['by_state'] if 'by_state' in d else '')\nE\ngit diff --stat 63e18ed 0c24f5f -- app/llm/prompts evals/golden evals/library tests/fixtures | cat | tail -3; python3 -c \"print(55/57,56/57,54/57)\""
}
````

### User / tool · 2026-11-02T12:59:58.711Z

**tool result**
````
stale vs HEAD: []
{'needs_review': {'cases': ['case_01_date_formats', 'case_03_rate_and_ocr', 'case_07_prompt_injection', 'sample'], 'matched': 9, 'total': 9}, 'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', 'case_07_prompt_injection', 'case_08_diagnosis_temptation', 'case_09_nonvisit_hides_gap', 'sample'], 'matched': 84, 'total': 85}}
 evals/golden/judge_controls.jsonl         |  3 +++
 evals/golden/judge_controls_heldout.jsonl |  8 +++++---
 3 files changed, 18 insertions(+), 5 deletions(-)
0.9649122807017544 0.9824561403508771 0.9473684210526315
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:00:38.270Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/GATE-M2-qa.md",
 "content": "# GATE-M2 qa review (ship bar, CONTRACT 8.2 and REQUIREMENTS section 7, D-046)\n\nPinned commit under review: `0c24f5f`. Verdict: **changes** (0 blockers, 1 major, 4 minors). The ship-bar numbers are met in the committed live evidence. That evidence was measured at `63e18ed`, not at the commit that will carry the `m2` tag. A fresh live 3-run at the tag commit is required before tagging (F1).\n\n## 1. Ship-bar rows against the committed live evidence\n\nThree live 3-runs (`claude-cli`, generator `claude-sonnet-5-5`, judge `claude-haiku-5-5`), all printing \"Source commit `63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6`, tree clean\", plus controls at `bea3984`, tree clean.\n\n| Row | Bar | 113305Z | 115041Z | 120809Z | Met |\n|---|---|---|---|---|---|\n| 1 Grounding | 100% | 1.000 (237) | 1.000 (238) | 1.000 (237) | yes |\n| 2 Entry recall | >= 0.95 | 0.965 | 0.982 | 0.982 | yes |\n| 2 Amount recall | >= 0.95 | 1.000 | 1.000 | 1.000 | yes |\n| 3 Flags (gap, conflict, pre_existing, causation) | P and R >= 0.9 each | 1.000 / 1.000 each | same | same | yes |\n| 3 gap_28 not flagged, gap_73 flagged | true | no missed must flags | same | same | yes |\n| 4 unsupported_count_3run | 0 | 0 | 0 | 0 | yes |\n| 4 determinism_3run | 1.0 | 1.0 | 1.0 | 1.0 | yes |\n| 4 hallucination_catch_rate | >= 0.95 | 40/40 | 40/40 | 40/40 | yes |\n| 4 golden_must_not_hits | 0 | 0 | 0 | 0 | yes |\n| 4 (D-046) J3 seeded controls | all wrong caught, 0 false agree | 16/16 x3, 0 false agree | same | same | yes |\n| 4 (D-046) J4 seeded controls | same | 12/12 x3, 0 false agree | same | same | yes |\n\n`evals/reports/controls-20261102T123937Z.md` (`bea3984`, `controls_ok: True`): J3 19/19 wrong caught x3 (13 in-sample, 6 held-out), correct accepted 18/18, false agree 0, unstable []. J4 12/12 x3 (9 in-sample, 3 held-out), correct accepted 15/15, false agree 0. This also satisfies D-046. The judge prompts and the golden and library data did not change between `63e18ed` and `0c24f5f` except the control files, so the judge-level controls still apply at the tag commit.\n\nRow 5 (reviewability) is a persona and E2E row. I did not re-run it. The latest whole-sample paralegal score is `verify_quickly` 4 (`reviews/T-060-paralegal-pass5.md`, at `b612176`, verdict changes with 2 majors). The frontend has changed since (`671f054`, T-136). The M2 paralegal panel member has to re-score it. Playwright E2E was not run for this review.\n\nHygiene checks:\n- Each of the three reports names its commit with a clean tree.\n- The per-run directories exist and are committed in `5dfba88`: `evals/reports/runs/20261102T111525Z`, `...T113305Z`, `...T115041Z` (14 files each: `run1..3.json`, `sample.json`, 9 case files, `calibration.json`).\n- `63e18ed` is an ancestor of `0c24f5f`.\n\n## 2. Exercised at 0c24f5f (git archive copy, scratchpad)\n\n- Unit suite: `pytest tests/unit` gives **3450 passed, 8 skipped, 0 failed** (194 s).\n- Fixture eval: `python -m evals.run --backend fixture`. Everything measurable replays at the bar:\n  - grounding 1.000 (241 checked)\n  - entry_recall 0.982 (same single case_06 E3 miss as live)\n  - amount_recall 1.000\n  - all four flag types 1.000 / 1.000\n  - hallucination_catch_rate 40/40, judge unavailable 0\n  - golden_must_not_hits 0\n  - unsplit_paste and case_07_total_420 true\n- The three blockers it prints are the fixture backend's by-design ones: determinism_3run and unsupported_count_3run are live-only, and the J3/J4 controls are not measured on fixture. They are not defects.\n\n## 3. Could the post-63e18ed changes move the live numbers?\n\nChanged after `63e18ed` and before `0c24f5f` (`git diff --stat`): `app/backend` (grounding, summary_trim, lexicon_scan, flags, export, present, trace, pipeline, ingest and others), `app/llm/lexicon.yaml`, `app/frontend`, and `evals/run.py` (report text only). No prompt file changed.\n\n- Recall, flags and amounts are code-deterministic over the recorded model output. The fixture replay at HEAD reproduces the live values, so these rows are very unlikely to move. The thin one is entry recall. The 57-entry denominator allows 2 misses: 55/57 = 0.965 passes and 54/57 = 0.947 fails. case_06 E3 is missed in every run and in the fixture, and case_02 E1 flaps.\n- Row 4 (unsupported_count_3run, determinism_3run) can move, and the fixture cannot show it. The cause is T-128 plus the T-105 and T-133 lexicon edits:\n  - The D-054 summary trim was what stopped item 4 flapping about one run in three on case_02. At HEAD it is strictly narrower (`summary_trim.py` docstring):\n    - it trims a suffix only;\n    - it never removes the first clause;\n    - it requires at least 2 content words in the kept prefix;\n    - when a rule says no, the summary is returned unchanged and goes whole to judge 1.\n  - A summary that `63e18ed` would have cut can now reach the judge untrimmed. It can come back \"partially\" or \"unsupported\", or be reworded by the new code checks.\n  - Live, the trim fired in only 1 of the 3 runs (case_02, 1 clause). The result is therefore sensitive to which wording the live model produces on a given day. The fixture run shows 0 trims because it replays an older recording, so it cannot exercise this path.\n  - Judge input text changed (trimmed summaries, `added_qualifier` lists, deny/denying as negation words), so the live J1 verdicts are not guaranteed identical.\n- The T-134 export gate and T-132 `lexicon_scan` changes act after the model and only block or flag more. They cannot add an ungrounded statement, but they change the lexicon-flag set (`history_significant_for` is a new pre_existing entry). That is a live-precision risk for the pre_existing type that fixture cannot rule out for unseen model wording.\n- Process: CONTRACT 8.3 says any change to a lexicon requires re-running `evals.run`. The lexicon hash in the live reports is `a2518d8f...` (the `63e18ed` file). HEAD is `c0178e30...`. `python -m evals.run --check-fresh` on the archive exits 1 (lexicon.yaml changed since the report).\n\n**Answer: yes. A fresh confirming live 3-run at the tag commit is needed before `m2` is tagged.** One run from a clean worktree of the final HEAD is enough, and the three-consecutive requirement is not needed for a confirming run. The earlier runs took about 17 minutes each. If any later gate fix changes `app/` or the lexicon after that run, it has to be repeated at the new tag commit.\n\n## 4. calibration.json\n\n`evals/reports/calibration.json` has only ever been regenerated on the **fixture** backend (`backend: fixture`, `source_commit 6fa8eccdc8`, clean tree, `f3ac48f`; earlier regens `1218b2e`, `4065ef2` were also fixture). Its counts are verified 84/85 and needs_review 9/9, on recorded replies. The live `claude-cli` calibration (83/84 verified; needs_review 9/10, then 10/10, 10/10) exists only inside the three timestamped reports at `63e18ed`. The file is not stale against HEAD prompts or lexicon (hashes match `HEAD:`), and it labels its backend, so it is honest. The product note must not present the 84/85 as live-model calibration.\n\n## 5. Findings\n\n```json\n{\n  \"card\": \"GATE-M2\",\n  \"persona\": \"qa\",\n  \"model\": \"claude-sonnet-5-5\",\n  \"verdict\": \"changes\",\n  \"summary\": \"Ship-bar rows 1-4 and the D-046 J3/J4 controls are met in committed, clean-tree live evidence measured at 63e18ed, and the unit suite and fixture eval pass at 0c24f5f. The live evidence does not cover the tag commit: lexicon, trim, lexicon_scan and export-gate code changed after it, so one confirming live 3-run at the tag commit is required before the m2 tag.\",\n  \"findings\": [\n    {\n      \"id\": \"F1\",\n      \"severity\": \"major\",\n      \"title\": \"Live ship-bar evidence is at 63e18ed; the tag commit has a different lexicon and a narrower summary trim, and CONTRACT 8.3 requires a live re-run\",\n      \"evidence\": \"evals/reports/20261102T113305Z.md, 115041Z.md, 120809Z.md all say 'Source commit 63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6'. Lexicon sha256 in 120809Z.md is a2518d8f... ; HEAD app/llm/lexicon.yaml is c0178e30... ; `python -m evals.run --check-fresh` exits 1 on the 0c24f5f archive ('lexicon.yaml changed since the report'). git diff --stat 63e18ed 0c24f5f changes app/backend/summary_trim.py (suffix-only, first clause never removed, unchanged when a rule says no), grounding.py, lexicon_scan.py, export.py, flags.py and lexicon.yaml (T-105 added_qualifier lists, T-133 deny/denying and history_significant_for). Row 4 (unsupported_count_3run, determinism_3run) is live-only and the fixture run reports it as None, so fixture cannot confirm it. The D-054 trim fired in 1 of 3 live runs (20261102T113305Z.md 'items_trimmed: 1', case_02).\",\n      \"recommendation\": \"Run one live `python -m evals.run` (3 runs, claude-cli) from a clean worktree of the final tag commit, commit the report and its runs/ directory, and require ship_bar_met True with unsupported_count_3run 0, determinism_3run 1.0 and J3/J4 controls unchanged. Re-run again if any later change touches app/ or the lexicon.\"\n    },\n    {\n      \"id\": \"F2\",\n      \"severity\": \"minor\",\n      \"title\": \"calibration.json has only been regenerated on the fixture backend\",\n      \"evidence\": \"evals/reports/calibration.json: backend 'fixture', source_commit 6fa8eccdc877d1660c55103534fd7ebd370d545c, verified 84/85, needs_review 9/9. Regenerated by 1218b2e, 4065ef2, f3ac48f, all fixture. Live claude-cli counts (83/84 verified; 9/10, 10/10, 10/10 needs_review) appear only in the three timestamped reports at 63e18ed. Hashes match HEAD prompts and lexicon (not stale).\",\n      \"recommendation\": \"The product note and Part 2 quote the live report counts and say which backend produced them; the app keeps its fixture label. After the F1 live run, decide in a card whether to regenerate the served file from the live run.\"\n    },\n    {\n      \"id\": \"F3\",\n      \"severity\": \"minor\",\n      \"title\": \"latest.json is a stale fixture report, not the ship-bar report\",\n      \"evidence\": \"evals/reports/latest.json: backend 'fixture', ship_bar_met False, generated_at 2026-11-02T09:56:40Z, source_commit None. REQUIREMENTS R-SU-3 says numbers in the note equal 'the latest eval report'. --check-fresh also flags judge_conflict_v6.md against this file's hashes.\",\n      \"recommendation\": \"The F1 live run should be the one that rewrites latest.json, and the writer should cite the timestamped live report by path.\"\n    },\n    {\n      \"id\": \"F4\",\n      \"severity\": \"minor\",\n      \"title\": \"Report timestamp and per-run directory timestamp are offset by one run\",\n      \"evidence\": \"20261102T113305Z.md lists 'per-run artifacts: evals/reports/runs/20261102T111525Z'; 20261102T115041Z.md lists runs/20261102T113305Z; 20261102T120809Z.md lists runs/20261102T115041Z. All three directories exist (14 files each, commit 5dfba88), but runs/20261102T113305Z belongs to report 115041Z, not to report 113305Z.\",\n      \"recommendation\": \"Cite the per-run path printed inside each report, never the report's own timestamp. Add a one-line mapping to the F1 commit message.\"\n    },\n    {\n      \"id\": \"F5\",\n      \"severity\": \"minor\",\n      \"title\": \"Row 5 (reviewability) and E2E were not re-verified at the tag commit; entry-recall margin is two misses\",\n      \"evidence\": \"Last whole-sample paralegal score is verify_quickly 4 in reviews/T-060-paralegal-pass5.md at b612176 (verdict changes, 2 majors); frontend changed in 671f054 afterwards. Playwright E2E was not run in this review. entry_recall is 55/57 = 0.965 in run 1; 54/57 = 0.947 would fail the 0.95 bar.\",\n      \"recommendation\": \"The M2 paralegal panel member re-scores verify_quickly at the tag commit and the orchestrator runs `pytest tests/e2e` there. The product note reports the recall misses (case_06 E3 every run; case_02 E1 in run 1) as found.\"\n    }\n  ],\n  \"exercised\": [\n    \"Read CONTRACT 8.2, REQUIREMENTS section 7 and D-046 and mapped each ship-bar row to the report metrics\",\n    \"Read all three live reports (113305Z, 115041Z, 120809Z) and controls-20261102T123937Z.md; checked source commit, tree-clean line, hashes and per-run artifact lines\",\n    \"Checked evals/reports/runs/{111525Z,113305Z,115041Z} exist and are committed (14 files each, commit 5dfba88); 63e18ed is an ancestor of 0c24f5f\",\n    \"git archive 0c24f5f into scratchpad: pytest tests/unit gave 3450 passed, 8 skipped\",\n    \"git archive 0c24f5f: python -m evals.run --backend fixture (all measurable metrics at the bar; the 3 blockers are fixture-only by design)\",\n    \"git archive 0c24f5f: python -m evals.run --check-fresh (exit 1, lexicon changed since the report)\",\n    \"git diff --stat 63e18ed 0c24f5f over app, evals, prompts, golden; read the diffs of summary_trim.py, flags.py, pipeline.py, ingest.py and lexicon.yaml\",\n    \"Checked calibration.json backend, source commit, counts and hashes against HEAD blobs\",\n    \"Not exercised: Playwright E2E, live LLM backend, paralegal re-score\"\n  ]\n}\n```\n"
}
````

### User / tool · 2026-11-02T13:00:38.391Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/GATE-M2-qa.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:00:42.671Z

Verdict **changes**: 0 blockers, 1 major, 4 minors; the review is in `/Users/arsis/zlayt-pm-project/reviews/GATE-M2-qa.md`.
- **Ship bar:** Rows 1–4 and the D-046 J3/J4 controls are met in all three live reports (113305Z, 115041Z, 120809Z) and in `controls-20261102T123937Z.md`. Each report names its commit with a clean tree, and the three per-run directories exist. On a `git archive 0c24f5f` copy, the unit suite gave 3450 passed, 8 skipped, and the fixture eval is at the bar apart from its three by-design live-only blockers. I did not run E2E or re-score row 5.
- **Major (F1):** Yes, a fresh live 3-run at the tag commit is needed before `m2`. The live evidence is at `63e18ed`, and the lexicon hash has changed (`--check-fresh` exits 1). T-128's suffix-only trim means judge 1 can now see untrimmed summaries, which can move `unsupported_count_3run` and `determinism_3run`; fixture can't show that because both are live-only. The `evals/reports/calibration.json` file has only been regenerated on the fixture backend (source `6fa8ecc`, 84/85); the live counts are only in the timestamped reports.
