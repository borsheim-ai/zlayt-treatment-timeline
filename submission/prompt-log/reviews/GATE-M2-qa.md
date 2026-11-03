# GATE-M2 qa review (ship bar, CONTRACT 8.2 and REQUIREMENTS section 7, D-046)

Pinned commit under review: `0c24f5f`. Verdict: **changes** (0 blockers, 1 major, 4 minors). The ship-bar numbers are met in the committed live evidence. That evidence was measured at `63e18ed`, not at the commit that will carry the `m2` tag. A fresh live 3-run at the tag commit is required before tagging (F1).

## 1. Ship-bar rows against the committed live evidence

Three live 3-runs (`claude-cli`, generator `claude-sonnet-5-5`, judge `claude-haiku-5-5`), all printing "Source commit `63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6`, tree clean", plus controls at `bea3984`, tree clean.

| Row | Bar | 113305Z | 115041Z | 120809Z | Met |
|---|---|---|---|---|---|
| 1 Grounding | 100% | 1.000 (237) | 1.000 (238) | 1.000 (237) | yes |
| 2 Entry recall | >= 0.95 | 0.965 | 0.982 | 0.982 | yes |
| 2 Amount recall | >= 0.95 | 1.000 | 1.000 | 1.000 | yes |
| 3 Flags (gap, conflict, pre_existing, causation) | P and R >= 0.9 each | 1.000 / 1.000 each | same | same | yes |
| 3 gap_28 not flagged, gap_73 flagged | true | no missed must flags | same | same | yes |
| 4 unsupported_count_3run | 0 | 0 | 0 | 0 | yes |
| 4 determinism_3run | 1.0 | 1.0 | 1.0 | 1.0 | yes |
| 4 hallucination_catch_rate | >= 0.95 | 40/40 | 40/40 | 40/40 | yes |
| 4 golden_must_not_hits | 0 | 0 | 0 | 0 | yes |
| 4 (D-046) J3 seeded controls | all wrong caught, 0 false agree | 16/16 x3, 0 false agree | same | same | yes |
| 4 (D-046) J4 seeded controls | same | 12/12 x3, 0 false agree | same | same | yes |

`evals/reports/controls-20261102T123937Z.md` (`bea3984`, `controls_ok: True`): J3 19/19 wrong caught x3 (13 in-sample, 6 held-out), correct accepted 18/18, false agree 0, unstable []. J4 12/12 x3 (9 in-sample, 3 held-out), correct accepted 15/15, false agree 0. This also satisfies D-046. The judge prompts and the golden and library data did not change between `63e18ed` and `0c24f5f` except the control files, so the judge-level controls still apply at the tag commit.

Row 5 (reviewability) is a persona and E2E row. I did not re-run it. The latest whole-sample paralegal score is `verify_quickly` 4 (`reviews/T-060-paralegal-pass5.md`, at `b612176`, verdict changes with 2 majors). The frontend has changed since (`671f054`, T-136). The M2 paralegal panel member has to re-score it. Playwright E2E was not run for this review.

Hygiene checks:
- Each of the three reports names its commit with a clean tree.
- The per-run directories exist and are committed in `5dfba88`: `evals/reports/runs/20261102T111525Z`, `...T113305Z`, `...T115041Z` (14 files each: `run1..3.json`, `sample.json`, 9 case files, `calibration.json`).
- `63e18ed` is an ancestor of `0c24f5f`.

## 2. Exercised at 0c24f5f (git archive copy, scratchpad)

- Unit suite: `pytest tests/unit` gives **3450 passed, 8 skipped, 0 failed** (194 s).
- Fixture eval: `python -m evals.run --backend fixture`. Everything measurable replays at the bar:
  - grounding 1.000 (241 checked)
  - entry_recall 0.982 (same single case_06 E3 miss as live)
  - amount_recall 1.000
  - all four flag types 1.000 / 1.000
  - hallucination_catch_rate 40/40, judge unavailable 0
  - golden_must_not_hits 0
  - unsplit_paste and case_07_total_420 true
- The three blockers it prints are the fixture backend's by-design ones: determinism_3run and unsupported_count_3run are live-only, and the J3/J4 controls are not measured on fixture. They are not defects.

## 3. Could the post-63e18ed changes move the live numbers?

Changed after `63e18ed` and before `0c24f5f` (`git diff --stat`): `app/backend` (grounding, summary_trim, lexicon_scan, flags, export, present, trace, pipeline, ingest and others), `app/llm/lexicon.yaml`, `app/frontend`, and `evals/run.py` (report text only). No prompt file changed.

- Recall, flags and amounts are code-deterministic over the recorded model output. The fixture replay at HEAD reproduces the live values, so these rows are very unlikely to move. The thin one is entry recall. The 57-entry denominator allows 2 misses: 55/57 = 0.965 passes and 54/57 = 0.947 fails. case_06 E3 is missed in every run and in the fixture, and case_02 E1 flaps.
- Row 4 (unsupported_count_3run, determinism_3run) can move, and the fixture cannot show it. The cause is T-128 plus the T-105 and T-133 lexicon edits:
  - The D-054 summary trim was what stopped item 4 flapping about one run in three on case_02. At HEAD it is strictly narrower (`summary_trim.py` docstring):
    - it trims a suffix only;
    - it never removes the first clause;
    - it requires at least 2 content words in the kept prefix;
    - when a rule says no, the summary is returned unchanged and goes whole to judge 1.
  - A summary that `63e18ed` would have cut can now reach the judge untrimmed. It can come back "partially" or "unsupported", or be reworded by the new code checks.
  - Live, the trim fired in only 1 of the 3 runs (case_02, 1 clause). The result is therefore sensitive to which wording the live model produces on a given day. The fixture run shows 0 trims because it replays an older recording, so it cannot exercise this path.
  - Judge input text changed (trimmed summaries, `added_qualifier` lists, deny/denying as negation words), so the live J1 verdicts are not guaranteed identical.
- The T-134 export gate and T-132 `lexicon_scan` changes act after the model and only block or flag more. They cannot add an ungrounded statement, but they change the lexicon-flag set (`history_significant_for` is a new pre_existing entry). That is a live-precision risk for the pre_existing type that fixture cannot rule out for unseen model wording.
- Process: CONTRACT 8.3 says any change to a lexicon requires re-running `evals.run`. The lexicon hash in the live reports is `a2518d8f...` (the `63e18ed` file). HEAD is `c0178e30...`. `python -m evals.run --check-fresh` on the archive exits 1 (lexicon.yaml changed since the report).

**Answer: yes. A fresh confirming live 3-run at the tag commit is needed before `m2` is tagged.** One run from a clean worktree of the final HEAD is enough, and the three-consecutive requirement is not needed for a confirming run. The earlier runs took about 17 minutes each. If any later gate fix changes `app/` or the lexicon after that run, it has to be repeated at the new tag commit.

## 4. calibration.json

`evals/reports/calibration.json` has only ever been regenerated on the **fixture** backend (`backend: fixture`, `source_commit 6fa8eccdc8`, clean tree, `f3ac48f`; earlier regens `1218b2e`, `4065ef2` were also fixture). Its counts are verified 84/85 and needs_review 9/9, on recorded replies. The live `claude-cli` calibration (83/84 verified; needs_review 9/10, then 10/10, 10/10) exists only inside the three timestamped reports at `63e18ed`. The file is not stale against HEAD prompts or lexicon (hashes match `HEAD:`), and it labels its backend, so it is honest. The product note must not present the 84/85 as live-model calibration.

## 5. Findings

```json
{
  "card": "GATE-M2",
  "persona": "qa",
  "model": "claude-sonnet-5-5",
  "verdict": "changes",
  "summary": "Ship-bar rows 1-4 and the D-046 J3/J4 controls are met in committed, clean-tree live evidence measured at 63e18ed, and the unit suite and fixture eval pass at 0c24f5f. The live evidence does not cover the tag commit: lexicon, trim, lexicon_scan and export-gate code changed after it, so one confirming live 3-run at the tag commit is required before the m2 tag.",
  "findings": [
    {
      "id": "F1",
      "severity": "major",
      "title": "Live ship-bar evidence is at 63e18ed; the tag commit has a different lexicon and a narrower summary trim, and CONTRACT 8.3 requires a live re-run",
      "evidence": "evals/reports/20261102T113305Z.md, 115041Z.md, 120809Z.md all say 'Source commit 63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6'. Lexicon sha256 in 120809Z.md is a2518d8f... ; HEAD app/llm/lexicon.yaml is c0178e30... ; `python -m evals.run --check-fresh` exits 1 on the 0c24f5f archive ('lexicon.yaml changed since the report'). git diff --stat 63e18ed 0c24f5f changes app/backend/summary_trim.py (suffix-only, first clause never removed, unchanged when a rule says no), grounding.py, lexicon_scan.py, export.py, flags.py and lexicon.yaml (T-105 added_qualifier lists, T-133 deny/denying and history_significant_for). Row 4 (unsupported_count_3run, determinism_3run) is live-only and the fixture run reports it as None, so fixture cannot confirm it. The D-054 trim fired in 1 of 3 live runs (20261102T113305Z.md 'items_trimmed: 1', case_02).",
      "recommendation": "Run one live `python -m evals.run` (3 runs, claude-cli) from a clean worktree of the final tag commit, commit the report and its runs/ directory, and require ship_bar_met True with unsupported_count_3run 0, determinism_3run 1.0 and J3/J4 controls unchanged. Re-run again if any later change touches app/ or the lexicon."
    },
    {
      "id": "F2",
      "severity": "minor",
      "title": "calibration.json has only been regenerated on the fixture backend",
      "evidence": "evals/reports/calibration.json: backend 'fixture', source_commit 6fa8eccdc877d1660c55103534fd7ebd370d545c, verified 84/85, needs_review 9/9. Regenerated by 1218b2e, 4065ef2, f3ac48f, all fixture. Live claude-cli counts (83/84 verified; 9/10, 10/10, 10/10 needs_review) appear only in the three timestamped reports at 63e18ed. Hashes match HEAD prompts and lexicon (not stale).",
      "recommendation": "The product note and Part 2 quote the live report counts and say which backend produced them; the app keeps its fixture label. After the F1 live run, decide in a card whether to regenerate the served file from the live run."
    },
    {
      "id": "F3",
      "severity": "minor",
      "title": "latest.json is a stale fixture report, not the ship-bar report",
      "evidence": "evals/reports/latest.json: backend 'fixture', ship_bar_met False, generated_at 2026-11-02T09:56:40Z, source_commit None. REQUIREMENTS R-SU-3 says numbers in the note equal 'the latest eval report'. --check-fresh also flags judge_conflict_v6.md against this file's hashes.",
      "recommendation": "The F1 live run should be the one that rewrites latest.json, and the writer should cite the timestamped live report by path."
    },
    {
      "id": "F4",
      "severity": "minor",
      "title": "Report timestamp and per-run directory timestamp are offset by one run",
      "evidence": "20261102T113305Z.md lists 'per-run artifacts: evals/reports/runs/20261102T111525Z'; 20261102T115041Z.md lists runs/20261102T113305Z; 20261102T120809Z.md lists runs/20261102T115041Z. All three directories exist (14 files each, commit 5dfba88), but runs/20261102T113305Z belongs to report 115041Z, not to report 113305Z.",
      "recommendation": "Cite the per-run path printed inside each report, never the report's own timestamp. Add a one-line mapping to the F1 commit message."
    },
    {
      "id": "F5",
      "severity": "minor",
      "title": "Row 5 (reviewability) and E2E were not re-verified at the tag commit; entry-recall margin is two misses",
      "evidence": "Last whole-sample paralegal score is verify_quickly 4 in reviews/T-060-paralegal-pass5.md at b612176 (verdict changes, 2 majors); frontend changed in 671f054 afterwards. Playwright E2E was not run in this review. entry_recall is 55/57 = 0.965 in run 1; 54/57 = 0.947 would fail the 0.95 bar.",
      "recommendation": "The M2 paralegal panel member re-scores verify_quickly at the tag commit and the orchestrator runs `pytest tests/e2e` there. The product note reports the recall misses (case_06 E3 every run; case_02 E1 in run 1) as found."
    }
  ],
  "exercised": [
    "Read CONTRACT 8.2, REQUIREMENTS section 7 and D-046 and mapped each ship-bar row to the report metrics",
    "Read all three live reports (113305Z, 115041Z, 120809Z) and controls-20261102T123937Z.md; checked source commit, tree-clean line, hashes and per-run artifact lines",
    "Checked evals/reports/runs/{111525Z,113305Z,115041Z} exist and are committed (14 files each, commit 5dfba88); 63e18ed is an ancestor of 0c24f5f",
    "git archive 0c24f5f into scratchpad: pytest tests/unit gave 3450 passed, 8 skipped",
    "git archive 0c24f5f: python -m evals.run --backend fixture (all measurable metrics at the bar; the 3 blockers are fixture-only by design)",
    "git archive 0c24f5f: python -m evals.run --check-fresh (exit 1, lexicon changed since the report)",
    "git diff --stat 63e18ed 0c24f5f over app, evals, prompts, golden; read the diffs of summary_trim.py, flags.py, pipeline.py, ingest.py and lexicon.yaml",
    "Checked calibration.json backend, source commit, counts and hashes against HEAD blobs",
    "Not exercised: Playwright E2E, live LLM backend, paralegal re-score"
  ]
}
```
