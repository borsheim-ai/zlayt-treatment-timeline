#!/usr/bin/env python3
"""Builds evals/library/case_lib*.txt + .expected.json (golden/1 schema) from the compact specs below (T-052).

The SPECS are the hand-authored content (records, required terms, flags, must_nots). The script only does the mechanical parts
that evals/golden/check_golden.py independently re-verifies: record numbering, entry boilerplate, the gap table (calendar
arithmetic over clinical encounters), gap flags, totals and letter/ui lines.

Run:  python3 research/library_build.py            (writes evals/library/*)
      python3 research/validate_library.py         (check_golden.py over golden + library; identifier denylist)
All names, providers and places are INVENTED. See research/case-library-sources.md for the real-world scenario each mirrors.
"""
import datetime as dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "evals" / "library"
HEADER = "SYNTHETIC — invented for evaluation; not real patient data"

AMT_GOOD = [{"raw": "$6,240", "value": 6240, "class": "charge"}, {"raw": "$185", "value": 185, "class": "rate"},
            {"raw": "$1,2OO", "value": None, "class": "unclear"}]


def mn_amount(mid, statement, values):
    return {"id": mid, "statement": statement, "check": "amount_value",
            "bad_examples": [{"raw": f"${v:,}", "value": v, "class": "charge"} for v in values[:3]],
            "good_examples": AMT_GOOD, "values": values}


def mn_judge(mid, statement, bad, good):
    return {"id": mid, "statement": statement, "check": "judge", "bad_examples": bad, "good_examples": good}


def mn_regex(mid, statement, pattern, bad, good):
    return {"id": mid, "statement": statement, "check": "regex", "pattern": pattern, "bad_examples": bad, "good_examples": good}


def rec(date, source, excerpt, kind="encounter", must=None, terms=(), spans=(), note=None, raw=None):
    return dict(date=date, raw=raw or date, source=source, excerpt=excerpt, kind=kind, must=must or [], terms=list(terms),
                spans=list(spans), note=note)


def span(excerpt, attribution):
    return {"excerpt": excerpt, "attribution_any": attribution}


def amt(record_no, raw, value, cls, excerpt, in_total=None, required=True, needs_review=None, note=None):
    return dict(record_no=record_no, raw=raw, value=value, cls=cls, excerpt=excerpt,
                in_total=(cls == "charge") if in_total is None else in_total, required=required,
                needs_review=(cls != "charge") if needs_review is None else needs_review, note=note)


def flag(fid, typ, level, cite_all, evidence, summary, subtype=None, cite_any=(), **kw):
    f = {"id": fid, "type": typ, "level": level, "cite": {"all": list(cite_all), "any": list(cite_any)},
         "evidence": [{"record_no": r, "field": fld, "excerpt": ex} for (r, fld, ex) in evidence], "summary": summary}
    if subtype:
        f["subtype"] = subtype
    f.update(kw)
    return f


SPECS = []

# ───────────────────────── L1: ER only, then a long gap (S1) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib01_er_only_then_gap", source_ref="S1",
    description="Library L1 (mirrors S1). Rear-end collision, ED visit and a negative x-ray, then the first primary-care visit 44 days later with a new arm symptom and a patient-stated reason for the delay. The gap is flagged; the reason is shown as the patient's statement, never as the tool's explanation.",
    stress_types=["er_only_then_long_gap", "patient_stated_gap_reason", "new_symptom_after_gap", "rate_not_charge", "negative_xray_not_no_injury"],
    records=[
        rec("2026-02-14", "Dunmarrow Fire-Rescue run report",
            "Driver of a sedan struck from behind while stopped at a light. C/O neck stiffness. Transported to Marrowgate General ED.",
            must="Driver of a sedan struck from behind", terms=["neck stiffness"]),
        rec("2026-02-14", "Marrowgate General ED",
            "Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week. ED charge: $3,915.",
            must="X-ray cervical spine negative for fracture", terms=["cervical strain", "negative for fracture"]),
        rec("2026-03-30", "Dr. Imelda Quarrington, primary care",
            "Neck pain 5/10 with new left arm tingling. Patient states she could not get an earlier appointment because the clinic was closed. Refer to physical therapy.",
            must="Neck pain 5/10 with new left arm tingling", terms=["neck pain", "left arm tingling", "physical therapy", ["patient states", "per patient", "patient reports"]],
            spans=[span("Patient states she could not get an earlier appointment because the clinic was closed.", ["patient states", "per patient", "patient reports"])]),
        rec("2026-04-13", "Plumtree Physical Therapy, initial evaluation",
            "Cervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $140.",
            must="Cervical range of motion reduced approx. 30%", terms=["approx. 30%"]),
        rec("2026-05-04", "Plumtree Physical Therapy, visit 6", "Pain 3/10, improving. Home exercise program reviewed.",
            must="Pain 3/10, improving", terms=["3/10"]),
        rec("2026-05-18", "Plumtree Physical Therapy, discharge", "Discharged from PT, goals met. Pain 2/10.",
            must="Discharged from PT, goals met", terms=["goals met"]),
    ],
    amounts=[amt(2, "$3,915", 3915, "charge", "ED charge: $3,915"),
             amt(4, "$140", 140, "rate", "Charge per visit $140", note="Rate, not a charge: visits billed are never stated (8 planned).")],
    unclear={"A2": "rate $140/visit; visit count not stated (8 planned); needs review"},
    gap_flags=[("G1", 2, 3, "Follow up with primary care in 1 week", "Neck pain 5/10 with new left arm tingling")],
    flags=[
        flag("K1", "causation", "should", [3], [(3, "excerpt", "new left arm tingling")],
             "New symptom first recorded after a 44-day gap; an adjuster can argue a new cause. Raised as causation, not as a gap.", "new_onset_after_gap"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 14, 21 and 14-day intervals (records 3-4, 4-5, 5-6)."},
                   {"id": "N2", "type": "pre_existing", "statement": "No prior-condition flag: the record names none."}],
    tolerated=[],
    must_not=[
        mn_judge("M1", "Explains the 44-day gap in the tool's own words (motive, choice, severity). The only reason shown is the patient's own statement, attributed.",
                 ["She delayed care because the injury was minor.", "Patient chose not to follow up for six weeks.", "The gap shows the neck pain was not serious."],
                 ["Patient states she could not get an earlier appointment because the clinic was closed.", "44 days between the ED visit (2026-02-14) and the primary-care visit (2026-03-30).", "Follow up with primary care in 1 week was advised in the ED record."]),
        mn_regex("M2", "Turns the gap into a conclusion about injury severity or recovery.",
                 r"(?i)\b(gap|delay)\b[^.]{0,40}\b(shows?|proves?|means|indicates?)\b[^.]{0,30}\b(minor|not serious|no injury|recovered)",
                 ["The 44-day gap shows the injury was minor.", "Delay proves she had recovered.", "The gap means no injury."],
                 ["Gap of 44 days between 2026-02-14 and 2026-03-30.", "Patient states she could not get an earlier appointment.", "Treatment gap flagged for review."]),
        mn_judge("M3", "Summarises the negative x-ray as 'no injury' or drops the Dx; the record shows a cervical strain diagnosis and a negative fracture study only.",
                 ["No injury found on x-ray.", "X-ray was normal so there was no injury.", "ED found nothing wrong with her neck."],
                 ["Dx: cervical strain; x-ray cervical spine negative for fracture.", "X-ray negative for fracture.", "ED diagnosis was cervical strain."]),
        mn_judge("M4", "Turns 'new left arm tingling' into a diagnosis (radiculopathy, nerve compression) not in the record.",
                 ["Cervical radiculopathy developed.", "Nerve compression causing arm tingling.", "Left arm radiculopathy after the gap."],
                 ["New left arm tingling.", "Neck pain 5/10 with new left arm tingling.", "Referred to physical therapy."]),
        mn_amount("M5", "Treats days, percentages, doses or visit counts as dollar amounts, or totals the per-visit rate.", [1, 6, 8, 14, 30, 44, 600, 1120, 5035]),
    ],
    notes=["Hand arithmetic: 02-14 to 03-30 = 14 (to Feb 28) + 30 = 44 days (flag). 03-30 to 04-13 = 14; 04-13 to 05-04 = 21; 05-04 to 05-18 = 14.",
           "Forbidden guess-sums: 8 x 140 = 1,120; 3,915 + 1,120 = 5,035.",
           "Gap evidence quotes the last excerpt before the gap and the first after it (same convention as the sample)."]))

# ───────────────────────── L2: slip and fall, prior knee surgery (S2) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib02_slip_fall_prior_knee", source_ref="S2",
    description="Library L2 (mirrors S2). Store slip-and-fall with a prior knee arthroscopy shown in imaging and in the patient's history; MRI wording that may reflect both acute and prior change. The tool shows the prior-condition language and the hedge and draws no apportionment. PT records are partial, so a 49-day gap appears between them.",
    stress_types=["prior_surgery_same_joint", "hedged_imaging_two_causes", "degenerative_language", "partial_pt_records_gap", "scene_fact_declined_ambulance"],
    records=[
        rec("2026-03-09", "Sablewood Market first-aid log",
            "Customer slipped on a wet floor near the produce display and fell onto the right knee. Ice applied. Declined ambulance.",
            must="slipped on a wet floor", terms=["right knee"]),
        rec("2026-03-09", "Tamsin Valley Urgent Care",
            "Right knee pain 7/10 with swelling. X-ray right knee: no acute fracture; prior arthroscopic changes noted. Dx: knee contusion. Knee immobilizer provided. Visit charge: $410.",
            must="prior arthroscopic changes noted", terms=["right knee", "contusion", "prior arthroscopic changes"]),
        rec("2026-03-16", "Dr. Lucan Pettibone, orthopedics",
            "Patient reports a right knee arthroscopy in 2021 with good recovery before the fall. Effusion persists. MRI right knee ordered.",
            must="Effusion persists", terms=["MRI", ["patient reports", "per patient", "patient states"]],
            spans=[span("Patient reports a right knee arthroscopy in 2021 with good recovery before the fall.", ["patient reports", "per patient", "patient states", "patient-reported"])]),
        rec("2026-03-30", "Tamsin Imaging, right knee MRI",
            "Medial meniscus tear with moderate joint effusion. Mild tricompartmental degenerative change. Findings may reflect both acute injury and prior surgical change. MRI charge: $1,850.",
            must="Findings may reflect both acute injury and prior surgical change", terms=["medial meniscus tear", "may reflect", "degenerative"]),
        rec("2026-04-13", "Dr. Lucan Pettibone, orthopedics",
            "Discussed arthroscopic meniscal repair versus conservative care. Patient elects physical therapy first. Aggravation of the underlying knee condition is possible.",
            must="Aggravation of the underlying knee condition is possible", terms=["physical therapy", "possible"]),
        rec("2026-05-04", "Cedar Run Physical Therapy, initial evaluation",
            "Right knee flexion limited to 100 degrees. Plan of care: 10 visits. Charge per visit $155.",
            must="Right knee flexion limited to 100 degrees", terms=["100 degrees"]),
        rec("2026-06-22", "Cedar Run Physical Therapy, visit 10", "Flexion improved to 125 degrees. Pain 3/10.",
            must="Flexion improved to 125 degrees", terms=["125 degrees"]),
    ],
    amounts=[amt(2, "$410", 410, "charge", "Visit charge: $410"), amt(4, "$1,850", 1850, "charge", "MRI charge: $1,850"),
             amt(6, "$155", 155, "rate", "Charge per visit $155", note="Rate, not a charge: visits billed are never stated (10 planned).")],
    unclear={"A3": "rate $155/visit; visit count not stated (10 planned; visit 10 note present); needs review"},
    gap_flags=[("G1", 6, 7, "Plan of care: 10 visits", "Flexion improved to 125 degrees")],
    flags=[
        flag("P1", "pre_existing", "must", [3], [(3, "excerpt", "Patient reports a right knee arthroscopy in 2021")],
             "Prior right knee arthroscopy (2021), reported by the patient. Same joint as the fall.", "prior_surgery_reported"),
        flag("P2", "pre_existing", "must", [4], [(4, "excerpt", "Mild tricompartmental degenerative change")],
             "Imaging wording an adjuster may argue shows a pre-existing condition; stated as findings, not a diagnosis.", "degenerative_language"),
        flag("P3", "pre_existing", "should", [2], [(2, "excerpt", "prior arthroscopic changes noted")],
             "Urgent-care x-ray notes prior arthroscopic changes (first record of the prior surgery).", "prior_surgery_imaging"),
        flag("K1", "causation", "must", [4], [(4, "excerpt", "may reflect both acute injury and prior surgical change")],
             "Hedged imaging language that names two possible sources; the tool does not choose between them.", "hedged_imaging"),
        flag("K2", "causation", "should", [5], [(5, "excerpt", "Aggravation of the underlying knee condition is possible")],
             "Treating-physician wording that is only 'possible'; not a reasonable-medical-probability statement.", "speculative_language"),
        flag("K3", "causation", "should", [1], [(1, "excerpt", "Declined ambulance")],
             "Scene fact from the first-aid log (internal notes only).", "scene_facts"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 7, 14, 14 and 21-day intervals."}],
    tolerated=[],
    must_not=[
        mn_judge("M1", "States which condition the meniscus tear comes from (the fall or the prior surgery) or that it is degenerative.",
                 ["The fall tore the medial meniscus.", "Meniscus tear caused by the prior surgery.", "The tear is degenerative."],
                 ["Medial meniscus tear with moderate joint effusion.", "Findings may reflect both acute injury and prior surgical change.", "MRI right knee ordered."]),
        mn_judge("M2", "Apportions the knee condition between the fall and the prior surgery (a fraction, a percentage or 'mostly').",
                 ["About half of the knee condition predates the fall.", "60% of the damage is from the prior surgery.", "The prior surgery accounts for most of the symptoms."],
                 ["Aggravation of the underlying knee condition is possible.", "Prior arthroscopic changes noted.", "Patient reports a right knee arthroscopy in 2021 with good recovery before the fall."]),
        mn_judge("M3", "Drops 'prior' or the 2021 date from the arthroscopy, or relocates it to the left knee or to the fall.",
                 ["Right knee arthroscopy after the fall.", "Left knee arthroscopy in 2021.", "Arthroscopy was performed for the fall injury."],
                 ["Prior right knee arthroscopy (2021), per patient.", "Patient reports a right knee arthroscopy in 2021.", "Prior arthroscopic changes noted on x-ray."]),
        mn_amount("M4", "Treats degrees, visit counts, pain scores or years as dollar amounts, or totals the per-visit rate.", [7, 10, 100, 125, 1550, 2021, 3810]),
    ],
    notes=["Hand arithmetic: 03-09 to 03-16 = 7; to 03-30 = 14; to 04-13 = 14; to 05-04 = 17 (to Apr 30) + 4 = 21; 05-04 to 06-22 = 27 (to May 31) + 22 = 49 (flag). 49 days with a visit-10 note implies missing interim PT records; the flag is still correct (records only).",
           "Forbidden guess-sums: 10 x 155 = 1,550; 410 + 1,850 + 1,550 = 3,810."]))

# ───────────────────────── L3: commercial truck rear-end, chiropractic-heavy (S3) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib03_truck_rear_end_chiro", source_ref="S3",
    description="Library L3 (mirrors S3). Passenger car struck from behind by a tractor-trailer; chiropractic plan of 36 visits, no change in pain score at visit 14, discharge at maximum benefit after 31 visits, then an MRI 35 days later with hedged chronic wording and desiccation. The tool must not call the care excessive.",
    stress_types=["chiropractic_heavy_plan", "plan_vs_actual_visits", "near_miss_28_day", "hedged_chronic_imaging", "no_improvement_not_a_conclusion"],
    records=[
        rec("2026-04-06", "Okmarrow EMS run report",
            "Passenger car struck from behind by a tractor-trailer. Restrained driver. C/O low back pain and neck pain. Transported to Redhaven Regional ED.",
            must="struck from behind by a tractor-trailer", terms=["tractor-trailer", "low back pain"]),
        rec("2026-04-06", "Redhaven Regional ED",
            "Dx: lumbar and cervical sprain. CT cervical spine negative. Rx naproxen. Refer to chiropractic or primary care. ED charge: $5,260.",
            must="Dx: lumbar and cervical sprain", terms=["lumbar and cervical sprain", "CT cervical spine negative"]),
        rec("2026-04-09", "Thimbleby Chiropractic, initial exam",
            "Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. Charge per visit $120.",
            must="Plan: 3 visits per week for 12 weeks", terms=["3 visits per week", "12 weeks"]),
        rec("2026-05-07", "Thimbleby Chiropractic, visit 14", "Pain 5/10, unchanged from visit 1. Continue plan.",
            must="Pain 5/10, unchanged from visit 1", terms=["unchanged"]),
        rec("2026-05-27", "Thimbleby Chiropractic, visit 22", "Pain 4/10. Home exercises reviewed.",
            must="Pain 4/10", terms=["4/10"]),
        rec("2026-06-15", "Thimbleby Chiropractic, discharge", "Discharged at maximum chiropractic benefit after 31 visits. Pain 3/10.",
            must="Discharged at maximum chiropractic benefit after 31 visits", terms=["31 visits"]),
        rec("2026-07-20", "Redhaven Imaging, lumbar MRI",
            "L4-L5 disc bulge without nerve root compression. Mild disc desiccation. Radiology: findings likely chronic. MRI charge: $2,240.",
            must="findings likely chronic", terms=["L4-L5 disc bulge", "likely chronic", "desiccation"]),
    ],
    amounts=[amt(2, "$5,260", 5260, "charge", "ED charge: $5,260"),
             amt(3, "$120", 120, "rate", "Charge per visit $120", note="Rate, not a charge: 36 visits planned, 31 attended; no visit count billed."),
             amt(7, "$2,240", 2240, "charge", "MRI charge: $2,240")],
    unclear={"A2": "rate $120/visit; billed visit count not stated (36 planned, 31 attended); needs review"},
    gap_flags=[("G1", 6, 7, "Discharged at maximum chiropractic benefit after 31 visits", "findings likely chronic")],
    flags=[
        flag("P1", "pre_existing", "must", [7], [(7, "excerpt", "Mild disc desiccation")],
             "Imaging term an adjuster may argue shows degeneration; stated as a finding only.", "degenerative_language"),
        flag("K1", "causation", "must", [7], [(7, "excerpt", "findings likely chronic")],
             "Hedged radiology wording ('likely chronic') that an adjuster can use against causation.", "hedged_imaging"),
        flag("C1", "conflict", "should", [3, 6], [(3, "excerpt", "Plan: 3 visits per week for 12 weeks"), (6, "excerpt", "Discharged at maximum chiropractic benefit after 31 visits")],
             "Plan of 36 visits (3 per week for 12 weeks) vs discharge after 31 visits; shown side by side, not resolved.", "treatment_plan"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "from_date": "2026-04-09", "to_date": "2026-05-07", "days": 28, "statement": "28-day interval (records 3 to 4) is a near-miss and must NOT be flagged as a gap."},
                   {"id": "N2", "type": "gap", "statement": "No gap flag for the 3, 20 and 19-day intervals."}],
    tolerated=[flag("T1", "causation", "tolerated", [4], [(4, "excerpt", "Pain 5/10, unchanged from visit 1")],
                    "'Unchanged' pain at visit 14 may be raised as a plateau note; the tool must word it as the record does.", "no_improvement")],
    must_not=[
        mn_judge("M1", "Characterises the chiropractic care as excessive, unnecessary or over-treatment (an adjuster's argument, not a record fact).",
                 ["Excessive chiropractic care (31 visits).", "Over-treatment by the chiropractor.", "Chiropractic visits were not medically necessary."],
                 ["Plan: 3 visits per week for 12 weeks.", "Discharged at maximum chiropractic benefit after 31 visits.", "Pain 5/10, unchanged from visit 1."]),
        mn_judge("M2", "States the disc bulge is chronic or degenerative as fact; the record says 'findings likely chronic' (a hedge) and 'mild disc desiccation'.",
                 ["Chronic L4-L5 disc disease.", "The disc bulge is chronic.", "Degenerative disc disease at L4-L5."],
                 ["Mild disc desiccation; radiology says findings likely chronic.", "L4-L5 disc bulge without nerve root compression.", "Radiology: findings likely chronic."]),
        mn_regex("M3", "Adds a diagnosis the records do not state (whiplash, herniation, radiculopathy).",
                 r"(?i)\b(whiplash|herniat\w+|radiculopath\w+)\b",
                 ["Whiplash injury.", "L4-L5 herniation.", "Lumbar radiculopathy."],
                 ["Disc bulge without nerve root compression.", "Dx: lumbar and cervical sprain.", "Cervical and lumbar spasm."]),
        mn_amount("M4", "Treats visit counts, weeks or pain scores as dollars, or totals the per-visit rate (36 x 120 = 4,320; 31 x 120 = 3,720).", [3, 12, 31, 36, 3720, 4320, 11820]),
    ],
    notes=["Hand arithmetic: 04-06 to 04-09 = 3; 04-09 to 05-07 = 21 (to Apr 30) + 7 = 28 (near-miss); 05-07 to 05-27 = 20; 05-27 to 06-15 = 19; 06-15 to 07-20 = 15 (to Jun 30) + 20 = 35 (flag).",
           "Forbidden guess-sums: 36 x 120 = 4,320; 31 x 120 = 3,720; 7,500 + 4,320 = 11,820."]))

# ───────────────────────── L4: dog bite, plastics, scar revision (S4) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib04_dog_bite_scar_revision", source_ref="S4",
    description="Library L4 (mirrors S4). Facial dog bite repaired in the ED, plastic-surgery follow-ups with scar photographs, a planned 8-week interval that the tool still flags, a $6,500 revision estimate and a later revision with a surgeon fee. The tool must not predict permanence or disfigurement.",
    stress_types=["planned_interval_still_flagged", "estimate_vs_actual_amount", "scar_documentation", "long_gap_before_revision", "no_prediction_of_permanence"],
    records=[
        rec("2025-09-13", "Wrenfield EMS run report",
            "Adult bitten on the left cheek and chin by a neighbor's dog. Bleeding controlled. Transported to Harlow Memorial ED.",
            must="bitten on the left cheek and chin by a neighbor's dog", terms=["left cheek", "chin"]),
        rec("2025-09-13", "Harlow Memorial ED",
            "Dx: dog bite, left cheek laceration 4 cm and chin laceration 2 cm. Wounds irrigated and sutured. Amoxicillin-clavulanate prescribed. ED charge: $4,730.",
            must="left cheek laceration 4 cm and chin laceration 2 cm", terms=["4 cm", "2 cm", "sutured"]),
        rec("2025-09-20", "Dr. Odalys Pennywhistle, plastic surgery",
            "Suture removal. Wounds healing with erythema along the cheek scar. Patient states she is self-conscious about the scar.",
            must="Suture removal", terms=["suture removal", ["patient states", "per patient", "patient reports"]],
            spans=[span("Patient states she is self-conscious about the scar.", ["patient states", "per patient", "patient reports"])]),
        rec("2025-10-18", "Dr. Odalys Pennywhistle, plastic surgery",
            "Cheek scar 4 cm, raised and erythematous. Silicone sheeting and massage started. Photographs taken for the chart. Return in 8 weeks.",
            must="Cheek scar 4 cm, raised and erythematous", terms=["4 cm", "silicone"]),
        rec("2025-12-13", "Dr. Odalys Pennywhistle, plastic surgery",
            "Scar remains raised at 3 months. Revision discussed if no improvement by 12 months. Estimated revision cost: $6,500.",
            must="Scar remains raised at 3 months", terms=["raised", "3 months", "revision"]),
        rec("2026-09-12", "Dr. Odalys Pennywhistle, plastic surgery, operative note",
            "Scar revision performed under local anesthesia. Surgeon fee: $3,900. Photographs taken.",
            must="Scar revision performed under local anesthesia", terms=["scar revision", "local anesthesia"]),
    ],
    amounts=[amt(2, "$4,730", 4730, "charge", "ED charge: $4,730"),
             amt(5, "$6,500", 6500, "estimate", "Estimated revision cost: $6,500", note="Estimate, not a charge; the later fee is stated separately in record 6.", required=True),
             amt(6, "$3,900", 3900, "charge", "Surgeon fee: $3,900")],
    unclear={"A2": "estimate $6,500 for a revision; not a billed charge; needs review"},
    gap_flags=[("G1", 4, 5, "Return in 8 weeks", "Scar remains raised at 3 months"),
               ("G2", 5, 6, "Revision discussed if no improvement by 12 months", "Scar revision performed under local anesthesia")],
    flags=[],
    must_not_flag=[{"id": "N1", "type": "pre_existing", "statement": "No prior-condition flag: the record names none."},
                   {"id": "N2", "type": "causation", "statement": "'Bitten ... by a neighbor's dog' is mechanism of injury, not weakening language."},
                   {"id": "N3", "type": "gap", "from_date": "2025-09-13", "to_date": "2025-09-20", "days": 7, "statement": "No gap flag for the 7 and 28-day intervals."}],
    tolerated=[],
    must_not=[
        mn_judge("M1", "Predicts permanence, disfigurement or the future course of the scar; the record gives size, appearance and a revision plan only.",
                 ["Permanent facial disfigurement.", "The scar will never fade.", "Disfigured for life."],
                 ["Cheek scar 4 cm, raised and erythematous.", "Scar remains raised at 3 months.", "Scar revision performed under local anesthesia."]),
        mn_judge("M2", "Adds dog ownership, breed, liability or provocation facts that the record does not state.",
                 ["The neighbor's unleashed pit bull attacked her.", "The owner is liable for the bite.", "The dog was provoked."],
                 ["Adult bitten on the left cheek and chin by a neighbor's dog.", "Rabies status was not stated in the record.", "Dx: dog bite."]),
        mn_judge("M3", "Treats the $6,500 estimate as a billed charge, or replaces the estimate with the actual fee as if the estimate had not been stated.",
                 ["Revision cost $6,500.", "Billed charges include the $6,500 revision.", "The revision was originally billed at $3,900."],
                 ["Estimated revision cost: $6,500 (estimate, not counted).", "Surgeon fee: $3,900.", "Revision discussed if no improvement by 12 months."]),
        mn_amount("M4", "Counts the estimate in a total or treats centimetres, weeks or months as dollars.", [2, 4, 8, 12, 6500, 10400, 15130]),
    ],
    notes=["Hand arithmetic: 2025-09-13 to 09-20 = 7; 09-20 to 10-18 = 10 (to Sep 30) + 18 = 28 (near-miss, no flag); 10-18 to 12-13 = 13 (to Oct 31) + 30 + 13 = 56 (flag; record 4 says 'Return in 8 weeks', so the interval is planned but still flagged by code); 12-13 to 2026-09-12 = 19 (to Jan 1) + 254 = 273 (flag).",
           "Charges counted: $4,730 + $3,900 = $8,630. The $6,500 estimate is not counted. Forbidden: 4,730 + 6,500 + 3,900 = 15,130; 6,500 + 3,900 = 10,400."]))

# ───────────────────────── L5: pedestrian, ORIF, hardware removal (S5) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib05_pedestrian_orif_hardware", source_ref="S5",
    description="Library L5 (mirrors S5). Pedestrian struck in a crosswalk; tibial plateau fracture with ORIF, PT, persistent pain, hardware removal seven months later and a hedged future knee replacement. A prior arthroscopy appears in the history. Two gaps (49 and 119 days).",
    stress_types=["operative_report", "hardware_removal_second_surgery", "two_gaps", "prior_surgery_in_history", "hedged_future_care"],
    records=[
        rec("2026-01-22", "Brightwater EMS run report",
            "Pedestrian struck by a vehicle in a crosswalk. Left knee deformity, unable to bear weight. Transported to Coldharbor Trauma Center.",
            must="Pedestrian struck by a vehicle in a crosswalk", terms=["left knee", "unable to bear weight"]),
        rec("2026-01-22", "Coldharbor Trauma Center ED",
            "Dx: left tibial plateau fracture and left fibular fracture. Splinted. Admitted to orthopedics. ED charges: $38,420.",
            must="Dx: left tibial plateau fracture and left fibular fracture", terms=["left tibial plateau fracture", "left fibular fracture"]),
        rec("2026-01-24", "Dr. Casimir Voss, orthopedic surgery, operative report",
            "Open reduction and internal fixation, left tibial plateau, two screws. Non-weight-bearing 8 weeks.",
            must="Open reduction and internal fixation, left tibial plateau, two screws", terms=["open reduction and internal fixation", "two screws", "8 weeks"]),
        rec("2026-02-19", "Dr. Casimir Voss, orthopedic surgery, clinic",
            "Incision healing. Radiographs show hardware in good position. Begin physical therapy. Patient reports a prior left knee arthroscopy in 2019.",
            must="Radiographs show hardware in good position", terms=["physical therapy", ["patient reports", "per patient", "patient states"]],
            spans=[span("Patient reports a prior left knee arthroscopy in 2019.", ["patient reports", "per patient", "patient states", "patient-reported"])]),
        rec("2026-03-05", "Mosswood Physical Therapy, initial evaluation",
            "Left knee flexion limited to 80 degrees. Plan of care: 16 visits. Charge per visit $175.",
            must="Left knee flexion limited to 80 degrees", terms=["80 degrees"]),
        rec("2026-04-23", "Mosswood Physical Therapy, visit 12", "Flexion 115 degrees. Pain 4/10.",
            must="Flexion 115 degrees", terms=["115 degrees"]),
        rec("2026-08-20", "Dr. Casimir Voss, orthopedic surgery, clinic",
            "Persistent knee pain 5/10 with atrophy of left thigh. Hardware removal discussed.",
            must="Persistent knee pain 5/10 with atrophy of left thigh", terms=["5/10", "hardware removal"]),
        rec("2026-09-10", "Dr. Casimir Voss, orthopedic surgery, operative report",
            "Removal of hardware, left tibial plateau. Subchondral cyst repaired. Total knee replacement may be needed in the future. Surgeon fee: $6,150.",
            must="Total knee replacement may be needed in the future", terms=["removal of hardware", "subchondral cyst", "may be needed"]),
    ],
    amounts=[amt(2, "$38,420", 38420, "charge", "ED charges: $38,420"),
             amt(5, "$175", 175, "rate", "Charge per visit $175", note="Rate, not a charge: visits billed are never stated (16 planned; visit 12 note present)."),
             amt(8, "$6,150", 6150, "charge", "Surgeon fee: $6,150")],
    unclear={"A2": "rate $175/visit; visit count not stated (16 planned); needs review"},
    gap_flags=[("G1", 5, 6, "Plan of care: 16 visits", "Flexion 115 degrees"),
               ("G2", 6, 7, "Flexion 115 degrees. Pain 4/10", "Persistent knee pain 5/10")],
    flags=[
        flag("P1", "pre_existing", "must", [4], [(4, "excerpt", "Patient reports a prior left knee arthroscopy in 2019")],
             "Prior left knee arthroscopy (2019), reported by the patient. Same knee as the fracture.", "prior_surgery_reported"),
        flag("K1", "causation", "should", [8], [(8, "excerpt", "Total knee replacement may be needed in the future")],
             "Future care stated only as possible; the tool does not predict it.", "speculative_language"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 2, 26, 14 and 21-day intervals."},
                   {"id": "N2", "type": "causation", "statement": "'Pedestrian struck by a vehicle' is mechanism of injury, not weakening language."}],
    tolerated=[],
    must_not=[
        mn_judge("M1", "States a future knee replacement or permanent impairment as certain or probable.",
                 ["She will need a total knee replacement.", "Permanent knee impairment.", "Knee replacement is inevitable."],
                 ["Total knee replacement may be needed in the future.", "Persistent knee pain 5/10 with atrophy of left thigh.", "Hardware removal discussed."]),
        mn_judge("M2", "Attributes the persistent pain or the atrophy to the prior arthroscopy or to the collision.",
                 ["Pain is from the 2019 arthroscopy.", "Persistent pain caused by the crash.", "Atrophy due to the prior knee condition."],
                 ["Persistent knee pain 5/10 with atrophy of left thigh.", "Patient reports a prior left knee arthroscopy in 2019.", "Subchondral cyst repaired."]),
        mn_judge("M3", "Changes the side, bone or procedure (right knee, femur fracture, knee replacement performed).",
                 ["Right tibial plateau fracture.", "Femur fracture repaired.", "Total knee replacement performed on 2026-09-10."],
                 ["Left tibial plateau fracture and left fibular fracture.", "Open reduction and internal fixation, left tibial plateau, two screws.", "Removal of hardware, left tibial plateau."]),
        mn_amount("M4", "Treats degrees, weeks, visits or years as dollars, or totals the per-visit rate (16 x 175 = 2,800).", [8, 12, 16, 80, 115, 2019, 2800, 47370]),
    ],
    notes=["Hand arithmetic: 01-22 to 01-24 = 2; 01-24 to 02-19 = 7 (to Jan 31) + 19 = 26; 02-19 to 03-05 = 9 (to Feb 28) + 5 = 14; 03-05 to 04-23 = 26 (to Mar 31) + 23 = 49 (flag); 04-23 to 08-20 = 119 (flag); 08-20 to 09-10 = 21.",
           "Charges counted: $38,420 + $6,150 = $44,570. Forbidden: 44,570 + 2,800 = 47,370."]))

# ───────────────────────── L6: letter of protection, billed vs adjusted amounts (S6) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib06_lop_billed_vs_adjusted", source_ref="S6",
    description="Library L6 (mirrors S6). Side-impact collision, attorney-referred clinic treating under a letter of protection, a billing statement with a balance, and an imaging bill with an adjustment and an amount due. Only stated charges are counted; adjustments, balances and amounts due are unclear and appear in internal notes only (D-019). The billing statement sits inside a 35-day visit gap.",
    stress_types=["letter_of_protection", "attorney_referral", "billed_vs_adjusted_amounts", "billing_statement_inside_gap", "balance_double_count_trap"],
    records=[
        rec("2026-05-02", "Eastvale Fire-Rescue run report",
            "Car struck on the passenger side at an intersection. Driver C/O shoulder pain. Transported to Larchmont Ridge ED.",
            must="Car struck on the passenger side at an intersection", terms=["shoulder pain"]),
        rec("2026-05-02", "Larchmont Ridge ED",
            "Dx: right shoulder contusion. X-ray negative. Sling provided. ED charge: $2,880.",
            must="Dx: right shoulder contusion", terms=["right shoulder contusion", "x-ray negative"]),
        rec("2026-05-13", "Gannet and Moor Injury Clinic, new patient",
            "Patient referred by attorney. Right shoulder pain 6/10. Treating under a letter of protection. Plan: MRI and injections.",
            must="Patient referred by attorney", terms=["referred by attorney", "letter of protection", "6/10"]),
        rec("2026-06-03", "Gannet and Moor Injury Clinic, billing statement",
            "Statement of charges: office visits $1,100; MRI referral fee $450. Balance under letter of protection: $1,550.",
            kind="billing_statement", must="Statement of charges", terms=["statement of charges"],
            note="Billing statement: listed as an entry, never a gap endpoint."),
        rec("2026-06-17", "Larchmont Ridge Imaging, right shoulder MRI",
            "Mild supraspinatus tendinosis; no full-thickness tear. Charge: $2,400. Insurance adjustment: -$1,250. Amount due: $1,150.",
            must="no full-thickness tear", terms=["supraspinatus tendinosis", "no full-thickness tear"]),
        rec("2026-07-08", "Gannet and Moor Injury Clinic, injection visit", "Subacromial injection performed. Pain 4/10.",
            must="Subacromial injection performed", terms=["injection"]),
        rec("2026-09-02", "Gannet and Moor Injury Clinic, follow-up", "Pain 3/10. Continue home exercises.",
            must="Pain 3/10", terms=["3/10"]),
    ],
    amounts=[amt(2, "$2,880", 2880, "charge", "ED charge: $2,880"),
             amt(4, "$1,100", 1100, "charge", "office visits $1,100"),
             amt(4, "$450", 450, "charge", "MRI referral fee $450"),
             amt(4, "$1,550", None, "unclear", "Balance under letter of protection: $1,550", note="Balance equals the two statement lines ($1,100 + $450); counting it would double count."),
             amt(5, "$2,400", 2400, "charge", "Charge: $2,400"),
             amt(5, "$1,250", None, "unclear", "Insurance adjustment: -$1,250", note="Adjustment, not a charge; negative sign."),
             amt(5, "$1,150", None, "unclear", "Amount due: $1,150", note="Net amount due after adjustment; not the billed charge.")],
    unclear={"A4": "balance $1,550 equals statement lines A2 + A3; not counted; needs review",
             "A6": "insurance adjustment -$1,250; not a charge; needs review (billed vs paid/incurred is a legal question, not a tool decision)",
             "A7": "amount due $1,150 after adjustment; not the billed charge; needs review"},
    gap_flags=[("G1", 3, 5, "Plan: MRI and injections", "Mild supraspinatus tendinosis"),
               ("G2", 6, 7, "Subacromial injection performed", "Continue home exercises")],
    flags=[
        flag("K1", "causation", "should", [3], [(3, "excerpt", "Patient referred by attorney")],
             "Attorney referral and letter-of-protection treatment (internal notes only, D-001/D-018); the tool states the record wording and draws no inference about charges.", "litigation_referral"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 11 and 21-day intervals; the 2026-06-03 billing statement is not a gap endpoint."}],
    tolerated=[flag("T1", "pre_existing", "tolerated", [5], [(5, "excerpt", "Mild supraspinatus tendinosis")],
                    "Tendinosis wording an adjuster may argue is degenerative; tolerated, not required.", "degenerative_language")],
    must_not=[
        mn_judge("M1", "Implies the attorney steered treatment, that charges are inflated or unreasonable, or that the letter of protection changes the care (adjuster arguments, not record facts).",
                 ["The attorney steered her to this clinic to build the claim.", "Charges exceed the reasonable value of the care.", "Treatment was inflated by the letter of protection."],
                 ["Patient referred by attorney; treating under a letter of protection.", "Plan: MRI and injections.", "Right shoulder pain 6/10."]),
        mn_judge("M2", "Nets the adjustment or states the amount due as the billed charge; the letter total counts stated charges only.",
                 ["MRI billed at $1,150.", "Charges after insurance adjustment total $5,280.", "MRI charge was reduced to $1,150."],
                 ["Charge: $2,400 (adjustment and amount due listed in notes).", "Billed charges stated in these records: $6,830.00.", "Insurance adjustment appears in the record; not netted."]),
        mn_amount("M3", "Counts the adjustment, the amount due or the balance as a charge, or double counts the balance (values 1,150 / 1,250 / 1,550 / 8,380).", [1150, 1250, 1550, 8380, 5280]),
    ],
    notes=["Hand arithmetic: encounters 05-02 (rec 1, 2), 05-13, 06-17, 07-08, 09-02; the 06-03 billing statement is excluded. 05-02 to 05-13 = 11; 05-13 to 06-17 = 18 (to May 31) + 17 = 35 (flag); 06-17 to 07-08 = 21; 07-08 to 09-02 = 23 (to Jul 31) + 31 + 2 = 56 (flag).",
           "Charges counted: 2,880 + 1,100 + 450 + 2,400 = 6,830. Forbidden: 6,830 + 1,550 = 8,380; 2,880 + 2,400 = 5,280 (statement lines omitted)."]))

# ───────────────────────── L7: workplace-adjacent fall, missing outside records (S7) ─────────────────────────
SPECS.append(dict(
    case_id="case_lib07_parking_lot_fall_outside_records", source_ref="S7",
    description="Library L7 (mirrors S7). Fall on ice in the employer's parking lot before a shift (patient says not on duty), wrist fracture plus low back pain, a prior back surgery in another state with outside records requested and not received, MRI with postoperative changes and a cannot-be-excluded hedge, and an orthopedist who declines to state causation to a reasonable degree of medical probability. No gaps: every interval is 28 days.",
    stress_types=["workplace_adjacent_not_work_comp", "prior_surgery_outside_records_missing", "physician_declines_causation_opinion", "hedge_cannot_be_excluded", "all_intervals_28_days"],
    records=[
        rec("2026-02-10", "Quarry Hill Occupational Health, intake",
            "Employee slipped on ice in the employer parking lot before the shift and fell on the right wrist and low back. Reported to supervisor. Not on duty at the time per patient.",
            must="slipped on ice in the employer parking lot", terms=["right wrist", "low back", ["per patient", "patient states"]],
            spans=[span("Not on duty at the time per patient.", ["per patient", "patient states", "patient reports"])]),
        rec("2026-02-10", "Cobblestone Imaging",
            "X-ray right wrist: nondisplaced distal radius fracture. X-ray lumbar spine: mild degenerative changes. Charge: $640.",
            must="nondisplaced distal radius fracture", terms=["nondisplaced distal radius fracture", "mild degenerative changes"]),
        rec("2026-02-17", "Dr. Eudora Fennimore, orthopedics",
            "Casted right distal radius fracture. Patient states she had prior low back surgery in another state and outside records have been requested. Low back pain 6/10.",
            must="Casted right distal radius fracture", terms=["casted", "outside records", ["patient states", "per patient", "patient reports"]],
            spans=[span("Patient states she had prior low back surgery in another state and outside records have been requested.", ["patient states", "per patient", "patient reports"])]),
        rec("2026-03-17", "Dr. Eudora Fennimore, orthopedics", "Wrist healing in cast. Outside records not yet received. Low back pain persists.",
            must="Outside records not yet received", terms=["outside records not yet received"]),
        rec("2026-04-14", "Dr. Eudora Fennimore, orthopedics", "Cast removed. Wrist range of motion improving. Low back pain 5/10; lumbar MRI ordered.",
            must="Cast removed", terms=["cast removed", "lumbar MRI"]),
        rec("2026-05-12", "Cobblestone Imaging, lumbar MRI",
            "L4-L5 disc protrusion with mild canal narrowing. Postoperative changes at L4-L5. Possible aggravation of a pre-existing condition cannot be excluded. MRI charge: $1,980.",
            must="Possible aggravation of a pre-existing condition cannot be excluded", terms=["L4-L5 disc protrusion", "postoperative changes", "cannot be excluded"]),
        rec("2026-06-09", "Dr. Eudora Fennimore, orthopedics",
            "Surgeon cannot state to a reasonable degree of medical probability whether the fall aggravated the low back condition. Recommend epidural steroid injection at L4-L5.",
            must="cannot state to a reasonable degree of medical probability", terms=["cannot state", "reasonable degree of medical probability", "epidural steroid injection"]),
    ],
    amounts=[amt(2, "$640", 640, "charge", "Charge: $640"), amt(6, "$1,980", 1980, "charge", "MRI charge: $1,980")],
    unclear={},
    gap_flags=[],
    flags=[
        flag("P1", "pre_existing", "must", [2], [(2, "excerpt", "mild degenerative changes")],
             "Lumbar x-ray wording an adjuster may argue shows a pre-existing condition; stated as a finding only.", "degenerative_language"),
        flag("P2", "pre_existing", "must", [3], [(3, "excerpt", "prior low back surgery in another state")],
             "Prior low back surgery reported by the patient; outside records requested, not in this packet.", "prior_surgery_reported"),
        flag("P3", "pre_existing", "must", [6], [(6, "excerpt", "Postoperative changes at L4-L5")],
             "Imaging shows postoperative change at the level later injected; the tool does not link it to the fall.", "prior_surgery_imaging"),
        flag("K1", "causation", "must", [6], [(6, "excerpt", "Possible aggravation of a pre-existing condition cannot be excluded")],
             "Hedged radiology language; possibility only.", "hedged_imaging"),
        flag("K2", "causation", "must", [7], [(7, "excerpt", "cannot state to a reasonable degree of medical probability")],
             "The treating surgeon declines to give a causation opinion at the legal standard.", "no_causation_opinion"),
    ],
    must_not_flag=[{"id": "N1", "type": "gap", "from_date": "2026-02-17", "to_date": "2026-03-17", "days": 28, "statement": "Every interval after the first is 28 days (near-miss); no gap flag for any interval."}],
    tolerated=[flag("T1", "pre_existing", "tolerated", [4], [(4, "excerpt", "Outside records not yet received")],
                    "Missing outside records may be noted as an open item; tolerated, not required.", "missing_prior_records")],
    must_not=[
        mn_judge("M1", "Decides whether the back condition is pre-existing, aggravated or caused by the fall.",
                 ["The fall aggravated her pre-existing back condition.", "Her back problem predates the fall.", "The fall caused the L4-L5 protrusion."],
                 ["Possible aggravation of a pre-existing condition cannot be excluded.", "Surgeon cannot state to a reasonable degree of medical probability whether the fall aggravated the low back condition.", "Postoperative changes at L4-L5."]),
        mn_regex("M2", "Classifies the fall as a work injury or workers' compensation matter; the record says only 'not on duty at the time per patient'.",
                 r"(?i)\bwork(?:ers['’]?)?\s*comp\w*|\bon[- ]the[- ]job\b|\binjured on duty\b|\bwork injury\b",
                 ["Work injury; workers' compensation applies.", "Injured on duty in the parking lot.", "On-the-job fall."],
                 ["Employee slipped on ice in the employer parking lot before the shift.", "Not on duty at the time per patient.", "Reported to supervisor."]),
        mn_judge("M3", "States the prior back surgery's date, type or level, or what the outside records show; none is in the packet.",
                 ["Prior L4-L5 fusion in 2018.", "Outside records confirm a prior discectomy.", "The prior surgery was a laminectomy."],
                 ["Prior low back surgery in another state, per patient.", "Outside records not yet received.", "Outside records have been requested."]),
        mn_amount("M4", "Treats the 28-day interval, pain scores or levels as dollars.", [4, 5, 6, 28, 5]),
    ],
    notes=["Hand arithmetic: 02-10 to 02-17 = 7; then 02-17 to 03-17 = 11 (to Feb 28) + 17 = 28; 03-17 to 04-14 = 14 + 14 = 28; 04-14 to 05-12 = 16 + 12 = 28; 05-12 to 06-09 = 19 + 9 = 28. No flags (strictly > 30).",
           "Charges counted: $640 + $1,980 = $2,620."]))


# ───────────────────────── builder ─────────────────────────
def build(sp):
    recs = sp["records"]
    lines = [HEADER, ""]
    for i, r in enumerate(recs, 1):
        lines += [f"=== Record {i} ===", f"Date: {r['raw']}", f"Source: {r['source']}", f'Excerpt: "{r["excerpt"]}"', ""]
    txt = "\n".join(lines)

    records = [{"record_no": i, "raw_date": r["raw"], "date": r["date"], "kind": r["kind"], "source": r["source"]} for i, r in enumerate(recs, 1)]
    entries = []
    for i, r in enumerate(recs, 1):
        e = {"id": f"E{i}", "record_nos": [i], "date": r["date"], "date_status": "parsed", "encounter": r["kind"] == "encounter",
             "provider": r["source"], "must_contain_excerpt": r["must"], "required_terms": r["terms"]}
        if r["spans"]:
            e["self_report_spans"] = r["spans"]
        if r["note"]:
            e["note"] = r["note"]
        entries.append(e)

    by = {}
    excluded = []
    for i, r in enumerate(recs, 1):
        if r["kind"] == "encounter":
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

    amounts, ids = [], {}
    for n, a in enumerate(sp["amounts"], 1):
        aid = f"A{n}"
        d = {"id": aid, "record_no": a["record_no"], "raw": a["raw"], "value": a["value"], "class": a["cls"], "excerpt": a["excerpt"],
             "in_total": a["in_total"], "required": a["required"], "needs_review": a["needs_review"]}
        if a["note"]:
            d["note"] = a["note"]
        amounts.append(d)
    total = sum(a["value"] for a in amounts if a["in_total"])
    counted = [a["id"] for a in amounts if a["in_total"]]
    unclear_items = [{"amount_id": k, "reason": v, "total_computed": False} for k, v in sp["unclear"].items()]
    for k in sp["unclear"]:
        assert any(a["id"] == k and not a["in_total"] for a in amounts), (sp["case_id"], k)
    totals = {"explicit_charges_total": total, "counted_amount_ids": counted, "amounts_found": len(amounts),
              "status": "partial_unclear" if unclear_items else "complete", "unclear_items": unclear_items,
              "letter_line": f"Billed charges stated in these records: ${total:,.2f}", "ui_line": f"Accepted charges: ${total:,.2f}",
              "notes_lines": [f"{next(a['raw'] for a in amounts if a['id'] == k)}: {v}" for k, v in sp["unclear"].items()]}

    ex = {"schema_version": "golden/1", "case_id": sp["case_id"], "synthetic": True, "input_file": sp["case_id"] + ".txt",
          "description": sp["description"], "stress_types": sp["stress_types"], "records": records, "entries": entries,
          "expected_entry_count": len(entries), "gap_excluded_records": excluded, "gap_table": gap_table, "amounts": amounts,
          "totals": totals, "flags": flags, "must_not_flag": sp["must_not_flag"], "tolerated": sp["tolerated"], "record_warnings": [],
          "must_not": sp["must_not"],
          "notes": [f"Library packet; real-world scenario source: {sp['source_ref']} (research/case-library-sources.md). All names invented."] + sp["notes"]}
    return txt, ex


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for sp in SPECS:
        txt, ex = build(sp)
        (OUT / (sp["case_id"] + ".txt")).write_text(txt)
        (OUT / (sp["case_id"] + ".expected.json")).write_text(json.dumps(ex, indent=2, ensure_ascii=False) + "\n")
        print("wrote", sp["case_id"], "records", len(sp["records"]), "total", ex["totals"]["explicit_charges_total"],
              "gaps", [g["days"] for g in ex["gap_table"]])


if __name__ == "__main__":
    main()
