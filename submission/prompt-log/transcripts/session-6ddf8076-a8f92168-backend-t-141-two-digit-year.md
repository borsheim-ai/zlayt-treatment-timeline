# Subagent: Backend: T-141 two-digit year (Backend: T-141 two-digit year)

Source: `agent-a8f9216818ef46977.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T15:26:18.090Z

You are a backend worker in /Users/arsis/zlayt-pm-project on board card T-141. Claim it with `--force`, then read reviews/T-141-staff-engineer-r7.md (the blocker).

In conflicts.py at lines 67-69, the plural-history date guard must parse two-digit-year dates, such as 3/1/26 or 03-01-26, so that a list naming a date on or after the accident is not exempt. Write the reviewer's blocker case as a test, plus 4-digit and 2-digit variants. Verify from a `git archive HEAD` copy.

Touch only conflicts.py and its tests. Commit with a pathspec, write the handoff, and move the card to in_review. Reply in 1 line.

### User / tool · 2026-11-02T15:26:18.098Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:26:21.471Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-141 --agent backend --force 2>&1 | tail -3; cat reviews/T-141-staff-engineer-r7.md | head -80; sed -n 40,100p app/backend/conflicts.py; git status --short | head"
}
````

### User / tool · 2026-11-02T15:26:21.771Z

**tool result**
````
T-141 claimed by backend
# T-141 staff-engineer scoped check, round 7 (ff1256e, HEAD ba21b4b)

Verdict: **fail** (1 blocker, 1 major).

Scope: only the three items the orchestrator named after r6 (ff1256e), plus lib11 unchanged and the conflict suites. Verified on a `git archive ba21b4b` copy. HEAD ba21b4b differs from ff1256e only in memory/SCOPE_CUTS.md, so the code reviewed is the ff1256e code.

Results by item:
1. Governance per clause: PASS. 19 probe rows (G1-G19) match. 'No prior accidents and was rear-ended 3/1.' is a conflict.
2. Plural and bare hit/impact forms: PASS for every form in the r6 F2 spec and the orchestrator's list (20 rows, P1-P20, plus controls). Residual bare-hit phrasings ('Hit in the head', 'Hit the windshield', 'Hit his head') read info-only. Not counted: they are residual phrasings under scope cut 13f.
3. Plural-history exemption vs date on/after the accident, or this/the/current: FAIL. Q15, Q11, and the this/the/current/last rows hold, but a labelled plural list that names the accident date in a two-digit-year form still prints info. Blocker (finding 1). I did not count it under 13f: 13f records word-rule phrasings that D-061 leaves info, and this is a date the rule names explicitly and the code's own comment says it covers ('a year counts at its year', conflicts.py:61-62).

Also checked: lib11 is byte-identical from 824984f to HEAD (blob 0af8fb2). The conflict unit suites pass (554 across 9 modules). The e2e file that tests the lib11 conflict UI is red at HEAD (finding 2). The red predates ff1256e.

Findings

- **blocker, F1 (item 3):** a labelled plural list that names the accident date with a two-digit year stays info. 'History per patient: car accidents in 2019 and 2022, one on 1/3/26.' (stated accident date 2026-01-03) prints info. Date forms in the same miss class: '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26'. The guard at conflicts.py:67 counts only parsed dates; `dates.find_dates` returns status 'ambiguous' with no iso for numeric forms like '1/3/26', and 'Jan 3, 26' and '3rd Jan 26' are not parsed either. The year fallback at conflicts.py:69 only matches four-digit years. Repro: probe_r7.py row Q19 (artifacts/review-evidence/T-141-r7/probe_r7_head_ba21b4b.txt: 'MISS Q19 item3 expect=conflict got=info'). Pins: `grep -c "/26" tests/unit/test_t141_r6_probes.py` returns 0. Mutant (mutant_plural_guard_off.txt): disabling the parsed-date and referent clauses turns only X12 and X13 red. Q15 and Q11 are carried by the four-digit-year clause alone, so the two-digit form is the untested hole.
  Why it matters: item 3 says the exemption does not apply when the list names a date on or after the accident. The code hides that date conflict, which loses a fact the paralegal needs (D.2 blocker). The gap is in the code, not in D-061's wording, so it is not the major-class gap r6 recorded for Q15.
  Fix: in `_plural_list_ok` (conflicts.py:60-69), read a two-digit year as 20xx and compare it with the stated year. Also treat an 'ambiguous' numeric date whose year is on or after the stated year as on or after it (safe direction, D-055). Keep the parsed-date and four-digit-year clauses.
  Acceptance test: probe_r7.py row Q19 prints conflict. Add pins to tests/unit/test_t141_r6_probes.py for '1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26' and '1/26' on the stated date, each conflict. 'one 2015' and the lib11 record 1 text stay info. A mutant that removes the new two-digit clause turns the new pins red.

- **major, F2 (conflict suite, e2e):** tests/e2e/test_conflict_skipped.py is 8 of 9 red on HEAD. The red is not from ff1256e. The same file passes 9 of 9 at 824984f (the r6-reviewed commit) and is 8 of 9 at 83f1afd (the parent of ff1256e) and at acad4f6. At 6379c0b and c2913a6, tests/e2e/conftest.py has a SyntaxError (line 89), so the module does not collect there. Evidence: pytest_e2e_skip_824984f.txt ('9 passed'), pytest_e2e_skip_83f1afd.txt and pytest_e2e_skip_acad4f6.txt ('8 failed, 1 passed'), pytest_e2e_skip_6379c0b.txt and pytest_e2e_skip_c2913a6.txt (collection error), pytest_lib11_modules_head.txt lines 30 and 45 (test_conflict_skipped.py:69 and :83). The UI difference I could establish: at HEAD the case opens on the Case overview step and `[data-testid="flags-panel"]` is not in the DOM after the timeline loads (repro_lib11_ui_head.txt: 'no flags-panel on open'). At 824984f the panel is present on open with 2 conflict cards and 1 note (repro_lib11_ui_824984f.txt). The backend data is correct at HEAD (repro_lib11_api_head.txt: denial_vs_history checked, skipped [], 1 RECORDS_PREDATE_ACCIDENT note, 2 pending conflict flags). I did not find the route from the overview to the flags panel at HEAD; clicking btn-start-review did not reveal it in my script.
  Why it matters: the brief asks me to confirm the conflict suites pass. This module is a conflict suite and it is red at HEAD. Whether the landing step change is intended (frontend commits in 824984f..acad4f6, e.g. 6379c0b, 0b2ce9c) or the test is stale is an orchestrator decision, so I rate it major, not blocker.
  Fix: decide the intended landing. Either restore the flags group on open for a case with conflicts, or update the test to the documented route to the flags group and say so in the test. Also add a collection check so a conftest SyntaxError cannot hide a red suite.
  Acceptance test: `tests/e2e/test_conflict_skipped.py` 9 of 9 on a git archive of the fix commit. repro_lib11_ui.py shows the conflict group with the lib11 note and the two denial cards on the documented route.

Residuals not counted (scope cut 13f)
- Bare hit forms outside the r6 F2 spec read info: 'Hit in the head in October 2025.', 'Hit the windshield in October 2025.', 'Hit his head in 2025.' (probe output in probe_r7_head_ba21b4b.txt is the item-2 set; these three were run inline with the same function).
- 13f names 'Denies any accident on 01/03/2026' (info) and 'No prior accidents or collisions' (conflict). The second has the same shape as G7 and conflicts. I did not re-run the first.

Minor (I would have done it differently; does not violate the rule as written)
- Q27 'History per patient: car accidents in 2019 and 2022, treated at the clinic.' is a conflict because the literal word 'the' is in `_PLURAL_REFERENT` (conflicts.py:30). The rule text says 'this/the/current', so this matches it. Narrowing to 'the latest' or 'the most recent' would avoid false conflicts on benign lists. Safe direction.

Exercised
1. Read personas/staff-engineer.md in full; reviews/T-141-staff-engineer-r6.md; `python3 tools/board.py show T-141` (notes through the 15:11:07 dispatch); memory/ORCHESTRATOR_DECISIONS.md D-061 (line 69); memory/SCOPE_CUTS.md 13f (line 91); my T-141 r5, r6 and evidence-sha memory notes.
2. `git log --oneline -3` shows ba21b4b, ff1256e, 83f1afd. `git diff --stat ff1256e HEAD` shows memory/SCOPE_CUTS.md only.
3. `git archive ba21b4b | tar -x` into the scratchpad copy T141r7_head. sha256 of app/backend/conflicts.py (32433731...) equals `git show ba21b4b:app/backend/conflicts.py`.
4. Conflict unit suites on the archive, `.venv/bin/python -I -m pytest -q -p no:cacheprovider` over 9 modules (test_conflicts, test_conflict_candidates, test_t093_j3_controls_reachable, test_t141_checks_per_case, test_t141_r3_variants, test_t116_r4_all_dated_records, test_api_routes, test_t141_d061_closed_exemption, test_t141_r6_probes): 554 passed. Log: pytest_conflict_suites_head.txt.
5. lib11-referencing modules on the archive (the 9 above minus the ones not referencing lib11, plus test_amounts_t140, test_t139_unmarked and tests/e2e/test_conflict_skipped.py): 8 failed, 590 passed. All 8 failures are in test_conflict_skipped.py. Log: pytest_lib11_modules_head.txt.
6. e2e skip file on archives 824984f, 83f1afd, acad4f6, 6379c0b, c2913a6 (logs pytest_e2e_skip_<sha>.txt).
7. lib11: `git ls-tree` blob for evals/library/case_lib11_priors_and_ledger.txt is 0af8fb2 at 824984f, ff1256e and ba21b4b. `git diff --stat 824984f ba21b4b -- evals/library/case_lib11_priors_and_ledger.*` is empty.
8. Probe set for the three items, probe_r7.py run on the archive: 54 rows, 53 match, 1 miss (Q19). Log: probe_r7_head_ba21b4b.txt. Inline `dates.find_dates` and `_describes_event` checks on 14 date spellings (output in the exercised notes above).
9. Private fixture server from the archive, lib11 run through the HTTP API (repro_lib11_api.py): repro_lib11_api_head.txt.
10. Headless Chromium on the archive servers (repro_lib11_ui.py): repro_lib11_ui_head.txt (no flags-panel on open) and repro_lib11_ui_824984f.txt (conflict group, 2 cards, 1 note).
11. Mutant in a fresh scratch copy (mutant_guard.py, no product file touched): parsed-date and referent clauses of `_plural_list_ok` disabled. tests/unit/test_t141_r6_probes.py and test_t141_d061_closed_exemption.py: 2 failed (X12, X13), 202 passed. Log: mutant_plural_guard_off.txt.
12. `grep -c "/26" tests/unit/test_t141_r6_probes.py`: 0.
13. `python3 tools/board.py validate`: ok (163 files), before this file was written.
Not run: full unit suite (the handoff reports other cards' dirty files), pipeline CLI on sample.txt, eval runner, live judge controls, E2E beyond the skip file. No server on :7860.

```json
{"card": "T-141", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git ba21b4b (HEAD; code identical to ff1256e, only memory/SCOPE_CUTS.md differs). app/backend/conflicts.py, tests/unit/test_t141_r6_probes.py, tests/unit/test_t141_d061_closed_exemption.py, tests/e2e/test_conflict_skipped.py. Evidence: artifacts/review-evidence/T-141-r7/. App: private fixture servers started from git archives on loopback (lib11 library case); nothing on :7860.",
 "exercised": [
  "Read personas/staff-engineer.md; reviews/T-141-staff-engineer-r6.md; board.py show T-141; memory/ORCHESTRATOR_DECISIONS.md D-061; memory/SCOPE_CUTS.md 13f.",
  "git log -3 (ba21b4b, ff1256e, 83f1afd); git diff --stat ff1256e HEAD (memory/SCOPE_CUTS.md only); git archive ba21b4b into scratchpad T141r7_head; sha256 of conflicts.py matches git show.",
  "Conflict unit suites on the archive, 9 modules incl. test_t141_r6_probes: 554 passed (pytest_conflict_suites_head.txt).",
  "lib11-referencing modules on the archive, 9 modules incl. tests/e2e/test_conflict_skipped.py: 8 failed, 590 passed; all 8 failures in test_conflict_skipped.py (pytest_lib11_modules_head.txt).",
  "tests/e2e/test_conflict_skipped.py on archives 824984f (9 passed), 83f1afd (8 failed), acad4f6 (8 failed), 6379c0b and c2913a6 (conftest SyntaxError at line 89); logs pytest_e2e_skip_<sha>.txt.",
  "lib11 blob 0af8fb2 at 824984f, ff1256e, ba21b4b (git ls-tree); git diff --stat 824984f ba21b4b on lib11 files is empty.",
  "probe_r7.py on the archive: 54 rows (G1-G19 governance, P1-P20 plural and bare forms, Q11-Q28 labelled-list date and referent guard): 53 match, 1 miss Q19 (probe_r7_head_ba21b4b.txt).",
  "dates.find_dates and _describes_event on 14 date spellings (1/3/26, 01/03/26, 3/27/26, 1-3-26, 01.03.26, Jan 3, 26, 3rd Jan 26, 1/26, 1/3/2026, 01/03/2026, Jan 3 2026, 2026-01-03, in Jan 2026, 01/2026).",
  "repro_lib11_api.py on the HEAD archive: status ready, conflict_types include denial_vs_history, skipped [], 1 RECORDS_PREDATE_ACCIDENT note, 2 pending conflict flags (repro_lib11_api_head.txt).",
  "repro_lib11_ui.py (headless Chromium) on HEAD: no flags-panel on open, case opens on Case overview (repro_lib11_ui_head.txt); on 824984f: conflict group with 2 cards and 1 note (repro_lib11_ui_824984f.txt).",
  "mutant_guard.py on a fresh scratch copy: parsed-date and referent clauses of _plural_list_ok disabled; r6 probes and d061 suite: 2 failed (X12, X13), 202 passed (mutant_plural_guard_off.txt).",
  "grep -c '/26' tests/unit/test_t141_r6_probes.py: 0 two-digit-year rows.",
  "python3 tools/board.py validate: ok (163 files).",
  "Not run: full unit suite, pipeline CLI on sample.txt, eval runner, live judge controls, E2E beyond the skip file."
 ],
 "verdict": "fail",
 "scores": {"item1_per_clause_governance": 5, "item2_plural_and_bare_forms": 4, "item3_plural_list_date_guard": 2, "lib11_unchanged": 5, "conflict_unit_suites": 5, "conflict_e2e_suite": 2, "tests_assert_behaviour": 3, "llm_code_boundary": 5},
 "findings": [
  {"severity": "blocker",
   "title": "F1 (item 3): a labelled plural list that names the accident date with a two-digit year stays info",
   "evidence": "probe_r7.py row Q19 in artifacts/review-evidence/T-141-r7/probe_r7_head_ba21b4b.txt: 'MISS Q19 item3 expect=conflict got=info | History per patient: car accidents in 2019 and 2022, one on 1/3/26.' Date guard counts parsed dates only (conflicts.py:67); find_dates returns status 'ambiguous' with no iso for '1/3/26'; 'Jan 3, 26' and '3rd Jan 26' are not parsed. Year fallback matches four-digit years only (conflicts.py:69). grep -c '/26' tests/unit/test_t141_r6_probes.py = 0. mutant_plural_guard_off.txt: disabling the parsed-date and referent clauses turns only X12, X13 red.",
   "why_it_matters": "Item 3 says the plural-history exemption does not apply when the list names a date on or after the accident. The code hides that date conflict for two-digit-year and month-name short forms, so a fact the paralegal needs is lost (D.2 blocker). The gap is in the code, not in D-061's wording, so it is not the major-class wording gap r6 recorded for Q15. Scope cut 13f does not cover it: 13f records word-rule phrasings that D-061 leaves info, and this date is inside the rule the orchestrator named.",
   "fix": "In _plural_list_ok (conflicts.py:60-69), read a two-digit year as 20xx and compare it with the stated year. Treat an ambiguous numeric date whose year is on or after the stated year as on or after it (safe direction, D-055). Keep the parsed-date and four-digit-year clauses.",
   "acceptance_test": "probe_r7.py row Q19 prints conflict. New pins in tests/unit/test_t141_r6_probes.py: '1/3/26', '01/03/26', '1-3-26', '01.03.26', 'Jan 3, 26', '3rd Jan 26', '1/26' on the stated date each conflict; 'one 2015' and the lib11 record 1 text stay info. A mutant removing the new two-digit clause turns the new pins red."},
  {"severity": "major",
   "title": "F2 (conflict suite): tests/e2e/test_conflict_skipped.py is 8 of 9 red on HEAD; the red predates ff1256e",
   "evidence": "pytest_lib11_modules_head.txt:30 (test_conflict_skipped.py:69, conflict-note count 0) and :45 (:83, data-item-id count 0). pytest_e2e_skip_824984f.txt '9 passed'; pytest_e2e_skip_83f1afd.txt and pytest_e2e_skip_acad4f6.txt '8 failed, 1 passed'; pytest_e2e_skip_6379c0b.txt and pytest_e2e_skip_c2913a6.txt: SyntaxError in tests/e2e/conftest.py (line 89). repro_lib11_ui_head.txt: 'no flags-panel on open' (case opens on Case overview). repro_lib11_ui_824984f.txt: conflict group count 1, 2 cards, 1 note. repro_lib11_api_head.txt: backend data correct (denial_vs_history checked, skipped [], 1 note, 2 pending conflict flags).",
   "why_it_matters": "The brief asks for confirmation that the conflict suites pass. This module is a conflict suite and it is red at HEAD, and the lib11 conflict is not visible on open in the browser. The red is not from the ff1256e logic (the API output is correct and the file is red at 83f1afd, the parent). Whether the landing change is intended (frontend commits between 824984f and acad4f6, e.g. 6379c0b and 0b2ce9c) or the test is stale is an orchestrator decision, so it is major, not blocker. I did not establish the route from the overview to the flags group at HEAD.",
    ends it as a reference to the accident itself. T-141 r6 (F1): a governor carries across 'and', 'or', 'with', 'for', 'of' only to an injury word; a
    second accident or mechanism word after one is a new event, ungoverned."""
    toks = clause[:m.start()].split()
    crossed = False
    for i in range(len(toks) - 1, -1, -1):
        raw = toks[i]
        w = raw.strip(".:()\"'?[]").lower()
        if raw.endswith(":") or not w:                                                    # a label ("History:", "Allergies:") closes the scope
            return bool(raw.endswith(":") and _HISTORY_LABEL.fullmatch(" ".join(toks[:i + 1]).lower()) and _PLURAL_EVENT.fullmatch(m.group(0)) and plural_ok)
        if w in _NEGATOR or w in _HIST_WORD or (w in _HIST_VERBS and i and any(t.strip(".:()\"'?[]").lower() == "previously" for t in toks[max(0, i - 2):i])):
            return not crossed or bool(_INJURY.fullmatch(m.group(0)))
        if w in _LINKS:
            crossed = True
            continue
        if w in _FILLER or _EVENT.fullmatch(w):
            continue
        return False
    return False


def _plural_list_ok(unit: str, iso) -> bool:
    """T-141 r6 (F3): the plural-under-a-history-label exemption holds only when the whole sentence names no date on or after the stated accident date (a year
    counts at its year) and no referent word ('this one', 'the latest', 'current'): 'History per patient: accidents, this one on 01/03/2026' is the accident."""
    if any(w.strip(".,;:()\"'").lower() in _PLURAL_REFERENT for w in unit.split()):
        return False
    if not iso:
        return True
    if any(d["status"] == "parsed" and d["iso"] >= iso for d in dates.find_dates(unit)):
        return False
    return not any(int(y) >= int(iso[:4]) for y in re.findall(r"\b((?:19|20)\d\d)\b", unit))


def _describes_event(rec: dict, iso=None) -> bool:
    """D-061: the record has ANY injury, mechanism or accident word not governed by an explicit prior/previous/earlier or a negation (judged per clause and per word)."""
    from app.backend import sentences
    text = rec.get("excerpt") or ""
    for a, b in sentences.stripped_spans(text):
        unit = text[a:b]
        plural_ok = _plural_list_ok(unit, iso)
        for d in dates.find_dates(unit):                                     # "January 9, 2026" is one date, not two clauses
            unit = unit[:d["start"]] + d["text"].replace(",", "\x01") + unit[d["end"]:]
        for clause in (c.replace("\x01", ",") for c in _CLAUSE_SPLIT.split(unit)):
            for m in _EVENT.finditer(clause):
                if not _governed(clause, m, plural_ok):
                    return True
    return False


def _event_records(s: dict, records: list) -> list:
    """Records dated before the stated date that describe the collision itself."""
    return [o for o in records if o.get("date_iso") and o["date_iso"] < s["iso"] and _describes_event(o, s["iso"])]


def _encounters(records):
    """D-055: every dated record counts for the earliest date. Whether the earliest one is paperwork is shown beside it (see accident_date_conflicts)."""
    return [r for r in records if r.get("date_iso")]


def stated_accident_dates(records: list) -> list:
    """[{record_no, iso, quote, start, end}]: a lexicon phrase followed within 40 characters by a parsed date, per record excerpt."""
    out = []
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:26:24.792Z

**tool call — Bash**
````
{
 "command": "git log --oneline -3 && git status --short app/backend/conflicts.py tests/unit | head; python3 - <<'E'\nfrom app.backend import dates\nfor t in [\"one on 1/3/26.\",\"01/03/26\",\"1-3-26\",\"01.03.26\",\"Jan 3, 26\",\"3rd Jan 26\",\"1/26\",\"3/1/26\",\"03-01-26\",\"1/3/2026\",\"3/1/2026\"]:\n    print(t, [(d['status'],d.get('iso'),d['text']) for d in dates.find_dates(t)])\nE\nsed -n 1,40p tests/unit/test_t141_r6_probes.py; grep -n \"_plural_list_ok\\|def test.*Q15\\|Q15\" tests/unit/test_t141_r6_probes.py | head"
}
````

### User / tool · 2026-11-02T15:26:24.977Z

**tool result**
````
2de5ba9 fix(frontend): T-154 r3 the a-key guard moves from mountSection() (ReferenceError on every case load) into the keydown handler; the duplicate sentence is the backend's own; e2e test_no_console_errors
c3a2af8 docs(orchestrator): D-062 amended - notes yield charges only without a same-provider itemized bill
2ac96cf fix(backend): T-140 D-062 total line 'Billed charges accepted from these records', charge sources by billing header, per-figure rule, CPT/HCPCS normalization
 M tests/unit/test_t139_charge_text.py
 M tests/unit/test_t139_r3.py
 M tests/unit/test_t139_unmarked.py
 M tests/unit/test_t146_r3_decided_items_never_lowered.py
 M tests/unit/test_t159_flag_audit.py
 M tests/unit/test_t161_first_run_stage_down.py
?? tests/unit/test_t139_r4.py
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/arsis/zlayt-pm-project/app/backend/dates.py", line 8, in <module>
    from app.backend import spanish_text
  File "/Users/arsis/zlayt-pm-project/app/backend/spanish_text.py", line 14, in <module>
    from app.backend import grounding, language
  File "/Users/arsis/zlayt-pm-project/app/backend/grounding.py", line 10, in <module>
    import yaml
ModuleNotFoundError: No module named 'yaml'
"""T-141 r6 fix-up (D-061): every probe of reviews/T-141-staff-engineer-r6.md (probe.py, probe2.py) as a test, plus connector, plural, bare-form and
date/pronoun variants. Case: stated accident date 2026-01-09, record 1 (2026-01-05) carries the text. Expectation 'conflict' = accident_date_conflicts raises;
'info' = no conflict and a RECORDS_PREDATE_ACCIDENT note. N1 ('Denies any accident on 01/03/2026.') is info by D-061's negation clause; the reviewer listed it as a
question, not a finding."""
import pytest

from app.backend import conflicts as C


def R(n, d, src, ex):
    return dict(n=n, date_iso=d, source=src, excerpt=ex, kind="encounter")


def recs(ex, src="ER"):
    return [R(1, "2026-01-05", src, ex), R(2, "2026-01-12", "PT", "Exam: ok."), R(3, "2026-01-20", "Intake", "Date of accident per intake form: 2026-01-09.")]


def classify(ex, src="ER"):
    r = recs(ex, src)
    if C.accident_date_conflicts(r):
        return "conflict"
    return "info" if C.accident_date_note(r) else "none"


CASES = [
    ("R1", "conflict", "Rear-end collision in October 2025.", "ER"),
    ("R2", "conflict", "MVC in October 2025.", "ER"),
    ("R3", "conflict", "MVA in October 2025.", "ER"),
    ("R4", "conflict", "Collision in October 2025.", "ER"),
    ("R5", "conflict", "Crash in October 2025.", "ER"),
    ("R6", "conflict", "Involved in an MVA in October 2025.", "ER"),
    ("R7", "conflict", "Airbag deployed in October 2025.", "ER"),
    ("R8", "conflict", "Rear-ended last year.", "ER"),
    ("R9", "conflict", "Rear end collision in October 2025.", "ER"),
    ("R10", "conflict", "Rear-end crash in October 2025.", "ER"),
    ("R11", "conflict", "Rear-ended 03/14/2024, resolved.", "ER"),
    ("R12", "conflict", "Rear-end collision 03/14/2024, resolved.", "ER"),
    ("R13", "conflict", "MVA on 03/04/2024, resolved.", "ER"),
    ("R14", "conflict", "MVA in 2015, resolved.", "ER"),
    ("R15", "conflict", "Car accident last year, fully recovered.", "ER"),
136:    ("Q15", "conflict", "History per patient: accidents, this one on 01/03/2026.", "PCP"),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:26:28.919Z

**tool call — Bash**
````
{
 "command": "ls -d .venv; .venv/bin/python - <<'E'\nfrom app.backend import dates\nfor t in [\"one on 1/3/26.\",\"01/03/26\",\"1-3-26\",\"01.03.26\",\"Jan 3, 26\",\"3rd Jan 26\",\"1/26\",\"3/1/26\",\"03-01-26\",\"1/3/2026\",\"3/1/2026\",\"in 2015\",\"at 10/26 visit\",\"BP 120/80\"]:\n    print(t, [(d['status'],d.get('iso'),d['text']) for d in dates.find_dates(t)])\nE\nsed -n 125,175p tests/unit/test_t141_r6_probes.py; ls reviews/ artifacts/review-evidence/T-141-r7 2>/dev/null | grep -i \"T-141-r7\\|probe_r7\" | head"
}
````

### User / tool · 2026-11-02T15:26:29.075Z

**tool result**
````
.venv
one on 1/3/26. [('ambiguous', None, '1/3/26')]
01/03/26 [('ambiguous', None, '01/03/26')]
1-3-26 [('ambiguous', None, '1-3-26')]
01.03.26 []
Jan 3, 26 []
3rd Jan 26 []
1/26 []
3/1/26 [('ambiguous', None, '3/1/26')]
03-01-26 [('ambiguous', None, '03-01-26')]
1/3/2026 [('ambiguous', None, '1/3/2026')]
3/1/2026 [('ambiguous', None, '3/1/2026')]
in 2015 []
at 10/26 visit []
BP 120/80 []
    ("Q4", "conflict", "History per patient: car accidents in 2019 and 2022 and crashes last week.", "PCP"),
    ("Q5", "conflict", "History per patient: car accidents in 2019 and 2022, MVCs this month.", "PCP"),
    ("Q6", "conflict", "History per patient: car accidents in 2019 and 2022. Rear-end collisions this month.", "PCP"),
    ("Q7", "conflict", "History per patient: car accidents in 2019 and 2022 and collisions this month.", "PCP"),
    ("Q8", "conflict", "History per patient: car accidents in 2019 and 2022; struck this week.", "PCP"),
    ("Q9", "conflict", "History per patient: car accidents in 2019 and 2022 with a collision this week.", "PCP"),
    ("Q10", "conflict", "History per patient: car accidents in 2019 and 2022 with collisions this week.", "PCP"),
    ("Q11", "conflict", "History per patient: car accidents in 2019 and 2022, the latest one on 01/03/2026.", "PCP"),
    ("Q12", "conflict", "History per patient: car accidents in 2019 and 2022 or an MVA this week.", "PCP"),
    ("Q13", "conflict", "History per patient: car accidents in 2019 and 2022 with neck pain after the accidents.", "PCP"),
    ("Q14", "conflict", "History per patient: car accidents in 2019 and 2022; accidents in 2026 with neck pain.", "PCP"),
    ("Q15", "conflict", "History per patient: accidents, this one on 01/03/2026.", "PCP"),
    ("Q16", "conflict", "Denies prior accidents; rear-ended in October 2025.", "ER"),
    ("N1", "info", "Denies any accident on 01/03/2026.", "ER"),
    ("N2", "info", "Denies whiplash or headache.", "ER"),
    ("N3", "conflict", "No LOC after the accident.", "ER"),
    ("N4", "conflict", "Denies whiplash; restrained driver, rear-ended.", "ER"),
    ("N5", "conflict", "No injury reported after the accident on 01/03/2026.", "ER"),
]

EXTRA = [   # T-141 r6 fix-up: connector, plural, bare-form and date/pronoun shapes beyond the reviewer's probes
    ("X1", "conflict", "No prior accidents and was rear-ended 3/1.", "ER"),
    ("X2", "conflict", "No prior accidents and hit from behind on 01/03/2026.", "ER"),
    ("X3", "conflict", "Denies prior accidents or hits from behind.", "ER"),
    ("X4", "conflict", "Previous crashes and impacts noted last year.", "ER"),
    ("X5", "conflict", "Hits to the left side last year.", "ER"),
    ("X6", "conflict", "Impacts noted in October 2025.", "ER"),
    ("X7", "conflict", "Hit and run in October 2025.", "ER"),
    ("X8", "conflict", "Prior wrecks and wrecks last week.", "ER"),
    ("X9", "conflict", "History per patient: car accidents in 2019 and 2022, now in 2026.", "PCP"),
    ("X10", "conflict", "History per patient: car accidents in 2019, 2022 and 2026.", "PCP"),
    ("X11", "conflict", "History per patient: car accidents in 2019 and 2022 and on 01/20/2026.", "PCP"),
    ("X12", "conflict", "History per patient: car accidents in 2019 and 2022, current one pending.", "PCP"),
    ("X13", "conflict", "History per patient: car accidents in 2019 and 2022, the most recent last week.", "PCP"),
    ("Y1", "info", "Patient hit her weight goal of 150 lb.", "PCP"),
    ("Y2", "info", "Impact of diabetes on diet counselled.", "PCP"),
    ("Y3", "info", "Previous accident with whiplash.", "ER"),
    ("Y4", "info", "No prior accidents or injuries.", "ER"),
    ("Y5", "info", "Negative for whiplash.", "ER"),
    ("Y6", "info", "No history of prior injury.", "ER"),
    ("Y7", "info", "History per patient: car accidents in 2019 and 2022 with neck pain.", "PCP"),
    ("Y8", "info", "History per patient: MVAs in 2019 and 2022.", "PCP"),
]


@pytest.mark.parametrize("cid,exp,ex,src", CASES + EXTRA, ids=[c[0] for c in CASES + EXTRA])
def test_probe(cid, exp, ex, src):
    assert classify(ex, src) == exp, ex
artifacts/review-evidence/T-141-r7:
probe_r7.py
probe_r7_head_ba21b4b.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:26:47.502Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/conflicts.py'\ns=open(p).read()\nold='''    return not any(int(y) >= int(iso[:4]) for y in re.findall(r\"\\\\b((?:19|20)\\\\d\\\\d)\\\\b\", unit))\n'''\nnew='''    if any(int(y) >= int(iso[:4]) for y in re.findall(r\"\\\\b((?:19|20)\\\\d\\\\d)\\\\b\", unit)):\n        return False\n    return not any(2000 + int(y) >= int(iso[:4]) for y in _TWO_DIGIT_YEARS.findall(unit) for y in [next(g for g in y if g)])  # T-141 r7 (F1): '1/3/26' reads as 2026\n'''\nassert old in s\ns=s.replace(old,new)\nanchor='def _plural_list_ok('\nhelper='''_MONTH = r\"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\\\\.?\"\n_TWO_DIGIT_YEARS = re.compile(                                                        # a two-digit year in a date shape; the year is the one group that matched\n    r\"(?<![\\\\d/.\\\\-])(?:0?[1-9]|[12]\\\\d|3[01])[/.\\\\-](?:0?[1-9]|[12]\\\\d|3[01])[/.\\\\-](\\\\d{2})(?![\\\\d/.\\\\-]*\\\\d)\"        # 1/3/26, 01/03/26, 1-3-26, 01.03.26\n    r\"|(?<![\\\\d/.\\\\-])(?:0?[1-9]|1[0-2])/(\\\\d{2})(?![\\\\d/.\\\\-]*\\\\d)\"                                            # 1/26 (month/year)\n    r\"|\\\\b\" + _MONTH + r\"\\\\s+\\\\d{1,2}(?:st|nd|rd|th)?,?\\\\s+(\\\\d{2})(?!\\\\d)\"                                # Jan 3, 26\n    r\"|\\\\b\\\\d{1,2}(?:st|nd|rd|th)?\\\\s+\" + _MONTH + r\",?\\\\s+(\\\\d{2})(?!\\\\d)\",                                # 3rd Jan 26\n    re.I)\n\n\n'''\ns=s.replace(anchor,helper+anchor,1)\nopen(p,'w').write(s)\nE\nsed -n 60,85p app/backend/conflicts.py"
}
````

### User / tool · 2026-11-02T15:26:47.613Z

**tool result**
````
_MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?"
_TWO_DIGIT_YEARS = re.compile(                                                        # a two-digit year in a date shape; the year is the one group that matched
    r"(?<![\d/.\-])(?:0?[1-9]|[12]\d|3[01])[/.\-](?:0?[1-9]|[12]\d|3[01])[/.\-](\d{2})(?![\d/.\-]*\d)"        # 1/3/26, 01/03/26, 1-3-26, 01.03.26
    r"|(?<![\d/.\-])(?:0?[1-9]|1[0-2])/(\d{2})(?![\d/.\-]*\d)"                                            # 1/26 (month/year)
    r"|\b" + _MONTH + r"\s+\d{1,2}(?:st|nd|rd|th)?,?\s+(\d{2})(?!\d)"                                # Jan 3, 26
    r"|\b\d{1,2}(?:st|nd|rd|th)?\s+" + _MONTH + r",?\s+(\d{2})(?!\d)",                                # 3rd Jan 26
    re.I)


def _plural_list_ok(unit: str, iso) -> bool:
    """T-141 r6 (F3): the plural-under-a-history-label exemption holds only when the whole sentence names no date on or after the stated accident date (a year
    counts at its year) and no referent word ('this one', 'the latest', 'current'): 'History per patient: accidents, this one on 01/03/2026' is the accident."""
    if any(w.strip(".,;:()\"'").lower() in _PLURAL_REFERENT for w in unit.split()):
        return False
    if not iso:
        return True
    if any(d["status"] == "parsed" and d["iso"] >= iso for d in dates.find_dates(unit)):
        return False
    if any(int(y) >= int(iso[:4]) for y in re.findall(r"\b((?:19|20)\d\d)\b", unit)):
        return False
    return not any(2000 + int(y) >= int(iso[:4]) for y in _TWO_DIGIT_YEARS.findall(unit) for y in [next(g for g in y if g)])  # T-141 r7 (F1): '1/3/26' reads as 2026


def _describes_event(rec: dict, iso=None) -> bool:
    """D-061: the record has ANY injury, mechanism or accident word not governed by an explicit prior/previous/earlier or a negation (judged per clause and per word)."""
    from app.backend import sentences
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:27:01.304Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/conflicts.py'\ns=open(p).read()\ns=s.replace(\"(?![\\\\d/.\\\\-]*\\\\d)\",\"(?!\\\\d)\")\ns=s.replace(\"    return not any(2000 + int(y) >= int(iso[:4]) for y in _TWO_DIGIT_YEARS.findall(unit) for y in [next(g for g in y if g)])  # T-141 r7 (F1): '1/3/26' reads as 2026\\n\",\n\"    return not any(2000 + int(next(g for g in m if g)) >= int(iso[:4]) for m in _TWO_DIGIT_YEARS.findall(unit))     # T-141 r7 (F1): '1/3/26' reads as 2026\\n\")\nopen(p,'w').write(s)\nE\ncat > tests/unit/test_t141_r7_two_digit_year.py <<'E'\n\"\"\"T-141 r7 (F1, staff-engineer blocker): a labelled plural history list that names a date on or after the stated accident date in a two-digit-year form\n('1/3/26', '1-3-26', 'Jan 3, 26', '1/26') is the accident, not history: conflict. Years before the stated year, and four-digit variants, behave as before.\nCase: stated accident date 2026-01-03 (so '1/3/26' is the accident date itself).\"\"\"\nimport pytest\n\nfrom app.backend import conflicts as C\n\nLABEL = \"History per patient: car accidents in 2019 and 2022, \"\n\n\ndef classify(ex):\n    r = [dict(n=1, date_iso=\"2026-01-02\", source=\"PCP\", excerpt=ex, kind=\"encounter\"),\n         dict(n=2, date_iso=\"2026-01-12\", source=\"PT\", excerpt=\"Exam: ok.\", kind=\"encounter\"),\n         dict(n=3, date_iso=\"2026-01-20\", source=\"Intake\", excerpt=\"Date of accident per intake form: 2026-01-03.\", kind=\"encounter\")]\n    if C.accident_date_conflicts(r):\n        return \"conflict\"\n    return \"info\" if C.accident_date_note(r) else \"none\"\n\n\nON_OR_AFTER = [   # the reviewer's Q19 and its date-form class, plus 4-digit variants\n    \"one on 1/3/26.\", \"one on 01/03/26.\", \"one on 1-3-26.\", \"one on 03-01-26.\", \"one on 3/1/26.\", \"one on 01.03.26.\", \"one on Jan 3, 26.\", \"one on 3rd Jan 26.\",\n    \"one on 1/26.\", \"one on 3/27/26.\", \"one on 1/3/2026.\", \"one on 01/03/2026.\", \"one on 03-01-2026.\", \"one on Jan 3, 2026.\", \"one in 2026.\",\n]\nBEFORE = [\"one in 2015.\", \"one on 1/3/15.\", \"one on 01-03-15.\", \"one on 1/3/25.\", \"one on Jan 3, 25.\", \"one on 3rd Jan 25.\", \"one on 12/25.\", \"one on 1/3/2015.\"]\n\n\n@pytest.mark.parametrize(\"tail\", ON_OR_AFTER)\ndef test_two_and_four_digit_dates_on_or_after_the_accident_are_a_conflict(tail):\n    assert classify(LABEL + tail) == \"conflict\", tail\n\n\n@pytest.mark.parametrize(\"tail\", BEFORE)\ndef test_dates_before_the_accident_year_stay_history(tail):\n    assert classify(LABEL + tail) == \"info\", tail\n\n\ndef test_reviewer_blocker_case_q19():\n    assert classify(\"History per patient: car accidents in 2019 and 2022, one on 1/3/26.\") == \"conflict\"\n\n\ndef test_blood_pressure_is_not_a_date():\n    assert classify(\"History per patient: car accidents in 2019 and 2022, BP 120/80.\") == \"info\"\nE\n.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t141_r7_two_digit_year.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T15:27:01.866Z

**tool result**
````
.........................                                                [100%]
25 passed in 0.15s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:27:10.971Z

**tool call — Bash**
````
{
 "command": "git add app/backend/conflicts.py tests/unit/test_t141_r7_two_digit_year.py && git commit -q -m \"fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- app/backend/conflicts.py tests/unit/test_t141_r7_two_digit_year.py && SHA=$(git rev-parse --short HEAD) && echo $SHA\nD=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a141\nrm -rf $D; mkdir -p $D; git archive HEAD | tar -x -C $D; ln -s /Users/arsis/zlayt-pm-project/.venv $D/.venv 2>/dev/null\ncd $D && .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t141_r7_two_digit_year.py tests/unit/test_conflicts.py tests/unit/test_conflict_candidates.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t141_r3_variants.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py tests/unit/test_t141_d061_closed_exemption.py tests/unit/test_t141_r6_probes.py 2>&1 | tail -4\n# mutant: revert fix\ngit -C /Users/arsis/zlayt-pm-project show HEAD~1:app/backend/conflicts.py > $D/app/backend/conflicts.py; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t141_r7_two_digit_year.py 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T15:27:11.060Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: git add app/backend/conflicts.py tests/unit/test_t141_r7_two_digit_year.py && git commit -q -m "fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:27:12.563Z

**tool call — Bash**
````
{
 "command": "git add app/backend/conflicts.py tests/unit/test_t141_r7_two_digit_year.py"
}
````

### User / tool · 2026-11-02T15:27:12.677Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:27:13.226Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- app/backend/conflicts.py tests/unit/test_t141_r7_two_digit_year.py; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T15:27:16.358Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
78b6a33
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:27:24.512Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a141\nrm -rf $D; mkdir -p $D; git archive HEAD | tar -x -C $D; ln -s /Users/arsis/zlayt-pm-project/.venv $D/.venv\ncd $D && .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t141_r7_two_digit_year.py tests/unit/test_conflicts.py tests/unit/test_conflict_candidates.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t141_r3_variants.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py tests/unit/test_t141_d061_closed_exemption.py tests/unit/test_t141_r6_probes.py 2>&1 | tail -4\ngit -C /Users/arsis/zlayt-pm-project show HEAD~1:app/backend/conflicts.py > $D/app/backend/conflicts.py; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t141_r7_two_digit_year.py 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T15:27:39.103Z

**tool result**
````
........................................................................ [ 87%]
........................................................................ [ 99%]
...                                                                      [100%]
579 passed in 12.76s
FAILED tests/unit/test_t141_r7_two_digit_year.py::test_reviewer_blocker_case_q19
10 failed, 15 passed in 0.14s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:27:44.161Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-141 --sha 78b6a33 --agent backend; $B handoff T-141 --agent backend --text \"r7 F1 fixed. conflicts.py: _plural_list_ok now also reads a two-digit year (m/d/yy, m-d-yy, d.m.yy, m/yy, 'Jan 3, 26', '3rd Jan 26') as 20yy and exempts only when it is before the stated year (ambiguous numeric dates compare at year, D-055 safe direction). Tests: tests/unit/test_t141_r7_two_digit_year.py (25: Q19, 2- and 4-digit on/after = conflict, earlier years and BP 120/80 = info). Verified on git archive 78b6a33: 579 passed over the 9 conflict modules + new file; with the pre-fix conflicts.py, 10 of the new tests fail. Left: F2 (e2e test_conflict_skipped) is not backend scope. Commit 78b6a33.\" && $B move T-141 in_review --agent backend"
}
````

### User / tool · 2026-11-02T15:27:44.408Z

**tool result**
````
T-141: commit 78b6a33 recorded
handoff written on T-141
T-141: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:27:46.621Z

T-141 is in_review: the plural-history date guard in `conflicts.py` now reads two-digit-year dates (`1/3/26`, `03-01-26`, `Jan 3, 26`, `1/26`) as 20yy and flags them as conflicts when on or after the accident year. The new test file `tests/unit/test_t141_r7_two_digit_year.py` has the reviewer's blocker case plus 2- and 4-digit variants. On a `git archive` of commit 78b6a33, those and the nine existing conflict modules pass (579 tests); with the old `conflicts.py` swapped in, 10 of the new tests fail. I did not touch F2, the red `test_conflict_skipped.py` e2e file, which is outside backend scope.
