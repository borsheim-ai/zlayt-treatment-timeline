# Subagent: Backend: T-072 neutral flag title (Backend: T-072 neutral flag title)

Source: `agent-a603bb8df35cb0ec3.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:45:32.040Z

You own board card T-072 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `board.py show T-072`. The rule is D-040 in memory/ORCHESTRATOR_DECISIONS.md: no label asserts who spoke.

- Rename the patient_reported_onset flag's user-facing title from "Patient self-report" to a neutral title such as "Reported onset" (flag_templates, flags.py), and update tests.
- Remove the "(patient self-report)" suffix from app/backend/export.py, and update the export tests and any byte-exact export golden.
- If evals/golden files need to change, post a card note that lists the exact lines for qa; don't edit golden yourself. Note that the export golden may be byte-exact (D-019), so check `tests/fixtures/make_curated.py --check` and `python -m evals.run`: hallucination catch must stay 40/40.

Run `.venv/bin/python -m pytest -q tests/unit`. If another worker has uncommitted hunks in a file you touch, commit from a temp index (GIT_INDEX_FILE), adding only your hunks. Otherwise stage with `git add <paths>` and then commit with `git commit -m "..." -- <paths>` in a separate command. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-072 in_review --agent backend`. Reply in 2 lines.

### User / tool · 2026-11-02T02:45:32.044Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:34.356Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-072; grep -n \"D-040\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -40; grep -rn -i \"self-report\" app/backend app/llm tests evals --include=* -l 2>/dev/null | head -30; git status --short | head -20"
}
````

### User / tool · 2026-11-02T02:45:34.602Z

**tool result**
````
---
id: "T-072"
title: "Neutral title for patient_reported_onset flag; drop '(patient self-report)' from export (D-040 follow-through)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:45:10Z"
updated_at: "2026-11-02T02:45:23Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:45:23Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Flag title no longer asserts the speaker (e.g. 'Reported onset'); export no longer appends '(patient self-report)'; flag templates, export tests and golden expectations updated (qa note for golden lines); hallucination catch 40/40", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:45:23Z backend: claimed

## Handoff (filled when moving to in_review)

48:| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
app/backend/flag_templates.py
app/backend/export.py
app/backend/grounding.py
app/backend/narrative.py
app/llm/lexicon.yaml
tests/unit/test_grounding.py
tests/unit/test_narrative.py
tests/unit/test_export_edge.py
tests/e2e/test_flags_panel.py
evals/golden/hallucinations.jsonl
evals/golden/README.md
evals/golden/check_golden.py
evals/lexicon_heldout.jsonl
evals/golden/sample.export.expected.txt
evals/golden/sample.expected.json
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/llm/backends/fixture.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-065.md
 M board/cards/T-066.md
 M board/cards/T-067.md
 M evals/reports/latest.json
 M evals/run.py
 M memory/LESSONS.md
 M tests/fixtures/llm/056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:36.642Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"self-report\" app/backend/flag_templates.py app/backend/export.py app/backend/flags.py app/backend/narrative.py app/backend/grounding.py app/llm/lexicon.yaml tests/unit/*.py tests/e2e/*.py evals/golden/sample.export.expected.txt evals/golden/sample.expected.json evals/golden/README.md evals/golden/check_golden.py evals/golden/hallucinations.jsonl | cut -c1-260; git status --short app/backend tests evals/golden | head"
}
````

### User / tool · 2026-11-02T02:45:36.776Z

**tool result**
````
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Patient self-report", f"Patient self-report (not a physician's opinion) in {_at(v)}{_quote(v)}."),
app/backend/export.py:310:            s += " (patient self-report)"
app/backend/export.py:365:                    lab += " (patient self-report)"
app/backend/narrative.py:4:no dropped hedge / self-report / negation (D-022), no causation or adverse wording that the quote itself does not contain, no flag
app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
app/backend/grounding.py:58:# ---------------------------------------------------------------- lexicon (hedge / self-report sets)
app/llm/lexicon.yaml:26:#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
app/llm/lexicon.yaml:86:# "per <wife|husband|EMS|...>"). Bare "S:", "Subjective:" and "Self-reported" headers are not matched by any self_report entry,
app/llm/lexicon.yaml:90:  note: 'T-061 r1: anchored to the sentence SUBJECT (a sentence that starts with a non-patient speaker, or with "Per <non-patient>"); a patient subject that merely mentions EMS or a wife stays patient. Sentence-level test: the sentence 
app/llm/lexicon.yaml:496:  rationale: 'A self-reported prior history is the record''s own admission of an earlier condition.'
app/llm/lexicon.yaml:764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is 
tests/unit/test_export_edge.py:63:    assert "Conflict, PT plan:" in n and '"Charge per visit $185."' in n and "(patient self-report)" in n
tests/unit/test_grounding.py:124:    """R-TL-10(b)/D-022: summary omits a negation / hedge / self-report marker / 'approx.' the excerpt carries -> SUMMARY_DROPS_QUALIFIER."""
tests/unit/test_narrative.py:50:E5 = "On February 20, 2026, Capital PT recorded pain 4/10, improving"     # e5 quote: 'Pain 4/10, improving.' (no hedge, no self-report marker)
tests/e2e/test_flags_panel.py:20:    """R-FL-7: the record-9 causation flag shows 'Patient self-report'."""
tests/e2e/test_flags_panel.py:21:    open_case(page, sample_case); assert "Patient self-report" in flags(page).inner_text()
evals/golden/sample.export.expected.txt:58:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed
evals/golden/sample.export.expected.txt:69:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).
evals/golden/check_golden.py:21:    date; summaries satisfy required_terms (summary alone) and keep self-report attribution; numbers in summaries come from the
evals/golden/check_golden.py:491:                errs.append(f"export letter: summary for record {n} drops the self-report attribution for {sp['excerpt'][:30]!r}")
evals/golden/check_golden.py:543:        exported[int(m.group(1))] = {x.strip().lower().replace(" (patient self-report)", "") for x in m.group(2).split(";")}
evals/golden/README.md:72:* **Entries.** Found when the product emits an entry that covers `record_nos`, has the same `date` (or both ambiguous), `provider` equal to the record's header label after whitespace normalization (code copies it; merged duplicates ta
evals/golden/hallucinations.jsonl:10:{"id": "H10", "synthetic": true, "category": "causation", "record_text": "Record 9 | 2026-06-12 | Hill Country Pain Management, follow-up | \"Recommend cervical epidural steroid injection. Patient states symptoms began afte
evals/golden/sample.expected.json:626:      "summary": "Causation rests on patient self-report, not a physician's causation opinion.",
evals/golden/sample.expected.json:992:      "statement": "Presents the patient's self-report (records 1, 9) as a physician's opinion or examination finding.",
 M tests/fixtures/llm/056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
 M tests/fixtures/llm/067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd.json
 M tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
 M tests/fixtures/llm/07aab6f4f7a87ed2477b3cb9ebdb02449815ddf270c7f8aafdfa3c2338c9be19.json
 M tests/fixtures/llm/096042ca0286b135b1ff8db5f6d20a32cbf7c3989c5e10fc7ef5bf33da0670c2.json
 M tests/fixtures/llm/0cee28a9faf640b117982bccb05b874c1bc8b7359cd3ff5dc846f1ac8db9c8c9.json
 M tests/fixtures/llm/0e7db52d0c5b7b4b77cced05c5e9bae39d5038d4866d2baa759dd0396aa9707e.json
 M tests/fixtures/llm/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
 M tests/fixtures/llm/11245ae85d4b50423fb2ce331e7adbe7b3436e8dccf11252c833ecfa6e11db67.json
 M tests/fixtures/llm/128383b890348cd75ed0f2eb15f8516ffb0e90785d18225192c7a1b405bcf58d.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:39.427Z

**tool call — Bash**
````
{
 "command": "sed -n 295,320p app/backend/export.py; sed -n 355,370p app/backend/export.py; sed -n 118,130p app/backend/flag_templates.py; sed -n 55,66p tests/unit/test_export_edge.py; sed -n 536,546p evals/golden/check_golden.py; sed -n 60,72p evals/golden/sample.export.expected.txt | cut -c1-400; git status --short app/backend tests/unit tests/e2e evals/golden | grep -v fixtures/llm; grep -rn \"patient_reported_onset\\|Patient self-report\" app tests evals --include=*.py --include=*.yaml --include=*.md --include=*.html --include=*.js -l | head"
}
````

### User / tool · 2026-11-02T02:45:39.585Z

**tool result**
````
                        head = v.cite_dated(n)
                        segs.append(_terminate(head if k == 0 else _cap(head)))
            tail = "The tool does not choose between the dates."
            known = [r["date_iso"] for r in v.records.values() if r.get("date_iso")]
            if known:
                tail += f" First recorded treatment: {_long_date(min(known))}."
            return f"{label}: " + " ".join(segs + [tail])
        items = [f'{v.cite(n)} "{v.quote(n, by_rec[n][0]["excerpt"], whole_sentence=True)}"' if by_rec[n] else v.cite(n)
                 for n in order]
        return _terminate(f"{label}: " + "; ".join(items))
    items = []
    for x in _excerpt_ev(f) or ev:
        n = x["record_no"]
        s = f'{v.cite(n)} "{v.quote(n, x["excerpt"])}"' if x.get("field", "excerpt") == "excerpt" else v.cite(n)
        if f.get("subtype") in _SELF_REPORT_SUBTYPES:
            s += " (patient self-report)"
        items.append(s)
    return f"{label}: " + "; ".join(items)


def _flag_block(v, flags):
    """One line per gap/conflict flag, one merged line per other type; types in fixed order (gap, conflict, prior, causation)."""
    keyed, merged = [], {}
    for idx, f in enumerate(flags):
        t = f.get("type")
        if t in ("gap", "conflict"):
                    if _flag_label(f) not in hits:
                        hits.append(_flag_label(f))
            for x in _excerpt_ev(f):
                i = exc.find(x["excerpt"])
                if x["record_no"] != n or i < 0:
                    continue
                j = i + len(x["excerpt"])
                keep.update(k for k, (s, t) in enumerate(spans) if s < j and t > i)
                lab = _flag_label(f)
                if f.get("subtype") in _SELF_REPORT_SUBTYPES:
                    lab += " (patient self-report)"
                if lab not in hits:
                    hits.append(lab)
        if hits:
            quote = " ".join(exc[spans[k][0]:spans[k][1]] for k in sorted(keep)) or exc
            out.append(f'- {_cap(v.cite(n))}: "{quote}" {_terminate(_cap("; ".join(hits[:1] + [h[:1].lower() + h[1:] for h in hits[1:]])))}')
    "accident_dates_differ": _acc_differ,
    "provider_name_variant": _provider_variant,
    "treatment_plan_vs_actual": _pair("Treatment plan and what followed differ"),
    "other_fact_mismatch": _pair("Records differ on a fact"),
    "pre_existing": lambda v: ("Mention of a prior or pre-existing condition", f"{_at(v)} mentions a prior or pre-existing condition{_quote(v)}."),
    "degenerative_language": lambda v: ("Degenerative wording", f"{_at(v)} uses degenerative wording{_quote(v)}."),
    "prior_surgery": lambda v: ("Mention of prior surgery or repair", f"{_at(v)} mentions prior surgery or repair{_quote(v)}."),
    "speculative_language": lambda v: ("Hedged wording", f"Hedged wording in {_at(v)}{_quote(v)}."),
    "patient_report": lambda v: ("Patient self-report", f"Patient self-report (not a physician's opinion) in {_at(v)}{_quote(v)}."),
    "missed_care": lambda v: ("Missed or ended care", f"Wording about missed appointments or ending care in {_at(v)}{_quote(v)}."),
    "new_onset": lambda v: ("New-onset wording", f"New-onset wording in {_at(v)}{_quote(v)}."),
    "scene_facts": lambda v: ("Scene facts", f"Scene facts recorded by {_at(v)}{_quote(v)}."),
    "alternative_cause": lambda v: ("Mention of another injury or event", f"Mention of another injury or event in {_at(v)}{_quote(v)}."),
    for a in c["amounts"]:
        if a["cls"] in ("charge", "rate"):
            a["excerpt"] = full[a["record_no"]]
    for f in c["flags"]:
        f["subtype"] = {"treatment_plan": "treatment_plan_vs_actual", "patient_reported_onset": "patient_report"}.get(f["subtype"], f["subtype"])
    out = X.build_export(c)
    assert 'Source [Ex. __ / Bates __]: "ER charges: $6,240."' in out["letter_text"]
    n = out["internal_notes_text"]
    assert "Conflict, PT plan:" in n and '"Charge per visit $185."' in n and "(patient self-report)" in n
    order = []
    for line in (sec.group(1).split("\n") if sec else []):
        m = re.match(r'- Record (\d+) \([^)]*\): "[^"]+" (.+)\.$', line)
        if not m:
            errs.append(f"export notes: malformed flagged-language line: {line[:60]}")
            continue
        order.append(int(m.group(1)))
        exported[int(m.group(1))] = {x.strip().lower().replace(" (patient self-report)", "") for x in m.group(2).split(";")}
    if exported != derived or order != sorted(order):
        errs.append(f"export notes: flagged-language section != derived from golden flags (D-012/R-EX-4). derived={derived} exported={exported}")
    head = lambda lbl: lbl.split(",")[0]
FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).

AMOUNTS NOT TOTALED
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
 M tests/unit/test_eval_runner.py
app/llm/lexicon.yaml
app/frontend/mock_flags.js
app/frontend/dev/mock-data.js
app/backend/flag_templates.py
app/backend/export.py
tests/unit/test_export_edge.py
tests/e2e/test_flags_panel.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:42.415Z

**tool call — Bash**
````
{
 "command": "grep -n \"_SELF_REPORT_SUBTYPES\\|patient_report\" app/backend/*.py | cut -c1-220; grep -n \"patient_reported_onset\" -B2 -A8 app/llm/lexicon.yaml | cut -c1-240 | head -40; grep -n \"Patient self-report\\|self-report\" app/frontend/mock_flags.js app/frontend/dev/mock-data.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T02:45:42.525Z

**tool result**
````
app/backend/flag_templates.py:25:    ("causation", "patient_reported_onset"): "patient_report",
app/backend/flag_templates.py:35:    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Patient self-report", f"Patient self-report (not a physician's opinion) in {_at(v)}{_quote(v)}."),
app/backend/export.py:42:_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
app/backend/export.py:45:_SELF_REPORT_SUBTYPES = ("patient_reported_onset", "patient_report")
app/backend/export.py:309:        if f.get("subtype") in _SELF_REPORT_SUBTYPES:
app/backend/export.py:364:                if f.get("subtype") in _SELF_REPORT_SUBTYPES:
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (Jun
app/frontend/dev/mock-data.js:748:   "title": "Patient self-report",
app/frontend/dev/mock-data.js:749:   "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): \u201cPatient states symptoms began aft
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:48.395Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='app/backend/flag_templates.py'; s=open(p).read()\ns=s.replace('(\"Patient self-report\", f\"Patient self-report (not a physician\\'s opinion) in {_at(v)}{_quote(v)}.\")','(\"Reported onset\", f\"Onset wording reported in {_at(v)}{_quote(v)}.\")')\nopen(p,'w').write(s)\np='app/backend/export.py'; s=open(p).read()\ns=s.replace('''        if f.get(\"subtype\") in _SELF_REPORT_SUBTYPES:\n            s += \" (patient self-report)\"\n''','').replace('''                if f.get(\"subtype\") in _SELF_REPORT_SUBTYPES:\n                    lab += \" (patient self-report)\"\n''','')\nopen(p,'w').write(s)\np='tests/unit/test_export_edge.py'; s=open(p).read()\ns=s.replace(' and \"(patient self-report)\" in n',' and \"self-report\" not in n')\nopen(p,'w').write(s)\np='tests/e2e/test_flags_panel.py'; s=open(p).read()\ns=s.replace(\"shows 'Patient self-report'\",\"shows 'Reported onset'\").replace('\"Patient self-report\" in flags','\"Reported onset\" in flags')\nopen(p,'w').write(s)\nE\ngrep -n \"_SELF_REPORT_SUBTYPES\" app/backend/export.py; git diff --stat app/backend tests/e2e tests/unit/test_export_edge.py; grep -rn \"Patient self-report\\|self-report\" tests/unit tests/e2e app/frontend/*.js | cut -c1-160"
}
````

### User / tool · 2026-11-02T02:45:48.586Z

**tool result**
````
45:_SELF_REPORT_SUBTYPES = ("patient_reported_onset", "patient_report")
 app/backend/export.py          | 4 ----
 app/backend/flag_templates.py  | 2 +-
 tests/e2e/test_flags_panel.py  | 4 ++--
 tests/unit/test_export_edge.py | 2 +-
 4 files changed, 4 insertions(+), 8 deletions(-)
tests/unit/test_export_edge.py:63:    assert "Conflict, PT plan:" in n and '"Charge per visit $185."' in n and "self-report" not in n
tests/unit/test_grounding.py:124:    """R-TL-10(b)/D-022: summary omits a negation / hedge / self-report marker / 'approx.' the excerpt carries -> SUMMARY_DROPS
tests/unit/test_narrative.py:50:E5 = "On February 20, 2026, Capital PT recorded pain 4/10, improving"     # e5 quote: 'Pain 4/10, improving.' (no hedge, no self
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:51.535Z

**tool call — Bash**
````
{
 "command": "sed -i '/^_SELF_REPORT_SUBTYPES = /d' app/backend/export.py && cat >> tests/unit/test_export_edge.py <<'E'\n\n\ndef test_patient_report_flag_title_is_neutral():\n    \"\"\"D-040: no label asserts who spoke; the flag title and explanation carry no speaker claim.\"\"\"\n    from app.backend import flag_templates as T\n    title, _ = T._TEMPLATES[\"patient_report\"](type(\"V\", (), {\"__getattr__\": lambda s, k: (lambda *a, **kw: \"x\")})()) if hasattr(T, \"_TEMPLATES\") else (\"Reported onset\", \"\")\n    assert title == \"Reported onset\"\nE\ngrep -n \"^[A-Z_]* *= *{$\\|^def \" app/backend/flag_templates.py | head -20; sed -n 100,112p app/backend/flag_templates.py"
}
````

### User / tool · 2026-11-02T02:45:51.633Z

**tool result**
````
sed: 1: "app/backend/export.py
": command a expects \ followed by text
12:ALIASES = {
30:TYPE_OF = {
42:def _d(iso):
46:def _who(v, key="provider"):
51:def _when(v, key="date"):
55:def _quote(v, key="quote"):
59:def _at(v, key="provider", dkey="date"):
63:def _single(title, lead):
68:def _pair(title):
76:def _gap(v):
83:def _acc_after(v):
93:def _acc_differ(v):
99:def _provider_variant(v):
105:def _date_amb(v):
110:def _inj(v):
115:TEMPLATES = {
143:def category_of(flag_type: str, subtype: str) -> str:
151:def render(flag_type: str, subtype: str, **vars) -> tuple:
    a = f"{_who(v, 'provider_a')}" + (f" (“{v['quote_a']}”)" if v.get("quote_a") else "")
    b = f"{_who(v, 'provider_b')}" + (f" (“{v['quote_b']}”)" if v.get("quote_b") else "")
    return "Provider name differs between records", f"{a} and {b} may name the same provider."


def _date_amb(v):
    raw = f"The date “{v['raw']}” in " if v.get("raw") else "A date in "
    return "Date to confirm", f"{raw}{_who(v)} can be read more than one way; choose one reading."


def _inj(v):
    return ("Instruction-like text in a record",
            f"{_at(v)} contains instruction-like text{_quote(v)}. It is shown unchanged and everything from this record needs review.")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:52.724Z

The sed failed on macOS and my appended test was sloppy; I'll fix both.

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:45:54.782Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/export.py'; s=open(p).read()\ns=s.replace('_SELF_REPORT_SUBTYPES = (\"patient_reported_onset\", \"patient_report\")\\n','')\nopen(p,'w').write(s)\np='tests/unit/test_export_edge.py'; s=open(p).read()\ni=s.index('\\n\\ndef test_patient_report_flag_title_is_neutral')\ns=s[:i]+'''\n\ndef test_patient_report_flag_title_is_neutral():\n    \"\"\"D-040: no label asserts who spoke.\"\"\"\n    from app.backend import flag_templates as T\n    title, expl = T.render(\"causation\", \"patient_reported_onset\", provider=\"Hill Country Pain Management\", date=\"2026-06-12\", quote=\"Patient states symptoms began after the January collision.\")\n    assert title == \"Reported onset\" and \"self-report\" not in (title + expl).lower() and \"patient self\" not in expl.lower()\n'''\nopen(p,'w').write(s)\nE\nsed -n 143,165p app/backend/flag_templates.py; .venv/bin/python -m pytest -q tests/unit 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T02:46:17.322Z

**tool result**
````
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
ValueError: substring not found
def category_of(flag_type: str, subtype: str) -> str:
    """Resolve (type, subtype) to an ADR-013 category; KeyError if neither the category nor a golden alias (closed list)."""
    key = ALIASES.get((flag_type, subtype), subtype)
    if key not in TEMPLATES or TYPE_OF[key] != flag_type:
        raise KeyError(f"no flag template for {flag_type}/{subtype}")
    return key


def render(flag_type: str, subtype: str, **vars) -> tuple:
    extra = set(vars) - ALLOWED_VARS
    if extra:
        raise KeyError(f"unknown template variable(s): {sorted(extra)}")
    v = {k: x for k, x in vars.items() if x not in (None, "")}
    title, expl = TEMPLATES[category_of(flag_type, subtype)](v)
    return title, expl.replace(".”.", ".”")      # a quote that already ends in a period needs no second one
E         ...Full output truncated, use '-vv' to show

tests/unit/test_export.py:36: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_case_extras.py::test_default_export_is_byte_identical_to_golden_and_config_fills_the_citation
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
FAILED tests/unit/test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte
3 failed, 940 passed in 21.56s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:20.661Z

**tool call — Bash**
````
{
 "command": "grep -rn \"patient_report\\b\" app tests evals --include=*.py --include=*.js --include=*.yaml --include=*.md --include=*.json --include=*.jsonl --include=*.html | grep -v \"patient_reported\" | cut -c1-200; sed -n 10,40p app/backend/flag_templates.py; sed -n 38,46p app/backend/export.py"
}
````

### User / tool · 2026-11-02T02:46:20.805Z

**tool result**
````
app/README-arch.md:36:  lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
app/llm/lexicon.yaml:20:#   pre_existing, degenerative_language, speculative_language, patient_report, missed_care, new_onset).
app/llm/lexicon.yaml:26:#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
app/llm/lexicon.yaml:84:# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
app/llm/lexicon.yaml:741:  category: patient_report
app/llm/lexicon.yaml:757:  category: patient_report
app/frontend/dev/mock-data.js:746:   "category": "patient_report",
app/llm/prompts/flags_v1.md:13:- "patient_report": the patient's own statement about onset or cause ("patient states symptoms began after ...").
app/backend/flag_templates.py:35:    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (Jun
tests/unit/test_flags_pass.py:148:    """D-040 (supersedes D-033/D-035/D-037): nothing in code decides who is speaking, so the chip helpers are gone and no module sets patient_report."""
tests/unit/test_flags_pass.py:153:        assert 'source_kind="patient_report"' not in p.read_text() and '"source_kind": "patient_report"' not in p.read_text(), p.name
tests/fixtures/make_curated.py:30:    9: [("causation", "patient_report", "Patient states symptoms began after the January collision.")],
tests/fixtures/llm/eadc16a0cec098ac5d852b835fd3b35cc09643704bcca5995cec606dcdc06afa.json:5:    "category": "patient_report",
tests/fixtures/llm/4245be292c4c2242673445b1ba1ad1648c9a5e8807c40c4f5a55f7d7b7abca68.json:5:    "category": "patient_report",
tests/fixtures/llm/curated/eadc16a0cec098ac5d852b835fd3b35cc09643704bcca5995cec606dcdc06afa.json:6:    "category": "patient_report",
evals/golden/README.md:40:      "self_report_spans": [{"excerpt": "verbatim subjective sentence", "source_kind": "patient_report",
evals/golden/sample.expected.json:264:          "source_kind": "patient_report",
evals/golden/sample.expected.json:628:      "source_kind": "patient_report"
evals/library/case_lib02_slip_fall_prior_knee.expected.json:117:          "source_kind": "patient_report",
evals/library/case_lib04_dog_bite_scar_revision.expected.json:111:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:77:          "source_kind": "patient_report",
evals/golden/case_06_subtle_pre_existing.expected.json:150:          "source_kind": "patient_report",
evals/golden/check_golden.py:87:    if sp.get("source_kind") != "patient_report":
evals/golden/check_golden.py:88:        out.append("source_kind must be 'patient_report' (D-022)")
evals/golden/check_golden.py:160:        not span_problems(dict(excerpt="Tenderness over the anterior shoulder", source_kind="patient_report", attribution_any=["x"])) or \
evals/golden/check_golden.py:161:        span_problems(dict(excerpt="C/O neck pain", source_kind="patient_report", attribution_any=["C/O"])):
evals/golden/case_01_date_formats.expected.json:178:          "source_kind": "patient_report",
evals/library/case_lib01_er_only_then_gap.expected.json:111:          "source_kind": "patient_report",
evals/library/case_lib07_parking_lot_fall_outside_records.expected.json:87:          "source_kind": "patient_report",
evals/library/case_lib07_parking_lot_fall_outside_records.expected.json:133:          "source_kind": "patient_report",
evals/library/case_lib05_pedestrian_orif_hardware.expected.json:140:          "source_kind": "patient_report",

# golden-file subtypes (evals/golden) -> ADR-013 category
ALIASES = {
    ("gap", "treatment_gap"): "gap_over_30",
    ("conflict", "accident_date"): "accident_date_after_treatment",
    ("conflict", "provider_name"): "provider_name_variant",
    ("conflict", "treatment_plan"): "treatment_plan_vs_actual",
    ("conflict", "history_inconsistency"): "other_fact_mismatch",
    ("pre_existing", "prior_injury_prior_treatment"): "pre_existing",
    ("pre_existing", "prior_condition_reported"): "pre_existing",
    ("pre_existing", "prior_other_region"): "pre_existing",
    ("pre_existing", "baseline_symptom"): "pre_existing",
    ("pre_existing", "prior_surgery_same_region"): "prior_surgery",
    ("causation", "hedged_imaging"): "speculative_language",
    ("causation", "noncompliance"): "missed_care",
    ("causation", "patient_reported_onset"): "patient_report",
    ("causation", "temporal_after_gap"): "new_onset",
    ("causation", "accident_date_inconsistency"): "accident_date_provenance",
}

TYPE_OF = {
    "gap_over_30": "gap",
    "accident_date_after_treatment": "conflict", "accident_dates_differ": "conflict", "provider_name_variant": "conflict",
    "treatment_plan_vs_actual": "conflict", "other_fact_mismatch": "conflict",
    "pre_existing": "pre_existing", "degenerative_language": "pre_existing", "prior_surgery": "pre_existing",
    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
    "scene_facts": "causation", "alternative_cause": "causation", "litigation_referral": "causation",
    "objective_negative": "causation", "accident_date_provenance": "causation", "credibility_language": "causation",
    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning", "llm_split": "record_warning",
}

                 "accident_dates_differ": "accident date", "accident_date_after_treatment": "accident date"}
_ACCIDENT_SUBS = ("accident_date", "accident_dates_differ", "accident_date_after_treatment")
_COLLISION_RE = re.compile(r"rear-ended|collision|accident|crash|\bMV[AC]\b|struck|hit by", re.I)
# Order inside a merged flag line (most adjuster-actionable first); both the lexicon subtypes and the closed category names.
_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
          "temporal_after_gap", "new_onset", "accident_date_inconsistency", "accident_date_provenance"]
_FUTURE_RE = re.compile(r"^\s*recommend", re.I)  # extend by card (R-EX-4 section 7)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:25.719Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_export_edge.py <<'E'\n\n\ndef test_patient_report_flag_title_is_neutral():\n    \"\"\"D-040: no label asserts who spoke.\"\"\"\n    from app.backend import flag_templates as T\n    title, expl = T.render(\"causation\", \"patient_reported_onset\", provider=\"Hill Country Pain Management\", date=\"2026-06-12\", quote=\"Patient states symptoms began after the January collision.\")\n    assert title == \"Reported onset\" and \"self-report\" not in (title + expl).lower() and \"patient self\" not in expl.lower()\nE\n.venv/bin/python -m pytest -q tests/unit 2>&1 | grep -E \"^(FAILED|E  )\" | cut -c1-300 | head -20; git stash list | head -1; git diff tests/unit/test_e2e_contract.py | head"
}
````

### User / tool · 2026-11-02T02:46:25.789Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not run git stash (it rewinds shared board/memory files of other agents)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:28.071Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_export_edge.py <<'E'\n\n\ndef test_patient_report_flag_title_is_neutral():\n    \"\"\"D-040: no label asserts who spoke.\"\"\"\n    from app.backend import flag_templates as T\n    title, expl = T.render(\"causation\", \"patient_reported_onset\", provider=\"Hill Country Pain Management\", date=\"2026-06-12\", quote=\"Patient states symptoms began after the January collision.\")\n    assert title == \"Reported onset\" and \"self-report\" not in (title + expl).lower() and \"patient self\" not in expl.lower()\nE\n.venv/bin/python -m pytest -q tests/unit 2>&1 | grep -E \"^(FAILED|E  )\" | cut -c1-300 | head -20"
}
````

### User / tool · 2026-11-02T02:46:49.284Z

**tool result**
````
E       assert ('TREATMENT CH...ds: $8,390.00' == 'TREATMENT CH...ds: $8,390.00'
E         
E         Skipping 2713 identical leading characters in diff, use -v to show
E           : $8,390.00 and 'INTERNAL REV...LUDED\n- none' == 'INTERNAL REV...LUDED\n- none'
E         
E         Skipping 1538 identical leading characters in diff, use -v to show
E         - ollision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
E         ?           ----------------------
E         + ollision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
E           
E           FLAGS DISMISSED...
E         
E         ...Full output truncated, use '-vv' to show)
E       AssertionError: ['btn-undo-batch']
E       assert not ['btn-undo-batch']
E       assert 'INTERNAL REV...LUDED\n- none' == 'INTERNAL REV...LUDED\n- none'
E         
E         Skipping 1538 identical leading characters in diff, use -v to show
E         - ollision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
E         ?           ----------------------
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:51.929Z

**tool call — Bash**
````
{
 "command": "grep -rn \"patient self-report\" evals/golden/*.txt tests/fixtures 2>/dev/null | cut -c1-80 | awk -F: '{print $1\":\"$2}'; .venv/bin/python tests/fixtures/make_curated.py --check 2>&1 | tail -5; .venv/bin/python -m evals.run 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T02:46:53.576Z

**tool result**
````
evals/golden/sample.export.expected.txt:58
evals/golden/sample.export.expected.txt:69
entries: 9 non-verified: []
narrative: 9 sentences, removed: []
letter equal: True | notes equal: False
llm call failed call_id=cb4ec5fa063a1 step=extract attempt=1 prompt_hash=4b3235bcc27fc57d8df381ddb636080623de75ee126ef90ad5acc8fb69609bfb
llm call failed call_id=c27d85c2113d3 step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
llm call failed call_id=c78764ce6b984 step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=c7c69e21687ac step=conflicts attempt=1 prompt_hash=72f2b8a330ffbf0fe899b1558f048a20e812d19112dca07a3b4e2469aba19140
llm call failed call_id=c6f7ed10eea12 step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
llm call failed call_id=c416a51737aa6 step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
llm call failed call_id=c3178d15df78f step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
ship_bar_met=False backend=fixture report=/Users/arsis/zlayt-pm-project/evals/reports/20261102T024653Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:55.582Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"hallucination\\|catch\\|no_invented\" evals/reports/20261102T024653Z.md | head -12; ls -t evals/reports | head -4"
}
````

### User / tool · 2026-11-02T02:46:55.680Z

**tool result**
````
5:Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
16:| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
33:- seeded hallucinations not caught: []
latest.json
20261102T024653Z.md
20261102T024355Z.md
20261102T024348Z.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:46:57.693Z

**tool call — Bash**
````
{
 "command": "grep -n \"Blockers\\|invented\" evals/reports/20261102T024355Z.md evals/reports/20261102T024653Z.md | cut -c1-260; sed -n 17,32p evals/reports/20261102T024653Z.md | cut -c1-220"
}
````

### User / tool · 2026-11-02T02:46:57.790Z

**tool result**
````
evals/reports/20261102T024355Z.md:5:Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
evals/reports/20261102T024653Z.md:5:Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | None | 0 | R-TL-4 |
| determinism_3run | None | 1.0 | R-CO-7 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |

Assertions: {"gap_28_not_flagged": true, "gap_73_flagged": true, "all_gap_rows_correct": true}
spec_matches_golden: True

## Misses (report what was found)

- entry misses: {"case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}
- missed must flags: {}
- grounding failures: []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:02.177Z

**tool call — Bash**
````
{
 "command": "sed -n 58p evals/golden/sample.export.expected.txt | grep -o '.\\{60\\}(patient self-report).\\{30\\}'; git add app/backend/flag_templates.py app/backend/export.py tests/unit/test_export_edge.py tests/e2e/test_flags_panel.py && git diff --cached --stat | tail -6"
}
````

### User / tool · 2026-11-02T02:47:02.307Z

**tool result**
````
Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain 
 app/backend/export.py          | 5 -----
 app/backend/flag_templates.py  | 2 +-
 tests/e2e/test_flags_panel.py  | 4 ++--
 tests/unit/test_export_edge.py | 9 ++++++++-
 4 files changed, 11 insertions(+), 9 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:04.022Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"feat(backend): neutral 'Reported onset' flag title; drop '(patient self-report)' from export (D-040, T-072)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/flag_templates.py app/backend/export.py tests/unit/test_export_edge.py tests/e2e/test_flags_panel.py && git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T02:47:04.391Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
3b6a3fe
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:12.691Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B commit T-072 --sha 3b6a3fe --agent backend\n$B note T-072 --agent backend --text \"QA ACTION (golden is yours, not edited): evals/golden/sample.export.expected.txt remove the suffix ' (patient self-report)' on line 58 (INTERNAL REVIEW causation entry for record 9: ...January collision.\\\" (patient self-report); record 7 -> ...January collision.\\\"; record 7) and on line 69 ('Causation language (patient self-report).' -> 'Causation language.'). Until then tests/unit/test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte, test_case_extras.py::test_default_export_is_byte_identical_to_golden... and make_curated --check ('notes equal: False', letter equal True) fail. check_golden.py:543 .replace(' (patient self-report)','') is now a harmless no-op, can be dropped. Unrelated pre-existing failure: tests/unit/test_e2e_contract.py::test_every_test_id_is_declared ('btn-undo-batch', frontend). evals.run: hallucination_catch 40/40; blocker 4_no_invented_facts + fixture-determinism were already present in the prior report. Coordinator ask re patient_report template: neutralized (key kept as internal category id; title 'Reported onset', explanation 'Onset wording reported in ...'). Renaming the category id would change prompts/flags_v1.md (hash -> fixture re-record), lexicon.yaml (researcher), curated fixtures, frontend mocks; and flags_v1.md:13 still defines it as 'the patient's own statement' - propose follow-up card if wanted.\"\n$B ac T-072 --check 1 --agent backend --evidence \"commit 3b6a3fe; tests/unit/test_export_edge.py::test_patient_report_flag_title_is_neutral passes; unit 940 pass, 2 fail only on byte-exact export golden (qa note posted) + 1 unrelated frontend; evals.run hallucination_catch 40/40 (evals/reports/20261102T024653Z.md)\"\n$B handoff T-072 --agent backend --text \"Changed: patient_report template title -> 'Reported onset' (explanation 'Onset wording reported in ...'); removed both '(patient self-report)' suffixes and _SELF_REPORT_SUBTYPES from export.py; updated export/e2e tests, added neutral-title test. Verified: pytest tests/unit (940 pass; export golden byte-exact tests fail until qa edits sample.export.expected.txt lines 58 and 69, listed in note); evals.run hallucination 40/40. Left: qa golden edit; optional follow-up to rename category id/prompt line (needs fixture re-record). Surprised: category id patient_report is wired through prompt, lexicon, fixtures, so only user-facing text was neutralized.\"\n$B move T-072 in_review --agent backend"
}
````

### User / tool · 2026-11-02T02:47:13.034Z

**tool result**
````
T-072: commit 3b6a3fe recorded
noted on T-072
AC 1 checked: commit 3b6a3fe; tests/unit/test_export_edge.py::test_patient_report_flag_title_is_neutral passes; unit 940 pass, 2 fail only on byte-exact export golden (qa note posted) + 1 unrelated frontend; evals.run hallucination_catch 40/40 (evals/reports/20261102T024653Z.md)
handoff written on T-072
T-072: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:16.043Z

T-072 is in_review (commit 3b6a3fe), but two byte-exact export-golden unit tests still fail until qa edits `evals/golden/sample.export.expected.txt`. The flag title is now "Reported onset", and the "(patient self-report)" suffixes are gone from `export.py`. Hallucination catch is still 40/40.

- **Tests:** unit run is 940 pass, 3 fail. Two failures are the golden tests; I posted a card note giving qa the exact lines to change (58 and 69), and `make_curated --check` shows the same mismatch in the notes. The third is a frontend contract test (`btn-undo-batch`) that I didn't touch.
- **`patient_report` template:** I neutralized it rather than renaming it. The key is also the category id in `prompts/flags_v1.md`, `lexicon.yaml` and the fixtures, so a rename would force a fixture re-record. The `flags_v1.md` line still defines it as "the patient's own statement"; I noted a possible follow-up card in the board note.
