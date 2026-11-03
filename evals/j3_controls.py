"""J3 seeded controls, built from pairs the shipped code actually proposes (T-093 r4, staff-engineer r3 major 1).

The first J3 controls were hand-written pairs (laterality, dates, doses, pain scores). conflict_candidates.candidates() never proposes those, so the
gate measured a path the product does not have. Here every J3 control input IS a candidate: the generator is run over the golden and library packets
(origin "packet": the real candidates) and over deliberately crafted variants of those real candidates (origin "variant": one quote replaced, the
other kept). A variant is only written if the generator proposes exactly that pair; the quotes in the file are the generator's own output.

Labels are LOCKED in SPEC below, with a rationale per item, before any live run (D-046): a failing item is a finding, never a relabel. `python -m
evals.j3_controls` regenerates the J3 rows of judge_controls.jsonl / judge_controls_heldout.jsonl and leaves the J4 rows byte for byte as they are.
`python -m evals.j3_controls --check` verifies the committed files equal the build (no live model, no network).

Row fields beyond the J4 rows: rule (the code rule that proposes it), origin, packet + packet_record_nos (real candidates), derived_from (variants),
records (the record texts the generator was run on, so a test can re-derive the pair)."""
import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GOLD = ROOT / "evals" / "golden"
PACKET_DIRS = ("evals/golden", "evals/library")
PLAN_OUT = ("2026-01-23", "2026-03-06")        # the dates of the real sample plan (record 4) and outcome (record 6)
DENIAL = ("2026-09-14", "2026-09-21")          # the dates of the real case_06 denial (record 1) and a later history record

PLAN, TREAT, OTHER = "plan_vs_outcome", "treatment_plan_vs_actual", "other_fact_mismatch"
CONFLICT, BENIGN = "conflict", "benign"


def packet_paths():
    out = []
    for d in PACKET_DIRS:
        out += sorted((ROOT / d).glob("*.txt"))
    return out


def packet_records(path):
    """The records the pipeline hands the conflict pass for one packet (pipeline.py: the distinct records of supported languages, in group order)."""
    from app.backend import ingest
    ing = ingest.ingest(pathlib.Path(path).read_text())
    by = {r["n"]: r for r in ing["records"]}
    return [by[g[0]] for g in ing["groups"] if by[g[0]].get("lang") != "other"]


def packet_candidates():
    """[(packet path relative to ROOT, candidate)] for every golden and library packet, in file order."""
    from app.backend import conflict_candidates as CC
    out = []
    for p in packet_paths():
        out += [(p.relative_to(ROOT).as_posix(), c) for c in CC.candidates(packet_records(p))]
    return out


def slim(r):
    return {"n": r["n"], "date_iso": r.get("date_iso"), "source": r.get("source") or "SYNTHETIC", "excerpt": r["excerpt"]}


# --------------------------------------------------------------------------------------------------------- the locked spec
# kind "wrong" = the right answer is benign (the judge must NOT confirm the conflict); "correct" = the right answer is conflict.
# Real candidates: (id, kind, split, pair, packet, record numbers (a, b), a-quote, b-quote, why).
REAL = [
    ("J3R1", "correct", "in_sample", "evals/golden/sample.txt", (4, 6), "Plan of care: 12 visits.", "Discharged from PT after two missed appointments.",
     "plan of 12 visits, then a discharge after missed appointments: the plan and the outcome differ (golden sample expects treatment_plan_vs_actual)"),
    ("J3R2", "correct", "in_sample", "evals/golden/case_06_subtle_pre_existing.txt", (1, 2), "Patient denies prior neck problems.",
     "Has been seeing a chiropractor off and on since a lifting injury several years ago.",
     "a general-region denial against years of intermittent chiropractic care: the golden case_06 expects this conflict (judge_conflict_v5 rule 2c)"),
    ("J3R3", "correct", "in_sample", "evals/golden/case_06_subtle_pre_existing.txt", (1, 3), "Patient denies prior neck problems.",
     "History: occasional stiffness in the mornings at baseline.",
     "baseline symptoms before the accident against a denial of prior neck problems; the stiffness names no other body part (rule 2c); the golden case_06 lists it as a subtle pre-existing signal"),
    ("J3R4", "wrong", "in_sample", "evals/golden/case_06_subtle_pre_existing.txt", (1, 5), "Patient denies prior neck problems.",
     "Patient notes the old shoulder problem is acting up again.",
     "the denial is about the neck, the old problem is the shoulder: two facts that can both be true (rule 2a). The shoulder problem is a pre_existing flag of its own, not a contradiction of this denial"),
    # T-141 (GATE-M2 lib11): form-field denials are candidates now. Labels fixed here, before any run of these pairs; judge_conflict_v6 is unchanged.
    ("J3R5", "correct", "in_sample", "evals/library/case_lib11_priors_and_ledger.txt", (6, 1), "Prior accidents? Yes [ ] No [X].",
     "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.",
     "the intake form answers No to prior accidents and the primary-care note lists two earlier accidents: the golden-style lib11 conflict C1 (GATE-M2 paralegal major); both statements are the patient's own"),
    ("J3R6", "correct", "in_sample", "evals/library/case_lib11_priors_and_ledger.txt", (6, 1), "Prior injuries? Yes [ ] No IX].",
     "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.",
     "No to prior injuries against earlier accidents with neck and back pain treated with physical therapy: injuries that were treated (rule 2c)"),
    ("J3R7", "correct", "in_sample", "evals/library/case_lib11_priors_and_ledger.txt", (6, 1), "Prior injuries? Yes [ ] No IX].",
     "Problem list: hypertension, type 2 diabetes, chronic low back pain.",
     "No to prior injuries against a chronic low back pain problem-list entry: a paralegal wants to see it; `unsure` would be defensible. A correct item is reported, not gated (D-046)"),
]

# Variants: (id, kind, split, rule/category, pair-shape, derived_from, records [(date, text), (date, text)], a-quote, b-quote, why).
# The records are one earlier and one later record; the generator must propose exactly (a-quote, b-quote) from them.
V_PLAN = [
    # ---- in sample: a = the real sample plan "Plan of care: 12 visits." (J3R1) unless noted
    ("J3V1", "wrong", "in_sample", "J3R1", "Plan of care: 12 visits.", "Cyclobenzaprine discontinued due to drowsiness.",
     "stopping a medicine is not the course of care ending; the code's early-end pattern fires on the word 'discontinued' and the judge must not follow it"),
    ("J3V18", "wrong", "in_sample", "J3R1", "Twelve visits authorized.", "Patient discontinued smoking after the accident.",
     "quitting smoking is not the care course ending; the code fires on 'discontinued'. Was H3V1, labelled held_out; moved to in_sample in T-113 r2 because judge_conflict_v6 rule 1 names \"quitting smoking\""),
    ("J3V19", "wrong", "in_sample", "J3R1", "PT x 12 visits.", "Patient no longer attends the gym.",
     "gym attendance is not the care course; the code fires on 'no longer attends'. Was H3V3, labelled held_out; moved to in_sample in T-113 r2 because judge_conflict_v6 rule 1 names \"no longer going to the gym\""),
    ("J3V14", "wrong", "in_sample", "J3R1", "Plan of care: 12 visits.", "Ibuprofen was discontinued because of stomach upset.",
     "a second medicine stop (added in T-113 with judge_conflict_v6, before its first run): stopping a drug is not the course of care ending"),
    ("J3V2", "wrong", "in_sample", "J3R1", "Plan of care: 12 visits.", "Cancelled the appointment due to snow and rebooked for the next day.",
     "one cancelled and rebooked appointment: the course continues, so the plan and the outcome agree"),
    ("J3V3", "wrong", "in_sample", "J3R1", "Plan of care: 12 visits.", "Therapy stopped after visit 12 as planned.",
     "stopped at exactly the planned number of visits: the plan was carried out in full, nothing to reconcile (rule 1, a completed course is benign)"),
    ("J3V4", "correct", "in_sample", "J3R1", "Plan of care: 12 visits.", "Patient left PT after 4 sessions.",
     "12 planned, 4 attended, and the patient left: the plan and the outcome differ"),
    ("J3V5", "wrong", "in_sample", "J3R1", "Refer to physical therapy 2x/week for 6 weeks.", "Missed one appointment, made up the following week;",
     "the generator cuts the sentence at the semicolon, so the judge sees only this clause; it already says the visit was made up, so the course was not cut short"),
    ("J3V6", "correct", "in_sample", "J3R1", "Refer to physical therapy 2x/week for 6 weeks.", "PT discontinued after the first visit;",
     "a frequency-duration plan (12 visits, which code multiplies) that ended after the first visit; the outcome states no count, so no one multiplies to see it"),
]
V_DENIAL = [
    ("J3V20", "wrong", "in_sample", "J3R5", "Prior accidents? Yes [ ] No [X].", "Her roommate was in a car accident in 2019.",
     "T-141 twin of J3R5: the earlier accident is a roommate's (rule 2b), a person the code list does not name, so it still reaches the judge; the form answers about the patient's own accidents"),
    ("J3V7", "wrong", "in_sample", "J3R2", "Patient denies prior neck problems.", "History: left knee injury in 2022 treated with physical therapy.",
     "the denial names the neck, the injury is the left knee: both can be true (rule 2a)"),
    ("J3V10", "wrong", "in_sample", "J3R2", "Patient denies prior neck problems.", "History of seasonal allergies.",
     "a denied neck problem and an allergy history are two different conditions (rule 2a)"),
    ("J3V15", "wrong", "in_sample", "J3R2", "Patient denies prior neck problems.", "The at-fault motorist reported a previous collision at this intersection.",
     "the earlier collision is the other motorist's (rule 2b). Replaces J3V9: conflict_candidates now drops 'the other driver' pairs before the judge (T-113), so J3V9 is no longer a candidate; this wording is one the code list does not name, so it still reaches the judge"),
    ("J3V16", "wrong", "in_sample", "J3R2", "Patient denies any prior injury.", "Her roommate has a history of neck injury treated with physical therapy.",
     "a general denial is still about the patient; the roommate's injury is another person's (rule 2b). Replaces J3V13 (mother), which code now drops; 'roommate' is not on the code list"),
    ("J3V11", "correct", "in_sample", "J3R2", "Patient denies prior neck problems.", "Patient had a prior cervical strain in 2022.",
     "a cervical strain is a neck problem: the denial and the history cannot both be accurate"),
    ("J3V12", "correct", "in_sample", "J3R2", "Patient denies any prior injury.", "History: left knee injury in 2022 treated with physical therapy.",
     "the denial is general (any prior injury), so a named knee injury contradicts it (rule 2c); the twin of J3V7, where the denial names the neck"),
    ("J3V17", "wrong", "in_sample", "J3R2", "Patient denies any prior neck injury.", "Her teammate had a prior neck injury.",
     "the earlier injury is a teammate's (rule 2b). Was H3V16, labelled held_out; moved to in_sample in T-113 r2 because it was committed together with judge_conflict_v6, whose rule 2a names \"a teammate\". "
     "Replaced H3V7 (husband), which code drops; 'teammate' is not on the code list"),
]
HELD_PLAN = [
    ("H3V2", "correct", "held_out", "J3R1", "Twelve visits authorized.", "Patient dropped out of PT after visit 5.",
     "12 authorized, the patient dropped out after 5: the plan and the outcome differ"),
    ("H3V4", "correct", "held_out", "J3R1", "PT x 12 visits.", "Patient did not return after the second session;",
     "12 visits ordered, no return after the second session: the course ended early"),
    ("H3V5", "correct", "held_out", "J3R1", "Chiropractic 3x/week for 4 weeks.", "Cancelled the Tuesday appointment;",
     "relabelled from wrong (D-046, second-agent ruling reviews/T-093-staff-engineer-r4.md F1): judge_conflict rule 1 counts fewer visits attended than planned as a conflict whatever the reason, a cancellation with no make-up in the shown clause is that, and rule 5 makes a cut-off clause unsure at most; never benign. Accepted answers: conflict or unsure"),
    ("H3V6", "correct", "held_out", "J3R1", "Chiropractic 3x/week for 4 weeks.", "Missed three appointments in the second week.",
     "3x/week for 4 weeks is 12 visits and three were missed in week two: the course was not completed as planned"),
    # ---- T-113 r2: written and committed AFTER judge_conflict_v6 and BEFORE any run, to replace the three contaminated items (J3V17..J3V19). Phrasing the prompt does not
    # name: an unlisted medicine, stopped in a clause the generator cuts at a semicolon (the judge sees the cut-off clause); a pair of intake-form denials; a person the
    # code list does not name. Their distinguishing words are in HELD_TERMS and must not appear in the prompt (tests/unit/test_t113_heldout_audit.py).
    ("H3V17", "wrong", "held_out", "J3R1", "Ten visits of PT were authorized.", "Naproxen was discontinued after one week;",
     "stopping a medicine is not the course of care ending (judge_conflict rule 1); the code fires on 'discontinued' and the generator cuts the sentence at the semicolon, so the judge sees only this clause. "
     "An unlisted drug, and the prompt names none"),
    ("H3V18", "correct", "held_out", "J3R1", "Ten visits of PT were authorized.", "Patient stopped coming to PT after the third visit.",
     "10 authorized, the patient stopped coming after the third visit: the plan and the outcome differ; the twin of H3V17 on the same first quote"),
]
HELD_DENIAL = [
    ("H3V8", "correct", "held_out", "J3R2", "Patient denies any prior neck injury.", "Cervical strain in 2022 treated with physical therapy.",
     "a cervical strain is a neck injury: the denial and the history cannot both be accurate"),
    ("H3V9", "wrong", "held_out", "J3R2", "Denies prior back surgery.", "Prior surgery on the right knee in 2019.",
     "back surgery denied, knee surgery reported: different body parts, both can be true (rule 2a)"),
    ("H3V10", "correct", "held_out", "J3R2", "Denies prior back surgery.", "Prior lumbar fusion in 2019.",
     "a lumbar fusion is back surgery: the denial and the history cannot both be accurate"),
    ("H3V11", "wrong", "held_out", "J3R2", "No history of low back problems.", "Cervical strain in 2022 treated with physical therapy.",
     "a denied low back history and a neck strain: different regions, both can be true (rule 2a)"),
    ("H3V12", "correct", "held_out", "J3R2", "No history of low back problems.", "History: chronic low back pain since 2020.",
     "chronic low back pain since 2020 contradicts a denied low back history"),
    ("H3V13", "wrong", "held_out", "J3R2", "Patient denies prior neck problems.", "Patient was previously treated for migraines.",
     "a denied neck problem and migraines are different conditions (rule 2a)"),
    ("H3V14", "correct", "held_out", "J3R2", "Patient denies prior neck problems.", "Preexisting neck arthritis noted on X-ray.",
     "a pre-existing neck arthritis is a neck problem: the denial and the finding cannot both be accurate"),
    ("H3V15", "correct", "held_out", "J3R2", "No previous accidents.", "Patient reports an earlier collision in 2021 with a claim filed.",
     "an earlier collision with a claim contradicts 'no previous accidents'"),
    # ---- T-113 r2 (see the note above HELD_PLAN's new rows): a person the code list does not name, and an intake-form denial with its twin
    ("H3V19", "wrong", "held_out", "J3R2", "Patient denies any prior neck injury.", "The passenger in the other vehicle reported a prior neck injury.",
     "the earlier injury is the other vehicle's passenger's, not the patient's (rule 2a: anyone other than the patient). 'passenger' is not on the code list, so this reaches the judge; the twin is H3V8 on the same first quote"),
    ("H3V20", "correct", "held_out", "J3R2", "Patient denies any prior back injury.", "History: lumbar strain in 2021 treated with physical therapy.",
     "the denial is on the new-patient intake form; the patient's own record of a lumbar strain contradicts it (a lumbar strain is a back injury). A denial on an intake form is still the patient's statement and is compared"),
    ("H3V21", "wrong", "held_out", "J3R2", "Patient denies any prior back injury.", "Prior surgery on the right shoulder in 2018.",
     "the intake-form denial names the back, the surgery is the right shoulder: different body parts, both can be true (rule 2b); the twin of H3V20"),
]

# Records whose header makes gaps.admin_label() read them as paperwork (the source is the header). Only the denial side is used: an intake form is never a plan or an outcome.
SOURCE_A = {"H3V20": "Riverside Family Clinic, new patient intake form (SYNTHETIC)", "H3V21": "Riverside Family Clinic, new patient intake form (SYNTHETIC)"}

# The distinguishing words of every held-out J3 control, lower case. A held-out control is only held out while NONE of these appears in the current judge_conflict prompt
# (tests/unit/test_t113_heldout_audit.py, evals/heldout_audit.py): a word in the prompt measures keyword matching, not generalisation (T-113 r2, staff-engineer F1).
HELD_TERMS = {
    "H3V2": ["dropped out"], "H3V4": ["did not return"], "H3V5": ["tuesday"], "H3V6": ["second week"],
    "H3V8": ["cervical strain"], "H3V9": ["right knee"], "H3V10": ["lumbar fusion"], "H3V11": ["low back"], "H3V12": ["chronic low back"], "H3V13": ["migraine"],
    "H3V14": ["arthritis"], "H3V15": ["claim filed", "earlier collision"],
    "H3V17": ["naproxen"], "H3V18": ["stopped coming"], "H3V19": ["passenger"], "H3V20": ["lumbar strain"], "H3V21": ["shoulder"],
}


def _variant_rows():
    """[(spec tuple, shape)] where shape is 'plan' or 'denial'."""
    return [(s, "plan") for s in V_PLAN + HELD_PLAN] + [(s, "denial") for s in V_DENIAL + HELD_DENIAL]


def build_rows():
    """The J3 rows, in a fixed order, each produced by running the generator. Raises if the generator does not propose a spec'd pair."""
    from app.backend import conflict_candidates as CC
    rows = []
    real_by_id = {}
    for (i, kind, split, packet, nos, qa, qb, why) in REAL:
        recs = packet_records(ROOT / packet)
        cands = CC.candidates(recs)
        hit = [c for c in cands if (c["a"].record_no, c["b"].record_no) == nos and c["a"].text == qa and c["b"].text == qb]
        if len(hit) != 1:
            raise SystemExit(f"{i}: the generator does not propose exactly one candidate {nos} ({qa!r} / {qb!r}) on {packet}")
        c = hit[0]
        by = {r["n"]: r for r in recs}
        rows.append(_row(i, kind, split, c, why, origin="packet", extra={"packet": packet, "packet_record_nos": list(nos)},
                         records=[slim(by[n]) for n in sorted(set(nos))]))
        real_by_id[i] = c
    for (i, kind, split, derived, qa, qb, why), shape in _variant_rows():
        d1, d2 = PLAN_OUT if shape == "plan" else DENIAL
        recs = [{"n": 1, "date_iso": d1, "source": SOURCE_A.get(i, "SYNTHETIC"), "excerpt": qa}, {"n": 2, "date_iso": d2, "source": "SYNTHETIC", "excerpt": qb}]
        hit = [c for c in CC.candidates(recs) if c["a"].text == qa and c["b"].text == qb and (c["a"].record_no, c["b"].record_no) == (1, 2)]
        if len(hit) != 1:
            raise SystemExit(f"{i}: the generator does not propose ({qa!r}, {qb!r}) from its two records; got {[(c['a'].text, c['b'].text) for c in CC.candidates(recs)]}")
        want_rule = real_by_id[derived]["rule"]
        if hit[0]["rule"] != want_rule:
            raise SystemExit(f"{i}: rule {hit[0]['rule']} is not the rule of {derived} ({want_rule})")
        rows.append(_row(i, kind, split, hit[0], why, origin="variant", extra={"derived_from": derived}, records=recs))
    return rows


def _row(i, kind, split, c, why, origin, extra, records):
    return {"id": i, "synthetic": True, "judge": "j3", "kind": kind, "split": split, "pair": f"{c['rule']}:{c['a'].text}", "why": why,
            "category": c["category"], "excerpt_a": c["a"].text, "excerpt_b": c["b"].text, "expected": BENIGN if kind == "wrong" else CONFLICT,
            "rule": c["rule"], "origin": origin, **extra, "records": records}


FILES = (("judge_controls.jsonl", "in_sample"), ("judge_controls_heldout.jsonl", "held_out"))


def render(existing_lines, rows, split):
    """J3 rows of this split first, then the existing J4 rows byte for byte (J3 rows of the old file are dropped)."""
    keep = [l for l in existing_lines if l.strip() and json.loads(l)["judge"] != "j3"]
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows if r["split"] == split) + "".join(l.rstrip("\n") + "\n" for l in keep)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="fail if the committed control files differ from the build")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(ROOT))
    rows = build_rows()
    bad = 0
    for name, split in FILES:
        p = GOLD / name
        out = render(p.read_text().splitlines(True) if p.exists() else [], rows, split)
        if a.check:
            if p.read_text() != out:
                print(f"{name}: differs from the build"); bad = 1
        else:
            p.write_text(out)
            print(f"wrote {p.relative_to(ROOT)}")
    return bad


if __name__ == "__main__":
    raise SystemExit(main())
