# T-142 legal-nurse review (legal-nurse-reviewer, Linda Chen, RN, LNC persona)

Verdict: **changes** (0 blockers, 1 major, 3 minors). Pinned commit 07c7558 (HEAD at review start; contains c5c18a6). I ran `git archive 07c7558` into the scratchpad (`r2-07c7558`) and served it on 127.0.0.1:7931 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. The server (PID 11479) was stopped by PID: `lsof` exit 1, curl 000. Scripts, screenshots and outputs: `artifacts/review-evidence/T-142-legal-nurse/`. This is a read of what the tool tells the reader about coverage, not a clinical opinion on any record.

## What the card asked, and what I saw

GATE-M2 major 1 was "No conflicts found." as an all-clear on lib09 (left shoulder in the ED note, right shoulder everywhere after) and lib08 (loss of consciousness denied, then stated).

- **Empty state: fixed.** lib09, lib08 and lib02 all read "No conflicts found among the kinds checked. Other kinds of conflict are not checked." with the coverage block open (`n1-run.stdout.txt`; `n1-lib08-conflict-group.png`). A bare "No conflicts found." appears nowhere.
- **Text comes from the API, so it cannot drift.** For the sample case, lib09, lib08 and lib02 the checked items and not-checked items on screen are identical to `GET /api/cases/{token}` `checks` (`"UI checked == API labels: True ; UI not_checked == API: True"` four times). The real backend sends `checks` at this commit (`present.py:317`), so the real-backend variant of the test now runs; 23 passed from the archive (`n0-e2e-run.txt`).
- **lib09 (the left/right case):** the not-checked list now says "Left versus right across records (checked only inside one summary)". That discloses the gap I raised.
- **Sample case with two conflicts** (accident date; plan vs discharge): both cards show with both excerpts. The coverage block is collapsed and its heading reads "What the conflict check covers (4 kinds checked)" (`n1-sample-conflict-group.png`). After I dismissed both, the group reads "No open conflicts among the kinds checked (2 dismissed, below). Other kinds are not checked." (`n1-run.stdout.txt` line 32).
- **Fallback with no `checks`:** read from `flags.js:84-86`; covered by the card's route-stub tests. I did not run the UI against a server with `checks` removed.

## Findings

**F-1 (major). On a Spanish case the panel says the denial and plan checks were run; the code that runs them reads English only.** lib09 lists as checked: "A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record" and "A stated plan of care ... against a later record where the course ended early". The Spanish case's panel is word for word the same as the English cases' (`n1-run.stdout.txt`, lib09 block), and the conflict group has no word about language (`n4-lib09-body.py`: "CONFLICT GROUP mentions English/Spanish: False"). The matchers are English regexes: `_DENIAL` ("denies|denied ... prior|previous", "no prior ..."), `_FORM_STEM` ("Prior accidents?") in `app/backend/conflict_candidates.py:44-50`; `grep -i "niega|spanish|language"` on that file and `conflicts.py` finds nothing. I probed `history_denials` in process on the archive (`n3-spanish-denial-probe.py`, output `n3-spanish-denial-probe.out.txt`):

```
EN control: denies prior / prior knee surgery        candidates=1
EN form control: Prior accidents? No [X]             candidates=1
ES denial: Niega lesiones previas en la espalda      candidates=0
ES form: Accidentes anteriores? No [X] vs accidente previo   candidates=0
ES form vs English prior                             candidates=0
```

lib09 record 4 is exactly that form ("Accidentes anteriores? Si [ ] No [X]"). A reader of the Spanish case is told a denial check ran and found none. It never read the Spanish. This is the same kind of unsupported assurance as the original major, narrower in scope: "among the kinds checked" is true only for English wording. Fix: when the case has Spanish records (the `SPANISH_RECORDS` warning already exists), the coverage block must say that the denial and plan checks read English wording only and were not applied to the Spanish records (name them: "Records 2 and 4"), or the backend `checks` must carry a per-case `not_checked` entry for it that the panel prints. Acceptance test: on lib09 the conflict group shows a sentence naming the Spanish records as not covered by the denial and plan-of-care checks; on an English-only case that sentence is absent; unit probe of the Spanish denial lines above either yields a candidate or the sentence is shown.

**F-2 (minor). The loss of consciousness case (lib08) is not named in the server's not-checked list.** The card's text for this fix names "side, LOC, ..." and the frontend fallback lists "A change in loss of consciousness history between records" (`flags.js:86`). The list the server actually sends (`conflict_candidates.py:234-241`) has dosage, left versus right, diagnosis, pain score, months, and history from a relative. On lib08 the panel therefore never names the LOC contradiction I raised (r9 "Denies LOC per patient" against r12 "Patient states brief loss of consciousness at the second collision"). The generic sentence "anything not listed above, including these, is not looked for" does cover it, so the panel is honest, but it does not give the reader the item that was found missing. Fix: add `{"type": "loc_history", "label": "A change in loss of consciousness or other symptom history between records"}` to `NOT_CHECKED`. Acceptance test: lib08's not-checked list contains an LOC line.

**F-3 (minor). With conflicts present, the "others are not checked" statement is behind a collapsed disclosure.** Sample case: the visible line is "What the conflict check covers (4 kinds checked)" and nothing says other kinds are not checked until it is opened (`n1-sample-conflict-group.png`; `flags.js:118,121` passes `open` only when the list is empty). The card's AC says the empty state and the conflict panel both say it. Fix: make the closed summary read "What the conflict check covers (4 kinds checked; others are not checked)". Acceptance test: the summary text contains "not checked" with conflicts present.

**F-4 (minor). The export's internal notes carry no coverage line.** For lib09 and lib08, with all entries accepted, the notes headings are FLAGS ACCEPTED, FLAGS DISMISSED, AMOUNTS NOT TOTALED, RECORDS NOT IN THE TREATMENT SECTION, EDITED ITEMS, PENDING ITEMS NOT INCLUDED, and nothing mentions conflicts or what was checked (`n5-export-notes.out.txt`: "lines mentioning conflict/checked in letter+notes: []"). My GATE-M2 fix asked for the sentence on the empty state, the internal notes and the CLI. The card's AC covers only the screen, so this is outside the AC as written; it is the same silence once she leaves the screen. Fix: one internal-notes line, "Conflict check covered: ...; not checked: ...", from the same `checks`. Acceptance test: lib09 export notes contain that line.

## What I ran

1. `git rev-parse --short HEAD` gave 07c7558; `git archive 07c7558 | tar -x` into `r2-07c7558` in the scratchpad (my first extract landed in the scratchpad root by mistake; no repo file was touched); server on 7931; curl 200.
2. `n1-conflict-coverage.py`: sample case (pasted), lib09, lib08 and lib02 (library entries) in a browser at 1440x900. Read the Conflicts group: heading, empty line, coverage open or closed, checked and not-checked items; compared with `GET /api/cases/{token}` `checks`; on the sample dismissed both conflicts and re-read the group.
3. `n2-types-fired.py`: all 15 library cases through the API: 14 had no conflict flag; only lib11 had two "Records differ on a fact". So in the fixture set no library case shows the provider-name rule firing; I could not confirm that checked kind from a case.
4. `n3-spanish-denial-probe.py`: `conflict_candidates.history_denials` in process on the archive, English controls against Spanish wording.
5. `n4-lib09-body.py`: lib09 page text searched for any language caveat near conflicts.
6. `n5-export-notes.py`: lib09 and lib08, accept every entry, GET export, search letter and notes for conflict or checked wording.
7. `tests/e2e/test_conflict_coverage.py` and `test_edit_to_check.py` from the archive with plain pytest: 23 passed.
8. Read: `reviews/GATE-M2-legal-nurse.md`, `app/frontend/flags.js`, `app/backend/conflict_candidates.py`, card T-142 and its handoff. Screenshots read: `n1-lib08-conflict-group.png`, `n1-sample-conflict-group.png`.

```json
{"card": "T-142", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 07c7558 (HEAD at review start; includes c5c18a6) served on http://127.0.0.1:7931 (PID 11479, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case plus library cases case_lib09_spanish_interpreter_espalda, case_lib08_second_crash_mri_after, case_lib02_slip_fall_prior_knee; all 15 library cases through the API",
 "exercised": [
  "git archive 07c7558 into a fresh scratchpad dir; server on 7931 under .venv/bin/python -I with the T-060 pass-4 launcher; curl 200; stopped by PID 11479 (lsof exit 1, curl 000)",
  "browser at 1440x900: sample (pasted), lib09, lib08, lib02; Conflicts group text, coverage block open or closed, checked and not-checked items compared with GET /api/cases/{token} checks (n1-conflict-coverage.py)",
  "sample case: dismissed both conflict flags and re-read the group text (n1-sample-after-dismiss.png)",
  "all 15 library cases created and run through the API; conflict flags and presence of checks listed (n2-types-fired.py)",
  "in-process probe of conflict_candidates.history_denials with English controls and Spanish denial and form wording (n3-spanish-denial-probe.py)",
  "lib09 page text searched for a language caveat near the conflict group (n4-lib09-body.py)",
  "lib09 and lib08 with every entry accepted: GET export, letter and internal notes searched for conflict or checked wording (n5-export-notes.py)",
  "tests/e2e/test_conflict_coverage.py and test_edit_to_check.py from the archive with plain pytest: 23 passed",
  "read reviews/GATE-M2-legal-nurse.md, app/frontend/flags.js, app/backend/conflict_candidates.py, card T-142; screenshots n1-lib08-conflict-group.png and n1-sample-conflict-group.png. Not exercised: UI with checks removed from GET case (fallback read from code only); live-model behavior (fixture backend only)"
 ],
 "verdict": "changes",
 "scores": {"conflict_coverage_disclosure": 3, "empty_state_honesty": 5, "api_sourced_text": 5, "spanish_honesty": 2, "no_inferred_dx_severity_causation": 5},
 "findings": [
  {"severity": "major", "title": "On a Spanish case the panel lists the denial-vs-history and plan-vs-end checks as run, but they read English wording only",
   "evidence": "n1-run.stdout.txt lib09 block: checked list includes 'A denial of prior problems (including a form answered No) against a prior condition...' and the panel is identical to the English cases; n4-lib09-body.py: 'CONFLICT GROUP mentions English/Spanish: False'; app/backend/conflict_candidates.py:44-50 _DENIAL and _FORM_STEM are English regexes, no Spanish terms in conflict_candidates.py or conflicts.py; n3-spanish-denial-probe.out.txt: English controls candidates=1, 'Niega lesiones previas en la espalda' candidates=0, 'Accidentes anteriores? Si [ ] No [X]' candidates=0; lib09 record 4 is that form",
   "why_it_matters": "The reader of a Spanish case is told a denial check ran and found nothing when it never read the Spanish. It is the same unsupported assurance as the GATE-M2 major, for Spanish wording.",
   "fix": "When the case has Spanish records (SPANISH_RECORDS warning exists), have the coverage block name those records as not covered by the denial and plan-of-care checks, or have the backend checks carry a per-case not_checked entry for it that the panel prints. Do not list them as checked for those records.",
   "acceptance_test": "lib09 conflict group contains a sentence naming the Spanish records as not covered by the denial and plan checks; an English-only case does not show it; or the Spanish denial lines in n3-spanish-denial-probe.py yield a candidate."},
  {"severity": "minor", "title": "The server's not-checked list does not name loss of consciousness (lib08), though the fallback does",
   "evidence": "app/frontend/flags.js:86 FALLBACK_NOT includes 'A change in loss of consciousness history between records'; app/backend/conflict_candidates.py:234-241 NOT_CHECKED has dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history; n1-run.stdout.txt lib08 not_checked list has no LOC line",
   "why_it_matters": "The lib08 contradiction (r9 'Denies LOC per patient' against r12 'Patient states brief loss of consciousness at the second collision') is the case I raised; the panel covers it only through the generic 'anything not listed above' sentence.",
   "fix": "Add a loc_history entry to NOT_CHECKED: 'A change in loss of consciousness or other symptom history between records'.",
   "acceptance_test": "GET case checks.not_checked contains an LOC entry and lib08's panel prints it."},
  {"severity": "minor", "title": "With conflicts present, 'others are not checked' is behind a collapsed disclosure",
   "evidence": "n1-sample-conflict-group.png: closed line 'What the conflict check covers (4 kinds checked)'; app/frontend/flags.js:118,121 open only when the list is empty",
   "why_it_matters": "The card says the empty state and the conflict panel both say others are not checked; with two conflicts shown the reader sees only a count.",
   "fix": "Closed summary: 'What the conflict check covers (4 kinds checked; others are not checked)'.",
   "acceptance_test": "Sample case conflict group summary text contains 'not checked'."},
  {"severity": "minor", "title": "Export internal notes carry no coverage line (outside the AC as written)",
   "evidence": "n5-export-notes.out.txt: lib09 and lib08 'lines mentioning conflict/checked in letter+notes: []'; reviews/GATE-M2-legal-nurse.md fix asked for the empty state, internal notes and CLI",
   "why_it_matters": "Once she leaves the screen, the notes say nothing about what the conflict check covered.",
   "fix": "One internal-notes line from the same checks: 'Conflict check covered: ...; not checked: ...'.",
   "acceptance_test": "lib09 export internal_notes_text contains that line."}
 ],
 "whats_right": [
  "The empty state never says a bare 'No conflicts found.'; it reads 'among the kinds checked. Other kinds of conflict are not checked.' and the coverage list opens by default.",
  "On the sample, lib09, lib08 and lib02 the on-screen checked and not-checked items equal GET case checks word for word, so the text cannot drift.",
  "lib09's not-checked list now says 'Left versus right across records (checked only inside one summary)', which discloses the gap I raised."
 ],
 "questions_for_chris": []}
```
