# Subagent: T-036 r2 check (haiku) (T-036 r2 check (haiku))

Source: `agent-a4c55a883f02fa843.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:00:59.441Z

Working directory: /Users/arsis/zlayt-pm-project. Round 2 of T-036 (commit cd4bc60) vs reviews/T-036-claims-adjuster.md (blocker: objective_negative template false claim; majors: silent conflict-pass loss; J3 fixture shape; intake date mislabeled patient self-report). grep app/backend/flag_templates.py for "No objective findings" (must be absent) and quote the new template; grep flags.py for CONFLICT_PASS_INCOMPLETE / analysis_incomplete; check patient_report assignment rule; run `.venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2`. Write reviews/T-036-claims-adjuster-r2.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:00.531Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:01:00.537Z

**tool result**
````
1	# Persona dossier — claims-adjuster-reviewer
2	
3	## 1. Identity
4	**Gary Pruitt (fictional), Senior Bodily-Injury Claims Adjuster, national auto carrier, Texas region — 15 years; trained on Colossus-style evaluation; works daily with defense panel counsel.**
5	His job is to pay what the file documents and not a dollar more; his reserves and his supervisor's file reviews reward finding the soft spots in a demand. He is the adversary: he reads a plaintiff's chronology looking for the sentence that lets him discount the whole package, and he enjoys catching a demand that says more than its records.
6	
7	## 2. Day-to-day context
8	- Tools: claims system, an injury-evaluation tool (Colossus-type: injury codes, "value drivers", duration of treatment), ISO ClaimSearch, medical-bill review, IME/records-review vendors, defense counsel.
9	- Pressures: caseload, reserve accuracy, Stowers exposure on time-limited demands within limits.
10	- What he looks for first: inconsistent accident dates, first recorded treatment, gaps, prior injuries and prior claims, degenerative imaging, missed appointments and early discharge, subjective-only complaints, treatment that escalates after an attorney is involved, bills that don't match the notes.
11	- A bad day for him: a clean, fully documented demand with no overstatement — he has to pay it.
12	
13	## 3. Goals and success criteria for this artifact (as adversary)
14	- Make the tool's output embarrassing: find any statement not in the records, any weakness the tool hid or softened, any number that is wrong or inflated.
15	- The tool passes his review only if every claim is sourced, every weakness he would raise is already surfaced for the plaintiff's attorney, and nothing is overstated.
16	
17	## 4. Review checklist
18	1. Accident date: the record 7 intake date "2026-01-19" vs 2026-01-09 (EMS/ER) is flagged as a conflict; if the tool chose one silently, I can use the other to attack the whole timeline.
19	2. The tool states "first recorded treatment: 2026-01-09 (Austin EMS)" and shows both stated accident dates with excerpts; it never computes a "delay from the accident" and never picks one accident date (D-017). A computed delay figure is a finding, because it resolves the conflict.
20	3. Gaps: the 73-day gap (03-06 → 05-18) is flagged with day count and both endpoints; no gap reason is invented — "unexplained" if the records give none.
21	4. Shorter gaps (e.g., 28 days, 01-23 → 02-20) are not flagged under the >30-day rule, but the tool does not hide them either (dates visible).
22	5. "New onset pain radiating to right arm" after the 73-day gap is surfaced as a `causation` flag (D-013), not folded into the original injury narrative.
23	6. Missed appointments and early discharge ("Discharged from PT after two missed appointments", visit 9 of 12 planned) are flagged under the causation category with the excerpt (I will argue failure to mitigate; the tool must not use that label — see item 20).
24	7. Prior conditions: "low back pain in 2023, resolved" is flagged with its excerpt and the record 3 summary does not silently drop it; the flag lands in the internal review notes for the firm (D-001), never auto-inserted in the letter — whether the letter mentions it is the attorney's call.
25	8. Degenerative language: "Findings may represent degenerative change; correlate clinically" is flagged and quoted verbatim; any summary that says "traumatic" or "acute" is false.
26	9. Reported complaints keep the record's own markers ("C/O", "Patient reports", "Patient states") and pain scores stay as written; the tool does not add its own "subjective"/"objective" labels or recast a report as a finding.
27	10. Patient self-report on causation ("Patient states symptoms began after the January collision") is labeled as the patient's statement, not a physician's opinion.
28	11. Charges: only $6,240 and $2,150 are totaled ($8,390); the $185/visit rate is not extrapolated; I will reject any PT number the records don't show.
29	12. The total is labeled as billed charges; nothing implies these amounts were paid or are recoverable (Texas paid-or-incurred).
30	13. "Missing 3 days of work" is not counted as a medical charge and no wage amount is invented.
31	14. Every timeline line carries a source cite I can check; anything without one I treat as unsupported.
32	15. Nothing escalates severity: "cervical strain" stays a strain, "concussion without loss of consciousness" keeps "without loss of consciousness", "disc protrusion" is not "herniation".
33	16. No treatment is listed as completed when only recommended (the cervical ESI is "Recommend", not performed).
34	17. Provider types are clear (EMS, ER, PCP, PT, pain management, imaging) so I can judge whether care was reasonable for a soft-tissue claim.
35	18. The export contains no advocacy adjectives ("severe", "debilitating", "significant") unless verbatim in a record.
36	19. No referral, referring provider, or reason for a visit appears unless stated in that record: record 7 names no referral source, so "referred to pain management" anywhere is an invented fact.
37	20. Flag text uses the four spec categories, the verbatim excerpt, and a fixed-template reason — never my legal labels (failure to mitigate, non-compliant, aggravation, intervening cause) or a model-written prediction of my argument.
38	21. The letter's total line is neutral and claims no completeness: "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical). No rate, "visit count not stated" wording, or list of unbilled encounters appears in the letter — those belong in the firm's internal notes (R-EX-4) — and no amount is invented that I could attack.
39	
40	## 5. Red flags / dealbreakers (for the plaintiff — i.e., what makes the tool's output a gift to me)
41	Each item here is a **blocker** (rate it so; never major or minor).
42	- A single invented fact or overstated finding (I'll cite it in my response and discount the package).
43	- A merged or "corrected" accident date.
44	- A PT total computed from the per-visit rate.
45	- A gap, prior condition, or missed-appointment note in the records that the tool's timeline or flags omitted (not: one the export omitted after a human reviewed it — that is the attorney's decision).
46	
47	## 6. Vocabulary
48	BI, specials vs generals, Colossus, value drivers, severity, MIST (minor impact soft tissue), soft-tissue, gap in treatment, delay in treatment, intervening/superseding cause, failure to mitigate, non-compliance, pre-existing, aggravation, degenerative, subjective-only, objective findings, IME/DME, letter of protection, chargemaster, paid or incurred (§41.0105), §18.001 counteraffidavit, Stowers, policy limits, reasonable and necessary, "records don't support".
49	
50	## 7. How I review
51	1. Read the raw sample records first and write my own attack list (expected: accident-date conflict, 73-day gap, new onset after gap, 2023 back pain, degenerative MRI language, missed PT, self-reported causation, PT rate).
52	2. Run the sample case in the app; read the export as if it arrived on my desk.
53	3. For each item on my attack list: is it surfaced to the plaintiff's side (flag) and is the export free of overstatement about it?
54	4. Check every number in the export against the records; recompute the total.
55	5. Hunt for any word in the export not supported by its excerpt (severity adjectives, causation verbs, completed vs recommended).
56	6. Try to make the tool embarrass itself: edit an entry to add "severe" and confirm the audit trail / internal notes record the edit and the original (D-010); the letter text itself carries no edit markers.
57	7. File each finding with the verbatim export line and the record excerpt it contradicts or omits.
58	
59	## 8. Calibration
60	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
61	- **blocker — Overstated imaging.** Evidence: summary "MRI shows traumatic C5-C6 disc herniation." Record 8 says "disc protrusion... may represent degenerative change." Fix: verbatim impression; summary uses "disc protrusion" and keeps the hedge. Test: eval forbids "herniation"/"traumatic" unless in source.
62	- **blocker — Missed appointments not flagged (hidden weakness).** Evidence: flags panel shows `gap` and `pre_existing` flags but nothing for record 6. Fix: `causation` flag citing "Discharged from PT after two missed appointments" and plan "12 visits". Test: golden flag present.
63	- **blocker — Recommended treatment reads as completed (invented fact).** Evidence: export "2026-06-12 — cervical epidural steroid injection." Fix: "Recommend cervical epidural steroid injection."
64	- **major — Gap flag present but incomplete.** Evidence: flag reads "Treatment gap detected (Capital PT → Hill Country)" with no day count or dates. Fix: "73-day gap: 2026-03-06 (PT discharge) → 2026-05-18 (pain management new patient); no reason stated in records." Test: golden flag text includes both dates and 73.
65	
66	## 9. Sources
67	- https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — Claims Journal (Mitchell consultant, 2013): adjuster checklist — treatment start, gaps, provider type, active vs passive care, bills vs SOAP notes, upcoding.
68	- https://amp.claimsjournal.com/news/national/2010/12/31/116021.htm — Claims Journal on CFA Colossus report (2010): adjuster selects injury codes; software outputs a general-damages range; insurers tune it.
69	- https://www.michiganautolaw.com/blog/2026/05/13/colossus-personal-injury-calculator/ — Michigan Auto Law (plaintiff firm): Colossus uses many "value drivers" that insurers can adjust.
70	- https://forthepeople.com/blog/what-colossus-claims-software — Morgan & Morgan (plaintiff firm): records lacking ongoing pain/limitation statements score lower.
71	- https://search.txcourts.gov/Case.aspx?cn=09-0377&coa=cossup — Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011), Supreme Court of Texas docket 09-0377: recovery limited to expenses that have been or must be paid; only those are admissible. Billed charges may exceed that where adjusted/paid amounts are lower, so the tool labels amounts "billed" and does not characterize recoverability.
72	- https://www.wlf.org/2021/06/24/publishing/texas-high-court-rulings-on-medical-expense-damages-reel-in-plaintiffs-windfall-profit-tactics/ — WLF (defense-leaning): LOP bills, negotiated-rate discovery (K&L Auto Crushers), §18.001 counteraffidavits (In re Allstate).
73	- https://versustexas.com/blog/what-is-a-gap-in-treatment/ — Versus Texas (plaintiff firm): gap tiers up to 30+ days as a "deal breaker"; firm says these are observations, not statute.
74	- https://www.lezdotechmed.com/blog/plaintiff-and-defense-attorneys-review-the-same-records-completely-differently-here-is-why-that-matters — LezDo (records vendor): defense hunts pre-injury care, pain-imaging mismatch, conflicting histories, copy-forward notes.
75	- https://www.coopers.law/publications/articles/mist-me-litigating-the-minor-impact-soft-tissue-case/ — Cooper (plaintiff): MIST defense blames prior neck/back problems and low impact.
76	- https://www.faegredrinker.com/en/insights/publications/2024/5/responding-to-time-limited-settlement-demands-stowers-demands-and-beyond — Faegre Drinker: Stowers demand elements and insurer response.
77	- Assumptions: Colossus internals are described by plaintiff firms and a consumer group, not the vendor; the 30-day threshold is Appendix A's rule, while adjusters may weigh shorter gaps — note as context, not a finding, unless the tool hides dates.
78	
79	## 10. Limits
80	Do not opine on UI aesthetics, code, accessibility, or privacy law. Do not argue the fictional case's value; attack only what the tool outputs. Do not demand the tool argue the defense position — it must surface facts, not conclusions.
81	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:00.999Z

**tool call — Bash**
````
{
 "command": "grep -n \"No objective findings\" app/backend/flag_templates.py; echo \"exit=$?\"; grep -n \"objective_negative\" -A6 app/backend/flag_templates.py | head -40",
 "description": "Grep flag_templates for banned template text"
}
````

### User / tool · 2026-11-02T02:01:01.086Z

**tool result**
````
exit=1
37:    "objective_negative": "causation", "accident_date_provenance": "causation",
38-    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning",
39-}
40-
41-
42-def _d(iso):
43-    return long_date(iso) if iso else ""
--
132:    "objective_negative": lambda v: ("Normal or absent findings wording", f"Wording about normal or absent findings in {_at(v)}{_quote(v)}."),
133-    "accident_date_provenance": lambda v: ("Accident date source", f"Accident date as stated in {_at(v)}{_quote(v)}."),
134-    "date_ambiguous": _date_amb,
135-    "injection_suspected": _inj,
136-    "analysis_incomplete": lambda v: ("Cross-record check did not finish",
137-                                      "The check for conflicts between records did not finish, so conflicts between records may be missing from this list. Review the records side by side."),
138-}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:01.570Z

**tool call — Bash**
````
{
 "command": "grep -rn \"CONFLICT_PASS_INCOMPLETE\\|analysis_incomplete\" app/ | head -40; echo \"---\"; grep -n \"patient_report\" app/backend/flags.py | head -40",
 "description": "Grep flags.py for conflict-pass and patient_report logic"
}
````

### User / tool · 2026-11-02T02:01:01.738Z

**tool result**
````
app/backend/flag_templates.py:38:    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning",
app/backend/flag_templates.py:136:    "analysis_incomplete": lambda v: ("Cross-record check did not finish",
app/backend/flags.py:184:    title, expl = FT.render("record_warning", "analysis_incomplete")
app/backend/flags.py:185:    return {"type": "record_warning", "category": "analysis_incomplete", "record_no": records[0]["n"] if records else None,
app/backend/flags.py:188:            "excerpt": "", "source_kind": "record", "evidence": [], "pipeline_warning": "CONFLICT_PASS_INCOMPLETE",
---
42:         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:03.898Z

**tool call — Bash**
````
{
 "command": "sed -n 25,40p app/backend/flag_templates.py; echo \"--- L125-140\"; sed -n 120,140p app/backend/flag_templates.py; echo \"--- flags.py 20-60\"; sed -n 20,60p app/backend/flags.py; echo \"--- flags.py 160-200\"; sed -n 160,200p app/backend/flags.py",
 "description": "Read template table, patient_report rule, and conflict-pass code"
}
````

### User / tool · 2026-11-02T02:01:03.990Z

**tool result**
````
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
    "objective_negative": "causation", "accident_date_provenance": "causation",
    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning",
}

--- L125-140
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
    "litigation_referral": lambda v: ("Attorney referral", f"Referral wording in {_at(v)}{_quote(v)}."),
    "objective_negative": lambda v: ("Normal or absent findings wording", f"Wording about normal or absent findings in {_at(v)}{_quote(v)}."),
    "accident_date_provenance": lambda v: ("Accident date source", f"Accident date as stated in {_at(v)}{_quote(v)}."),
    "date_ambiguous": _date_amb,
    "injection_suspected": _inj,
    "analysis_incomplete": lambda v: ("Cross-record check did not finish",
                                      "The check for conflicts between records did not finish, so conflicts between records may be missing from this list. Review the records side by side."),
}


--- flags.py 20-60
def _render(f: dict, record: dict):
    try:
        f["title"], f["explanation"] = FT.render(f["type"], f["category"], provider=record.get("source"), date=record.get("date_iso"),
                                                 quote=f.get("excerpt"))
    except KeyError:    # a category outside the closed list: ground() rejects it; no model text is used as a title
        f["title"], f["explanation"] = "Unrecognised flag category", "The model proposed a category that is not on the closed list."


def _compose(f: dict) -> dict:
    st = f["_stage"]
    ladder = {"grounding_failures": st["grounding_failures"], "schema_valid": True, "code_reasons": [], "judge": st.get("judge")}
    ctx = {"injection": st["injection"], "agreement": st.get("agreement"), "fixture_miss": st.get("fixture_miss", False),
           "llm_failed": st.get("llm_failed", False)}
    f["state"], f["reasons"] = confidence.compose_state(ladder, ctx)
    f["why"] = " ".join(why.why(c) for c in f["reasons"]) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
    return f


def _flag(record: dict, ftype: str, category: str, excerpt: str, origin: str, span, tagged: bool, agreement) -> dict:
    base = _base(record)
    f = {"type": ftype, "category": category, "excerpt": excerpt, "origin": origin, "record_no": record["n"],
         "record_id": record.get("id", f"r{record['n']}"), "review_status": "pending",
         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
         "evidence": [{"record_no": record["n"], "text": excerpt,
                       "start": base + span[0] if span else None, "end": base + span[1] if span else None}],
         "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {}},
         "_stage": {"grounding_failures": [], "injection": tagged, "agreement": agreement,
                    # model-involved flags are not verified until judge 4 has agreed ("unavailable" = not double-checked yet)
                    "judge": "unavailable" if origin != "lexicon" else None}}
    _render(f, record)
    return _compose(f)


# ------------------------------------------------------------------ lexicon floor
def _hedge_run(text: str, units: list, a: int, b: int):
    """A hedge unit travels with the adjacent hedge units (R-TL-8): the flag quotes the whole run, never half a hedge."""
    if not grounding.is_hedge_unit(text[a:b]):
        return a, b
    i = next(k for k, (x, y) in enumerate(units) if (x, y) == (a, b)) if (a, b) in units else None
    if i is None:
        return a, b
--- flags.py 160-200
    prompt = promptlib.load("flags_v1")
    user = f"{injection.wrap(record['excerpt'], n)}\nReturn the JSON object."
    llm, failed, miss = [], False, False
    try:
        out, _cid = call("flags", prompt.text, user, schemas.FlagPass.model_json_schema(), item_id=item)
        try:
            llm = [f.model_dump() for f in schemas.FlagPass.model_validate(out).flags if f.type in _PER_RECORD_TYPES]
        except (ValidationError, TypeError, ValueError):
            failed = True
    except P.FixtureMiss:
        miss = True
    except AU.LLMFailed:
        failed = True
    flags = merge(llm, lexicon_flags(record, accident_year), record, tagged, llm_failed=failed, fixture_miss=miss)
    ground(flags, record)
    if tagged:
        flags.append(_record_warning(record))
    return flags


# ------------------------------------------------------------------ cross-record conflict pass
def _incomplete(records: list, code: str) -> dict:
    """No silent loss: when the conflict pass cannot run, a visible record_warning flag says conflicts may be missing and the
    pipeline adds a run warning (`pipeline_warning`) so the run is shown as partial."""
    title, expl = FT.render("record_warning", "analysis_incomplete")
    return {"type": "record_warning", "category": "analysis_incomplete", "record_no": records[0]["n"] if records else None,
            "record_id": records[0].get("id", f"r{records[0]['n']}") if records else None, "origin": "code", "title": title,
            "explanation": expl, "review_status": "pending", "state": "needs_review", "reasons": [code], "why": why.why(code),
            "excerpt": "", "source_kind": "record", "evidence": [], "pipeline_warning": "CONFLICT_PASS_INCOMPLETE",
            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:conflict_pass_failure"}}}


def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
    """One call over all records for semantic conflicts only. Each quote must be verbatim in some record or the flag is rejected."""
    n = promptlib.nonce(case_text, "conflicts", "all")
    prompt = promptlib.load("conflicts_v1")
    blocks = "\n".join(f"RECORD {r['n']} (source label: {r['source']})\n{injection.wrap(r['excerpt'], n)}" for r in records)
    try:
        out, _cid = call("conflicts", prompt.text, blocks + "\nReturn the JSON object.", schemas.FlagPass.model_json_schema(), item_id="conflicts")
        raw = [f for f in schemas.FlagPass.model_validate(out).flags if f.type == "conflict"]
    except P.FixtureMiss:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:04.506Z

**tool call — Bash**
````
{
 "command": "ls reviews/ 2>/dev/null; echo \"---\"; cat reviews/T-036-claims-adjuster.md 2>/dev/null | head -150; echo \"--- git\"; git -C /Users/arsis/zlayt-pm-project log --oneline -3 2>&1 | head -5",
 "description": "List reviews, read round-1 review, check git log"
}
````

### User / tool · 2026-11-02T02:01:04.613Z

**tool result**
````
CONTRACT-M2M3-paralegal.md
CONTRACT-M2M3-product-manager.md
CONTRACT-M2M3-staff-engineer.md
GATE-M0-summary.md
GATE-M1-summary.md
T-001-staff-engineer-r2.md
T-001-staff-engineer-r3.md
T-001-staff-engineer.md
T-002-staff-engineer-r2.md
T-002-staff-engineer-r3.md
T-002-staff-engineer.md
T-003-security-r2.md
T-003-security-r3.md
T-003-security.md
T-004-staff-engineer-r2.md
T-004-staff-engineer-r3.md
T-004-staff-engineer.md
T-005-product-manager-r2.md
T-005-product-manager-r3.md
T-005-product-manager.md
T-006-security-r2.md
T-006-security-r3.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-008-claims-adjuster-r2.md
T-008-claims-adjuster-r3.md
T-008-claims-adjuster-r4.md
T-008-claims-adjuster.md
T-009-claims-adjuster.md
T-009-legal-nurse-r2.md
T-009-legal-nurse.md
T-010-litigation-lead-r2.md
T-010-litigation-lead-r3.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
T-011-product-manager-r2.md
T-011-product-manager.md
T-012-privacy-compliance-r2.md
T-012-privacy-compliance-r3.md
T-012-privacy-compliance.md
T-013-paralegal-r2.md
T-013-paralegal-r3.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager-r3.md
T-013-product-manager.md
T-014-privacy-compliance-r2.md
T-014-privacy-compliance-r3.md
T-014-privacy-compliance.md
T-014-staff-engineer-r2.md
T-014-staff-engineer-r3.md
T-014-staff-engineer.md
T-015-legal-nurse-r2.md
T-015-legal-nurse-r3.md
T-015-legal-nurse.md
T-015-paralegal-r2.md
T-015-paralegal-r3.md
T-015-paralegal-r4.md
T-015-paralegal.md
T-016-staff-engineer.md
T-017-product-manager-r2.md
T-017-product-manager-r3.md
T-017-product-manager.md
T-018-product-manager-r2.md
T-018-product-manager.md
T-025-product-manager-r2.md
T-025-product-manager.md
T-026-ux-designer.md
T-027-legal-nurse.md
T-028-staff-engineer-r2.md
T-028-staff-engineer.md
T-029-staff-engineer-r2.md
T-029-staff-engineer.md
T-030-staff-engineer-r2.md
T-030-staff-engineer-r3.md
T-030-staff-engineer.md
T-031-staff-engineer-r2.md
T-031-staff-engineer.md
T-032-staff-engineer-r2.md
T-032-staff-engineer.md
T-033-staff-engineer-r2.md
T-033-staff-engineer.md
T-034-security-r2.md
T-034-security.md
T-035-staff-engineer-r2.md
T-035-staff-engineer.md
T-036-claims-adjuster.md
T-038-staff-engineer.md
T-039-staff-engineer-r2.md
T-039-staff-engineer.md
T-041-paralegal-r2.md
T-041-paralegal.md
T-042-ux-designer-r2.md
T-042-ux-designer.md
T-043-paralegal.md
T-047-ux-designer.md
T-048-staff-engineer.md
T-049-ux-designer.md
---
# T-036 LLM flag passes — claims-adjuster review (Gary Pruitt)

Verdict: **fail** (1 blocker, 3 major, 2 minor, 1 nit).

On the sample the lexicon floor does surface every flag I would use: 73-day gap, accident-date conflict (one flag, both sides shown, no choice made, no delay figure), prior LBP 2023 (rec 3), "may represent degenerative" (rec 8, as both `degenerative_language` and `speculative_language`), missed appointments (rec 6), new onset (rec 7), wrong intake date (rec 7, separate flag), and patient-states causation (rec 9, `patient_report`). K1–K5 + P1/P2 match one-to-one. Case_07 record 2's prior-ACL flag survives an obedient model and the full pipeline run. Judge #3/#4 error, unsure and disagree all land in `needs_review`. The 12-visits-vs-discharge conflict (C2) exists only if the model supplies it.

What I could attack:
- **The `objective_negative` title.** Its user-visible title is "No objective findings noted", which is false for a sentence like "Cervical ROM full, no spasm noted."
- **C2 can vanish silently.** If the conflict pass fails or returns an unexpected shape, C2 disappears and the run reports `status done` with no error or warning.
- **The suite is red.** `tests/unit/test_pipeline.py` has 3 failures that the handoff did not mention.
- **K5 is labelled "Patient self-report".** Nothing in record 7 says the patient wrote the intake form.

AC6 and AC8 are open on the board (`done: false`), deferred by the backend. I did not rate them.

```json
{"card": "T-036", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "app/backend/flags.py, lexicon_scan.py, flag_templates.py, judges.py, pipeline.py (flag/conflict stages), app/llm/prompts/flags_v1.md, tests/unit/test_flags_sample.py, test_flags_injection.py, test_flags_pass.py, test_pipeline.py; card commit 199785f; sample case + case_06/07/08 golden; no live app (fixture/scripted LLM only)",
 "exercised": [
  "python3 tools/board.py show T-036",
  ".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_schemas.py -q -> 50 passed",
  ".venv/bin/python -m pytest tests/unit -q -> 3 failed, 694 passed (FAILED tests/unit/test_pipeline.py::test_j3_error_or_unsure_makes_llm_conflicts_needs_review[j30], [j31], test_j3_conflict_verdict_keeps_semantic_conflict_and_code_conflict_is_unaffected)",
  ".venv/bin/python -m pytest tests/unit/test_flags_pass.py tests/unit/test_conflicts.py tests/unit/test_judges.py -q -> 40 passed",
  "artifacts/review-evidence/T-036-adjuster-probe.py on sample, case_06, case_07, case_08: per-record flags with the model returning nothing (outputs in T-036-sample-probe.txt, T-036-cases-probe.txt)",
  "artifacts/review-evidence/T-036-adjuster-probe2.py: J4 agree/disagree/unsure/error; LLM_ONLY; off-list category, prose field, non-verbatim quote, wrong type/category; conflict pass + J3 variants (T-036-probe2.txt)",
  "artifacts/review-evidence/T-036-probe3.py: full pipeline on sample with the conflict stage LLMFailed / FixtureMiss / plan-vs-actual scripted (T-036-probe3.txt)",
  "full pipeline on case_07 with an obedient model (T-036-case07-pipeline.txt): f_r2_1 prior_surgery 'History: prior ACL repair of the same knee in 2019.' present",
  "ad hoc lexicon probes for objective_negative / scene_facts / litigation_referral wording",
  "read flags.py, flag_templates.py, lexicon.yaml entries intake_form_accident_date and plan_not_completed, grounding.has_self_report, frontend/flags.js:63 and timeline.js tray, pipeline.py:255-295"
 ],
 "verdict": "fail",
 "scores": {"surfaces_every_attack_item_on_sample": 4, "no_invented_or_overstated_text": 2, "one_to_one_K1_K5": 5, "injection_isolation": 5, "judge_failure_handling": 4, "code_only_flag_text": 3, "test_honesty": 2},
 "findings": [
  {"severity": "blocker",
   "title": "objective_negative flags display the title 'No objective findings noted' - the word 'objective' is user-visible and false for the sentence it quotes",
   "evidence": "flag_templates.py:132 `\"objective_negative\": lambda v: (\"No objective findings noted\", ...)`. Probe: lexicon_flags on 'Cervical ROM full, no spasm noted.' -> category objective_negative, title 'No objective findings noted', explanation 'Wording about absent or normal findings in Dr X (March 1, 2026): “Cervical ROM full, no spasm noted.”.' Also 'No objective findings. Pain 4/10.' -> same title. The T-036 card note (2026-11-02T01:44:48Z) says: 'category objective_negative is internal; UI/flag templates must never display it as objective.' The handoff confirms: \"titles say 'No objective findings noted'\". The guarding test (test_flags_pass.py:80-83) only asserts the string 'objective_negative' is absent, and runs on record 2, which has no hit, so it passes vacuously.",
   "why_it_matters": "The tool states, in its own voice, that no objective findings were noted, when the quoted record documents an objective finding (full ROM, no spasm). Cervical ROM is a measured finding. That is an invented, overstated finding and my own 'subjective-only / objective findings' label supplied by the tool (checklist 9, 18). It breaks the orchestrator's explicit constraint.",
   "fix": "Retitle with neutral wording that quotes the record and uses no 'objective' or 'subjective' vocabulary, e.g. title 'Normal or absent findings wording', explanation 'Wording about normal or absent findings in <provider> (<date>): “<quote>”.' Keep the category key internal.",
   "acceptance_test": "Unit test that renders every category in flag_templates.TEMPLATES and, for every golden case and for lexicon hits on 'Cervical ROM full, no spasm noted.' and 'No objective findings.', asserts re.search(r'objective|subjective', title + explanation, re.I) is None."},
  {"severity": "major",
   "title": "C2 (12 planned visits vs discharge at visit 9) disappears silently when the conflict pass fails or returns an unexpected shape; run still says status done",
   "evidence": "flags.py:189-192 `except P.FixtureMiss: return []` and `except (AU.LLMFailed, ValidationError, TypeError, ValueError): return []`. Probe3 (pipeline on sample, conflicts=LLMFailed): `status done errors [] warnings []`, flags = gap, accident-date conflict, 7 lexicon flags, no f_cx*; identical for FixtureMiss. Same with the old record_id-shaped output in test_pipeline.py:168-169 -> run_conflict_pass(...) == []. The lexicon entry plan_not_completed ('Plan of care: 12 visits.') is strength low and produces no flag (probe: rec 4 -> no flags). The per-record pass degrades visibly (lexicon floor + LLM_FAILED_AFTER_RETRIES); the conflict pass has no floor and no marker.",
   "why_it_matters": "R-FL-2(b) is a sample 'must raise'. An outage is indistinguishable from 'no conflict found'. The attorney never sees that the plan-vs-actual comparison did not run, so a weakness I would attack is hidden without any signal.",
   "fix": "When the conflict pass errors, misses the fixture or fails schema, emit a visible needs_review item (a record_warning or conflict-group notice drawn from a code template) and a pipeline warning. Do not return an empty list silently. Optionally add a code floor for plan-count vs discharge.",
   "acceptance_test": "Pipeline test: conflicts=LLMFailed / FixtureMiss / schema-invalid -> out['warnings'] or a flag with a LLM_FAILED_AFTER_RETRIES-style reason is present; the result is not status done with zero signal."},
  {"severity": "major",
   "title": "Full unit suite is red: 3 test_pipeline.py failures that the handoff did not report; they are the only pipeline-level tests of AC5/AC9 judge #3 behaviour",
   "evidence": ".venv/bin/python -m pytest tests/unit -q -> `3 failed, 694 passed`; FAILED tests/unit/test_pipeline.py::test_j3_error_or_unsure_makes_llm_conflicts_needs_review[j30], [j31], test_j3_conflict_verdict_keeps_semantic_conflict_and_code_conflict_is_unaffected, each `assert ([])`. Cause: SEM fixture (test_pipeline.py:168-169) emits conflict flags with an extra `record_id` field and a single `excerpt`, which the new FlagPass schema rejects, so run_conflict_pass returns []. Handoff says 'Verified: 59 flag/boundary tests pass.' AC9 evidence cites judges.py paths, not this test.",
   "why_it_matters": "The J3 error and unsure handling is the AC the brief asks me to check, and its end-to-end test is failing. 'Done' evidence rests on unit-level tests alone. The failure is also swallowed with no signal (see the previous finding).",
   "fix": "Update the SEM fixture to the new two-quote shape (excerpt + excerpt_b), or make the pipeline contract explicit; run the full tests/unit before handoff.",
   "acceptance_test": ".venv/bin/python -m pytest tests/unit -q reports 0 failed, including the three test_pipeline.py J3 tests."},
  {"severity": "major",
   "title": "K5 (intake-form accident date) is labelled source_kind patient_report ('Patient self-report' chip), but record 7 does not say the patient supplied the intake form",
   "evidence": "Pipeline sample run: flag f_r7_1 (accident_date_provenance) `source_kind == 'patient_report'`; frontend/flags.js:63 renders chip 'Patient self-report' whenever source_kind is patient_report and the title is not 'Patient self-report'. Cause: lexicon.yaml `intake_form_accident_date` has `self_report: true`; grounding.has_self_report('Date of accident per EMS report.') also returns True. Record 7 text: 'Date of accident per intake form: 2026-01-19.' - no author stated. Golden K5 carries no source_kind.",
   "why_it_matters": "R-FL-7 reserves the label for wording that rests on the patient's own statement. Attributing an unattributed intake line to the patient is a fact the record does not state (checklist 10, 19). A chip on an EMS-sourced date would be plainly wrong.",
   "fix": "Set patient_report only on explicit patient-attribution markers (C/O, Patient states/reports, per patient). Remove self_report from intake_form_accident_date, and tighten the generic 'per ...' pattern so it cannot match 'per EMS report'.",
   "acceptance_test": "Unit test: source_kind of the record-7 intake flag == 'record'; of 'Date of accident per EMS report.' == 'record'; of rec 9 and rec 3 flags == 'patient_report'."},
  {"severity": "minor",
   "title": "An LLM conflict with only one quote is accepted and rendered as a two-sided conflict with garbled text",
   "evidence": "Probe: conflicts output {type conflict, category treatment_plan_vs_actual, excerpt 'Plan of care: 12 visits.'} (no excerpt_b) -> title 'Treatment plan and what followed differ', explanation 'Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.”. the record.', state needs_review JUDGE_UNAVAILABLE (J3 skipped at flags.py:238-239).",
   "why_it_matters": "The title asserts a difference but cites one side; it reads as an unfinished sentence ('the record.'), and no judge checked it.",
   "fix": "Require excerpt_b for conflict flags (reject as SCHEMA_INVALID otherwise), or render a single-quote variant that does not claim a difference.",
   "acceptance_test": "Test: conflict without excerpt_b is rejected or renders no 'differ' title and no 'the record.' fragment."},
  {"severity": "minor",
   "title": "Two code templates characterise causation instead of only quoting",
   "evidence": "flag_templates.py:125 'Wording that could be used to question causation in ...' (speculative_language); flag_templates.py:130 'Wording suggesting another cause in ...' (alternative_cause), shown on case_06 rec 2 'Has been seeing a chiropractor off and on since a lifting injury several years ago.'",
   "why_it_matters": "R-FL-4: 'The tool quotes the wording; it never rules on causation.' A template that predicts how the quote will be used, or says it suggests another cause, is the tool arguing my side. It also differs from the neutral 'Mention of a prior or pre-existing condition' style.",
   "fix": "Use neutral labels such as 'Hedged wording in <provider> (<date>): “...”' and 'Mention of another injury or event in ...'.",
   "acceptance_test": "Templates test forbids 'question', 'suggest', 'could be used' and 'cause' in title + explanation."},
  {"severity": "nit",
   "title": "Double terminal punctuation in every template explanation",
   "evidence": "'... mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.”.' (probe output, rec 3)",
   "why_it_matters": "A quote that already ends in a period is followed by a second one; it looks careless in a document that goes to counsel.",
   "fix": "Strip the trailing period inside the quote or omit the template period after a closing quote.",
   "acceptance_test": "Rendered explanations contain no '.”.' sequence."}
 ],
 "whats_right": [
  "Per-record isolation holds: 9 calls, one nonce block each, and case_07's prior-ACL flag survives an obedient model both at unit level and in the full pipeline.",
  "Flag text is code-only: an extra prose field in model output voids the model pass and leaves the lexicon flags, a non-verbatim quote is rejected, and an off-list category (accident_dates_differ, failure_to_mitigate) never reaches a title.",
  "J4/J3 disagree, unsure and error each yield needs_review (JUDGE_DISAGREES / JUDGE_UNSURE / JUDGE_UNAVAILABLE), and LEXICON_ONLY / LLM_ONLY are set correctly."
 ],
 "questions_for_chris": [
  "Should an LLM-unavailable conflict stage block the review (status not done) or only warn? I rated a silent pass as the problem either way."
 ]}
```
--- git
cd4bc60 fix(backend): neutral flag templates, visible conflict-pass failure, patient_report only on explicit attribution (T-036 r2)
8ec833f fix(harness): subagents may not stash or restore board/memory; D-027..D-029
6252c0a test: judge outputs carry reason_code per D-028 (fakes, judges, schemas, pipeline, review rules)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:07.553Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2; echo \"exit=${PIPESTATUS[0]}\"; echo \"---\"; git show --stat cd4bc60 | head -40",
 "description": "Run the three named test files and show round-2 commit stats"
}
````

### User / tool · 2026-11-02T02:01:08.174Z

**tool result**
````
................................................                         [100%]
48 passed in 0.27s
exit=0
---
commit cd4bc606c899bb291d41f38a1c42061a6024cfea
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:00:49 2026 -0600

    fix(backend): neutral flag templates, visible conflict-pass failure, patient_report only on explicit attribution (T-036 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/flag_templates.py | 10 ++++++----
 app/backend/flags.py          | 17 ++++++++++++++---
 app/backend/grounding.py      |  7 ++++---
 memory/contracts/api.md       |  2 +-
 tests/unit/test_flags_pass.py | 31 +++++++++++++++++++++++++++++--
 5 files changed, 54 insertions(+), 13 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:08.254Z

**tool call — Bash**
````
{
 "command": "ls tests/unit/ | grep -i \"flag\\|pipeline\\|conflict\" ; echo \"---lexicon self_report\"; grep -rn \"self_report\" app/ | head -20; echo \"---has_self_report\"; grep -n \"def has_self_report\" -A12 app/backend/grounding.py",
 "description": "List related test files and trace self-report attribution"
}
````

### User / tool · 2026-11-02T02:01:08.348Z

**tool result**
````
test_conflicts.py
test_flag_templates.py
test_flags_injection.py
test_flags_pass.py
test_flags_sample.py
test_pipeline.py
---lexicon self_report
app/README-arch.md:78:`app/llm/lexicon.yaml` v2 (researcher): `flag_type`, `hedge`, `self_report`, `strength`, plus the `accident_date_phrases`, `non_encounter` and `injection` categories. It blocks the gap rule, the accident-date rule and the injection scan, and its golden self-check (recall per `must` flag) gates the claim that the lexicon is a floor (ADR-008.4).
app/llm/lexicon.yaml:25:#   from an excerpt (ADR-016). `self_report: true` marks patient-attributed wording; code sets
app/llm/lexicon.yaml:93:  self_report: false
app/llm/lexicon.yaml:114:  self_report: false
app/llm/lexicon.yaml:131:  self_report: false
app/llm/lexicon.yaml:148:  self_report: false
app/llm/lexicon.yaml:164:  self_report: false
app/llm/lexicon.yaml:180:  self_report: false
app/llm/lexicon.yaml:196:  self_report: false
app/llm/lexicon.yaml:213:  self_report: false
app/llm/lexicon.yaml:231:  self_report: false
app/llm/lexicon.yaml:249:  self_report: false
app/llm/lexicon.yaml:266:  self_report: false
app/llm/lexicon.yaml:283:  self_report: false
app/llm/lexicon.yaml:299:  self_report: false
app/llm/lexicon.yaml:315:  self_report: false
app/llm/lexicon.yaml:331:  self_report: false
app/llm/lexicon.yaml:348:  self_report: false
app/llm/lexicon.yaml:366:  self_report: false
app/llm/lexicon.yaml:382:  self_report: false
---has_self_report
206:def has_self_report(text: str) -> bool:
207-    """True when the text carries a patient-attributed marker (source_kind = patient_report, ADR-013)."""
208-    return _self_report(text)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:09.919Z

**tool call — Bash**
````
{
 "command": "git show cd4bc60 -- app/backend/flag_templates.py app/backend/flags.py app/backend/grounding.py | head -150; echo \"--- _self_report\"; grep -n \"_self_report\" -A10 app/backend/grounding.py | head -40; echo \"--- intake lexicon\"; grep -n \"intake_form_accident_date\" -B2 -A10 app/llm/lexicon.yaml",
 "description": "Show round-2 diff and self-report pattern and intake lexicon entry"
}
````

### User / tool · 2026-11-02T02:01:10.041Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:23.960Z

**tool call — Bash**
````
{
 "command": "grep -rn \"pipeline_warning\\|CONFLICT_PASS_INCOMPLETE\\|LLM_FAILED_AFTER_RETRIES\\|FIXTURE_MISS\" app/ tests/ frontend/ 2>/dev/null | grep -v \"\\.pyc\" | head -30; echo \"--- source_kind users\"; grep -rn \"source_kind\\|self_report\\\"\\]\" app/backend/*.py | head -30",
 "description": "Trace pipeline_warning and source_kind consumers"
}
````

### User / tool · 2026-11-02T02:01:24.065Z

**tool result**
````
app/llm/_types.py:15:        super().__init__(f"FIXTURE_MISS {prompt_hash}")
app/llm/audited.py:28:    code = "LLM_FAILED_AFTER_RETRIES"
app/llm/audited.py:32:    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""
app/llm/audited.py:69:            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
app/backend/why.py:16:    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
app/backend/why.py:28:    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
app/backend/confidence.py:9:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:11:    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES",
app/backend/confidence.py:63:    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"),
app/backend/confidence.py:64:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
app/backend/flags.py:183:    pipeline adds a run warning (`pipeline_warning`) so the run is shown as partial."""
app/backend/flags.py:188:            "excerpt": "", "source_kind": "record", "evidence": [], "pipeline_warning": "CONFLICT_PASS_INCOMPLETE",
app/backend/flags.py:201:        return [_incomplete(records, "FIXTURE_MISS")]
app/backend/flags.py:203:        return [_incomplete(records, "LLM_FAILED_AFTER_RETRIES")]
app/backend/generator.py:51:        return {"failure": "FIXTURE_MISS", "record_no": record["n"]}
app/backend/generator.py:53:        return {"failure": "LLM_FAILED_AFTER_RETRIES", "record_no": record["n"]}
app/backend/generator.py:124:    tray only (R-TL-2). `failures` = [{'record_no', 'failure'}] for records with no output (LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS)."""
app/backend/pipeline.py:238:            errors.append(_err("LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"], "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
tests/unit/test_audited.py:47:    """ADR-003.7 / LLM_FAILED_AFTER_RETRIES: exactly 3 attempts, then a visible failure; no fourth call."""
tests/unit/test_audited.py:52:    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 3 and rows(conn, cid) == 3
tests/unit/test_audited.py:62:    """T-034 AC8 / T-037 AC7 / FIXTURE_MISS: a miss is final (one attempt, one row); the wrapper turns it into LLMFailed(LLM_FAILED_AFTER_RETRIES) and the row logs the prompt hash."""
tests/unit/test_audited.py:67:    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 1
tests/unit/test_generator.py:74:    """LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS: no entry is invented; the failure is listed."""
tests/unit/test_generator.py:76:    assert ents == [] and not rej and {f["failure"] for f in fails} == {"LLM_FAILED_AFTER_RETRIES"} and len(fails) == 9
tests/unit/test_generator.py:78:    assert ents == [] and {f["failure"] for f in fails} == {"FIXTURE_MISS"}
tests/unit/test_generator.py:113:    """ADR-005: judge call failure -> JUDGE_UNAVAILABLE; fixture miss -> FIXTURE_MISS; never verified."""
tests/unit/test_generator.py:119:    assert all("FIXTURE_MISS" in e["reasons"] and e["state"] == "needs_review" for e in ents)
tests/unit/test_t037_backend.py:33:    """T-037 AC2/AC7: replaying every golden input on the fixture backend reports 0 FixtureMiss (no error, no FIXTURE_MISS reason)."""
tests/unit/test_t037_backend.py:38:    assert not [i for i in items if "FIXTURE_MISS" in i.get("reasons", [])], case
tests/unit/test_provider_backends.py:134:    """T-034 AC8: miss -> LLM_FAILED_AFTER_RETRIES (still a FixtureMiss), one attempt, no default answer."""
--- source_kind users
app/backend/generator.py:61:        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
app/backend/generator.py:80:             source_kind="patient_report" if grounding.has_self_report(excerpt) else "record")
app/backend/grounding.py:207:    """True when the text carries a patient-attributed marker (source_kind = patient_report, ADR-013)."""
app/backend/flags.py:42:         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
app/backend/flags.py:150:            "source_kind": "record",
app/backend/flags.py:188:            "excerpt": "", "source_kind": "record", "evidence": [], "pipeline_warning": "CONFLICT_PASS_INCOMPLETE",
app/backend/flags.py:221:             "record_no": ref["n"], "record_id": ref.get("id", f"r{ref['n']}"), "review_status": "pending", "source_kind": "record",
app/backend/present.py:44:            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed, "source_kind":
app/backend/present.py:74:    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
app/backend/review.py:186:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
app/backend/pipeline.py:64:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:78:                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:123:    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:24.839Z

**tool call — Bash**
````
{
 "command": "grep -n \"run_conflict_pass\\|run_flag_pass\\|ground(\\|status\\|warnings\\|errors\" app/backend/pipeline.py | head -60; echo \"--- why codes\"; grep -n \"FIXTURE_MISS\\|LLM_FAILED\\|CONFLICT\\|analysis\" app/backend/why.py app/backend/confidence.py 2>/dev/null | head -20",
 "description": "Inspect pipeline conflict-stage wiring and why codes"
}
````

### User / tool · 2026-11-02T02:01:24.931Z

**tool result**
````
5:Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
6:No code path here sets review_status: every item leaves a run `pending`. A model failure loses only that item and is reported in `errors`.
40:    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
42:        ctx["date_status"] = "ambiguous"
64:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
72:    for w in ing["record_warnings"]:
75:        state, why_codes = confidence.compose_state({"code_reasons": []}, {"injection": inj, "date_status": None if inj else "ambiguous"})
78:                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
87:                "excerpt": body, "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
89:    warnings = list(ing["warnings"])
92:            warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
95:            "dates_to_confirm": ing["dates_to_confirm"], "flags": flags, "amounts": amounts, "damages": damages, "warnings": warnings,
106:                      source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
129:    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
130:    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
140:        if kind == "flag" and old["review_status"] != "pending":
145:                it["review_status"] = old["review_status"]
146:        elif old["review_status"] != "pending":
147:            it["review_status"] = old["review_status"]
150:        if oid not in keep and old["review_status"] == "pending":
151:            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
205:    errors, stage_done = [], []
210:        DB.update_case(conn, cid, status="running", stage=name)
215:    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
220:    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
223:    status = "done"
238:            errors.append(_err("LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"], "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
259:        pair = FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
268:            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
283:        f.setdefault("review_status", "pending")
301:        status = "timeout"
304:        status = "done_with_errors" if errors else "done"
306:    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
308:    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
310:    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
311:            "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
333:            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
334:            "dates_to_confirm": out["dates_to_confirm"], "status": out["status"], "errors": out["errors"],
398:    L = [f"Status: {out['status']}   backend: {P.backend_name()}   records: {len(out['records'])}   entries: {len(out['entries'])}"
412:    if out["errors"]:
413:        L += ["", "ERRORS"] + [f"  {e['code']} at {e['stage']}" + (f" record {e['record_no']}" if "record_no" in e else "") for e in out["errors"]]
437:    return 0 if out["status"] in ("done", "done_with_errors") else 1
--- why codes
app/backend/confidence.py:9:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:11:    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES",
app/backend/confidence.py:63:    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"),
app/backend/confidence.py:64:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
app/backend/why.py:16:    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
app/backend/why.py:28:    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:25.462Z

**tool call — Bash**
````
{
 "command": "git show cd4bc60 -- tests/unit/test_flags_pass.py; echo \"--- test_pipeline J3 fixture\"; sed -n 155,200p tests/unit/test_pipeline.py",
 "description": "Show round-2 test diff and J3 pipeline fixture"
}
````

### User / tool · 2026-11-02T02:01:25.562Z

**tool result**
````
commit cd4bc606c899bb291d41f38a1c42061a6024cfea
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:00:49 2026 -0600

    fix(backend): neutral flag templates, visible conflict-pass failure, patient_report only on explicit attribution (T-036 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_flags_pass.py b/tests/unit/test_flags_pass.py
index 7ff4e9a..1f7d955 100644
--- a/tests/unit/test_flags_pass.py
+++ b/tests/unit/test_flags_pass.py
@@ -67,8 +67,35 @@ def test_conflict_pass_grounds_both_quotes_and_j3_decides():
     bad = F.run_conflict_pass(recs, call=FakeCall({"conflicts": {"flags": [dict(flag, excerpt_b="Invented sentence.")]}}))
     assert bad[0]["state"] == "rejected"
 
-def test_conflict_pass_failure_returns_no_flags_not_an_error():
-    assert F.run_conflict_pass([rec(1)], call=FakeCall({"conflicts": AU.LLMFailed("x")})) == []
+def test_conflict_pass_failure_is_visible_not_silent():
+    """Review T-036: a failed or missed conflict pass yields a needs_review record_warning and a pipeline warning, never an empty list."""
+    for exc, code in ((AU.LLMFailed("x"), "LLM_FAILED_AFTER_RETRIES"), (P.FixtureMiss("x"), "FIXTURE_MISS")):
+        out = F.run_conflict_pass([rec(1)], call=FakeCall({"conflicts": exc}))
+        assert len(out) == 1 and out[0]["type"] == "record_warning" and out[0]["state"] == "needs_review"
+        assert code in out[0]["reasons"] and out[0]["pipeline_warning"] == "CONFLICT_PASS_INCOMPLETE" and out[0]["title"] and out[0]["explanation"]
+    bad = F.run_conflict_pass([rec(1)], call=FakeCall({"conflicts": {"flags": "not a list"}}))
+    assert bad and bad[0]["pipeline_warning"] == "CONFLICT_PASS_INCOMPLETE"
+
+def test_single_quote_conflict_is_rejected():
+    """Review T-036 minor: a conflict needs two quotes."""
+    recs = [rec(n) for n in range(1, 10)]
+    out = F.run_conflict_pass(recs, call=FakeCall({"conflicts": {"flags": [dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.")]}}))
+    assert out[0]["state"] == "rejected" and "SCHEMA_INVALID" in out[0]["reasons"]
+
+def test_templates_quote_the_record_and_never_say_objective():
+    """Review T-036 blocker: no flag title/explanation uses 'objective'; neutral wording for hedges and other-cause mentions."""
+    from app.backend import flag_templates as FT
+    for cat in FT.TYPE_OF:
+        if FT.TYPE_OF[cat] in ("pre_existing", "causation"):
+            t, e = FT.render(FT.TYPE_OF[cat], cat, provider="P", date="2026-01-02", quote="Cervical ROM full, no spasm noted.")
+            assert "objective" not in (t + e).lower()
+            assert "could be used" not in e and "suggesting another cause" not in e
+
+def test_intake_form_date_is_not_patient_self_report():
+    """Review T-036 major: only explicit patient attribution sets patient_report."""
+    fl = F.lexicon_flags(rec(7))
+    assert fl and all(f["source_kind"] == "record" for f in fl)
+    assert any(f["source_kind"] == "patient_report" for f in F.lexicon_flags(rec(9)))
 
 def test_no_flag_is_ever_accepted_and_patient_report_is_set_by_code():
     """R-FL-7 / invariant: every flag starts pending; record 9's flag is patient_report from the lexicon, not the model."""
--- test_pipeline J3 fixture
@pytest.mark.parametrize("j2,reason", [(AU.LLMFailed("down"), "JUDGE_UNAVAILABLE"), ({"verdict": "unsure", "reason_code": "NONE"}, "JUDGE_UNSURE")])
def test_j2_error_or_unsure_never_verifies_a_charge(tmp_path, j2, reason):
    """T-035 AC4 / T-036 AC9: a charge is verified only on 'agree'; judge 2 error -> JUDGE_UNAVAILABLE, unsure -> JUDGE_UNSURE; both needs_review."""
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(j2=j2)))
    for raw in ("$6,240", "$2,150"):
        a = by_raw(out)[raw]
        assert a["cls"] == "charge" and a["state"] == "needs_review" and reason in a["reasons"]

def test_j2_agree_verifies_charges_and_rate_stays_needs_review(tmp_path):
    """R-CH-2: with judge 2 agreeing, charges are verified; the $185 rate still carries AMOUNT_RATE_NOT_TOTALED."""
    out, _ = run_sample(tmp_path)
    assert by_raw(out)["$6,240"]["state"] == "verified" and "AMOUNT_RATE_NOT_TOTALED" in by_raw(out)["$185"]["reasons"]

SEM = [dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.",
            excerpt_b="Discharged from PT after two missed appointments.")]

@pytest.mark.parametrize("j3", [AU.LLMFailed("down"), {"verdict": "unsure", "reason_code": "NONE"}])
def test_j3_error_or_unsure_makes_llm_conflicts_needs_review(tmp_path, j3):
    """T-036 AC5/AC9: a semantic (LLM) conflict flag whose judge 3 failed or was unsure is needs_review (JUDGE_UNAVAILABLE / JUDGE_UNSURE), never verified."""
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(conflicts={"flags": SEM}, j3=j3)))
    llm = [f for f in out["flags"] if f["type"] == "conflict" and f.get("origin") != "code"]
    assert llm and all(f["state"] == "needs_review" and ({"JUDGE_UNAVAILABLE", "JUDGE_UNSURE"} & set(f["reasons"])) for f in llm)

def test_j3_conflict_verdict_keeps_semantic_conflict_and_code_conflict_is_unaffected(tmp_path):
    """T-036 AC2 (b): the 12-visit plan vs discharge-at-visit-9 conflict is raised from the LLM pass (judge 3 'conflict'); the accident-date conflict stays a single code flag."""
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(conflicts={"flags": SEM})))
    sem = [f for f in out["flags"] if f["type"] == "conflict" and f.get("category") == "treatment_plan_vs_actual"]
    assert sem and all(f["origin"] != "code" for f in sem)
    assert len([f for f in out["flags"] if f["type"] == "conflict" and f.get("subtype") == "accident_date"]) == 1   # D-025 / T-036 AC7

K_PRE = dict(type="pre_existing", category="pre_existing", excerpt="Patient reports low back pain in 2023, resolved.")

@pytest.mark.parametrize("j4,reason", [(AU.LLMFailed("down"), "JUDGE_UNAVAILABLE"), ({"verdict": "unsure", "reason_code": "NONE"}, "JUDGE_UNSURE"), ({"verdict": "disagree", "reason_code": "NONE"}, "JUDGE_DISAGREES")])
def test_j4_error_unsure_or_disagree_makes_flag_needs_review(tmp_path, j4, reason):
    """T-036 AC5/AC9: a model flag on record 3 whose judge 4 failed, was unsure or disagreed is needs_review with that reason."""
    def flags(user):
        return {"flags": [K_PRE]} if which_record(user) == [3] else {"flags": []}
    out, _ = run_sample(tmp_path, call=FakeCall(sample_script(flags=flags, j4=j4)))
    f3 = [f for f in out["flags"] if f["type"] == "pre_existing" and "low back pain in 2023" in f["excerpt"]]
    assert f3 and all(f["state"] == "needs_review" and reason in f["reasons"] for f in f3)

# ---- ladder and review state (T-037 AC5, R-CO-2, R-RV-6, row 20) ----
def test_ladder_and_pending(run):
    """T-037 AC5: every entry, amount and flag has a ladder record naming its backend, and nothing is accepted, edited or dismissed by a run."""
    out, _ = run
    items = out["entries"] + out["amounts"] + out["flags"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:29.672Z

**tool call — Bash**
````
{
 "command": "sed -n 250,300p app/backend/pipeline.py; echo \"--- pipeline tests\"; .venv/bin/python -m pytest tests/unit/test_pipeline.py tests/unit/test_flags_pass.py tests/unit/test_conflicts.py -q 2>&1 | tail -15",
 "description": "Read pipeline conflict wiring and run pipeline/flag-pass tests"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:30.127Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -6",
 "description": "Run full unit suite for baseline"
}
````

### User / tool · 2026-11-02T02:01:31.435Z

**tool result**
````
        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
                                        call=call, case_text=text)
        final_amounts = [_finish_amount(a, ing, verdicts.get(a["id"])) for a in dollars] + [_finish_amount(a, ing, None) for a in ing["damages"]]
    for a in final_amounts:
        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
    # 5: semantic conflicts (LLM) + J3
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"]]
    if guard("conflicts"):
        pair = FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
        for i, f in enumerate(pair, 1):
            f["id"] = f"f_cx{i}"
        llm_flags += FL.judge_flags(pair, call=call, case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
            for k, f in enumerate(fs, 1):
                f["id"] = f"f_r{r['n']}_{k}"
            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
    # 7: finalize
    set_stage("finalize")
    for f in llm_flags:
        f.setdefault("record_nos", [f["record_no"]])
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
        f.setdefault("review_status", "pending")
        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
        f.pop("record_no", None)
    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
    entries = [_clean(e) for e in entries]
    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
    undated = [e for e in entries if not dated_cut(e)]
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    now_t = clock()
    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
    _persist(conn, cid, "amount", final_amounts, now_t)
    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
    if timed_out:
--- pipeline tests
.............................................                            [100%]
45 passed in 1.37s
````

### User / tool · 2026-11-02T02:01:42.189Z

**tool result**
````
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_02_gap_boundaries]
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_08_diagnosis_temptation]
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_09_nonvisit_hides_gap]
FAILED tests/unit/test_t037_backend.py::test_judge_lines_replay - AssertionEr...
FAILED tests/unit/test_t037_backend.py::test_fixtures_come_only_from_golden_text
5 failed, 750 passed in 10.12s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:47.241Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_t037_backend.py -q 2>&1 | grep -E \"Error|assert|FAILED|^E \" | head -30; echo \"--- _clean\"; grep -n \"def _clean\" -A6 app/backend/pipeline.py; echo \"--- judge_flags\"; grep -n \"def judge_flags\" -A25 app/backend/flags.py | head -45",
 "description": "Inspect T-037 failure messages and clean/judge helpers"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:47.819Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ | grep -i \"T-036\" ; echo \"---\"; sed -n 1,60p artifacts/review-evidence/T-036-probe3.py",
 "description": "Locate round-1 probe scripts and read probe3"
}
````

### User / tool · 2026-11-02T02:01:48.854Z

**tool result**
````
>       assert view["errors"] == [] and view["status"] == "done"
E       AssertionError: assert ([{'code': 'LL...IXTURE_MISS'}] == []
E         
E         Left contains one more item: {'code': 'LLM_FAILED_AFTER_RETRIES', 'stage': 'extract', 'record_no': 1, 'cause': 'FIXTURE_MISS'}
E         Use -v to get more diff)
tests/unit/test_t037_backend.py:36: AssertionError
        assert view["errors"] == [] and view["status"] == "done"
>       assert not [i for i in items if "FIXTURE_MISS" in i.get("reasons", [])], case
E       AssertionError: case_08_diagnosis_temptation
E       assert not [{'type': 'causation', 'category': 'speculative_language', 'excerpt': 'Clinical correlation recommended.', 'origin': 'lexicon', ...}]
tests/unit/test_t037_backend.py:38: AssertionError
>       assert view["errors"] == [] and view["status"] == "done"
E       AssertionError: assert ([{'code': 'LL...IXTURE_MISS'}] == []
E         
E         Left contains 5 more items, first extra item: {'code': 'LLM_FAILED_AFTER_RETRIES', 'stage': 'extract', 'record_no': 1, 'cause': 'FIXTURE_MISS'}
E         Use -v to get more diff)
tests/unit/test_t037_backend.py:36: AssertionError
>                   assert PL.judge_summary(it["candidate_summary"], excerpt, label, "fixture") != "unavailable", it["id"]
E                   AssertionError: H01
E                   assert 'unavailable' != 'unavailable'
E                    +  where 'unavailable' = <function judge_summary at 0x108f62d40>('MRI showed a C5-C6 disc herniation caused by the collision.', 'C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.', 'Austin Imaging, cervical MRI', 'fixture')
E                    +    where <function judge_summary at 0x108f62d40> = PL.judge_summary
tests/unit/test_t037_backend.py:52: AssertionError
            assert d["recorded_from"]["backend"] and "output" in d
>       with pytest.raises(ValueError, match="not in evals/golden"):
E       AssertionError: Regex pattern did not match.
E         Expected regex: 'not in evals/golden'
E         Actual message: 'text is not an evals/golden input; refusing to record'
tests/unit/test_t037_backend.py:62: AssertionError
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_02_gap_boundaries]
--- _clean
25:def _clean(d: dict) -> dict:
26-    """Drop private '_' keys before an item is stored or returned."""
27-    return {k: v for k, v in d.items() if not k.startswith("_")}
28-
29-
30-def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
31-    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
--- judge_flags
239:def judge_flags(flags: list, *, call, case_text: str = "") -> list:
240-    """J4 on every model-involved pre_existing/causation flag; J3 on every model conflict. Lexicon-only flags have no judge.
241-    A disagreement, unsure answer or failed judge call leaves the flag needs_review (JUDGE_DISAGREES / JUDGE_UNSURE / JUDGE_UNAVAILABLE)."""
242-    for i, f in enumerate(flags):
243-        if f["type"] == "record_warning" or f["state"] == "rejected":
244-            continue
245-        item = f.get("id") or f"f{i}"
246-        nonce = promptlib.nonce(case_text, "j3" if f["type"] == "conflict" else "j4", item)
247-        try:
248-            if f["type"] == "conflict":
249-                if not f.get("excerpt_b"):
250-                    continue
251-                v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item)
252-                step, pv = "j3", "judge_conflict_v1"
253-            elif f["origin"] in ("llm", "both"):
254-                v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item_id=item)
255-                step, pv = "j4", "judge_flag_v1"
256-            else:
257-                continue
258-        except P.FixtureMiss:
259-            f["_stage"]["fixture_miss"] = True
260-            v, cid, reason, step, pv = "unavailable", None, "NONE", "j3" if f["type"] == "conflict" else "j4", "judge_conflict_v1"
261-        f["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": pv, "call_id": cid, "verdict": v, "reason_code": reason}
262-        f["_stage"]["judge"] = judges.to_ladder(step, v)
263-        _compose(f)
264-    return flags
````

### User / tool · 2026-11-02T02:01:48.942Z

**tool result**
````
T-036-adjuster-probe.py
T-036-adjuster-probe2.py
T-036-case07-pipeline.txt
T-036-cases-probe.txt
T-036-probe2.txt
T-036-probe3.py
T-036-probe3.txt
T-036-sample-probe.txt
---
import sys, pathlib, tempfile
sys.path.insert(0, "/Users/arsis/zlayt-pm-project")
from app.llm import audited as AU, provider as P
from tests.unit._fakes import run_sample, sample_script, FakeCall
def show(label, script):
    tmp = pathlib.Path(tempfile.mkdtemp(dir="/Users/arsis/zlayt-pm-project/artifacts/review-evidence"))
    call = FakeCall(script)
    try:
        out, _ = run_sample(tmp, call=call)
    except Exception as e:
        print(label, "EXC", type(e).__name__, e); return
    print("=====", label, "status", out.get("status"), "errors", out.get("errors"), "warnings", out.get("warnings"))
    for f in out["flags"]:
        print("  ", f["id"], f["type"], f.get("category"), f["state"], f.get("reasons"), "|", f.get("title"))
    print("   tray:", [(t["id"], t.get("reasons")) for t in out["tray"]])
show("conflicts LLMFailed", sample_script(conflicts=AU.LLMFailed("down")))
show("conflicts FixtureMiss", sample_script(conflicts=P.FixtureMiss("x")))
show("conflicts plan-vs-actual J3 ok", sample_script(conflicts={"flags":[dict(type="conflict",category="treatment_plan_vs_actual",excerpt="Plan of care: 12 visits.",excerpt_b="Discharged from PT after two missed appointments.")]}))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:01.142Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport yaml,re\nd=yaml.safe_load(open(\"app/llm/lexicon.yaml\"))\nents=[]\ndef walk(x):\n    if isinstance(x,dict):\n        if \"id\" in x and \"self_report\" in x: ents.append(x)\n        for v in x.values(): walk(v)\n    elif isinstance(x,list):\n        for v in x: walk(v)\nwalk(d)\nprint(\"entries with self_report key:\",len(ents))\nprint(\"self_report true:\",[ (e[\"id\"], e.get(\"category\")) for e in ents if e.get(\"self_report\")])\nEOF\necho \"---\"; grep -n \"self_report: true\" -B12 app/llm/lexicon.yaml | grep \"id:\" ",
 "description": "List lexicon entries marked self_report true"
}
````

### User / tool · 2026-11-02T02:02:01.323Z

**tool result**
````
entries with self_report key: 70
self_report true: [('self_reported_prior', 'pre_existing'), ('patient_attributes_causation', 'patient_report'), ('patient_reports_generic', 'patient_report'), ('intake_form_accident_date', 'accident_date_provenance')]
---
477-- id: self_reported_prior
727-- id: patient_attributes_causation
743-- id: patient_reports_generic
759-- id: intake_form_accident_date
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:02.006Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_flags_sample.py -q 2>&1 | tail -1; grep -rn \"No objective\\|objective\" frontend/*.js app/backend/*.py 2>/dev/null | grep -v \"^.*#\" | head -20; echo \"--- board\"; .venv/bin/python tools/board.py show T-036 2>&1 | head -60",
 "description": "Check lexicon self-report entries, UI objective wording, board card"
}
````

### User / tool · 2026-11-02T02:02:02.657Z

**tool result**
````
13 passed in 0.24s
app/backend/flag_templates.py:37:    "objective_negative": "causation", "accident_date_provenance": "causation",
app/backend/flag_templates.py:132:    "objective_negative": lambda v: ("Normal or absent findings wording", f"Wording about normal or absent findings in {_at(v)}{_quote(v)}."),
--- board
---
id: "T-036"
title: "LLM flag passes: per-record pre-existing/causation + lexicon floor, conflicts + judges #3/#4"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: ["T-027", "T-033", "T-035", "T-048"]
created_by: "orchestrator"
created_at: "2026-11-02T01:14:10Z"
updated_at: "2026-11-02T02:01:02Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:00:51Z"
rounds: 1
commits: ["199785f", "cd4bc60"]
reviews:
  - {"persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-036-claims-adjuster.md", "at": "2026-11-02T01:59:37Z"}
ac:
  - {"n": 1, "text": "flag output schema has category + excerpt spans only; extra or prose fields rejected (R-FL-8, row 14); proved by test_schemas::test_flag_schema_no_prose", "done": true, "evidence": "tests/unit/test_schemas.py::test_flag_output_has_no_prose_fields, test_flags_pass.py::test_flag_prompt_has_no_model_prose_fields_and_one_block pass"}
  - {"n": 2, "text": "fixture run on the sample raises: conflict (a) accident date and (b) 12-visit plan vs discharge at visit 9, pre_existing on records 3 and 8, causation K1-K5 as distinct flags with one-to-one matching via the check_golden matcher (R-FL-2b, R-FL-3, R-FL-4, rows 11-13); proved by tests/unit/test_flags_sample.py", "done": true, "evidence": "test_flags_sample::test_lexicon_floor_gives_distinct_one_to_one_matches_for_k1_to_k5 (P1,P2,K1-K5 via evals.matching.assign) + test_flags_pass::test_conflict_pass_grounds_both_quotes_and_j3_decides (plan vs discharge); accident-date conflict is code (conflicts.py, T-033); full fixture run waits for T-037"}
  - {"n": 3, "text": "only one of LLM/lexicon fires -> needs_review with LEXICON_ONLY or LLM_ONLY; case_06 28-day near-miss does not flag; case_05 provider-name conflict raised and name variants tolerated (R-FL-3, R-FL-2)", "done": true, "evidence": "test_flags_sample LEXICON_ONLY/LLM_ONLY/both tests pass; case_06 gap and case_05 provider conflict are code (T-033, D-025)"}
  - {"n": 4, "text": "per-record pass: each prompt contains exactly one record nonce block; case_07 record 2 pre_existing flag still raised despite the injected record (R-RV-6, rows 12, 16); proved by test_flags_injection.py", "done": true, "evidence": "test_flags_sample::test_flag_pass_is_one_call_per_record_and_isolated, test_flags_injection.py all pass (prior-ACL flag survives)"}
  - {"n": 5, "text": "judge #3 and #4 must agree or flag is needs_review; evidence that fails grounding -> rejected; source_kind patient_report set by code for record 9 (R-FL-5, R-FL-7, row 13)", "done": true, "evidence": "test_flags_pass: J4 agree/disagree/unsure/unavailable, J3 conflict/benign, ungrounded -> rejected, record 9 patient_report by code"}
  - {"n": 6, "text": "Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.", "done": true, "evidence": "orchestrator-owned: docs/M2M3_COVERAGE.md critical path, M2 cut order + cut trigger; per-card estimates appended to each card body"}
  - {"n": 7, "text": "Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033); the LLM conflict pass covers semantic conflicts only; exactly one accident-date conflict flag on the sample", "done": true, "evidence": "conflicts_v1 prompt excludes accident-date/provider conflicts (code); run_conflict_pass accepts only treatment_plan_vs_actual/other_fact_mismatch"}
  - {"n": 8, "text": "Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.", "done": false, "evidence": null}
  - {"n": 9, "text": "Contract review (T-018): T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a charge is verified only on agrees'. T-036 AC5 append: 'judge #3/#4 error or timeout -> needs_review JUDGE_UNAVAILABLE'.", "done": true, "evidence": "test_flags_pass::test_model_and_lexicon_agree_then_j4_decides: J4 LLMFailed -> JUDGE_UNAVAILABLE; conflict J3 same path via judges"}
  - {"n": 10, "text": "Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033); the LLM conflict pass covers semantic conflicts only; exactly one accident-date conflict flag on the sample", "done": true, "evidence": "same as AC7; one accident-date flag comes from conflicts.accident_date_conflicts (test_conflicts)"}
---
## Description
Hybrid flag engines with the lexicon as the floor, per R-FL-2b, R-FL-3 to R-FL-5, R-FL-7 and R-RV-6. Depends on existing researcher card T-027 (lexicon generalization) for held-out recall; LLM_VS_CODE rows 10 (provider variants), 11, 12, 13, 16.

Plan key: m2-be-llm-flags (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

Estimate: 45 min.

## Notes (append-only, newest last)
- 2026-11-02T01:22:45Z orchestrator: AC 6 added: Contract review (T-018): Rewrite M2M3_COVERAGE.md:3-4 with the 7-card chain and a per-card estimate (put it in each card's Description). Add an 'M2 cut order' that never touches ship-bar items, for example: (1) T-034 AC4 anthropic-api half stays mocked-SDK only, (2) T-031 AC3 24 h lazy purge moves to M4, (3) T-036 AC3 case_05 provider conflict becomes 'reported, not gated', (4) T-036 decouples from T-027 (see next finding). Log each cut in memory/SCOPE_CUTS.md.
- 2026-11-02T01:22:45Z orchestrator: AC 7 added: Contract review (T-018): Either raise T-027 to P0 with a timebox in its Description, or remove T-027 from T-036 depends_on and add a T-036 AC: 'runs against app/llm/lexicon.yaml at HEAD; lexicon recall per must-flag is reported by evals.run (see T-038 finding)'.
- 2026-11-02T01:22:45Z orchestrator: AC 8 added: Contract review (T-018): T-038 new AC: 'latest.json records sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml; `python -m evals.run --check-fresh` exits 1 when any current hash differs'. T-035 AC5 and T-036 AC1: 'handoff links evals/reports/<ts>.md whose prompt hashes equal HEAD (re-run once T-038 lands)'.
- 2026-11-02T01:22:46Z orchestrator: AC 9 added: Contract review (T-018): T-035 AC4 append: 'judge #2 unsure, error or timeout -> needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a charge is verified only on agrees'. T-036 AC5 append: 'judge #3/#4 error or timeout -> needs_review JUDGE_UNAVAILABLE'.
- 2026-11-02T01:22:46Z orchestrator: AC 10 added: Contract review (T-018): Either T-033 gains AC6 'case_05 provider conflict raised by code (normalized-name rule), no LLM call', or an ADR edits row 10 and T-036 AC3 says 'raised by the LLM conflict pass + judge #3'. T-036 AC2 append 'exactly one accident-date conflict flag in pipeline output (from T-033)'.
- 2026-11-02T01:22:47Z orchestrator: updated depends_on=['T-027', 'T-033', 'T-035', 'T-048']
- 2026-11-02T01:32:26Z orchestrator: AC 7 edited: Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033); the LLM conflict pass covers semantic conflicts only; exactly one accident-date conflict flag on the sample
- 2026-11-02T01:32:26Z orchestrator: AC 10 edited: Contract review (T-018), decided by D-025: provider-name conflicts come from code (T-033); the LLM conflict pass covers semantic conflicts only; exactly one accident-date conflict flag on the sample
- 2026-11-02T01:32:27Z orchestrator: updated body appended from artifacts/tmp/est_T-036.md
- 2026-11-02T01:44:48Z orchestrator: From T-027 review minor: category objective_negative is internal; UI/flag templates must never display it as 'objective'.
- 2026-11-02T01:51:01Z orchestrator: assigned: backend-1
- 2026-11-02T01:51:02Z backend: claimed
- 2026-11-02T01:55:45Z backend: AC 1 checked: tests/unit/test_schemas.py::test_flag_output_has_no_prose_fields, test_flags_pass.py::test_flag_prompt_has_no_model_prose_fields_and_one_block pass
- 2026-11-02T01:55:46Z backend: AC 2 checked: test_flags_sample::test_lexicon_floor_gives_distinct_one_to_one_matches_for_k1_to_k5 (P1,P2,K1-K5 via evals.matching.assign) + test_flags_pass::test_conflict_pass_grounds_both_quotes_and_j3_decides (plan vs discharge); accident-date conflict is code (conflicts.py, T-033); full fixture run waits for T-037
- 2026-11-02T01:55:46Z backend: AC 3 checked: test_flags_sample LEXICON_ONLY/LLM_ONLY/both tests pass; case_06 gap and case_05 provider conflict are code (T-033, D-025)
- 2026-11-02T01:55:46Z backend: AC 4 checked: test_flags_sample::test_flag_pass_is_one_call_per_record_and_isolated, test_flags_injection.py all pass (prior-ACL flag survives)
- 2026-11-02T01:55:46Z backend: AC 5 checked: test_flags_pass: J4 agree/disagree/unsure/unavailable, J3 conflict/benign, ungrounded -> rejected, record 9 patient_report by code
- 2026-11-02T01:55:46Z backend: AC 7 checked: conflicts_v1 prompt excludes accident-date/provider conflicts (code); run_conflict_pass accepts only treatment_plan_vs_actual/other_fact_mismatch
- 2026-11-02T01:55:46Z backend: AC 9 checked: test_flags_pass::test_model_and_lexicon_agree_then_j4_decides: J4 LLMFailed -> JUDGE_UNAVAILABLE; conflict J3 same path via judges
- 2026-11-02T01:55:46Z backend: AC 10 checked: same as AC7; one accident-date flag comes from conflicts.accident_date_conflicts (test_conflicts)
- 2026-11-02T01:55:46Z backend: moved in_progress -> in_review: AC6 (docs/SCOPE_CUTS, orchestrator paths) and AC8 (eval report, T-038) deferred
- 2026-11-02T01:55:56Z orchestrator: review dispatched: claims-adjuster (sonnet)
- 2026-11-02T01:56:16Z orchestrator: AC 6 checked: orchestrator-owned: docs/M2M3_COVERAGE.md critical path, M2 cut order + cut trigger; per-card estimates appended to each card body
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:06.679Z

**tool call — Bash**
````
{
 "command": "sed -n 477,492p app/llm/lexicon.yaml; echo ...; sed -n 727,758p app/llm/lexicon.yaml",
 "description": "Read the four self_report:true lexicon entries"
}
````

### User / tool · 2026-11-02T02:02:06.765Z

**tool result**
````
- id: self_reported_prior
  pattern: '\b(?:patient|pt\.?|he|she|client)\s+(?:reports|reported|states|stated|notes|endorses|admits|recalls)\s+(?:(?:a|an|some)\s+)?(?:prior|previous|past|old|earlier|history)\b'
  flag_type: pre_existing
  category: pre_existing
  hedge: false
  self_report: true
  strength: high
  negatable: false
  rationale: 'A self-reported prior history is the record''s own admission of an earlier condition.'
  source: 'AA A3, A6; Appendix C record 3'
  false_positive: 'Requires a prior/previous/history word straight after the reporting verb. "Patient reports no prior neck problems" does not match ("no" breaks it). "Patient reports missing 3 days of work" does not match.'
  appendix_c: []
  examples:
    hit: ['Patient reports prior neck pain.', 'pt endorses history of migraines']
    miss: ['Patient reports missing 3 days of work.', 'Patient reports no prior neck problems.']

...
- id: patient_attributes_causation
  pattern: '(?:\b(?:patient|pt\.?|he|she|client)\s+(?:states|stated|reports|reported|believes|attributes|relates|related|feels|claims|says|said|thinks)\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\bcomplain(?:s|ing)?\s+of\b|\bc/o\b)[^.;]{0,80}?\b(?:after|since|from|due\s+to|because\s+of|caused\s+by|following|began\s+with)\b[^.;]{0,40}?\b(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b|\b(?:patient|pt\.?|he|she|client)\s+(?:attributes?|relates?|links?|ascribes?|connects?|associates?|blames?)\b[^.;]{0,80}?\b(?:to|on|with)\s+(?:the\s+|this\s+|that\s+|a\s+)?(?:\w+\s+){0,2}(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b|\b(?:patient|pt\.?|he|she|client)\s+(?:believes|feels|thinks|states|claims|says|reports)\s+(?:that\s+)?(?:the\s+|this\s+)?(?:\w+\s+)?(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\s+(?:caused|led\s+to|resulted\s+in|is\s+(?:the\s+)?(?:cause|reason|why|responsible)|triggered|brought\s+on)\b|\b(?:after|since|from|due\s+to|following)\b[^.;]{0,60}?\b(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b[^.;]{0,40}?,?\s*per\s+(?:the\s+)?(?:patient|pt)\b'
  flag_type: causation
  category: patient_report
  hedge: false
  self_report: true
  strength: high
  negatable: false
  rationale: 'Patient-attributed causation is history, not a physician''s causation opinion. Texas generally requires expert testimony to prove causation of conditions outside lay knowledge (Guevara). The export may quote it only with attribution.'
  source: 'AA A6; AA src 9 (Guevara v. Ferrer), src 11; Appendix C record 9'
  false_positive: 'The note helps the claimant as history. The flag is about how the line may be described, not a claim that it is false.'
  appendix_c: [9]
  examples:
    hit: ['Patient states symptoms began after the January collision.', 'She reports the pain started after the accident.', 'Pt. reports neck pain since the MVA.', 'Complains of neck pain since the collision.', 'Per patient, the pain started after the accident.']
    miss: ['Physician opines symptoms are causally related to the collision.']

- id: patient_reports_generic
  pattern: '\b(?:patient|pt\.?|he|she|client|wife|husband|spouse|mother|father|parent|family|friend|witness|EMS)\s+(?:reports|reported|states|stated|endorses|complains|c/o|describes|relates|notes|admits|recalls)\b|\bc/o\b|\bcomplain(?:s|ing)?\s+of\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\b(?:patient|self)-?\s?reported\b|^\s*(?:subjective|S)\s*:'
  flag_type: causation
  category: patient_report
  hedge: false
  self_report: true
  strength: low
  negatable: false
  rationale: 'Marks subjective, self-reported content (as opposed to objective findings), which adjusters weight less. Context only; it keeps attribution in the summary ("C/O neck pain 7/10" must stay a complaint, not become a finding).'
  source: 'AA A9; AA src 1, src 18 (objective findings weighted above subjective); reviews/T-009-legal-nurse.md (minor: C/O)'
  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. "Per patient, pain 5/10 today" is benign and stays low.'
  appendix_c: [1, 3, 5, 9]
  examples:
    hit: ['Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.', 'C/O neck pain 7/10 and headache.', 'Pt states pain worse with rotation.', 'Patient endorses headaches.', 'Per patient, pain 5/10 today.']
    miss: ['Cervical range of motion reduced approx. 40%.']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:07.391Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p artifacts/review-evidence/T-036-probe3.py >/dev/null; sed -n 1,40p tests/unit/_fakes.py | head -60; echo \"--- sample records\"; ls evals/golden 2>/dev/null | head; ",
 "description": "Read fakes helpers and golden directory listing"
}
````

### User / tool · 2026-11-02T02:02:07.487Z

**tool result**
````
"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
import itertools, json, re
from tests.unit import _golden as G

_RUNS = itertools.count()

class FakeCall:
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
    def __init__(self, script=None):
        self.script = script or {}
        self.log = []
    def __call__(self, step, system, user, schema, *, item_id=None):
        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
        if isinstance(out, Exception):
            raise out
        return out, f"call{len(self.log)}"
    def steps(self):
        return [l["step"] for l in self.log]
    def prompts(self, step):
        return [l["user"] for l in self.log if l["step"] == step]

def golden_summaries():
    """{record_no: (summary, quote)} from the golden letter block."""
    letter, _ = G.export_blocks()
    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
    from datetime import datetime
    out = {}
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
    return out

def which_record(user, case="sample"):
    """Record numbers whose excerpt appears in the prompt text."""
    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]

--- sample records
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:39.047Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-036-r2-probe.py",
 "content": "\"\"\"T-036 round-2 adjuster probe (read-only on product code). Run with .venv/bin/python from repo root.\"\"\"\nimport sys, pathlib, tempfile, re\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nimport yaml\nfrom app.backend import flag_templates as FT, grounding\nfrom app.llm import audited as AU, provider as P\nfrom tests.unit._fakes import run_sample, sample_script, FakeCall\n\nprint(\"== 1. template sweep (every category, two quotes)\")\nQUOTES = [\"Cervical ROM full, no spasm noted.\", \"No objective findings. Pain 4/10.\"]\nBAD = re.compile(r\"\\b(objective|subjective|question|suggest\\w*|could be used|another cause|severe|significant|traumatic|acute|herniat\\w*)\\b\", re.I)\nfor cat, typ in FT.TYPE_OF.items():\n    for q in QUOTES:\n        t, e = FT.render(typ, cat, provider=\"Capital PT\", date=\"2026-01-23\", quote=q)\n        hits = BAD.findall(t + \" \" + e)\n        # strip the verbatim quote before scanning the tool's own words\n        own = (t + \" \" + e).replace(q, \"\")\n        own_hits = BAD.findall(own)\n        if own_hits or \".”.\" in e:\n            print(\"  OWN-VOICE HIT\", cat, q[:20], own_hits, \"| dbl-period\" if \".”.\" in e else \"\", \"|\", t, \"|\", e)\n    t, e = FT.render(typ, cat, provider=\"Capital PT\", date=\"2026-01-23\", quote=QUOTES[0])\n    if cat in (\"objective_negative\", \"speculative_language\", \"alternative_cause\", \"analysis_incomplete\", \"patient_report\"):\n        print(f\"  {cat}: title={t!r}\")\n        print(f\"     explanation={e!r}\")\nt, e = FT.render(\"record_warning\", \"analysis_incomplete\")\nprint(\"  analysis_incomplete:\", repr(t), repr(e))\n\nprint(\"== 2. conflict-pass failure paths on the sample (pipeline)\")\nfor label, script in [\n    (\"conflicts LLMFailed\", sample_script(conflicts=AU.LLMFailed(\"down\"))),\n    (\"conflicts FixtureMiss\", sample_script(conflicts=P.FixtureMiss(\"x\"))),\n]:\n    tmp = pathlib.Path(tempfile.mkdtemp(dir=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence\"))\n    out, _ = run_sample(tmp, call=FakeCall(script))\n    print(f\"  {label}: status={out['status']} errors={out['errors']} warnings={out['warnings']}\")\n    for f in out[\"flags\"]:\n        if f[\"type\"] == \"record_warning\" or f.get(\"pipeline_warning\"):\n            print(\"     \", f[\"id\"], f[\"type\"], f.get(\"category\"), f[\"state\"], f.get(\"reasons\"),\n                  \"record_nos=\", f.get(\"record_nos\"), \"pipeline_warning=\", f.get(\"pipeline_warning\"), \"|\", f.get(\"title\"), \"|\", f.get(\"why\"))\n    print(\"      flags total:\", len(out[\"flags\"]), \"| run-level keys:\", sorted(k for k in out if \"partial\" in k or \"pipeline\" in k))\n\nprint(\"== 3. source_kind parity: lexicon self_report:true patterns vs grounding.has_self_report\")\nlex = yaml.safe_load(open(\"/Users/arsis/zlayt-pm-project/app/llm/lexicon.yaml\"))\nents = []\ndef walk(x):\n    if isinstance(x, dict):\n        if \"id\" in x and x.get(\"self_report\") is True: ents.append(x)\n        for v in x.values(): walk(v)\n    elif isinstance(x, list):\n        for v in x: walk(v)\nwalk(lex)\nprobe_texts = [\n    \"Patient reports prior neck pain.\", \"Patient states symptoms began after the January collision.\",\n    \"Patient notes prior neck pain.\", \"Patient describes neck pain since the collision.\",\n    \"Patient links her neck pain to the collision.\", \"Subjective: neck pain 7/10.\",\n    \"Patient-reported neck pain 7/10.\", \"EMS reports neck pain 7/10.\", \"Witness states the impact was minor.\",\n    \"Date of accident per intake form: 2026-01-19.\", \"Date of accident per EMS report.\",\n    \"Per patient, pain 5/10 today.\", \"C/O neck pain 7/10 and headache.\",\n]\nfor e in ents:\n    rx = re.compile(e[\"pattern\"], re.I)\n    print(f\"  entry {e['id']} (category {e.get('category')}) examples.hit:\", e.get(\"examples\", {}).get(\"hit\"))\nfor txt in probe_texts:\n    lexhits = [e[\"id\"] for e in ents if re.search(e[\"pattern\"], txt, re.I)]\n    print(f\"  {txt!r:62} lexicon_self_report={lexhits or '-'} has_self_report={grounding.has_self_report(txt)}\")\n"
}
````

### User / tool · 2026-11-02T02:02:39.152Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-036-r2-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:40.447Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-036-r2-probe.py 2>&1 | tee artifacts/review-evidence/T-036-r2-probe.txt | head -120",
 "description": "Run round-2 adjuster probe and save output"
}
````

### User / tool · 2026-11-02T02:02:41.057Z

**tool result**
````
== 1. template sweep (every category, two quotes)
  OWN-VOICE HIT pre_existing Cervical ROM full, n [] | dbl-period | Mention of a prior or pre-existing condition | Capital PT (January 23, 2026) mentions a prior or pre-existing condition: “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT pre_existing No objective finding [] | dbl-period | Mention of a prior or pre-existing condition | Capital PT (January 23, 2026) mentions a prior or pre-existing condition: “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT degenerative_language Cervical ROM full, n [] | dbl-period | Degenerative wording | Capital PT (January 23, 2026) uses degenerative wording: “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT degenerative_language No objective finding [] | dbl-period | Degenerative wording | Capital PT (January 23, 2026) uses degenerative wording: “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT prior_surgery Cervical ROM full, n [] | dbl-period | Mention of prior surgery or repair | Capital PT (January 23, 2026) mentions prior surgery or repair: “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT prior_surgery No objective finding [] | dbl-period | Mention of prior surgery or repair | Capital PT (January 23, 2026) mentions prior surgery or repair: “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT speculative_language Cervical ROM full, n [] | dbl-period | Hedged wording | Hedged wording in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT speculative_language No objective finding [] | dbl-period | Hedged wording | Hedged wording in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  speculative_language: title='Hedged wording'
     explanation='Hedged wording in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.'
  OWN-VOICE HIT patient_report Cervical ROM full, n [] | dbl-period | Patient self-report | Patient self-report (not a physician's opinion) in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT patient_report No objective finding [] | dbl-period | Patient self-report | Patient self-report (not a physician's opinion) in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  patient_report: title='Patient self-report'
     explanation="Patient self-report (not a physician's opinion) in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”."
  OWN-VOICE HIT missed_care Cervical ROM full, n [] | dbl-period | Missed or ended care | Wording about missed appointments or ending care in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT missed_care No objective finding [] | dbl-period | Missed or ended care | Wording about missed appointments or ending care in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT new_onset Cervical ROM full, n [] | dbl-period | New-onset wording | New-onset wording in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT new_onset No objective finding [] | dbl-period | New-onset wording | New-onset wording in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT scene_facts Cervical ROM full, n [] | dbl-period | Scene facts | Scene facts recorded by Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT scene_facts No objective finding [] | dbl-period | Scene facts | Scene facts recorded by Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT alternative_cause Cervical ROM full, n [] | dbl-period | Mention of another injury or event | Mention of another injury or event in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT alternative_cause No objective finding [] | dbl-period | Mention of another injury or event | Mention of another injury or event in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  alternative_cause: title='Mention of another injury or event'
     explanation='Mention of another injury or event in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.'
  OWN-VOICE HIT litigation_referral Cervical ROM full, n [] | dbl-period | Attorney referral | Referral wording in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT litigation_referral No objective finding [] | dbl-period | Attorney referral | Referral wording in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT objective_negative Cervical ROM full, n [] | dbl-period | Normal or absent findings wording | Wording about normal or absent findings in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT objective_negative No objective finding [] | dbl-period | Normal or absent findings wording | Wording about normal or absent findings in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  objective_negative: title='Normal or absent findings wording'
     explanation='Wording about normal or absent findings in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.'
  OWN-VOICE HIT accident_date_provenance Cervical ROM full, n [] | dbl-period | Accident date source | Accident date as stated in Capital PT (January 23, 2026): “Cervical ROM full, no spasm noted.”.
  OWN-VOICE HIT accident_date_provenance No objective finding [] | dbl-period | Accident date source | Accident date as stated in Capital PT (January 23, 2026): “No objective findings. Pain 4/10.”.
  OWN-VOICE HIT injection_suspected Cervical ROM full, n [] | dbl-period | Instruction-like text in a record | Capital PT (January 23, 2026) contains instruction-like text: “Cervical ROM full, no spasm noted.”. It is shown unchanged and everything from this record needs review.
  OWN-VOICE HIT injection_suspected No objective finding [] | dbl-period | Instruction-like text in a record | Capital PT (January 23, 2026) contains instruction-like text: “No objective findings. Pain 4/10.”. It is shown unchanged and everything from this record needs review.
  analysis_incomplete: title='Cross-record check did not finish'
     explanation='The check for conflicts between records did not finish, so conflicts between records may be missing from this list. Review the records side by side.'
  analysis_incomplete: 'Cross-record check did not finish' 'The check for conflicts between records did not finish, so conflicts between records may be missing from this list. Review the records side by side.'
== 2. conflict-pass failure paths on the sample (pipeline)
  conflicts LLMFailed: status=done errors=[] warnings=[]
      f_cx1 record_warning analysis_incomplete needs_review ['LLM_FAILED_AFTER_RETRIES'] record_nos= [1] pipeline_warning= CONFLICT_PASS_INCOMPLETE | Cross-record check did not finish | The AI step failed on all three attempts, so this record has no AI-made entry.
      flags total: 10 | run-level keys: []
  conflicts FixtureMiss: status=done errors=[] warnings=[]
      f_cx1 record_warning analysis_incomplete needs_review ['FIXTURE_MISS'] record_nos= [1] pipeline_warning= CONFLICT_PASS_INCOMPLETE | Cross-record check did not finish | The demo has no recorded AI answer for this step, so this item has not been checked.
      flags total: 10 | run-level keys: []
== 3. source_kind parity: lexicon self_report:true patterns vs grounding.has_self_report
  entry self_reported_prior (category pre_existing) examples.hit: ['Patient reports prior neck pain.', 'pt endorses history of migraines']
  entry patient_attributes_causation (category patient_report) examples.hit: ['Patient states symptoms began after the January collision.', 'She reports the pain started after the accident.', 'Pt. reports neck pain since the MVA.', 'Complains of neck pain since the collision.', 'Per patient, the pain started after the accident.']
  entry patient_reports_generic (category patient_report) examples.hit: ['Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.', 'C/O neck pain 7/10 and headache.', 'Pt states pain worse with rotation.', 'Patient endorses headaches.', 'Per patient, pain 5/10 today.']
  entry intake_form_accident_date (category accident_date_provenance) examples.hit: ['Date of accident per intake form: 2026-01-19.', 'Date of injury per patient: 03/02/2026.']
  'Patient reports prior neck pain.'                             lexicon_self_report=['self_reported_prior', 'patient_reports_generic'] has_self_report=True
  'Patient states symptoms began after the January collision.'   lexicon_self_report=['patient_attributes_causation', 'patient_reports_generic'] has_self_report=True
  'Patient notes prior neck pain.'                               lexicon_self_report=['self_reported_prior', 'patient_reports_generic'] has_self_report=False
  'Patient describes neck pain since the collision.'             lexicon_self_report=['patient_reports_generic'] has_self_report=False
  'Patient links her neck pain to the collision.'                lexicon_self_report=['patient_attributes_causation'] has_self_report=False
  'Subjective: neck pain 7/10.'                                  lexicon_self_report=['patient_reports_generic'] has_self_report=False
  'Patient-reported neck pain 7/10.'                             lexicon_self_report=['patient_reports_generic'] has_self_report=False
  'EMS reports neck pain 7/10.'                                  lexicon_self_report=['patient_reports_generic'] has_self_report=False
  'Witness states the impact was minor.'                         lexicon_self_report=['patient_reports_generic'] has_self_report=False
  'Date of accident per intake form: 2026-01-19.'                lexicon_self_report=['intake_form_accident_date'] has_self_report=False
  'Date of accident per EMS report.'                             lexicon_self_report=- has_self_report=False
  'Per patient, pain 5/10 today.'                                lexicon_self_report=['patient_reports_generic'] has_self_report=True
  'C/O neck pain 7/10 and headache.'                             lexicon_self_report=['patient_reports_generic'] has_self_report=True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:54.701Z

**tool call — Bash**
````
{
 "command": "sed -n 22,28p app/llm/lexicon.yaml; echo \"--- flags.js\"; sed -n 60,66p frontend/flags.js 2>/dev/null; echo \"--- objective/subjective anywhere user-facing\"; grep -rniE \"objective|subjective\" app/backend frontend --include=*.py --include=*.js --include=*.html --include=*.md 2>/dev/null | grep -viE \"objective_negative|subjective:|\\\"subjective\\\"|'subjective'\" | head -20; echo \"--- category raw display?\"; grep -n \"\\.category\" frontend/*.js | head -10",
 "description": "Read lexicon contract, chip logic, and user-facing objective wording"
}
````

### User / tool · 2026-11-02T02:02:54.808Z

**tool result**
````
#   prior_surgery, alternative_cause, scene_facts, objective_negative, litigation_referral, recovery_context,
#   accident_date_provenance.
# - `hedge: true` marks the R-TL-8 hedge set: a sentence with a hedge hit is a qualifier unit and can never be cut
#   from an excerpt (ADR-016). `self_report: true` marks patient-attributed wording; code sets
#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
# - `strength`: high and medium raise a flag (origin lexicon, or lexicon+llm). low is context only: it never
#   raises a flag alone. It can still attach to an LLM flag, keep attribution in a summary, or mark a qualifier unit.
--- flags.js
--- objective/subjective anywhere user-facing
--- category raw display?
ugrep: warning: frontend/*.js: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:58.224Z

**tool call — Bash**
````
{
 "command": "find . -name \"flags.js\" -not -path \"./.venv/*\" -not -path \"*/node_modules/*\" 2>/dev/null | head; F=$(find . -name \"flags.js\" -not -path \"./.venv/*\" -not -path \"*/node_modules/*\" 2>/dev/null | head -1); [ -n \"$F\" ] && sed -n 60,66p \"$F\"; echo \"--- objective user-facing (app/ and any html/js)\"; grep -rniE \"objective|subjective\" app/ --include=*.py --include=*.js --include=*.html --include=*.md --include=*.yaml 2>/dev/null | grep -viE \"objective_negative|subjective:|objective\\s+findings\\s+are|\\bS\\s*:\" | grep -v \"lexicon.yaml\" | head -15; echo \"--- git status of product files (read-only check)\"; git -C /Users/arsis/zlayt-pm-project status --short 2>&1 | head -5",
 "description": "Locate chip logic and scan user-facing objective wording"
}
````

### User / tool · 2026-11-02T02:02:58.290Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: find . -name "flags.js" -not -path "./.venv/*" -not -path "*/node_modules/*" 2>/dev/null | head; F=$(find . -name "flags.js" -not -path "./.venv/*" -not -path "*/node_modules/*" 2>/dev/null | head -1)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:59.578Z

**tool call — Bash**
````
{
 "command": "find . -name \"flags.js\" -not -path \"./.venv/*\" -not -path \"*/node_modules/*\" 2>/dev/null | head -5",
 "description": "Locate flags.js in the repo"
}
````

### User / tool · 2026-11-02T02:02:59.680Z

**tool result**
````
./app/frontend/flags.js
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:00.164Z

**tool call — Bash**
````
{
 "command": "grep -rniE \"objective|subjective\" app/ --include=*.py --include=*.js --include=*.html --include=*.md 2>/dev/null | grep -viE \"objective_negative\" | head -15",
 "description": "Scan app for remaining objective or subjective wording"
}
````

### User / tool · 2026-11-02T02:03:00.252Z

**tool result**
````
app/llm/prompts/judge_flag_v1.md:5:Flag types: pre_existing (the quote mentions a condition, injury or treatment from before the accident, or a long-standing problem); causation (the quote weakens or questions whether the accident caused the condition: degenerative or speculative wording, missed care, scene facts, negative objective findings).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:01.662Z

**tool call — Bash**
````
{
 "command": "sed -n 58,66p app/frontend/flags.js",
 "description": "Read chip rendering in flags.js"
}
````

### User / tool · 2026-11-02T02:03:01.739Z

**tool result**
````
    return wrap;
  }

  function card(c, f) {
    const seqs = (RV.sourceTargets(f, "flag").ids || []).map((id) => recSeq(c, id));
    const label = f.source_kind === "patient_report" && f.title !== "Patient self-report" ? "Patient self-report" : null;
    const note = f.reviewer_note || (f.edited && f.edited.note);
    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", role: "group", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:20.640Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-036-r2-probe4.py <<'EOF'\nimport sys, pathlib, tempfile\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nfrom app.llm import audited as AU\nfrom tests.unit._fakes import run_sample, sample_script, FakeCall\ntmp = pathlib.Path(tempfile.mkdtemp(dir=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence\"))\nout, _ = run_sample(tmp, call=FakeCall(sample_script(conflicts=AU.LLMFailed(\"down\"))))\nprint(\"entries with record 1:\", [(e.get(\"id\"), e.get(\"record_ids\")) for e in out[\"entries\"] if \"r1\" in (e.get(\"record_ids\") or [])][:3])\nprint(\"flags:\", [(f[\"id\"], f[\"type\"], f.get(\"record_ids\"), f[\"state\"]) for f in out[\"flags\"]])\nprint(\"status:\", out[\"status\"], \"errors:\", out[\"errors\"], \"warnings:\", out[\"warnings\"])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-036-r2-probe4.py 2>&1 | tee artifacts/review-evidence/T-036-r2-probe4.txt",
 "description": "Check record 1 entries and run-level status on conflict failure"
}
````

### User / tool · 2026-11-02T02:03:21.145Z

**tool result**
````
entries with record 1: [('e1', ['r1'])]
flags: [('f_gap_r6_r7', 'gap', ['r6', 'r7'], 'verified'), ('f_accident_date_after_treatment_1_2_7', 'conflict', ['r1', 'r2', 'r7'], 'verified'), ('f_r3_1', 'pre_existing', ['r3'], 'needs_review'), ('f_r8_1', 'pre_existing', ['r8'], 'needs_review'), ('f_r6_1', 'causation', ['r6'], 'needs_review'), ('f_r7_1', 'causation', ['r7'], 'needs_review'), ('f_r7_2', 'causation', ['r7'], 'needs_review'), ('f_r8_2', 'causation', ['r8'], 'needs_review'), ('f_r9_1', 'causation', ['r9'], 'needs_review'), ('f_cx1', 'record_warning', ['r1'], 'needs_review')]
status: done errors: [] warnings: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:28.988Z

**tool call — Bash**
````
{
 "command": "grep -rn \"ADR-013\\|R-FL-7\" --include=*.md . 2>/dev/null | grep -v \"\\.venv\" | head -12",
 "description": "Find ADR-013 and R-FL-7 spec text"
}
````

### User / tool · 2026-11-02T02:03:29.086Z

**tool result**
````
artifacts/review-evidence/T-009-r2-resolution.md:38:| A-M4 | major | Taxonomy: no hedge category, compliance unmapped, self-report mixed with hedges | **partial** | Resolved: the hedge set equals R-TL-8's list; there are 4 self_report entries; no entry is both; compliance maps to causation. Not resolved: 6 lexicon categories are outside ADR-013's closed list. `objective_negative` (4 entries) should be `no_objective_findings`/`normal_exam`, and `litigation_referral` should be `attorney_referral`. The header (:17) calls `scene_facts` lexicon-only, but ADR-013 lists it. |
artifacts/review-evidence/T-013-trace.md:150:| PM-m3 | Self-report label undecidable | resolved | R-FL-7 (67) `source_kind == "patient_report"` | — |
artifacts/review-evidence/T-014-r2-privacy-resolution.md:16:| M4 | LLM-written flag title/explanation unchecked (major) | ADR-013:243 schema has no prose field; templates in `flag_templates.py`; LLM_VS_CODE row 14. | **Resolved** |
artifacts/review-evidence/T-013-r2-resolution.md:37:PM minors, spot-checked: R-SU-3 checklist :137 ✔; TOOLS.md and unedited :138 ✔; R-FL-7 `source_kind` :67 ✔; ambiguous-date placement :37 ✔; R-EX-3 order :105 and R-EX-2 scope :104 ✔; ship-bar row 5 :289 ✔; assumptions cited by ID :301-317 ✔; R-CH-7 marked as proposal :79 ✔; accepted/pending total :75 ✔.
artifacts/review-evidence/T-015-r2-nurse.md:103:Also: R-FL-7 defines `source_kind = "patient_report"` on **flags**. The golden uses `"patient_self_report"` on **entries**.
artifacts/review-evidence/T-014-r3-resolution.md:25:| R2-8 D-018 not reflected | minor | **Partly resolved (new M2)** | ADR-013 (DECISIONS.md:250-255) adds scene_facts, no_objective_findings, normal_exam, attorney_referral and the lexicon-v2 dependency. Lexicon v2 actually uses categories prior_surgery, alternative_cause, objective_negative, litigation_referral, recovery_context, accident_date_provenance (none in ADR-013) and none of no_objective_findings/normal_exam/attorney_referral. |
artifacts/review-evidence/T-014-r3-resolution.md:35:| N3 lexicon controls with no lexicon; P1 floor miss | major | **Mostly resolved; two gaps (M2, M5)** | Per-record flag pass (DECISIONS.md:191, D-021); conflicts pass carries the tag and the residual is stated; lexicon v2 now has an `injection` category (tags case_07 r3) and P1 "prior ACL repair" HITs (`prior_surgery_terms[high]`), recall gate in ADR-008.4. Gaps: P1's floor flag has category `prior_surgery`, which is not in ADR-013's closed list (no template); the cut line allows folding back to one pass. |
artifacts/review-evidence/T-014-r3-resolution.md:46:- M2 ADR-013 closed category list does not match lexicon v2 (6 lexicon categories missing, 3 ADR categories unused).
artifacts/review-evidence/T-014-r2-staff-resolution.md:21:| F8 | Flag text / self-report label | resolved | ADR-013 (:240-245), flag_templates.py, closed categories, `source_kind` set by code; api.md f_pat_9 | D-018 categories missing from the closed list (R2-8) |
artifacts/review-evidence/T-014-r2-staff-resolution.md:30:- D-001 R (ADR-009). D-002 R. D-003 R (ADR-010; `non_encounter` lexicon pending). D-004 R (ADR-011) but see R2-2. D-005 R (ADR-008.4). D-006 R (ADR-012, allowed-text deviation declared). D-007 R (ADR-013). D-008 R (ADR-006; ledger caveat R2-6). D-009 R (ADR-009, api `ai_drafted`, internal notes line). D-010 R (ADR-005, api review). D-011 R (ADR-015; no cut behaviour in docs). D-012 R in text, over-applied in ADR-016 (R2-4). D-013 R. D-014 R (ADR-016). D-015 R (ADR-017.9). D-016 D (no design impact; the data-flow paragraph in README-arch.md:68 is enough). D-017 R (ADR-014 template, no delay computation). D-018 X (handoff and ADR header cite D-001..D-017 only; closed flag-category lists in ADR-013 lack scene facts, no objective findings, normal exam, attorney referral).
artifacts/review-evidence/T-050/pre_6c3aeb1p/memory/DECISIONS.md:87:flags         id, case_id, type('gap'|'conflict'|'pre_existing'|'causation'|'record_warning', D-013), category (closed list, ADR-013), source_kind('record'|'patient_report'),
artifacts/review-evidence/T-050/pre_6c3aeb1p/memory/DECISIONS.md:246:## ADR-013 Flag text is rendered by code; the LLM returns a category and quoted spans only
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:30.792Z

**tool call — Bash**
````
{
 "command": "f=$(ls memory/DECISIONS.md 2>/dev/null); echo \"file=$f\"; [ -n \"$f\" ] && sed -n 246,262p memory/DECISIONS.md; echo \"--- R-FL-7 in spec\"; grep -rln \"R-FL-7\" memory docs 2>/dev/null | head -5; grep -rn \"R-FL-7\" memory docs 2>/dev/null | head -5",
 "description": "Read ADR-013 and R-FL-7 spec text"
}
````

### User / tool · 2026-11-02T02:03:30.889Z

**tool result**
````
file=memory/DECISIONS.md
## ADR-013 Flag text is rendered by code; the LLM returns a category and quoted spans only
- Status: accepted (round 2, amended round 3; D-007, D-013, D-018; resolves staff F8, R2-8)
- Context: flag explanations are where a model is most tempted to rule ("pre-existing degenerative disease"), which Appendix C forbids.
- Decision:
  - The flag-type vocabulary is `gap`, `conflict`, `pre_existing`, `causation`, `record_warning` everywhere (D-013). `record_warning` flags are created by code only (categories `date_ambiguous`, `injection_suspected`).
  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`medium` raise flags; `low` is context only). Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and understands field-style answers ("Prior injuries: No."). Categories the code relies on: `pre_existing`, `causation_weakening`, `compliance`, the hedge set, `patient_report`, `accident_date_phrases`, `damages`, `non_encounter`, `injection`. **`lexicon.yaml` v2 is a researcher deliverable that blocks the gap rule (`non_encounter`), the accident-date rule (`accident_date_phrases`) and the injection scan (`injection`); its self-check must run over every golden case and report recall per `must` flag.** The lexicon `causation_weakening` and `compliance` map to `causation`.
  - LLM flag passes run **per record** and return `{type, category, record_id, excerpt}`; the cross-record conflict pass returns `{category, a:{record_id, excerpt}, b:{...}}`. The schema rejects any extra prose field. `category` is from a closed list:
    The list equals the lexicon v2 category names (single vocabulary):
    - pre_existing: `pre_existing`, `degenerative_language`, `prior_surgery`;
    - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (no objective findings, normal exam, WNL/full ROM), `recovery_context`, `accident_date_provenance`;
    - conflict: `treatment_plan_vs_actual`, `provider_name_variant`, `other_fact_mismatch` (LLM or code), `accident_date_after_treatment`, `accident_dates_differ` (code);
    - gap: `gap_over_30` (code); record_warning: `date_ambiguous`, `injection_suspected` (code).
    **Template table (design text; slots `{date}` long date, `{provider}` header label as written, `{quote}` verbatim excerpt, `{days}`, `{a}`/`{b}` for two sources):**

    | Category | Title template | Explanation template |
    |---|---|---|
    | gap_over_30 | Gap of {days} days | Gap of {days} days between {date A} ({provider A}) and {date B} ({provider B}). |
--- R-FL-7 in spec
docs/M2M3_COVERAGE.md
docs/M2M3_COVERAGE.md:47:| R-FL-7 | T-036 (m2-be-llm-flags), T-043 (m3-fe-flags-charges-review) |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:32.521Z

**tool call — Bash**
````
{
 "command": "grep -n \"source_kind\\|self_report\\|self-report\" memory/DECISIONS.md | head -20; echo \"--- spec R-FL-7 text\"; grep -rn \"R-FL-7\\b\" memory/*.md docs/*.md 2>/dev/null | head; ls memory | head -30",
 "description": "Grep decisions for self-report and source_kind rule"
}
````

### User / tool · 2026-11-02T02:03:32.614Z

**tool result**
````
87:flags         id, case_id, type('gap'|'conflict'|'pre_existing'|'causation'|'record_warning', D-013), category (closed list, ADR-013), source_kind('record'|'patient_report'),
244:- **Dropped qualifiers (D-022, round 4).** A second function `grounding.dropped_qualifiers(summary, excerpt)` finds qualifiers in the excerpt (lexicon hedge set, `self_report` entries, negation words such as "without", laterality, "approx.") and requires each to appear in the summary; a missing one gives `needs_review` with `SUMMARY_DROPS_QUALIFIER`. The judge checks additions, not omissions, so this is code. Self-report is tagged per quote: each entry carries `source_kind` (`patient_report` | `record`) for its excerpt sentences, set by code from the lexicon. In evals, `required_terms` are checked against the summary alone. R-TL-10 gains this check (ADR-017).
251:  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`medium` raise flags; `low` is context only). Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and understands field-style answers ("Prior injuries: No."). Categories the code relies on: `pre_existing`, `causation_weakening`, `compliance`, the hedge set, `patient_report`, `accident_date_phrases`, `damages`, `non_encounter`, `injection`. **`lexicon.yaml` v2 is a researcher deliverable that blocks the gap rule (`non_encounter`), the accident-date rule (`accident_date_phrases`) and the injection scan (`injection`); its self-check must run over every golden case and report recall per `must` flag.** The lexicon `causation_weakening` and `compliance` map to `causation`.
272:    | patient_report | Patient self-report | Patient self-report (not a physician's opinion) in {provider} ({date}): “{quote}”. |
286:  - `source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt and drives the "Patient self-report" label. Origin is `lexicon`, `llm` or `lexicon+llm`; one-sided hits are `needs_review` (`LEXICON_ONLY`, `LLM_ONLY`). Flags are not editable except a reviewer note.
327:  4. **Codes and fields.** `EXCERPT_OMITS_QUALIFIER` adopted with D-021 scope. Neither `GROUNDING_DATE_MISMATCH` nor `GROUNDING_PROVIDER_NOT_IN_RECORD` exists; R-TL-3 and R-TL-9 are restated (ADR-016). `FIXTURE_MISS` and `JUDGE_UNAVAILABLE` on edits are new needs_review reasons. `source_kind` adopted; amount class `damages` replaces `other`.
334:  11. **Lexicon v2 dependency.** `lexicon.yaml` (flag_type, hedge, self_report, strength, `accident_date_phrases`, `non_encounter`, `injection`) is a researcher deliverable that blocks gaps, the accident-date conflict and the injection scan (ADR-013).
--- spec R-FL-7 text
docs/M2M3_COVERAGE.md:47:| R-FL-7 | T-036 (m2-be-llm-flags), T-043 (m3-fe-flags-charges-review) |
ASSUMPTIONS.md
DECISIONS.md
ENVIRONMENT.md
GLOSSARY.md
LESSONS.md
ORCHESTRATOR_DECISIONS.md
PROGRESS.md
SCOPE_CUTS.md
STATE.md
contracts
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:50.238Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def rec\\|^from\\|^import\" tests/unit/test_flags_pass.py | head -12; grep -n \"def rec\" -A4 tests/unit/test_flags_pass.py | head -8",
 "description": "Check record helper used by flag-pass tests"
}
````

### User / tool · 2026-11-02T02:03:50.328Z

**tool result**
````
2:from app.backend import flags as F
3:from app.llm import audited as AU, provider as P
4:from tests.unit import _golden as G
5:from tests.unit._fakes import FakeCall
9:def rec(n, case="sample", ex=EX):
9:def rec(n, case="sample", ex=EX):
10-    r = G.record(case, n)
11-    return dict(n=n, source=r["source"], excerpt=r["excerpt"], date_iso=ex["records"][n - 1]["date"])
12-
13-R8 = rec(8)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:52.887Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-036-r2-probe5.py <<'EOF'\nimport sys\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nfrom app.backend import flags as F\ndef mk(text, n=3):\n    return dict(n=n, source=\"Capital PT\", excerpt=text, date_iso=\"2026-01-23\", id=f\"r{n}\")\nfor txt in [\"Patient notes prior neck pain.\", \"Patient links her neck pain to the collision.\",\n            \"Patient reports prior neck pain.\", \"Date of accident per intake form: 2026-01-19.\"]:\n    fl = F.lexicon_flags(mk(txt))\n    for f in fl:\n        print(f\"{txt!r:50} type={f['type']:12} category={f['category']:18} source_kind={f['source_kind']:15} title={f['title']!r}\")\n    if not fl:\n        print(f\"{txt!r:50} no lexicon flag\")\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-036-r2-probe5.py 2>&1 | tee artifacts/review-evidence/T-036-r2-probe5.txt",
 "description": "Run flag-level source_kind probe on lexicon self-report lines"
}
````

### User / tool · 2026-11-02T02:03:53.227Z

**tool result**
````
'Patient notes prior neck pain.'                   type=pre_existing category=pre_existing       source_kind=record          title='Mention of a prior or pre-existing condition'
'Patient links her neck pain to the collision.'    type=causation    category=patient_report     source_kind=record          title='Patient self-report'
'Patient reports prior neck pain.'                 type=pre_existing category=pre_existing       source_kind=patient_report  title='Mention of a prior or pre-existing condition'
'Date of accident per intake form: 2026-01-19.'    type=causation    category=accident_date_provenance source_kind=record          title='Accident date source'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:52.110Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-036-claims-adjuster-r2.md",
 "content": "# T-036 LLM flag passes, round 2 (commit cd4bc60): claims-adjuster review (Gary Pruitt)\n\nVerdict: **fail** (1 blocker, 2 major, 1 minor, 1 nit).\n\nRound-1 items, status on cd4bc60:\n- Blocker `objective_negative` title \"No objective findings noted\": **resolved.** `grep -n \"No objective findings\" app/backend/flag_templates.py` returned nothing (exit 1). New template at flag_templates.py:132 reads `\"objective_negative\": lambda v: (\"Normal or absent findings wording\", f\"Wording about normal or absent findings in {_at(v)}{_quote(v)}.\")`. An own-voice sweep over all 21 TYPE_OF categories with two quotes found no \"objective\", \"subjective\", \"question\", \"suggest\", \"could be used\", \"another cause\", \"severe\", \"significant\", \"traumatic\", \"acute\" or \"herniation\" outside the verbatim quote.\n- Major, silent conflict-pass loss: **partly resolved.** The failure now yields a visible needs_review `record_warning` flag (flags.py:201, 203). The run-level signal the fix asked for does not exist (finding 2).\n- Major, J3 fixture shape: **resolved.** A conflict without `excerpt_b` is rejected (flags.py, `or not m.excerpt_b`), and test_pipeline.py's J3 tests now pass.\n- Major, intake date labelled patient self-report: **resolved for record 7, but the fix over-reaches.** Record 7's flag is now `record`. The lexicon self-report mechanism was removed for every entry, which breaks the spec (finding 1).\n\nFindings:\n1. **Blocker.** `source_kind` no longer comes from the lexicon `self_report` entries, which DECISIONS.md:286 requires. Lines that the lexicon itself marks as patient self-report now read as record statements. Flag-level probe: \"Patient notes prior neck pain.\" gives `pre_existing`, `source_kind=record`, and a title with no self-report attribution. \"Patient links her neck pain to the collision.\" gives `category=patient_report` with title \"Patient self-report\" but `source_kind=record`. The control \"Patient reports prior neck pain.\" gives `patient_report`. No fact is invented, since the verbatim quote keeps \"Patient notes\", but the attribution the spec requires is lost.\n2. **Major.** On a conflict-pass failure the run still reports `status=done` with no error or warning. flags.py:183 says \"the pipeline adds a run warning (`pipeline_warning`) so the run is shown as partial\", but nothing reads `pipeline_warning`.\n3. **Major.** The full unit suite is still red: `5 failed, 750 passed`, all in test_t037_backend.py. Round 1 reported 3.\n4. **Minor.** The conflict-pass warning is attached to record 1 and its \"why\" text says record 1 has no AI entry. Record 1 has entry e1.\n5. **Nit.** Every quote template still ends in `.”.`.\n\nWhat is right:\n- The objective_negative title is neutral, and the own-voice sweep over all 21 categories is clean.\n- The record-7 intake date is `record`, and the conflict-pass failure path now produces a visible needs_review item for both LLMFailed and FixtureMiss.\n- A single-quote conflict is rejected (`SCHEMA_INVALID`), and test_flags_pass.py covers it.\n\nOutside my lens: the wording of the FIXTURE_MISS \"why\" (\"The demo has no recorded AI answer...\", why.py:16) is product copy. I did not rate it.\n\n```json\n{\"card\": \"T-036\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit cd4bc60 (app/backend/flag_templates.py, flags.py, grounding.py, tests/unit/test_flags_pass.py) against 199785f; app/llm/lexicon.yaml, memory/DECISIONS.md:286 as the source_kind spec; sample case via fixture pipeline (no live app URL; LLM is scripted FakeCall)\",\n \"exercised\": [\n  \"Read personas/claims-adjuster.md in full\",\n  \"grep -n 'No objective findings' app/backend/flag_templates.py -> no output, exit=1\",\n  \"grep -n 'objective_negative' -A6 app/backend/flag_templates.py -> lines 37 and 132 (new template quoted in the summary)\",\n  \"grep -rn 'CONFLICT_PASS_INCOMPLETE|analysis_incomplete' app/ -> flag_templates.py:38,136; flags.py:184-188\",\n  \"grep -rn 'pipeline_warning|CONFLICT_PASS_INCOMPLETE' app/ tests/ -> only flags.py:183,188 (no reader in pipeline.py)\",\n  \"grep -n 'patient_report' app/backend/flags.py -> flags.py:42 source_kind = patient_report if grounding.has_self_report(excerpt)\",\n  \".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2 -> 48 passed in 0.27s\",\n  \".venv/bin/python -m pytest tests/unit/test_pipeline.py tests/unit/test_flags_pass.py tests/unit/test_conflicts.py -q -> 45 passed\",\n  \".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -6 -> 5 failed, 750 passed (test_t037_backend.py: test_replay_has_no_fixture_miss[case_02_gap_boundaries], [case_08_diagnosis_temptation], [case_09_nonvisit_hides_gap], test_judge_lines_replay, test_fixtures_come_only_from_golden_text)\",\n  \".venv/bin/python -m pytest tests/unit/test_t037_backend.py -q (failure messages read)\",\n  \"git show --stat cd4bc60; git show cd4bc60 -- app/backend/flag_templates.py app/backend/flags.py app/backend/grounding.py tests/unit/test_flags_pass.py\",\n  \"grep -n 'self_report' app/llm/lexicon.yaml; parsed lexicon.yaml: 4 entries with self_report: true (self_reported_prior, patient_attributes_causation, patient_reports_generic, intake_form_accident_date)\",\n  \"sed -n 22,28p app/llm/lexicon.yaml (header: code sets source_kind from self_report)\",\n  \"grep -n 'source_kind' memory/DECISIONS.md -> line 286 (source_kind set by code from the lexicon self_report entries)\",\n  \"app/frontend/flags.js:63 (chip logic: source_kind patient_report and title not 'Patient self-report')\",\n  \"artifacts/review-evidence/T-036-r2-probe.py -> T-036-r2-probe.txt (template sweep over 21 categories x 2 quotes; conflict-pass failure paths LLMFailed/FixtureMiss on the sample; has_self_report vs lexicon self_report hits on 13 lines)\",\n  \"artifacts/review-evidence/T-036-r2-probe4.py -> T-036-r2-probe4.txt (record-1 entries, f_cx1 record_ids, run status on LLMFailed)\",\n  \"artifacts/review-evidence/T-036-r2-probe5.py -> T-036-r2-probe5.txt (lexicon_flags source_kind on 4 lines)\",\n  \"python3 tools/board.py show T-036 (card AC, notes; AC2 defers full fixture run to T-037)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"surfaces_every_attack_item_on_sample\": 4, \"no_invented_or_overstated_text\": 3, \"patient_attribution_label\": 2, \"visible_conflict_failure\": 3, \"template_neutrality\": 5, \"test_honesty\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"source_kind no longer comes from lexicon self_report entries (spec DECISIONS.md:286); self-reported prior and causation lines lose patient attribution\",\n   \"evidence\": \"app/backend/grounding.py:174-176 `def _self_report(text): return bool(_SELF.search(text))` (round-2 diff deleted `or any(rx.search(text) for rx in _lexicon()['self_report'].values())`). Spec memory/DECISIONS.md:286: 'source_kind = \\\"patient_report\\\" is set by code from the lexicon self_report entries on the excerpt'. app/llm/lexicon.yaml:25-26 header: 'code sets source_kind = \\\"patient_report\\\" from it (ADR-013)'. Flag-level output artifacts/review-evidence/T-036-r2-probe5.txt: `'Patient notes prior neck pain.' type=pre_existing category=pre_existing source_kind=record title='Mention of a prior or pre-existing condition'` (lexicon self_reported_prior hit); `'Patient links her neck pain to the collision.' type=causation category=patient_report source_kind=record title='Patient self-report'`; control `'Patient reports prior neck pain.' ... source_kind=patient_report`. Sweep T-036-r2-probe.txt section 3: 'Subjective: neck pain 7/10.', 'Patient describes neck pain since the collision.', 'Patient-reported neck pain 7/10.' are lexicon hits with has_self_report=False.\",\n   \"why_it_matters\": \"The spec says the lexicon's self_report entries drive source_kind. The round-2 change removed that for every entry, not only the intake-form entry round 1 named. A patient's pre-existing or causation statement now reads as a record statement in the structured field, and for the pre-existing line the title carries no self-report attribution (checklist 9, 10). The verbatim quote still says 'Patient notes', so nothing is invented, but the attribution the spec requires is lost.\",\n   \"fix\": \"Restore the lexicon contribution in grounding._self_report (regex OR any lexicon self_report entry on the excerpt). Set self_report: false on intake_form_accident_date (lexicon.yaml:759-764) so the record-7 date stays 'record'. Remove EMS, witness, wife, husband, family and friend from patient_reports_generic (lexicon.yaml:743-746), because an EMS report is not a patient statement. If the narrowing was intended, amend DECISIONS.md:286 and lexicon.yaml:25-26 in the same commit (see questions_for_chris).\",\n   \"acceptance_test\": \"tests/unit/test_flags_pass.py: lexicon_flags on 'Patient notes prior neck pain.' and 'Patient links her neck pain to the collision.' give source_kind == 'patient_report'; 'Date of accident per intake form: 2026-01-19.' gives 'record'; grounding.has_self_report('EMS reports neck pain 7/10.') is False; the existing record-9 and record-7 tests still pass.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Conflict-pass failure is visible on the flag, but the run still reports status done with no warning or error\",\n   \"evidence\": \"artifacts/review-evidence/T-036-r2-probe.txt section 2: 'conflicts LLMFailed: status=done errors=[] warnings=[]' and 'conflicts FixtureMiss: status=done errors=[] warnings=[]'. artifacts/review-evidence/T-036-r2-probe4.txt: 'status: done errors: [] warnings: []'. app/backend/flags.py:183 docstring: 'pipeline adds a run warning (`pipeline_warning`) so the run is shown as partial'. grep -rn 'pipeline_warning' app/ returns only flags.py:183 and flags.py:188 (the flag key); app/backend/pipeline.py:304 `status = 'done_with_errors' if errors else 'done'` never reads it.\",\n   \"why_it_matters\": \"Round 1 asked for a visible item and a pipeline warning. The item exists, so the attorney sees 'Cross-record check did not finish' in the flags list. The run-level signal is missing, and the docstring claims it exists, so a reader is told the run is partial when the status says done. That is the silent-pass concern in another form. Major, not blocker, because the visible needs_review flag does reach the reviewer.\",\n   \"fix\": \"In pipeline.py, read the conflict-stage flag's pipeline_warning and append a warning {code: 'CONFLICT_PASS_INCOMPLETE', stage: 'conflicts'} to out['warnings'], and set status to 'done_with_errors' or a partial marker. Or correct the docstring and the handoff if the run-level status is out of scope.\",\n   \"acceptance_test\": \"test_pipeline.py: run_sample(..., conflicts=AU.LLMFailed('down')) -> 'CONFLICT_PASS_INCOMPLETE' in [w['code'] for w in out['warnings']] and out['status'] != 'done'; the same for P.FixtureMiss.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Full unit suite is still red: 5 failures in test_t037_backend.py (round 1 reported 3, all now in a different file)\",\n   \"evidence\": \".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -6 -> '5 failed, 750 passed in 10.12s'. Failures: test_t037_backend.py::test_replay_has_no_fixture_miss[case_02_gap_boundaries] (view errors: LLM_FAILED_AFTER_RETRIES at extract, record 1, cause FIXTURE_MISS; line 36), [case_08_diagnosis_temptation] (flag 'Clinical correlation recommended.' has reasons incl. FIXTURE_MISS; line 38), [case_09_nonvisit_hides_gap] (line 36), test_judge_lines_replay (H01: judge_summary returns 'unavailable'; line 52), test_fixtures_come_only_from_golden_text (message 'text is not an evals/golden input; refusing to record' vs expected 'not in evals/golden'; line 62). The round-1 test_pipeline.py J3 failures now pass: .venv/bin/python -m pytest tests/unit/test_pipeline.py tests/unit/test_flags_pass.py tests/unit/test_conflicts.py -q -> 45 passed.\",\n   \"why_it_matters\": \"A green unit suite is the gate the handoff relies on. Five red tests with no owner named keep the 'verified' claim unsupported. Scope note: board AC2 says the full fixture run waits for T-037, so these may belong to T-037. I did not check out HEAD~1 to prove cd4bc60 is not the cause, and I did not downgrade for that.\",\n   \"fix\": \"Either fix the golden fixtures for case_02, case_08 and case_09 and the judge line, or name the owning card for each failure in the handoff and make the suite count explicit.\",\n   \"acceptance_test\": \".venv/bin/python -m pytest tests/unit -q reports 0 failed, or the handoff lists each failing test with its owning card and the board shows that card in progress.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Case-wide conflict-pass warning is attached to record 1, and its why text says record 1 has no AI entry\",\n   \"evidence\": \"artifacts/review-evidence/T-036-r2-probe4.txt: 'f_cx1 record_warning ['r1'] needs_review' and 'entries with record 1: [('e1', ['r1'])]'. app/backend/flags.py:186-187 sets record_no=records[0]['n']. Why text from app/backend/why.py:28 'The AI step failed on all three attempts, so this record has no AI-made entry.' (LLM path); why.py:16 'The demo has no recorded AI answer for this step...' (FixtureMiss path).\",\n   \"why_it_matters\": \"The warning concerns the conflict check across all records, but it is pinned to record 1 and says record 1 has no AI entry. Record 1 does have entry e1. A paralegal could read it as record 1 being left out of review. The explanation text ('conflicts between records may be missing') is accurate; the attribution and the why are not.\",\n   \"fix\": \"Leave record_ids empty for the case-level warning, or attach it to every distinct record. Give it a conflict-specific why code instead of the per-record LLM_FAILED_AFTER_RETRIES text.\",\n   \"acceptance_test\": \"run_sample with conflicts=AU.LLMFailed: the f_cx record_warning has no single record_id, and its why does not contain 'has no AI-made entry'.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Every quote template still ends in a double period, '.”.'\",\n   \"evidence\": \"artifacts/review-evidence/T-036-r2-probe.txt section 1: 'Capital PT (January 23, 2026) mentions a prior or pre-existing condition: “Cervical ROM full, no spasm noted.”.' Same pattern in all quote templates (flag_templates.py _quote usage).\",\n   \"why_it_matters\": \"A quote that already ends in a period followed by a second one reads as careless in a document that goes to counsel. Carried from round 1; not changed.\",\n   \"fix\": \"Omit the template period after a closing quote, or strip the quote's trailing period.\",\n   \"acceptance_test\": \"No rendered explanation in flag_templates.TEMPLATES contains the sequence '.”.'.\"}\n ],\n \"whats_right\": [\n  \"The objective_negative title is neutral: 'Normal or absent findings wording'. No 'objective' or 'subjective' appears in any rendered title or explanation outside the verbatim quote, across 21 categories.\",\n  \"Record 7's intake-form date is source_kind 'record' (probe5), and a conflict-pass failure (LLMFailed or FixtureMiss) now yields a visible needs_review item instead of an empty list.\",\n  \"A single-quote conflict is rejected as SCHEMA_INVALID (test_flags_pass.py::test_single_quote_conflict_is_rejected passes), so the round-1 garbled 'the record.' rendering cannot reach the review.\"\n ],\n \"questions_for_chris\": [\n  \"Was narrowing grounding._self_report to regex-only an intended decision? If yes, DECISIONS.md:286 and lexicon.yaml:25-26 are stale and need amending; if no, finding 1 stands as written.\",\n  \"Is the 5-test red set in test_t037_backend.py owned by T-037 (board AC2 defers the full fixture run to T-037)? If so, should T-036 be allowed to hand off with the unit suite red?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:04:52.255Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-036-claims-adjuster-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:54.831Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json,re\nt=open('reviews/T-036-claims-adjuster-r2.md').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd=json.loads(blocks[0])\nsev=[f['severity'] for f in d['findings']]\nprint('verdict', d['verdict'], 'severities', sev, 'model', d['model'])\nexp='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('verdict rule ok:', exp==d['verdict'])\n\"",
 "description": "Validate JSON block and verdict rule in review file"
}
````

### User / tool · 2026-11-02T02:04:54.884Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:56.719Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-036-r2-validate.py <<'EOF'\nimport json, re\nt = open(\"/Users/arsis/zlayt-pm-project/reviews/T-036-claims-adjuster-r2.md\").read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict\", d[\"verdict\"], \"severities\", sev, \"model\", d[\"model\"])\nprint(\"verdict rule ok:\", exp == d[\"verdict\"])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-036-r2-validate.py",
 "description": "Validate review JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T02:04:56.823Z

**tool result**
````
json blocks: 1
verdict fail severities ['blocker', 'major', 'major', 'minor', 'nit'] model claude-haiku-5-5
verdict rule ok: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:01.990Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_flag_source_kind_and_run_signal.md",
 "content": "---\nname: flag-source-kind-and-run-signal\ndescription: T-036 r2 (cd4bc60): source_kind narrowed to regex-only, dropping the lexicon self_report contract (DECISIONS.md:286); conflict-pass warning documented as run-level but never read by pipeline.py\nmetadata:\n  type: project\n---\n\nRound 2 of T-036 fixed the round-1 intake-date mislabel by deleting the lexicon `self_report` contribution from `grounding._self_report` for every entry. The spec (memory/DECISIONS.md:286) says source_kind is set by code from the lexicon self_report entries. Result: \"Patient notes prior neck pain.\" and \"Patient links her neck pain to the collision.\" lose source_kind=patient_report, and the pre-existing line's title carries no self-report attribution.\n\nAlso: a docstring at app/backend/flags.py:183 claims the pipeline adds a `pipeline_warning` run warning. Nothing reads `pipeline_warning` (grep app/ shows only the flag key). Run status stays `done` on LLMFailed/FixtureMiss.\n\n**Why:** a fix narrowed to the one named entry (intake date) grew into removing a mechanism the spec requires. A round-1 suggestion (\"remove self_report from intake\") was over-applied.\n\n**How to apply:** when a finding's fix touches a classifier or label, check the spec line that defines the mechanism (DECISIONS.md, lexicon header) and probe at flag level (lexicon_flags on the lexicon's own hit examples), not only the named example. For \"pipeline warning\" claims, grep for the consumer. Evidence: artifacts/review-evidence/T-036-r2-probe*.py and their .txt outputs.\n\nRelated: [[feedback_lexicon_review_method]], [[project_flag_pass_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T02:05:02.086Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_flag_source_kind_and_run_signal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:03.071Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:05:03.077Z

**tool result**
````
1	- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
2	- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r4: omissions, invented Rivera facts, partial scope fixes (line 34 left open at r4); sweep prose + golden must-not regex
3	- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite
4	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:05.117Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "old_string": "- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite\n",
 "new_string": "- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite\n- [Source-kind narrowing and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2: source_kind dropped lexicon self_report (DECISIONS.md:286); pipeline_warning never read\n"
}
````

### User / tool · 2026-11-02T02:05:05.219Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:06.603Z

T-036 round 2 (cd4bc60) is a **fail**: 1 blocker (source_kind no longer driven by lexicon self_report, contrary to DECISIONS.md:286), 2 majors, 1 minor, 1 nit. Review is at /Users/arsis/zlayt-pm-project/reviews/T-036-claims-adjuster-r2.md (model claude-haiku-5-5).
