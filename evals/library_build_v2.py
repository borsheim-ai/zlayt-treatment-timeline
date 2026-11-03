#!/usr/bin/env python3
"""Builds evals/library/case_lib08..lib15 (.txt + .expected.json, golden/1 schema) from the compact specs below (T-079).

Same idea as research/library_build.py (v1 packets lib01-lib07, researcher-owned): the SPECS are hand-authored content, the script only
does the mechanical parts that evals/golden/check_golden.py independently re-verifies (record numbering, entries, gap table, gap flags,
totals, letter/ui lines). It reuses that file's helpers (rec, amt, flag, span, mn_*) by import and adds what v2 needs: ambiguous or
missing header dates, merged duplicate records, record warnings.

Run:  .venv/bin/python evals/library_build_v2.py      (writes evals/library/case_lib08..15*)
      python3 research/validate_library.py            (check_golden over golden + library; identifier denylist)

Scenario shapes come from research/case-library-sources-v2.md (P1-P17) and layouts from research/record-formats.md. Everything is
INVENTED and SYNTHETIC: names, providers, places, dates (2026-2027) and amounts. Each excerpt is ONE line (the golden checker's
parser reads one line per excerpt), so multi-line forms (ledgers, UB-04, CMS-1500, EOB) are flattened with '; ' between lines.

Golden-schema limits worth knowing:
 * kind is encounter | billing_statement | phone_note. Letters, affidavits and carrier correspondence are non-encounters, so they use
   phone_note (the nearest non-encounter kind; the product calls them records_admin). All three are excluded from gap arithmetic.
 * Flag types are gap | conflict | pre_existing | causation. Credibility wording (D-043) is a causation-type flag, category
   credibility_language. A cross-document billing mismatch is a tolerated conflict, not a required one (billing analysis is not a flag).
 * must_not amount_value never lists a value that the golden itself expects (a rate or an estimate keeps its value in amounts[]).
"""
import datetime as dt
import importlib.util
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "evals" / "library"
_spec = importlib.util.spec_from_file_location("library_build_v1", ROOT / "research" / "library_build.py")
V1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V1)
HEADER, rec, amt, flag, span, mn_amount, mn_judge, mn_regex = (V1.HEADER, V1.rec, V1.amt, V1.flag, V1.span, V1.mn_amount, V1.mn_judge, V1.mn_regex)

SELF = ["patient states", "per patient", "patient reports"]
PT = ["pt states", "patient states", "per patient", "patient reports", "reports"]
SRC = "research/case-library-sources-v2.md"


def R(date, source, excerpt, must, terms=(), spans=(), kind="encounter", raw=None, status="parsed", cands=None, dup_of=None, note=None):
    """v1 rec() plus v2 fields. date=None means the header date does not parse to one ISO day (status ambiguous or missing)."""
    r = rec(date, source, excerpt, kind=kind, must=must, terms=terms, spans=spans, note=note, raw=raw)
    r.update(status=status, cands=cands or [], dup_of=dup_of)
    return r


def A(record_no, raw, value, cls, excerpt, required=True, note=None):
    return amt(record_no, raw, value, cls, excerpt, required=required, note=note)


def build(sp):
    recs = sp["records"]
    lines = [HEADER, ""]
    for i, r in enumerate(recs, 1):
        lines += [f"=== Record {i} ===", f"Date: {r['raw']}", f"Source: {r['source']}", f'Excerpt: "{r["excerpt"]}"', ""]
    txt = "\n".join(lines)
    records = [{"record_no": i, "raw_date": r["raw"], "date": r["date"], "kind": r["kind"], "source": r["source"]} for i, r in enumerate(recs, 1)]

    entries, entry_of = [], {}
    for i, r in enumerate(recs, 1):
        if r["dup_of"]:
            e = entry_of[r["dup_of"]]
            e["record_nos"].append(i)
            assert r["excerpt"] == recs[r["dup_of"] - 1]["excerpt"] and r["source"] == recs[r["dup_of"] - 1]["source"] and r["date"] == recs[r["dup_of"] - 1]["date"], (sp["case_id"], i)
            continue
        e = {"id": f"E{len(entries) + 1}", "record_nos": [i], "date": r["date"], "date_status": r["status"], "encounter": r["kind"] == "encounter",
             "provider": r["source"], "must_contain_excerpt": r["must"], "required_terms": r["terms"]}
        if r["spans"]:
            e["self_report_spans"] = r["spans"]
        if r["status"] != "parsed":
            e["needs_review"] = True
            if r["cands"]:
                e["date_candidates"] = r["cands"]
        if r["note"]:
            e["note"] = r["note"]
        entries.append(e)
        entry_of[i] = e

    by, excluded = {}, []
    for i, r in enumerate(recs, 1):
        if r["kind"] == "encounter" and r["date"]:
            by.setdefault(r["date"], []).append(i)
        else:
            excluded.append(i)
    ds = sorted(by)
    gap_table = []
    for a, b in zip(ds, ds[1:]):
        days = (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days
        gap_table.append({"from_date": a, "to_date": b, "from_records": by[a], "to_records": by[b], "days": days, "flag": days > 30})

    flags = []
    for gid, ri_from, ri_to, ev_from, ev_to in sp["gap_flags"]:
        a, b = recs[ri_from - 1]["date"], recs[ri_to - 1]["date"]
        days = (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days
        assert days > 30, (sp["case_id"], gid, days)
        flags.append({"id": gid, "type": "gap", "level": "must", "from_date": a, "to_date": b, "days": days,
                      "cite": {"all": [ri_from, ri_to], "any": []},
                      "evidence": [{"record_no": ri_from, "field": "excerpt", "excerpt": ev_from},
                                   {"record_no": ri_to, "field": "excerpt", "excerpt": ev_to}],
                      "summary": f"Treatment gap of {days} days ({a} to {b}), longer than 30."})
    assert {(g["from_date"], g["to_date"]) for g in gap_table if g["flag"]} == {(f["from_date"], f["to_date"]) for f in flags}, sp["case_id"]
    flags += sp["flags"]

    amounts = []
    for n, a in enumerate(sp["amounts"], 1):
        d = {"id": f"A{n}", "record_no": a["record_no"], "raw": a["raw"], "value": a["value"], "class": a["cls"], "excerpt": a["excerpt"],
             "in_total": a["in_total"], "required": a["required"], "needs_review": a["needs_review"]}
        if a["note"]:
            d["note"] = a["note"]
        amounts.append(d)
    total = round(sum(a["value"] for a in amounts if a["in_total"]), 2)
    counted = [a["id"] for a in amounts if a["in_total"]]
    # every amount that is not counted (rate, estimate, unclear) is listed with its reason, as in lib01/lib06
    not_counted = {a["id"]: ((a["note"] or "not a charge").rstrip(".") + ("" if (a["note"] or "").endswith("needs review") else "; needs review")) for a in amounts if not a["in_total"]}
    unclear_items = [{"amount_id": k, "reason": v, "total_computed": False} for k, v in not_counted.items()]
    raw_of = {a["id"]: a["raw"] for a in amounts}
    totals = {"explicit_charges_total": total, "counted_amount_ids": counted, "amounts_found": len(amounts),
              "status": "partial_unclear" if unclear_items else "complete", "unclear_items": unclear_items,
              "letter_line": f"Billed charges accepted from these records: ${total:,.2f}", "ui_line": f"Accepted charges: ${total:,.2f}",
              "notes_lines": [f"{raw_of[k]}: {v}" for k, v in not_counted.items()]}
    assert abs(total - sp["expect_total"]) < 0.005, (sp["case_id"], total, sp["expect_total"])
    if sp.get("accept_all"):        # D-059: what the letter prints when every acceptable line is accepted one at a time, with the written reason it differs
        totals["accept_all_total"], totals["accept_all_reason"] = sp["accept_all"]

    ex = {"schema_version": "golden/1", "case_id": sp["case_id"], "synthetic": True, "input_file": sp["case_id"] + ".txt",
          "description": sp["description"], "stress_types": sp["stress_types"], "records": records, "entries": entries,
          "expected_entry_count": len(entries), "gap_excluded_records": excluded, "gap_table": gap_table, "amounts": amounts,
          "totals": totals, "flags": flags, "must_not_flag": sp["must_not_flag"], "tolerated": sp["tolerated"],
          "record_warnings": sp.get("record_warnings", []), "must_not": sp["must_not"],
          "notes": [f"Library packet (T-079); scenario shapes: {sp['patterns']} in {SRC}; layouts in research/record-formats.md. All names, "
                    "providers, places, dates and amounts are invented."] + sp["notes"]}
    return txt, ex


ACCEPT_ALL_LIB09 = ("Hand-verified: ED charge $2,940 + MRI charge $2,150 + the statement's consultas line $1,300 (2 x $650; the note's own $650 consult is inside it, counted once) = $6,390; "
                    "the four therapy sessions are a rate ($400 per session, sessions billed not stated) and the $2,900 saldo repeats the lines. A Spanish figure stays `unclear` until the paralegal reads the "
                    "original and reclassifies it (D-050), so accepting the acceptable lines one at a time gives $5,090.00 (ED + MRI); $6,390.00 is reached after she reclassifies the $1,300.00 consultas line.")

SPECS = []

# ───────────────────────── lib08: second crash before the first MRI (P1 + P13) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib08_second_crash_mri_after", patterns="P1 + P13", expect_total=11240,
    description="Library L8 (P1+P13). Pre-suit file: rear-end collision, ED, orthopedics, 11 weeks of PT, then a second collision 11 days after PT discharge (EMS in a hard collar, ED), the first MRI only after crash 2, an orthopedic note that dates the arm numbness to crash 1, and a neurology note with a loss-of-consciousness history that the ED denied. Two incident dates, a conflicting LOC history and a 42-day gap before neurology; the tool never apportions between the crashes.",
    stress_types=["second_accident_between_care_and_imaging", "loc_history_changes", "history_attributes_to_first_event", "ems_run_report", "gap_before_specialist", "rate_not_charge"],
    records=[
        R("2026-01-12", "Pelham Ridge EMS run report", "Restrained driver of a sedan struck from behind at a stoplight. Pt states neck pain 6/10. Denies LOC. Ambulatory at scene. Transported to Thornbury Regional ED.",
          "struck from behind at a stoplight", ["neck pain", ["denies loc", "denies loss of consciousness", "no loss of consciousness"]], [span("Pt states neck pain 6/10.", PT)]),
        R("2026-01-12", "Thornbury Regional ED", "Dx: cervical strain. CT head negative. Denies LOC per patient. Discharged on cyclobenzaprine. ED charge: $4,210.",
          "Dx: cervical strain", ["cervical strain", ["ct head negative", "negative ct", "head ct"]], [span("Denies LOC per patient.", ["per patient", "patient denies", "denies loc"])]),
        R("2026-01-16", "Dr. Philippa Wenlock, orthopedics, new patient", "Neck pain 5/10 without arm symptoms. Date of accident per intake form: 2026-01-12. Plan: physical therapy twice weekly.",
          "Neck pain 5/10 without arm symptoms", ["5/10", "physical therapy"]),
        R("2026-01-26", "Larkmoor Physical Therapy, initial evaluation", "Cervical range of motion reduced about 25%. Plan of care: 12 weeks, twice weekly. Charge per visit $145.",
          "Cervical range of motion reduced about 25%", ["25%"]),
        R("2026-02-23", "Larkmoor Physical Therapy, visit 12", "Pain 4/10. Home exercise program progressed.", "Pain 4/10", ["4/10"]),
        R("2026-03-23", "Larkmoor Physical Therapy, visit 22", "Pain 3/10. Range of motion improving.", "Pain 3/10", ["3/10"]),
        R("2026-04-13", "Larkmoor Physical Therapy, discharge", "Discharged from PT after 11 weeks, goals partly met. Pain 3/10.", "Discharged from PT after 11 weeks", ["discharged", "3/10"]),
        R("2026-04-24", "Pelham Ridge EMS run report", "Restrained driver in a second collision, struck on the driver side. Hard cervical collar applied. Pt states neck pain 8/10 and left arm numbness. Transported to Thornbury Regional ED.",
          "Hard cervical collar applied", ["collar", "left arm numbness"], [span("Pt states neck pain 8/10 and left arm numbness.", PT)]),
        R("2026-04-24", "Thornbury Regional ED", "Dx: cervical strain. CT cervical spine negative for fracture. Denies LOC per patient. ED charge: $4,680.",
          "CT cervical spine negative for fracture", ["cervical strain", "negative for fracture"], [span("Denies LOC per patient.", ["per patient", "patient denies", "denies loc"])]),
        R("2026-05-20", "Valley Imaging, cervical MRI", "C5-C6 disc herniation with mild canal narrowing. No prior imaging available for comparison. MRI charge: $2,350.",
          "C5-C6 disc herniation with mild canal narrowing", ["c5-c6", "herniation"]),
        R("2026-06-02", "Dr. Philippa Wenlock, orthopedics, follow-up", "Neck pain 7/10 with left arm numbness since the rear-end collision of 2026-01-12. MRI reviewed. Recommend referral to neurosurgery.",
          "left arm numbness since the rear-end collision of 2026-01-12", ["7/10", "left arm numbness", "neurosurgery"]),
        R("2026-07-14", "Dr. Ansgar Kellerman, neurology", "Patient states brief loss of consciousness at the second collision. Headaches and word-finding difficulty since. Referred for neuropsychological testing.",
          "brief loss of consciousness at the second collision", ["loss of consciousness", "headaches", "neuropsychological"],
          [span("Patient states brief loss of consciousness at the second collision.", SELF)]),
    ],
    amounts=[A(2, "$4,210", 4210, "charge", "ED charge: $4,210"),
             A(4, "$145", 145, "rate", "Charge per visit $145", note="Rate, not a charge: visits billed are never stated (12 weeks planned)."),
             A(9, "$4,680", 4680, "charge", "ED charge: $4,680"),
             A(10, "$2,350", 2350, "charge", "MRI charge: $2,350")],
    unclear={},
    gap_flags=[("G1", 11, 12, "Recommend referral to neurosurgery", "Headaches and word-finding difficulty since")],
    flags=[
        flag("C1", "conflict", "must", [9, 12], [(9, "excerpt", "Denies LOC per patient"), (12, "excerpt", "Patient states brief loss of consciousness at the second collision")],
             "LOC history differs: the ED record of the second collision has the patient denying LOC; neurology records the patient stating brief LOC at that collision. Both shown with attribution; the tool does not choose.", "loc_history_changed"),
        flag("C2", "conflict", "must", [3, 8], [(3, "excerpt", "Date of accident per intake form: 2026-01-12"), (8, "excerpt", "Restrained driver in a second collision")],
             "Two incidents in the chart: an intake accident date of 2026-01-12 and a second collision recorded by EMS on 2026-04-24. Human step: confirm which records belong to which event; the tool never apportions.", "second_incident"),
        flag("C3", "conflict", "should", [3, 11], [(3, "excerpt", "without arm symptoms"), (11, "excerpt", "left arm numbness since the rear-end collision of 2026-01-12")],
             "The 2026-06-02 note dates the left arm numbness to the first collision; the 2026-01-16 note records no arm symptoms and left arm numbness first appears in the 2026-04-24 EMS record. Both cited.", "history_attributes_to_first_event"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 4, 10, 28, 28, 21, 11, 26 and 13-day intervals."}],
    tolerated=[flag("T1", "causation", "tolerated", [10], [(10, "excerpt", "C5-C6 disc herniation with mild canal narrowing")],
                    "The first MRI is dated after the second collision; may be raised for review but the tool links it to neither event.", "first_imaging_after_second_event")],
    must_not=[
        mn_judge("M1", "Apportions the injury or the herniation between the two collisions, or says which collision caused it; no record does.",
                 ["The second collision caused the herniation.", "The herniation is from the first accident, not the second.", "Most of the neck injury came from the January crash."],
                 ["Left arm numbness first appears in the 2026-04-24 EMS record.", "The 2026-06-02 note dates the numbness to the 2026-01-12 collision.", "First MRI is dated 2026-05-20."]),
        mn_judge("M2", "States as the tool's own fact that she did or did not lose consciousness; the ED has the patient denying it and neurology has the patient stating it.",
                 ["She lost consciousness in the second collision.", "There was no loss of consciousness at either crash.", "She was knocked out in the second crash."],
                 ["Patient states brief loss of consciousness at the second collision.", "ED record of 2026-04-24: denies LOC per patient.", "LOC history differs between the ED and neurology records."]),
        mn_judge("M3", "Diagnoses a concussion or brain injury; the records chart headaches and word-finding difficulty only.",
                 ["She suffered a concussion in the second collision.", "Traumatic brain injury after the crash.", "Post-concussion syndrome developed."],
                 ["Headaches and word-finding difficulty since.", "Referred for neuropsychological testing.", "CT head negative."]),
        mn_amount("M4", "Multiplies or adds the per-visit rate, or treats percentages, weeks and pain scores as dollars (values 1,740 / 11,385 / 12,980 / 25 / 11).", [1740, 11385, 12980, 25, 11]),
    ],
    notes=["Hand arithmetic: 01-12 to 01-16 = 4; to 01-26 = 10; to 02-23 = 5 + 23 = 28; to 03-23 = 28; to 04-13 = 8 + 13 = 21 (about 11 weeks of PT from 01-26); to 04-24 = 11; to 05-20 = 6 + 20 = 26; to 06-02 = 11 + 2 = 13; to 07-14 = 28 + 14 = 42 (flag).",
           "Charges counted: 4,210 + 4,680 + 2,350 = 11,240. Forbidden guess-sums: 12 x 145 = 1,740; 11,240 + 145 = 11,385; 11,240 + 1,740 = 12,980.",
           "Pre-suit file: every record came from the firm's own request to that provider. Records 1-2, 8-9 are EMS and ED pairs for the two crashes; the orthopedic history in record 11 omits the second crash."]))

# ───────────────────────── lib09: Spanish-language note, interpreter, side flip (P9 + P4 + P11) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib09_spanish_interpreter_espalda", patterns="P9 + P4 + P11", expect_total=6390,
    accept_all=(5090, ACCEPT_ALL_LIB09),
    description="Library L9 (P9+P4+P11). Pedestrian struck in a parking lot. English ED record with history via the patient's son (left shoulder), a Spanish-language clinic note (day-first date, 'espalda' with no level, right shoulder), an English orthopedic note with a family interpreter (right shoulder, a different mechanism), a scanned Spanish intake form as OCR text with an ambiguous numeric date, and a Spanish statement of account. Side flips between ED and the later records; the excerpt stays in Spanish and any English rendering must be labeled as a translation.",
    stress_types=["spanish_language_record", "ad_hoc_interpreter", "left_right_transposition", "espalda_no_level", "day_first_date", "ambiguous_numeric_date", "ocr_noise_text", "rate_not_charge", "balance_double_count_trap"],
    records=[
        R("2026-03-03", "Quillmere Regional ED", "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940.",
          "Left shoulder pain 7/10", ["left shoulder", "negative for fracture"], [span("Patient states she was struck by a car while walking in a parking lot.", SELF)]),
        R("2026-04-14", "Consultorio Médico Aguaclara, nota de consulta", "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00.",
          "dolor de espalda y hombro derecho desde el atropello del 3 de marzo", [["hombro derecho", "right shoulder"], "6/10"],
          [span("Refiere dolor 6/10 que empeora al levantar el brazo.", ["refiere", "patient reports", "patient states", "reports", "per patient"])], raw="14/04/2026",
          note="Day-first numeric date (14 > 12, so unambiguous). Spanish excerpt stays in Spanish; an English summary must be labeled as a translation (D-042)."),
        R("2026-04-21", "Dr. Lucan Ostrowe, orthopedics, new patient", "Interpreter: patient's daughter. Patient states she fell in the parking lot after a car brushed her. Right shoulder pain 6/10. MRI right shoulder ordered.",
          "Right shoulder pain 6/10", ["right shoulder", "6/10"], [span("Patient states she fell in the parking lot after a car brushed her.", SELF)]),
        R(None, "Consultorio Médico Aguaclara, formulario de admisión (OCR)", "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible.",
          "dolor de espaIda y hombro derecho", [["hombro derecho", "right shoulder"]], raw="03/05/2026", status="ambiguous", cands=["2026-03-05", "2026-05-03"],
          note="Ambiguous numeric date (both readings valid): must not be guessed. The clinic's other note uses day-first dates, so D-042's date-convention suggestion may pre-select 3 May 2026 with that reason; the paralegal still confirms once. OCR noise in the excerpt (O for 0, I for l) is kept as scanned."),
        R("2026-05-05", "Cinder Valley Imaging, right shoulder MRI", "Partial-thickness supraspinatus tear. MRI charge: $2,150.", "Partial-thickness supraspinatus tear", ["partial-thickness", "supraspinatus"]),
        R("2026-05-12", "Dr. Lucan Ostrowe, orthopedics, follow-up", "Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10.",
          "Recommend physical therapy and subacromial injection", ["physical therapy", "injection", "5/10"]),
        R("2026-05-20", "Consultorio Médico Aguaclara, estado de cuenta (billing statement)", "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00.",
          "Estado de cuenta", [], kind="billing_statement"),
    ],
    amounts=[A(1, "$2,940", 2940, "charge", "ED charge: $2,940"),
             A(2, "$650.00", None, "unclear", "Consulta: $650.00", required=False,
               note="The note's own consult fee; the statement's plural 'consultas' line is $1,300.00 (2 x $650.00) and the packet holds one consult note, so this fee is probably inside that line. Counted once, through the statement line"),
             A(2, "$400.00", 400, "rate", "Costo por sesión de terapia física: $400.00", note="Rate per session (costo por sesión), not a charge: sessions billed are not stated."),
             A(5, "$2,150", 2150, "charge", "MRI charge: $2,150"),
             A(7, "$1,300.00", 1300, "charge", "consultas $1,300.00", note="The billed consult line; counted instead of the $650.00 note fee, which it probably includes"),
             A(7, "$400.00", 400, "rate", "4 sesiones a $400.00 por sesión", required=False, note="Rate per session; the four sessions have no stated charge total."),
             A(7, "$2,900.00", None, "unclear", "Saldo: $2,900.00", note="Balance (saldo) equals $1,300.00 + 4 x $400.00; counting it would double count.")],
    unclear={"A7": "balance (saldo) $2,900.00 equals the consultation charge plus 4 therapy sessions at the rate; not counted; needs review"},
    gap_flags=[("G1", 1, 2, "Dx: left shoulder contusion", "dolor de espalda y hombro derecho")],
    flags=[
        flag("C1", "conflict", "must", [1, 3], [(1, "excerpt", "Left shoulder pain 7/10"), (3, "excerpt", "Right shoulder pain 6/10")],
             "Side differs: the ED record (history via the patient's son) has the left shoulder; the Spanish clinic note, the scanned intake and orthopedics have the right shoulder. Both sides cited; the tool never picks one (human step: confirm side).", "laterality_mismatch"),
        flag("C2", "conflict", "should", [1, 3], [(1, "excerpt", "Patient states she was struck by a car while walking in a parking lot."), (3, "excerpt", "Patient states she fell in the parking lot after a car brushed her.")],
             "Mechanism worded differently in two records, each through a family interpreter (struck by a car vs fell after a car brushed her). Both attributed to the patient; the tool does not reconcile them.", "mechanism_differs"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 7, 14 and 7-day intervals; the ambiguous-date intake (record 4) and the statement of account (record 7) are not gap endpoints."}],
    tolerated=[flag("T1", "causation", "tolerated", [2], [(2, "excerpt", "desde el atropello del 3 de marzo")],
                    "Patient-stated onset in Spanish; may be shown as the patient's report, never as the tool's causation finding.", "patient_stated_onset"),
               flag("T2", "conflict", "tolerated", [7], [(7, "excerpt", "terapia física, 4 sesiones a $400.00 por sesión")],
                    "The statement bills 4 therapy sessions and the packet holds no physical-therapy note (only a recommendation, record 6); a billed-without-a-note notice may be raised for review but is not required, and the product has no flag type for it.", "billed_sessions_without_notes")],
    record_warnings=[{"id": "W1", "type": "record_warning", "category": "date_ambiguous", "record_no": 4, "field": "date", "level": "must", "excerpt": "03/05/2026", "expected_state": "needs_review"}],
    must_not=[
        mn_judge("M1", "Resolves left vs right (picks a side, calls one record a charting error) or merges the two sides into one finding.",
                 ["The right shoulder was the injured side.", "The ED recorded the wrong side.", "Left shoulder injury was a charting error."],
                 ["ED record has left shoulder pain 7/10; orthopedics and the clinic note have the right shoulder.", "Side differs between the 2026-03-03 ED record and later records.", "Right shoulder pain 6/10."]),
        mn_regex("M2", "Gives 'espalda' a spinal level or region (cervical, thoracic, lumbar, upper or lower back); the note says 'dolor de espalda' and nothing more.",
                 r"(?i)\b(?:lower|upper|mid|low)[- ]?back\b|\blumbar\b|\bcervical\b|\bthoracic\b|espalda\s+(?:baja|alta|media)",
                 ["Lower back pain after the accident.", "Patient reports lumbar pain (espalda).", "Dolor de espalda baja y hombro."],
                 ["Back pain (espalda), level not stated.", "Dolor de espalda y hombro derecho.", "Back and right shoulder pain per the Spanish note."]),
        mn_judge("M3", "States that the collision caused the tear or the shoulder condition; the MRI says only 'partial-thickness supraspinatus tear'.",
                 ["The collision tore her rotator cuff.", "Partial-thickness tear caused by being struck by the car.", "Her shoulder tear is from the accident."],
                 ["Partial-thickness supraspinatus tear on MRI.", "Patient states she was struck by a car while walking in a parking lot.", "MRI right shoulder ordered."]),
        mn_judge("M4", "Shows an English rendering of the Spanish note as if it were the record's own text (an unlabeled translation), or replaces the Spanish excerpt with it.",
                 ["The note says: she has right shoulder and back pain since being run over on March 3.", "In English the record reads: pain 6/10 when lifting the arm.", "Record text: patient denies loss of consciousness."],
                 ["Machine translation (unverified): right shoulder and back pain since March 3.", "Excerpt (Spanish): Refiere dolor 6/10 que empeora al levantar el brazo.", "Translation label: this English line is an AI translation of the Spanish note."]),
        mn_amount("M5", "Counts the balance, double counts the balance with its parts, totals the per-session rate, or adds the $650.00 consult note to the $1,300.00 statement line (values 2,900 / 1,600 / 9,290 / 7,990 / 7,040).", [2900, 1600, 9290, 7990, 7040]),
    ],
    notes=["Hand arithmetic (encounters with a parsed date): 03-03 to 04-14 = 28 + 14 = 42 (flag); 04-14 to 04-21 = 7; 04-21 to 05-05 = 9 + 5 = 14; 05-05 to 05-12 = 7. Record 4 (ambiguous date) and record 7 (statement) are excluded.",
           "Charges counted: 2,940 + 2,150 + 1,300 = 6,390. Round-2 call (T-079 r2): the statement's plural 'consultas' line is $1,300.00 = 2 x $650.00 and the packet holds one consult note ($650.00, record 2), so the note's fee is most likely inside the statement line; the statement is the billing record, so it is counted and the note's $650.00 is listed unclear. Counting both ($7,040) would bill the same visit twice. Forbidden: 6,390 + 2,900 = 9,290; 6,390 + 1,600 = 7,990; 6,390 + 650 = 7,040; 4 x 400 = 1,600.",
           "Gap in the product (no flag type): the statement bills 4 therapy sessions at $400.00 ($1,600.00) but the packet holds no PT note. The product has no billed-without-a-note flag type (flag types are gap, conflict, pre_existing, causation; billing analysis is not a flag), so expected.json lists it only as tolerated T2 and the card records the gap.",
           "Spanish text is composed fresh. 'atropello' is a Spanish word for being hit by a vehicle; any English summary of it is a labeled LLM translation (D-042, T-085).",
           "Record 4 is an OCR-style scan: the letter O stands in for zero and a capital I for l (as in 'espaIda'), kept verbatim."]))

# ───────────────────────── lib10: EOB vs provider bill, UB-04 rate-vs-charge, CMS-1500 OCR (P6 + P14) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib10_eob_ub04_cms1500", patterns="P6 + P14", expect_total=8123.5,
    description="Library L10 (P6+P14). Pickup struck at an intersection, ED then three days of observation. A UB-04 itemized hospital bill with an accommodation rate beside the line charge and a 0001 total line, a health-plan EOB for the same dates of service whose 'amount billed' is $100.00 lower than the UB-04 total, and an orthopedic CMS-1500 OCR copy whose money boxes lost their decimal point. Only stated line charges count; the rate, the 0001 repeat, every EOB figure and every decimal-less box are not counted.",
    stress_types=["ub04_rate_vs_charge", "ub04_0001_total_line", "eob_vs_provider_bill_mismatch", "cms1500_ocr_decimal_less", "billing_statement_inside_gap", "no_double_count"],
    records=[
        R("2026-06-09", "Rainhollow Fire-Rescue run report", "Driver of a pickup struck at an intersection. Pt states chest wall and left knee pain. Ambulatory at scene. Transported to Saltmarrow General Hospital.",
          "Driver of a pickup struck at an intersection", ["left knee"], [span("Pt states chest wall and left knee pain.", PT)]),
        R("2026-06-09", "Saltmarrow General Hospital ED", "Dx: left knee contusion, chest wall contusion. X-ray left knee negative for fracture. Admitted for observation.",
          "X-ray left knee negative for fracture", ["left knee contusion", "observation"]),
        R("2026-06-12", "Saltmarrow General Hospital, discharge summary", "Discharged after 3 days of observation. Dx: left knee contusion. Follow up with orthopedics.",
          "Discharged after 3 days of observation", ["discharged", "orthopedics"]),
        R("2026-06-19", "Saltmarrow General Hospital, UB-04 itemized bill", "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 pharmacy, 14 units, FL47 total charges $386.50. Rev 0300 laboratory, 6 units, FL47 total charges $712.00. Rev 0001 total charges $8,123.50.",
          "FL44 rate $1,640.00 per day", ["room and board"], kind="billing_statement",
          note="UB-04 room line: FL44 rate x FL46 days = FL47 charge (1,640.00 x 3 = 4,920.00). The 0001 line repeats the sum of the lines."),
        R("2026-06-24", "Dr. Ignatius Wardlaw, orthopedics, new patient", "Left knee pain 5/10. MRI left knee ordered. Patient states his health plan was billed for the hospital stay.",
          "Left knee pain 5/10", ["5/10", "mri"], [span("Patient states his health plan was billed for the hospital stay.", SELF)]),
        R("2026-07-03", "Quoinmere Mutual Health Plan, EOB", "Explanation of benefits, processed 07/03/2026, for dates of service 06/09/2026 to 06/12/2026. This is not a bill. Amount billed $8,023.50; network discount $3,610.00; allowed amount $4,413.50; plan paid $3,530.80; you may owe $882.70.",
          "This is not a bill", [["explanation of benefits", "eob"]], kind="billing_statement"),
        R("2026-07-08", "Dr. Ignatius Wardlaw, orthopedics, follow-up", "Left knee pain 3/10. Injection performed. Continue home exercises.", "Injection performed", ["3/10", "injection"]),
        R("2026-07-14", "Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)", "OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units. Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00.",
          "OCR of scanned CMS-1500", [["cms-1500", "claim"]], kind="billing_statement",
          note="Money boxes print no decimal point (cents sit right of a bar). Truth by position: 185.00, 210.00, 96.00 and a total of 491.00 (185 + 210 + 96); the tool must not read 18500 as $18,500. Every OCR-derived amount goes to review."),
        R("2026-08-26", "Dr. Ignatius Wardlaw, orthopedics, follow-up", "Left knee pain 2/10. Discharged from care.", "Discharged from care", ["2/10", "discharged"]),
    ],
    amounts=[A(4, "$1,640.00", 1640, "rate", "FL44 rate $1,640.00 per day", note="Accommodation rate (FL44), not a charge; the FL47 charge on the same line is rate x days."),
             A(4, "$4,920.00", 4920, "charge", "FL47 total charges $4,920.00"),
             A(4, "$2,105.00", 2105, "charge", "FL47 total charges $2,105.00"),
             A(4, "$386.50", 386.5, "charge", "FL47 total charges $386.50"),
             A(4, "$712.00", 712, "charge", "FL47 total charges $712.00"),
             A(4, "$8,123.50", None, "unclear", "Rev 0001 total charges $8,123.50", note="0001 line repeats the sum of the four lines; counting it doubles the bill."),
             A(6, "$8,023.50", None, "unclear", "Amount billed $8,023.50", note="EOB restates the provider charge and differs from the UB-04 total by $100.00 (mismatch for review); not a second charge."),
             A(6, "$3,610.00", None, "unclear", "network discount $3,610.00", required=False, note="Network discount; not a charge."),
             A(6, "$4,413.50", None, "unclear", "allowed amount $4,413.50", note="Allowed amount, not a charge."),
             A(6, "$3,530.80", None, "unclear", "plan paid $3,530.80", note="Payment by the plan; paid vs incurred is a legal question, not a tool decision."),
             A(6, "$882.70", None, "unclear", "you may owe $882.70", required=False, note="Patient responsibility estimate on an EOB; not a charge."),
             A(8, "18500", None, "unclear", "CPT 99204, 18500, 1 unit", required=False, note="Decimal-less CMS-1500 box; truth 185.00 by position, OCR-derived, needs review."),
             A(8, "21000", None, "unclear", "CPT 20610, 21000, 1 unit", required=False, note="Decimal-less box; truth 210.00."),
             A(8, "96 OO", None, "unclear", "CPT 97110, 96 OO, 4 units", required=False, note="Letter O for zero; truth 96.00 for 4 units."),
             A(8, "49100", None, "unclear", "Item 28 TOTAL CHARGE 49100", required=False, note="Item 28; truth 491.00. The tool compares the line sum with Item 28 in code.")],
    unclear={"A6": "0001 line repeats the sum of the four UB-04 lines; not counted; needs review",
             "A7": "EOB amount billed $8,023.50 differs from the UB-04 total by $100.00; restated charge, not counted; needs review",
             "A9": "allowed amount; not a charge; needs review",
             "A10": "plan payment; paid vs incurred is a legal question, not a tool decision; needs review"},
    gap_flags=[("G1", 7, 9, "Continue home exercises", "Left knee pain 2/10")],
    flags=[],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 3, 12 and 14-day intervals; the UB-04 (record 4), EOB (record 6) and CMS-1500 (record 8) are not gap endpoints."}],
    tolerated=[flag("T1", "conflict", "tolerated", [4, 6], [(4, "excerpt", "Rev 0001 total charges $8,123.50"), (6, "excerpt", "Amount billed $8,023.50")],
                    "Same dates of service, $100.00 apart between the UB-04 total and the EOB amount billed; a billing-analysis mismatch may be raised for review but is not required as a flag.", "billing_amount_mismatch")],
    must_not=[
        mn_amount("M1", "Sums every money figure on the UB-04, doubles the bill with the 0001 line, adds the EOB's amount billed, or reads an EOB/allowed/paid figure as a charge (values 17,887 / 16,247 / 16,147 / 8,023.50 / 4,413.50 / 3,530.80 / 3,610 / 882.70).", [17887, 16247, 16147, 8023.5, 4413.5, 3530.8, 3610, 882.7]),
        mn_amount("M2", "Reads decimal-less CMS-1500 boxes as whole dollars (18500 -> $18,500) (values 18,500 / 21,000 / 9,600 / 49,100).", [18500, 21000, 9600, 49100]),
        mn_judge("M3", "Chooses between billed, allowed and paid as the real cost, says the hospital overcharged, or states what was incurred; paid vs incurred is for the attorney.",
                 ["The hospital was paid $3,530.80, so that is the real cost.", "The charges were inflated; the plan allowed only $4,413.50.", "The amount incurred is $4,413.50."],
                 ["UB-04 total charges $8,123.50; the EOB lists amount billed $8,023.50, allowed $4,413.50 and plan paid $3,530.80.", "UB-04 and EOB totals differ by $100.00 for the same dates of service; flagged for review.", "Billed charges accepted from these records: $8,123.50."]),
    ],
    notes=["Hand arithmetic: 06-09 to 06-12 = 3; 06-12 to 06-24 = 12; 06-24 to 07-08 = 6 + 8 = 14; 07-08 to 08-26 = 23 + 26 = 49 (flag). UB-04 (06-19), EOB (07-03) and CMS-1500 (07-14) are non-encounters and sit inside the 49-day gap.",
           "Charges counted: 4,920.00 + 2,105.00 + 386.50 + 712.00 = 8,123.50. Naive sum of every UB-04 figure: 8,123.50 + 8,123.50 + 1,640.00 = 17,887.00. EOB billed 8,023.50: 8,023.50 - 3,610.00 = 4,413.50 allowed; 4,413.50 x 0.8 = 3,530.80 plan paid.",
           "Pre-suit: the EOB came from the client's health plan; the UB-04 and CMS-1500 came from the providers. Dedupe must not merge them (same dates of service, different documents)."]))

# ───────────────────────── lib11: priors denied on intake, ledger with adjustment and payment, LOP (P5 + P2) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib11_priors_and_ledger", patterns="P5 + P2", expect_total=6000,
    description="Library L11 (P5+P2). Rear-end collision two weeks after an annual primary-care visit that lists two earlier car accidents, a chronic low back problem and a baseline back pain score. Attorney-referred spine clinic under a letter of protection, a scanned intake form (OCR text) answering 'prior accidents: No', and an itemized ledger with charges, a payment, a courtesy adjustment and a balance. Only stated charges count; payment, adjustment and balance are listed unclear.",
    stress_types=["intake_denies_prior_accidents", "prior_accidents_in_older_note", "baseline_back_pain_before_accident", "itemized_ledger_billed_adjusted_paid", "letter_of_protection", "ocr_noise_text", "attorney_referral", "balance_double_count_trap"],
    records=[
        R("2026-03-04", "Dr. Hesper Alderton, primary care", "Annual visit. History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. Problem list: hypertension, type 2 diabetes, chronic low back pain. Low back pain 3/10 today.",
          "car accidents in 2019 and 2022", ["2019", "2022", "chronic low back pain"],
          [span("History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.", SELF)]),
        R("2026-03-18", "Ashgrove Fire-Rescue run report", "Passenger vehicle struck from behind. Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED.",
          "Passenger vehicle struck from behind", ["low back pain"], [span("Pt states neck and low back pain 7/10.", PT)]),
        R("2026-03-18", "Wexcombe Memorial ED", "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260.",
          "X-ray cervical and lumbar spine negative for fracture", ["cervical strain", "lumbar strain"]),
        R("2026-03-26", "Pellingham and Rook PLLC, correspondence (letter of protection)", "Letter of protection to Fennimoor Spine Clinic. This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending. Please send complete records and an itemized statement.",
          "Letter of protection to Fennimoor Spine Clinic", [["letter of protection", "lop"]], kind="phone_note"),
        R("2026-03-27", "Fennimoor Spine Clinic, new patient", "Patient referred by attorney. Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly.",
          "Patient referred by attorney", ["referred by attorney", "letter of protection", "7/10"]),
        R("2026-03-27", "Fennimoor Spine Clinic, new patient intake form (OCR text)", "Date of injury: 3/l8/26. How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7. Signed 3/27/2G.",
          "Prior accidents? Yes [ ] No [X]", [["prior accident", "previous accident", "accidents"]], raw="3/27/26",
          note="Scanned form as OCR text: l for 1, I for l, G for 6 are kept as scanned. Header date 3/27/26 is unambiguous (27 > 12). The accident date inside the form is evidence for conflict checks only, never a service date."),
        R("2026-04-24", "Fennimoor Spine Clinic, visit 8", "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued.", "Neck pain 5/10, low back pain 6/10", ["5/10", "6/10"]),
        R("2026-05-29", "Fennimoor Spine Clinic, visit 14", "Neck pain 4/10, low back pain 5/10. Care continues.", "Neck pain 4/10, low back pain 5/10", ["4/10", "5/10"]),
        R("2026-06-15", "Fennimoor Spine Clinic, itemized ledger", "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.",
          "Account held under letter of protection", [["letter of protection", "lop"]], kind="billing_statement"),
    ],
    amounts=[A(3, "$3,260", 3260, "charge", "ED charge: $3,260"),
             A(9, "$250.00", 250, "charge", "New patient exam charge $250.00"),
             A(9, "$180.00", 180, "charge", "x-ray charge $180.00"),
             A(9, "$2,310.00", 2310, "charge", "charge $2,310.00"),
             A(9, "$2,740.00", None, "unclear", "total charges $2,740.00", note="Ledger total repeats the three ledger lines above; counting it double counts."),
             A(9, "$300.00", None, "unclear", "Payment received $300.00", note="Payment, not a charge."),
             A(9, "$274.00", None, "unclear", "Adjustment (courtesy discount) -$274.00", note="Adjustment with a negative sign; not a charge and never netted from billed."),
             A(9, "$2,166.00", None, "unclear", "Balance due $2,166.00", note="Balance = 2,740.00 - 300.00 - 274.00; derived, not a charge.")],
    unclear={"A5": "ledger total repeats the three ledger lines; not counted; needs review",
             "A6": "payment received; not a charge; needs review",
             "A7": "courtesy discount adjustment; not a charge; billed vs paid/incurred is a legal question, not a tool decision",
             "A8": "balance due after payment and adjustment; not a charge; needs review"},
    gap_flags=[("G1", 7, 8, "Manual therapy and exercises continued", "Neck pain 4/10, low back pain 5/10")],
    flags=[
        flag("P1", "pre_existing", "must", [1], [(1, "excerpt", "chronic low back pain")], "Problem list entry before the collision; stated as the record's wording only.", "prior_condition_listed"),
        flag("P2", "pre_existing", "must", [1], [(1, "excerpt", "car accidents in 2019 and 2022")], "Two earlier car accidents reported by the patient in a note dated two weeks before the collision.", "prior_accidents_reported"),
        flag("P3", "pre_existing", "should", [1], [(1, "excerpt", "Low back pain 3/10 today")], "Back pain score recorded before the collision.", "baseline_symptom_before_accident"),
        flag("C1", "conflict", "must", [1, 6], [(1, "excerpt", "car accidents in 2019 and 2022"), (6, "excerpt", "Prior accidents? Yes [ ] No [X]")],
             "The intake form answers 'Prior accidents? No' while the primary-care note of 2026-03-04 lists accidents in 2019 and 2022. Both cited; the tool does not say which is right.", "intake_denies_prior_accidents"),
        flag("K1", "causation", "should", [5], [(5, "excerpt", "Patient referred by attorney")],
             "Attorney referral and letter-of-protection treatment (internal notes only, D-001/D-018); the record wording is stated and no inference is drawn about charges.", "litigation_referral"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 14, 9 and 28-day intervals; the letter of protection (record 4) and the ledger (record 9) are not gap endpoints."}],
    tolerated=[],
    must_not=[
        mn_amount("M1", "Counts the ledger total, payment, adjustment or balance as a charge, or adds the total line to the lines (values 2,740 / 2,166 / 274 / 300 / 8,740).", [2740, 2166, 274, 300, 8740]),
        mn_judge("M2", "Nets the payment or adjustment into the billed figure, calls the charges reduced, reasonable or inflated, or states what was incurred.",
                 ["Charges after the courtesy discount total $5,726.", "The clinic reduced its bill to $2,166.00.", "The amount incurred is $2,166.00."],
                 ["Ledger lists total charges $2,740.00, payment $300.00, a courtesy discount and a balance due; none netted.", "Billed charges accepted from these records: $6,000.00.", "Account held under letter of protection."]),
        mn_regex("M3", "Calls the intake answer false or dishonest (lied, false, misrepresented).",
                 r"(?i)\b(?:lied|lying|false(?:ly)?|dishonest\w*|misrepresent\w*)\b",
                 ["She lied on the intake form.", "The intake answer was false.", "Dishonest answer about prior accidents."],
                 ["Intake form answer: Prior accidents? No.", "The 2026-03-04 note lists car accidents in 2019 and 2022, per patient.", "Intake and primary-care note differ; both cited."]),
        mn_judge("M4", "Decides the neck or back complaints are pre-existing, old, or not caused by the collision, or apportions between the earlier accidents and this one.",
                 ["Her back pain predates the collision.", "Most of the low back pain is from the 2022 accident.", "The collision did not cause her low back pain."],
                 ["Chronic low back pain is on the 2026-03-04 problem list.", "History per patient: car accidents in 2019 and 2022 with neck and low back pain.", "Low back pain 7/10 on 2026-03-18."]),
    ],
    notes=["Hand arithmetic (encounters): 03-04 to 03-18 = 14; 03-18 to 03-27 = 9 (records 5 and 6 share 03-27); 03-27 to 04-24 = 4 + 24 = 28; 04-24 to 05-29 = 6 + 29 = 35 (flag). The LOP letter (03-26) and the ledger (06-15) are non-encounters.",
           "Charges counted: 3,260 + 250 + 180 + 2,310 = 6,000. Ledger arithmetic: 250 + 180 + 2,310 = 2,740; 2,740 - 300 - 274 = 2,166. Forbidden: 6,000 + 2,740 = 8,740.",
           "Older notes come from the firm's records request to the PCP; the intake form is the clinic's. D-042 calibrated confidence: the tool shows measured precision per state for the pre-existing flags, never an invented percentage.",
           "Ledger columns follow P5's billing items 1-4 and 6 (billed, adjustment, payment, balance, LOP); the carrier-contract item is a separate document and is not in this packet."]))

# ───────────────────────── lib12: pre-suit records review, Waddell lines (P7 + P8) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib12_records_review_credibility", patterns="P7 + P8", expect_total=5790,
    description="Library L12 (P7+P8). Lumbar strain after a pickup collision, PCP, physical therapy with Waddell lines charted four ways (two clean negations, a positive count with inconsistent effort, a mixed-side sentence and a contrast sentence with 'symptom magnification'), a 49-day gap, and a carrier records-review letter received after the demand that restates the same Waddell lines and offers an opinion. Clean negations must not flag; every other credibility sentence must (D-043). The tool never concludes malingering and never adopts the carrier's opinion.",
    stress_types=["waddell_clean_negation", "waddell_positive_and_mixed", "waddell_mixed_side_sentence", "symptom_magnification_contrast", "carrier_records_review_letter", "dismissal_pattern_guard", "gap_after_pt", "rate_not_charge"],
    records=[
        R("2026-02-09", "Tallowby Fire-Rescue run report", "Restrained driver of a pickup struck at an intersection. Minor damage to the rear bumper. Pt states low back pain 6/10. Transported to Orrin Vale Community ED.",
          "Restrained driver of a pickup struck at an intersection", ["low back pain"], [span("Pt states low back pain 6/10.", PT)]),
        R("2026-02-09", "Orrin Vale Community ED", "Dx: lumbar strain. X-ray lumbar spine negative for fracture. Discharged on ibuprofen. ED charge: $2,780.", "X-ray lumbar spine negative for fracture", ["lumbar strain", "negative for fracture"]),
        R("2026-02-23", "Dr. Marisol Dunmore, primary care", "Low back pain 6/10, likely a strain superimposed on mild degenerative changes. Referred to physical therapy.", "mild degenerative changes", ["6/10", "physical therapy"]),
        R("2026-03-09", "Harrowmere Physical Therapy, initial evaluation", "Lumbar flexion limited. 0/5 Waddell signs. Pain 6/10. Plan of care: 12 visits.", "Lumbar flexion limited", ["6/10"]),
        R("2026-03-30", "Harrowmere Physical Therapy, visit 8", "Pain 5/10. No Waddell signs. Good effort. Core strengthening progressed.", "Core strengthening progressed", ["5/10"]),
        R("2026-04-20", "Harrowmere Physical Therapy, functional capacity evaluation", "Pain 6/10. Waddell 3/5 positive; effort inconsistent. Lifting tolerance 25 pounds.", "Waddell 3/5 positive", ["waddell", "3/5"]),
        R("2026-05-04", "Harrowmere Physical Therapy, visit 16", "Pain 5/10. Waddell signs negative on the left and positive on the right. Full effort, but symptom magnification noted with light touch.",
          "symptom magnification noted with light touch", ["5/10", "waddell"]),
        R("2026-06-22", "Dr. Marisol Dunmore, primary care, follow-up", "Low back pain 4/10. Patient states she missed two physical therapy visits in May. Refer to pain management.", "Refer to pain management", ["4/10", "pain management"],
          [span("Patient states she missed two physical therapy visits in May.", SELF)]),
        R("2026-07-15", "Marlowe Assurance Group, correspondence, records review letter", "Records review requested by the carrier after the demand; the reviewer did not examine the claimant. The PT note of 03/09/2026 documents 0/5 Waddell signs. The functional capacity evaluation of 04/20/2026 documents Waddell 3/5 and inconsistent effort. The PT note of 05/04/2026 documents full effort but symptom magnification with light touch. Opinion: findings are consistent with a self-limited lumbar strain; treatment after 04/20/2026 was not reasonable or necessary.",
          "Records review requested by the carrier after the demand", ["records review"], kind="phone_note",
          note="Pre-suit carrier peer-review letter, not an exam (a defense medical exam is a post-suit event). Its opinion is shown with attribution only."),
        R("2026-07-31", "Harrowmere Physical Therapy, itemized statement", "Itemized statement: initial evaluation charge $210.00; treatment visits 1 through 16 charge $2,320.00; functional capacity evaluation charge $480.00. Fee schedule $145.00 per visit.",
          "initial evaluation charge $210.00", [], kind="billing_statement"),
    ],
    amounts=[A(2, "$2,780", 2780, "charge", "ED charge: $2,780"),
             A(10, "$210.00", 210, "charge", "initial evaluation charge $210.00"),
             A(10, "$2,320.00", 2320, "charge", "treatment visits 1 through 16 charge $2,320.00"),
             A(10, "$480.00", 480, "charge", "functional capacity evaluation charge $480.00"),
             A(10, "$145.00", 145, "rate", "Fee schedule $145.00 per visit", note="Fee schedule rate with no date of service: a rate, not a charge.")],
    unclear={},
    gap_flags=[("G1", 7, 8, "symptom magnification noted with light touch", "Low back pain 4/10")],
    flags=[
        flag("K1", "causation", "must", [6], [(6, "excerpt", "Waddell 3/5 positive; effort inconsistent.")],
             "Credibility wording (D-043): a positive Waddell count with inconsistent effort. Shown verbatim with the provider and date; the tool draws no conclusion about the claimant.", "credibility_language"),
        flag("K2", "causation", "must", [7], [(7, "excerpt", "Waddell signs negative on the left and positive on the right.")],
             "Credibility wording (D-043): a Waddell sentence with a side qualifier is not a clean negation and flags.", "credibility_language"),
        flag("K3", "causation", "must", [7], [(7, "excerpt", "Full effort, but symptom magnification noted with light touch.")],
             "Credibility wording (D-043): a contrast sentence containing 'symptom magnification' flags even though it begins 'Full effort'.", "credibility_language"),
        flag("K4", "causation", "must", [9], [(9, "excerpt", "The functional capacity evaluation of 04/20/2026 documents Waddell 3/5 and inconsistent effort.")],
             "Carrier restates the FCE Waddell count and inconsistent effort; shown as the carrier's sentence with its source.", "credibility_language"),
        flag("K5", "causation", "must", [9], [(9, "excerpt", "The PT note of 05/04/2026 documents full effort but symptom magnification with light touch.")],
             "Carrier restates the contrast sentence; flags under D-043.", "credibility_language"),
        flag("K6", "causation", "should", [9], [(9, "excerpt", "The PT note of 03/09/2026 documents 0/5 Waddell signs.")],
             "The carrier's sentence is not itself a bare clean negation, so it flags under D-043 (an extra flag costs one click).", "credibility_language"),
        flag("K7", "causation", "should", [9], [(9, "excerpt", "Opinion: findings are consistent with a self-limited lumbar strain")],
             "Carrier reviewer's opinion; attributed to the carrier, never adopted by the tool.", "carrier_opinion"),
        flag("P1", "pre_existing", "should", [3], [(3, "excerpt", "mild degenerative changes")], "Degenerative wording in the PCP note; dismissable.", "degenerative_language"),
        flag("K8", "causation", "should", [8], [(8, "excerpt", "missed two physical therapy visits in May")], "Patient-stated missed care; dismissable.", "missed_care"),
        flag("K9", "causation", "should", [1], [(1, "excerpt", "Minor damage to the rear bumper")], "Scene fact in the EMS record; dismissable.", "scene_facts"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 14, 14, 21, 21 and 14-day intervals; the carrier letter (record 9) and the statement (record 10) are not gap endpoints."},
                   {"id": "N2", "type": "causation", "record_nos": [4], "statement": "Record 4 charts '0/5 Waddell signs.' alone: a clean negation (D-043 allow-list) must not flag."},
                   {"id": "N3", "type": "causation", "record_nos": [5], "statement": "Record 5 charts 'No Waddell signs.' and 'Good effort.': clean negations must not flag."}],
    tolerated=[],
    must_not=[
        mn_judge("M1", "Concludes malingering, exaggeration, dishonesty or secondary gain, or says a Waddell count shows the pain is not genuine; the records chart signs and effort only.",
                 ["The claimant was malingering.", "She exaggerated her symptoms.", "Waddell signs show the pain is not genuine."],
                 ["The functional capacity evaluation of 2026-04-20 charts Waddell 3/5 positive; effort inconsistent.", "Carrier records review quotes the FCE: Waddell 3/5 and inconsistent effort.", "PT note of 2026-03-09 charts 0/5 Waddell signs."]),
        mn_regex("M2", "Uses the words malingering, feigning, faking, exaggerating or secondary gain in the tool's own text.",
                 r"(?i)\b(?:malinger\w*|feign\w*|fak(?:e|ed|ing)|exaggerat\w*|secondary gain)\b",
                 ["The claimant was malingering.", "She exaggerated her pain.", "Secondary gain is likely."],
                 ["Waddell 3/5 positive; effort inconsistent (FCE, 2026-04-20).", "Symptom magnification is the PT's wording.", "0/5 Waddell signs charted on 2026-03-09."]),
        mn_judge("M3", "States the carrier reviewer's opinion as fact (self-limited strain, treatment not necessary, MMI) instead of attributing it to the carrier's letter.",
                 ["Treatment after 04/20/2026 was not reasonable or necessary.", "The lumbar strain was self-limited.", "She reached maximum medical improvement on 04/20/2026."],
                 ["The carrier's records-review letter opines treatment after 04/20/2026 was not reasonable or necessary.", "Carrier reviewer (did not examine the claimant) opines the findings are consistent with a self-limited lumbar strain.", "Records review letter dated 2026-07-15."]),
        mn_judge("M4", "Adds, averages or trends Waddell counts across dates, or treats a positive count as proof of non-organic pain.",
                 ["Waddell signs totaled 3 across her visits.", "The average Waddell score was 1.5 out of 5.", "A positive Waddell count proves the pain is non-organic."],
                 ["0/5 Waddell signs on 2026-03-09 (PT).", "Waddell 3/5 positive on 2026-04-20 (FCE), as charted.", "Waddell signs negative on the left and positive on the right, as charted on 2026-05-04."]),
        mn_amount("M5", "Adds the fee-schedule rate to the charges or sums the statement lines into a figure the records do not state (values 5,935 / 6,270 / 2,925 / 3,010).", [5935, 6270, 2925, 3010]),
    ],
    notes=["Hand arithmetic: 02-09 to 02-23 = 14; to 03-09 = 5 + 9 = 14; to 03-30 = 21; to 04-20 = 1 + 20 = 21; to 05-04 = 10 + 4 = 14; to 06-22 = 27 + 22 = 49 (flag). The carrier letter (07-15) and statement (07-31) are non-encounters.",
           "Charges counted: 2,780 + 210 + 2,320 + 480 = 5,790. Forbidden: 5,790 + 145 = 5,935; 5,790 + 480 = 6,270; 2,780 + 145 = 2,925; 210 + 2,320 + 480 = 3,010 (never stated).",
           "Credibility sentences (D-043): clean negations in records 4 and 5 (must not flag); a positive count with inconsistent effort (record 6), a mixed-side sentence and a contrast sentence (record 7), and the carrier's three restatements (record 9) flag. Three further dismissable non-credibility flags (P1, K8, K9) exercise the dismissal-pattern guard (T-089): the tool must never learn to auto-dismiss credibility flags.",
           "Litigation-stage variant (not in this packet): the same wording in a post-suit TRCP 204 exam report."]))

# ───────────────────────── lib13: copied-forward ROS vs orthopedic complaint (P10 + P16) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib13_cloned_notes_cross_provider", patterns="P10 + P16", expect_total=5830,
    description="Library L13 (P10+P16). Rear-end collision on a highway on-ramp. Three PCP visits weeks apart carry the identical copied-forward ROS 'denies neck pain, denies back pain, denies numbness' while orthopedics, two days after the first PCP visit and again two weeks before the last, charts low back pain 8/10 radiating to the left leg. The orthopedist's surgical cost estimate is an estimate, not a charge. Near-identical notes from the same provider on different dates are separate visits and must not be merged.",
    stress_types=["cloned_ros_across_visits", "cross_provider_symptom_contradiction", "near_duplicate_not_merged", "surgical_estimate_not_charge", "gap_before_followup"],
    records=[
        R("2026-08-03", "Marlpit Fire-Rescue run report", "Driver rear-ended on a highway on-ramp. Pt states neck and low back pain. Ambulatory at scene. Transported to Vessel Grove Medical Center ED.",
          "Driver rear-ended on a highway on-ramp", ["low back pain"], [span("Pt states neck and low back pain.", PT)]),
        R("2026-08-03", "Vessel Grove Medical Center ED", "Dx: lumbar strain, cervical strain. X-ray lumbar and cervical spine negative for fracture. Discharged home. ED charge: $3,540.",
          "X-ray lumbar and cervical spine negative for fracture", ["lumbar strain", "cervical strain"]),
        R("2026-08-05", "Dr. Corwin Pettibone, primary care", "ROS: denies neck pain, denies back pain, denies numbness. Seen for medication refill. Plan: continue current medications.",
          "ROS: denies neck pain, denies back pain, denies numbness", [["denies back pain", "denied back pain", "denies neck pain", "denied neck pain"]]),
        R("2026-08-07", "Dr. Fenwick Larkspur, orthopedics, new patient", "Low back pain 8/10, radiating to the left leg. MRI lumbar spine ordered. Surgical consult if no improvement.",
          "Low back pain 8/10, radiating to the left leg", ["8/10", "mri"]),
        R("2026-08-26", "Dr. Corwin Pettibone, primary care, follow-up", "ROS: denies neck pain, denies back pain, denies numbness. Seen for blood pressure check. Plan: continue current medications.",
          "ROS: denies neck pain, denies back pain, denies numbness", [["denies back pain", "denied back pain", "denies neck pain", "denied neck pain"]]),
        R("2026-08-28", "Vessel Grove Imaging, lumbar MRI", "L5-S1 disc protrusion contacting the left S1 nerve root. MRI charge: $2,290.",
          "L5-S1 disc protrusion contacting the left S1 nerve root", ["l5-s1", "protrusion"]),
        R("2026-09-04", "Dr. Fenwick Larkspur, orthopedics, follow-up", "MRI reviewed. Low back pain 8/10. Recommend microdiscectomy. Estimated surgical cost $38,500.", "Recommend microdiscectomy", ["8/10", "microdiscectomy"]),
        R("2026-09-16", "Dr. Corwin Pettibone, primary care, follow-up", "ROS: denies neck pain, denies back pain, denies numbness. Seen for lab review. Plan: continue current medications.",
          "ROS: denies neck pain, denies back pain, denies numbness", [["denies back pain", "denied back pain", "denies neck pain", "denied neck pain"]]),
        R("2026-11-02", "Dr. Fenwick Larkspur, orthopedics, follow-up", "Low back pain 7/10. Surgery date pending authorization.", "Surgery date pending authorization", ["7/10"]),
    ],
    amounts=[A(2, "$3,540", 3540, "charge", "ED charge: $3,540"),
             A(6, "$2,290", 2290, "charge", "MRI charge: $2,290"),
             A(7, "$38,500", 38500, "estimate", "Estimated surgical cost $38,500", note="Estimate of future surgery, not a charge (D-019).")],
    unclear={},
    gap_flags=[("G1", 8, 9, "Seen for lab review", "Low back pain 7/10")],
    flags=[
        flag("C1", "conflict", "must", [3, 4], [(3, "excerpt", "denies back pain"), (4, "excerpt", "Low back pain 8/10")],
             "Two providers disagree within days: the PCP ROS of 2026-08-05 records 'denies back pain'; orthopedics on 2026-08-07 records low back pain 8/10. Both cited; the paralegal decides which to cite (HITL step).", "cross_provider_symptom"),
        flag("C2", "conflict", "should", [4, 5], [(4, "excerpt", "Low back pain 8/10"), (5, "excerpt", "denies back pain")],
             "The PCP follow-up of 2026-08-26 again records 'denies back pain' after orthopedics charted low back pain 8/10.", "cross_provider_symptom"),
        flag("C3", "conflict", "must", [7, 8], [(7, "excerpt", "Low back pain 8/10"), (8, "excerpt", "denies back pain")],
             "Twelve days apart, orthopedics charts low back pain 8/10 with an MRI finding while the PCP ROS again records 'denies back pain'.", "cross_provider_symptom"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 2, 2, 19, 2, 7 and 12-day intervals."}],
    tolerated=[flag("T1", "conflict", "tolerated", [3, 5], [(3, "excerpt", "ROS: denies neck pain, denies back pain, denies numbness"), (5, "excerpt", "ROS: denies neck pain, denies back pain, denies numbness")],
                    "Identical ROS text on two PCP visits 21 days apart; a near-duplicate notice may be shown for review but the visits are never merged.", "near_duplicate_text")],
    must_not=[
        mn_judge("M1", "Resolves the disagreement: picks a provider, says one is wrong or unreliable, or says the patient did or did not have back pain.",
                 ["She does not have back pain; the PCP records deny it.", "The orthopedist's back pain finding is wrong.", "The patient denied back pain, so the ortho note is unreliable."],
                 ["PCP ROS on 2026-08-05 records 'denies back pain'; orthopedics on 2026-08-07 records low back pain 8/10.", "Two providers disagree within days; both are cited.", "Orthopedics charts low back pain 8/10 on 2026-09-04."]),
        mn_judge("M2", "Presents the copied-forward ROS as a current, independent finding at each PCP visit (for example, that back pain had resolved by 2026-09-16).",
                 ["At the 2026-09-16 visit she denied back pain, so it had resolved.", "The PCP found no back pain at three visits.", "No neck or back pain per primary care in September."],
                 ["PCP ROS text on 2026-08-05, 2026-08-26 and 2026-09-16 is identical.", "ROS: denies neck pain, denies back pain, denies numbness (2026-09-16 visit, seen for lab review).", "Seen for lab review."]),
        mn_judge("M3", "Treats the $38,500 surgical estimate as a charge or as incurred, or adds it to billed charges.",
                 ["Surgery was billed at $38,500.", "Charges total $44,330 including the surgery.", "A $38,500 surgical charge is outstanding."],
                 ["Orthopedics estimates surgical cost at $38,500 (an estimate, not a charge).", "Billed charges accepted from these records: $5,830.00.", "Recommend microdiscectomy."]),
        mn_amount("M4", "Adds the estimate to the charges or treats pain scores, level numbers or interval days as dollars (values 44,330 / 8 / 10 / 47 / 19).", [44330, 8, 10, 47, 19]),
    ],
    notes=["Hand arithmetic: 08-03 to 08-05 = 2; to 08-07 = 2; to 08-26 = 19; to 08-28 = 2; to 09-04 = 3 + 4 = 7; to 09-16 = 12; to 11-02 = 14 + 31 + 2 = 47 (flag).",
           "Charges counted: 3,540 + 2,290 = 5,830. Forbidden: 5,830 + 38,500 = 44,330.",
           "Dedupe: the three PCP visits have the same provider and text but different dates, so they are three entries (expected_entry_count 9). Records 3, 5 and 8 are the copied-forward notes; the orthopedic notes in records 4 and 7 are the contradicting ones.",
           "Pre-suit: the PCP records came from the firm's own request after the client listed the PCP on intake."]))

# ───────────────────────── lib14: handwritten chiropractic scans, CMS-1500 OCR, ambulance invoice (P12 + P15) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib14_handwritten_chiro_scans", patterns="P12 + P15", expect_total=4527.05,
    description="Library L14 (P12+P15). Rear-end collision, EMS run report, ED, then faxed chiropractic daily notes as OCR text (checkbox treatment marks, a pain number circled, one handwritten header date with no year), a typed re-examination whose pain score disagrees with the handwritten pages, a CMS-1500 OCR copy that groups three days on one line (decimal-less money boxes), and an ambulance invoice with a base line plus per-mile mileage. The undated handwritten page is excluded from gap arithmetic and goes to review.",
    stress_types=["ocr_noise_text", "handwritten_date_no_year", "checkbox_treatment_marks", "typed_page_disagrees_with_handwritten", "cms1500_grouped_line_days_equal_units", "cms1500_ocr_decimal_less", "ambulance_base_plus_mileage", "ems_run_report", "rate_not_charge"],
    records=[
        R("2026-09-14", "Tarnwick Fire-Rescue run report", "Driver of a sedan struck from behind. Moderate damage to the rear of the vehicle. Pt ambulatory at scene. Pt states neck pain 6/10 and tingling in the right hand. Cervical collar applied. Transported to Orrin Mere Regional ED.",
          "Driver of a sedan struck from behind", ["collar"], [span("Pt states neck pain 6/10 and tingling in the right hand.", PT)]),
        R("2026-09-14", "Orrin Mere Regional ED", "Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant. ED charge: $2,960.", "X-ray cervical spine negative for fracture", ["cervical strain", "negative for fracture"]),
        R("2026-09-21", "Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text)", "Pain 7 circled on a 0-10 scale. Tenderness at C4-C6. [X] adjustment [X] e-stim [X] hot pack. Date written 9/2l/26.", "Tenderness at C4-C6", ["c4-c6"],
          note="Fax-quality scan as OCR text: the written date reads 9/2l/26 (letter l for 1); the header date is the packet's production date for the visit."),
        R("2026-10-06", "Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text)", "Pain 5 circled. Tenderness at C4-C5, improved. [X] adjustment [X] e-stim. Next visit 1O/2O.", "Tenderness at C4-C5, improved", ["c4-c5"]),
        R(None, "Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text)", "Pain 4 circled. Adjusted C4-C6. [X] e-stim. Pt states neck feels better.", "Adjusted C4-C6", ["c4-c6"],
          [span("Pt states neck feels better.", PT)], raw="10/20", status="missing",
          note="Handwritten header date '10/20' has no year: date_status missing, never guessed, excluded from gap arithmetic, sorts to the needs-review group."),
        R("2026-11-03", "Hollowbrook Chiropractic, re-examination (typed)", "Re-examination. Pain 6/10, unchanged from the initial visit. Plan: continue care three times weekly.", "Pain 6/10, unchanged from the initial visit", ["6/10"]),
        R("2026-11-10", "Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim)", "OCR of scanned CMS-1500. Item 14 injury date 091426 qualifier 431. Line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3. Line 2: 092126 to 092326, CPT 97014, 24F 7500, 24G 3. Item 28 TOTAL CHARGE 33000. Item 29 AMOUNT PAID 0 00. Item 31 signature date 110926.",
          "OCR of scanned CMS-1500", [["cms-1500", "claim"]], kind="billing_statement",
          note="Grouped lines: one line covers three consecutive days (24G 3 = days). Money boxes have no decimal point: truth 255.00, 75.00 and 330.00 (255 + 75). Item 14 (091426) is the injury date and Item 31 (110926) the signature date; neither is a visit."),
        R("2026-11-12", "Tarnwick Fire-Rescue, ambulance invoice", "Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05. Total charges $1,567.05. No payments posted. Letter of protection requested.",
          "ground mileage, loaded, 8.7 miles at $21.50 per mile", [["ambulance", "als emergency transport", "transport"]], kind="billing_statement"),
    ],
    amounts=[A(2, "$2,960", 2960, "charge", "ED charge: $2,960"),
             A(7, "25500", None, "unclear", "24F 25500", required=False, note="Decimal-less CMS-1500 box; truth 255.00 for 3 days; OCR-derived, needs review."),
             A(7, "7500", None, "unclear", "24F 7500", required=False, note="Decimal-less box; truth 75.00."),
             A(7, "33000", None, "unclear", "TOTAL CHARGE 33000", required=False, note="Item 28; truth 330.00."),
             A(8, "$1,380.00", 1380, "charge", "charge $1,380.00"),
             A(8, "$21.50", 21.5, "rate", "8.7 miles at $21.50 per mile", note="Per-mile rate; only the extended line charge ($187.05 = 8.7 x 21.50) is a charge."),
             A(8, "$187.05", 187.05, "charge", "charge $187.05"),
             A(8, "$1,567.05", None, "unclear", "Total charges $1,567.05", note="Invoice total repeats the two lines above; counting it double counts.")],
    unclear={"A8": "invoice total repeats the base and mileage lines; not counted; needs review"},
    gap_flags=[],
    flags=[
        flag("C1", "conflict", "should", [5, 6], [(5, "excerpt", "Pain 4 circled"), (6, "excerpt", "Pain 6/10, unchanged from the initial visit")],
             "The undated handwritten page records pain 4 circled; the typed re-examination of 2026-11-03 records pain 6/10 'unchanged from the initial visit'. Both cited; the tool does not pick.", "pain_score_differs"),
        flag("K1", "causation", "should", [1], [(1, "excerpt", "Moderate damage to the rear of the vehicle")], "Scene fact in the EMS record; dismissable.", "scene_facts"),
    ],
    record_warnings=[{"id": "W1", "type": "record_warning", "category": "date_ambiguous", "record_no": 5, "field": "date", "level": "must", "excerpt": "10/20", "expected_state": "needs_review"}],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 7, 15 and 28-day intervals; the undated handwritten page (record 5), the CMS-1500 (record 7) and the invoice (record 8) are not gap endpoints."}],
    tolerated=[flag("T1", "conflict", "tolerated", [3, 7], [(3, "excerpt", "Date written 9/2l/26"), (7, "excerpt", "092126 to 092326")],
                    "The CMS-1500 line groups 2026-09-21 to 2026-09-23 (3 units) while the packet holds a daily note for 2026-09-21 only; a billing-analysis notice may be raised for review but is not required as a flag.", "billed_dates_without_notes")],
    must_not=[
        mn_amount("M1", "Reads decimal-less CMS-1500 boxes as whole dollars (25500 -> $25,500) (values 25,500 / 7,500 / 33,000).", [25500, 7500, 33000]),
        mn_amount("M2", "Treats the mileage count as dollars, counts the invoice total with its lines, or sums them (values 8.7 / 1,567.05 / 6,094.10).", [8.7, 1567.05, 6094.1]),
        mn_judge("M3", "Supplies a year or a full date for the undated handwritten page (for example 2026-10-20), or places it in a visit sequence as if dated.",
                 ["Chiropractic visit on 2026-10-20.", "Visit dated October 20, 2026.", "Handwritten note from 10/20/2026."],
                 ["Handwritten note dated '10/20' with no year; date needs confirmation.", "Undated handwritten daily note (visit 12).", "Pain 4 circled. Adjusted C4-C6."]),
        mn_judge("M4", "Reads a scan or OCR glitch as a clinical fact (for example turns 'Next visit 1O/2O' into a stated date of service, or the circled pain number into a /10 score the note does not state).",
                 ["Next visit on 2026-10-20 was completed.", "Pain 5/10 was charted on 2026-10-06.", "Patient was seen on 9/21/26 and 9/22/26."],
                 ["Pain 5 circled.", "Next visit 1O/2O (OCR text).", "Date written 9/2l/26 (OCR text)."]),
    ],
    notes=["Hand arithmetic (dated encounters): 09-14 to 09-21 = 7; 09-21 to 10-06 = 9 + 6 = 15; 10-06 to 11-03 = 25 + 3 = 28. Record 5 (date missing), 7 and 8 are excluded; no interval exceeds 30, so this packet has no gap flag.",
           "Charges counted: 2,960 + 1,380.00 + 187.05 = 4,527.05. Mileage: 8.7 x 21.50 = 187.05; 1,380.00 + 187.05 = 1,567.05 (the invoice total, not counted). Forbidden: 4,527.05 + 1,567.05 = 6,094.10.",
           "Not representable in a text packet: the hidden text layer that differs from the page image (P12, T-087 builds that check on PDFs). Record 3 and 4 stand in for scanned pages; the page image itself belongs to the OCR feature (T-086).",
           "Pre-suit: the chiropractic records were faxed by the provider; the ambulance invoice is the agency's."]))

# ───────────────────────── lib15: conclusory narrative letter, 18.001 affidavit, minimal-damage language (P3 + P17) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib15_conclusory_letter_mist", patterns="P3 + P17", expect_total=3295,
    description="Library L15 (P3+P17). EMS notes minor damage and a refused transport, urgent care calls it a low-speed MVC, the chiropractor later records the patient saying the impact was violent, and the chiropractor's narrative letter states the collision caused all injuries and treatment with no reasoning. A custodian's section 18.001 affidavit restates the charges and says the services were necessary and the charges reasonable (it says nothing about causation), and its attached itemized statement duplicates the statement already in the file. Letter and affidavit language is shown verbatim and never upgraded to a finding; the duplicate merges, so the total is counted once.",
    stress_types=["minimal_damage_language", "refused_transport", "mechanism_description_changes", "conclusory_causation_letter", "section_18001_affidavit", "affidavit_duplicates_statement", "estimate_not_charge", "gap_before_discharge"],
    records=[
        R("2026-10-04", "Brindlewick Fire-Rescue run report", "Restrained driver in a low-speed rear-end collision. Minor damage to the rear bumper. Ambulatory at scene. Pt states mild neck stiffness. Pt refused transport against medical advice.",
          "Minor damage to the rear bumper", [["refused transport", "refused"]], [span("Pt states mild neck stiffness.", PT)]),
        R("2026-10-05", "Cobblewood Urgent Care", "Seen the day after a low-speed MVC. Neck pain 4/10. Mild paraspinal tenderness. X-ray cervical spine negative. Dx: cervical strain. Charge: $385.",
          "Seen the day after a low-speed MVC", ["4/10", "cervical strain"]),
        R("2026-10-19", "Sunderland Chiropractic, new patient", "Patient states the impact was violent and she was thrown against the seat belt. Neck pain 7/10 with headaches. Plan: chiropractic care three times weekly.",
          "Neck pain 7/10 with headaches", ["7/10", "headaches"], [span("Patient states the impact was violent and she was thrown against the seat belt.", SELF)]),
        R("2026-11-02", "Sunderland Chiropractic, visit 6", "Neck pain 6/10. Adjustment and e-stim. Patient states pain began right after the collision.", "Neck pain 6/10", ["6/10"],
          [span("Patient states pain began right after the collision.", SELF)]),
        R("2026-12-14", "Sunderland Chiropractic, visit 18", "Neck pain 4/10. Continue care.", "Neck pain 4/10", ["4/10"]),
        R("2027-01-11", "Sunderland Chiropractic, correspondence, narrative letter", "Letter to the attorney dated 01/11/2027. The patient reports she was rear-ended on 2026-10-04 and developed neck pain and headaches. Diagnoses: cervical sprain; post-traumatic headache. Prognosis: guarded. The collision of 2026-10-04 caused all of the injuries and treatment described in this letter. Future care: an estimated 12 additional visits at $150.00 per visit ($1,800.00).",
          "caused all of the injuries and treatment described in this letter", ["caused all"], kind="phone_note",
          note="Conclusory letter: the causation sentence is the provider's statement, shown verbatim, never upgraded to the tool's finding."),
        R("2027-01-20", "Sunderland Chiropractic, itemized statement", "Itemized statement: new patient exam charge $210.00; treatment visits 1 through 18 charge $2,700.00; total charges $2,910.00. Payment received $250.00 (med pay). Balance due $2,660.00. Account held under letter of protection.",
          "new patient exam charge $210.00", [], kind="billing_statement"),
        R("2027-01-20", "Sunderland Chiropractic, itemized statement", "Itemized statement: new patient exam charge $210.00; treatment visits 1 through 18 charge $2,700.00; total charges $2,910.00. Payment received $250.00 (med pay). Balance due $2,660.00. Account held under letter of protection.",
          "new patient exam charge $210.00", [], kind="billing_statement", dup_of=7,
          note="The statement attached to the affidavit: the same bill reproduced twice (same date, source and text). Merges into one entry."),
        R("2027-02-03", "Pennyroyal Records Retrieval, 18.001 affidavit", "Affidavit concerning cost and necessity of services (CPRC 18.001). The custodian of records states the attached records were kept in the regular course of business. Services provided 10/19/2026 through 12/14/2026. Total amount charged: $2,910.00. Amount paid: $250.00. Amount unpaid that the provider has a right to be paid: $2,660.00. The services were necessary and the charges reasonable. Sworn 02/01/2027.",
          "The services were necessary and the charges reasonable", [["18.001", "affidavit"]], kind="phone_note",
          note="Affidavit sworn 02/01/2027: its dates are paperwork, not care. Its range of service dates spans many visits. Obtained from the provider for later service; not yet served."),
    ],
    amounts=[A(2, "$385", 385, "charge", "Charge: $385"),
             A(6, "$150.00", 150, "rate", "12 additional visits at $150.00 per visit", note="Per-visit rate in a future-care estimate; not a charge."),
             A(6, "$1,800.00", 1800, "estimate", "($1,800.00)", note="Future care estimate (12 x 150), not incurred (D-019)."),
             A(7, "$210.00", 210, "charge", "new patient exam charge $210.00"),
             A(7, "$2,700.00", 2700, "charge", "charge $2,700.00"),
             A(7, "$2,910.00", None, "unclear", "total charges $2,910.00", note="Statement total repeats the two lines; counting it double counts."),
             A(7, "$250.00", None, "unclear", "Payment received $250.00", required=False, note="Payment; not a charge."),
             A(7, "$2,660.00", None, "unclear", "Balance due $2,660.00", required=False, note="Balance = 2,910.00 - 250.00; derived."),
             A(9, "$2,910.00", None, "unclear", "Total amount charged: $2,910.00", note="Affidavit restates the statement total; the attached bill duplicates records 7-8; not counted again."),
             A(9, "$250.00", None, "unclear", "Amount paid: $250.00", required=False, note="Payment stated in the affidavit; not a charge."),
             A(9, "$2,660.00", None, "unclear", "Amount unpaid that the provider has a right to be paid: $2,660.00", required=False, note="Affidavit's unpaid amount; not a charge.")],
    unclear={"A6": "statement total repeats the two lines; not counted; needs review",
             "A9": "affidavit restates the statement total; the attached statement duplicates records 7-8; not counted again; needs review"},
    gap_flags=[("G1", 4, 5, "Adjustment and e-stim", "Neck pain 4/10")],
    flags=[
        flag("C1", "conflict", "must", [1, 3], [(1, "excerpt", "Minor damage to the rear bumper"), (3, "excerpt", "Patient states the impact was violent and she was thrown against the seat belt.")],
             "The collision is described as low-speed with minor damage in the EMS record and as violent by the patient in the chiropractic record two weeks later. Both attributed; the tool does not characterize the crash.", "mechanism_description_changes"),
        flag("K1", "causation", "must", [6], [(6, "excerpt", "The collision of 2026-10-04 caused all of the injuries and treatment described in this letter.")],
             "The provider's causation sentence, given without reasoning. Shown verbatim and attributed to the letter; not upgraded to a finding.", "conclusory_causation_letter"),
        flag("K2", "causation", "should", [1], [(1, "excerpt", "Minor damage to the rear bumper")], "Scene fact in the EMS record (D-018); dismissable.", "scene_facts"),
        flag("K3", "causation", "should", [4], [(4, "excerpt", "pain began right after the collision")], "Patient-stated onset; shown as the patient's report.", "patient_report"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 1, 14 and 14-day intervals; the letter (record 6), the statements (records 7-8) and the affidavit (record 9) are not gap endpoints."}],
    tolerated=[flag("T1", "conflict", "tolerated", [2, 3], [(2, "excerpt", "low-speed MVC"), (3, "excerpt", "the impact was violent")],
                    "Urgent care calls it a low-speed MVC and the chiropractor records the patient calling it violent; may be shown alongside the required conflict C1.", "mechanism_description_changes")],
    must_not=[
        mn_judge("M1", "States as the tool's own fact that the collision caused the injuries or the treatment; the only causation statement is the chiropractor's unexplained sentence in a letter.",
                 ["The collision caused all of her injuries and treatment.", "The 2026-10-04 crash caused the cervical sprain and headaches.", "All of the treatment was caused by the accident."],
                 ["The chiropractor's narrative letter states the collision of 2026-10-04 caused all of the injuries and treatment described in the letter.", "Patient states pain began right after the collision.", "Diagnoses listed in the letter: cervical sprain; post-traumatic headache."]),
        mn_judge("M2", "Treats the section 18.001 affidavit as proof of causation, or states in the tool's voice that the services were necessary and the charges reasonable; the affiant says so, and the affidavit says nothing about causation.",
                 ["The 18.001 affidavit establishes that the treatment was caused by the crash.", "The charges were reasonable and the services necessary.", "The affidavit proves the treatment was necessary."],
                 ["Custodian's affidavit states the services were necessary and the charges reasonable (affiant's statement).", "Affidavit sworn 02/01/2027 attaches the itemized statement.", "The affidavit contains no causation statement."]),
        mn_judge("M3", "Characterizes the collision's severity in the tool's own voice (minor, fender-bender, violent, severe, unlikely to injure); each description is attributed to its source.",
                 ["The collision was a minor fender-bender.", "The crash was violent.", "A low-speed crash makes injury unlikely."],
                 ["EMS: minor damage to the rear bumper.", "Patient states the impact was violent and she was thrown against the seat belt.", "Urgent care: seen the day after a low-speed MVC."]),
        mn_amount("M4", "Counts the statement total, the affidavit's restated total, the estimate, or the statement twice (values 6,205 / 5,095 / 5,820 / 2,910 / 2,660 / 250).", [6205, 5095, 5820, 2910, 2660, 250]),
    ],
    notes=["Hand arithmetic (dated encounters): 10-04 to 10-05 = 1; 10-05 to 10-19 = 14; 10-19 to 11-02 = 12 + 2 = 14; 11-02 to 12-14 = 28 + 14 = 42 (flag). The letter (2027-01-11), both statement copies (2027-01-20) and the affidavit (2027-02-03) are non-encounters.",
           "Records 7 and 8 are one bill reproduced twice (same date, source and text) and merge into one entry (expected_entry_count 8). Charges counted: 385 + 210 + 2,700 = 3,295. Forbidden: 3,295 + 2,910 = 6,205; 3,295 + 1,800 = 5,095; 2 x 2,910 = 5,820.",
           "Statement arithmetic: 210 + 2,700 = 2,910; 18 visits x 150 = 2,700; 2,910 - 250 = 2,660. The affidavit's amounts match the statement's, so it adds nothing new.",
           "Pre-suit: the letter and the affidavit were obtained from the providers for later service and are not yet served."]))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for sp in SPECS:
        txt, ex = build(sp)
        (OUT / (sp["case_id"] + ".txt")).write_text(txt)
        (OUT / (sp["case_id"] + ".expected.json")).write_text(json.dumps(ex, indent=2, ensure_ascii=False) + "\n")
        print("wrote", sp["case_id"], "records", len(sp["records"]), "entries", ex["expected_entry_count"], "total", ex["totals"]["explicit_charges_total"],
              "gaps", [g["days"] for g in ex["gap_table"]])


if __name__ == "__main__":
    main()
