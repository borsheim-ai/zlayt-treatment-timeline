"""T-141 round 3: a record dated before the stated accident date is an earlier visit (info only) when it has no injury, mechanism or accident vocabulary, or
when every such clause is negated or plainly history. Any other record is a date conflict (a safe false positive beats a hidden conflict). The reviewer's
30 fresh variants (r2_variants.py V1-V20, r2_variants2.py W1-W10) and round-1 variants A-L are the cases."""
import pytest

from app.backend import conflicts as C


def R(n, d, src, ex):
    return dict(n=n, date_iso=d, source=src, excerpt=ex, kind="encounter")


INT = lambda n, d, date: R(n, d, "Intake", f"Date of accident per intake form: {date}.")      # noqa: E731
STD = lambda first, src="PCP": [R(1, "2026-01-05", src, first), R(2, "2026-01-12", "PT", "Exam: ok."), INT(3, "2026-01-20", "2026-01-09")]      # noqa: E731

V = [
    ("V1 billing names the collision", "conflict", [R(1, "2026-01-05", "Hobbleton Clinic, billing statement", "Emergency services after motor vehicle collision. Balance forward."), R(2, "2026-01-12", "Capital PT, visit 1", "Exam: ok."), INT(3, "2026-01-20", "2026-01-09")]),
    ("V2 billing no mechanism", "info", [R(1, "2026-01-05", "Hobbleton Clinic, billing statement", "Balance forward."), R(2, "2026-01-12", "Capital PT, visit 1", "Exam: ok."), INT(3, "2026-01-20", "2026-01-09")]),
    ("V3 intake says rear-ended", "conflict", [R(1, "2026-01-05", "Intake", "New patient intake. Neck pain after being rear-ended. Date of accident: 2026-01-09."), R(2, "2026-01-12", "PT", "Exam: ok.")]),
    ("V4 intake dated before the accident it states", "conflict", [R(1, "2026-01-05", "Intake", "New patient intake. Prior accidents? Yes [ ] No [X]. Date of accident: 2026-01-09."), R(2, "2026-01-12", "PT", "Exam: ok.")]),
    ("V5 slipped and fell on ice", "conflict", STD("Slipped and fell on ice, wrist pain.", "PT")),
    ("V6 slip and fall at the store", "conflict", STD("Slip and fall at the grocery store, wrist pain.", "PT")),
    ("V7 pedestrian vs auto", "conflict", STD("Pedestrian vs auto. Neck pain 7/10.", "ER")),
    ("V8 since the incident, whiplash", "conflict", STD("Neck pain since the incident. Whiplash pattern.", "Chiro")),
    ("V9 car accident last year", "conflict", STD("Annual physical. Reports a car accident last year, fully recovered.")),
    ("V10 rear-ended in March 2025", "conflict", STD("Annual physical. Was rear-ended in March 2025, resolved.")),
    ("V11 ER 12/30/2025 rear-ended in December 2025", "conflict", [R(1, "2025-12-30", "ER", "Rear-ended in December 2025. Neck pain."), R(2, "2026-01-05", "PT", "Exam: ok."), INT(3, "2026-02-20", "2026-01-05")]),
    ("V12 vehicle registration", "info", STD("Vehicle registration renewed.", "DMV")),
    ("V13 hit her weight goal", "info", STD("Patient hit her weight goal of 150 lb. Annual physical.")),
    ("V14 fall risk screen", "info", STD("Annual physical. Fall risk screen negative. Flu shot given in the fall.")),
    ("V15 MVA in 2019, resolved", "conflict", STD("Annual physical, history reviewed; MVA in 2019, resolved.")),
    ("V16 struck by a car after a negated clause", "conflict", STD("No prior neck problems, was struck by a car while crossing the street. Neck pain.", "ER")),
    ("V17 no history of prior injury; MVC", "conflict", STD("No history of prior injury; restrained driver, MVC. Neck pain.", "ER")),
    ("V18 MVC with no history of LOC", "conflict", STD("MVC with no history of loss of consciousness", "ER")),
    ("V19 benign first, collision second", "conflict", [R(1, "2026-01-02", "PCP", "Annual physical."), R(2, "2026-01-05", "ER", "Rear-end collision. Neck pain."), R(3, "2026-01-12", "PT", "Exam: ok."), INT(4, "2026-01-20", "2026-01-09")]),
    ("V20 collision after the stated date only", "none", [R(1, "2026-01-09", "ER", "Rear-end collision. Neck pain."), R(2, "2026-01-12", "PT", "Exam: ok."), INT(3, "2026-01-20", "2026-01-09")]),
    ("W1 denies any accidents or falls", "info", STD("Annual physical. Denies any accidents or falls.")),
    ("W2 no recent accidents or injuries", "info", STD("Annual physical. No recent accidents or injuries.")),
    ("W3 healthy prior to the rear-end collision", "conflict", STD("Healthy prior to the rear-end collision. Neck pain since.", "ER")),
    ("W4 previously asymptomatic until the motor vehicle collision", "conflict", STD("Previously asymptomatic until the motor vehicle collision.", "ER")),
    ("W5 MVC with no history of LOC", "conflict", STD("MVC with no history of LOC.", "ER")),
    ("W6 prior balance from MVA of 03/04/2024", "conflict", STD("Statement. Prior balance from MVA of 03/04/2024.", "Clinic billing statement")),      # D-061: "prior balance" is not "prior MVA"; the MVA word is ungoverned
    ("W7 MVA on 03/04/2024, resolved", "conflict", STD("Annual physical. MVA on 03/04/2024, resolved.")),
    ("W8 auto insurance card, 2019 Honda", "info", STD("Registration. Auto insurance card on file; vehicle: 2019 Honda Civic.", "Intake")),
    ("W9 hit by a car 2 days ago", "conflict", STD("Patient hit by a car 2 days ago. Neck pain.")),
    ("W10 rear-ended in 2021, resolved", "conflict", STD("Annual physical - rear-ended in 2021, resolved.")),
    # round-1 variants (probe2.py) that are not shape-identical to the above
    ("A lib11 shape", "info", [R(1, "2026-03-04", "PCP", "Annual visit. History per patient: car accidents in 2019 and 2022."), R(2, "2026-03-18", "EMS", "Passenger vehicle struck from behind."), R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-18.")]),
    ("B vehicle hit from behind", "conflict", [R(1, "2026-01-09", "ER", "Restrained driver, vehicle hit from behind at a stoplight. Neck pain."), R(2, "2026-01-19", "PT", "Follow-up. Neck pain 5/10."), INT(3, "2026-02-20", "2026-01-19")]),
    ("C MVA 12/30/2025 vs stated 2026-01-05", "conflict", [R(1, "2025-12-30", "ER", "MVA 12/30/2025, neck pain."), R(2, "2026-01-05", "PT", "Follow-up. Neck pain 5/10."), INT(3, "2026-02-20", "2026-01-05")]),
    ("D no history of LOC after the collision", "conflict", [R(1, "2026-01-09", "ER", "Rear-end collision, no history of loss of consciousness. Neck pain."), R(2, "2026-01-19", "PT", "Follow-up."), INT(3, "2026-02-20", "2026-01-19")]),
    ("F another vehicle hit them", "conflict", [R(1, "2026-01-09", "ER", "Pt in car when another vehicle hit them. Neck pain 7/10."), R(2, "2026-01-19", "PT", "Follow-up."), INT(3, "2026-02-20", "2026-01-19")]),
    ("G model year in the collision sentence", "conflict", [R(1, "2026-01-09", "ER", "Rear-end collision, driver of a 2019 Honda Civic. Neck pain."), R(2, "2026-01-19", "PT", "Follow-up."), INT(3, "2026-02-20", "2026-01-19")]),
    ("H fell off a ladder last week", "conflict", [R(1, "2026-03-04", "PCP", "Patient fell off a ladder last week. Wrist pain."), R(2, "2026-03-18", "EMS", "Passenger vehicle struck from behind."), R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-18.")]),
    ("L neck pain only, then the collision on the stated day", "info", [R(1, "2026-03-04", "Chiro", "Neck pain 6/10, adjusted."), R(2, "2026-03-18", "ER", "Neck strain."), R(3, "2026-03-19", "Intake", "Date of injury: 2026-03-18. Rear-end collision.")]),
]


@pytest.mark.parametrize("label,expected,recs", V, ids=[v[0].split()[0] for v in V])
def test_accident_date_variant(label, expected, recs):
    out, note = C.accident_date_conflicts(recs), C.accident_date_note(recs)
    got = "conflict" if out else ("info" if note else "none")
    assert got == expected, label
    if got == "conflict":
        assert note is None and out[0]["category"] in ("accident_date_after_treatment", "accident_dates_differ")


@pytest.mark.parametrize("sentence", [
    "t-boned at an intersection", "sideswiped on the highway", "run over by a truck", "ran over by a bus", "airbag deployed", "seatbelt bruising across the chest",
    "was hit by a truck", "got hit at a light", "the other car hit them", "he hit the guardrail", "vehicle accident on the interstate", "motor vehicle, restrained",
    "collided with a pole", "crashed her bike", "a wreck on I-35", "struck from behind", "the incident left her sore", "pedestrian on a crosswalk", "fell on the stairs",
    "falling off a ladder", "whiplash pattern", "head injury", "trauma to the knee", "impact to the left side", "positive LOC", "loss of consciousness at the scene",
    "MVI at 40 mph", "rear ended at a stoplight",
])
def test_each_word_list_member_alone_makes_a_pre_accident_record_a_conflict(sentence):
    out = C.accident_date_conflicts(STD(f"Seen at clinic. {sentence[0].upper() + sentence[1:]}."))
    assert len(out) == 1, sentence


@pytest.mark.parametrize("sentence", [
    "Prior accident, resolved.", "Prior rear-end collision 03/14/2024, resolved.", "Previous car accident in March 2025, resolved.",
    "No injury reported.", "Denies whiplash or headache.", "Negative for trauma.", "Without loss of consciousness.", "Reports a previous car accident years ago.",
])
def test_history_and_negated_wording_is_an_earlier_visit(sentence):
    r = STD(f"Annual physical. {sentence}")
    assert C.accident_date_conflicts(r) == [], sentence
    assert C.accident_date_note(r)["count"] == 1


def test_a_full_date_never_exempts_inside_or_outside_the_year_before_the_stated_date():
    """D-061: no date-distance exemption, so 12/30/2025 and 03/14/2024 both conflict; only an explicit prior exempts."""
    r = lambda ex: [R(1, "2025-12-30", "ER", ex), R(2, "2026-01-12", "PT", "Exam: ok."), INT(3, "2026-02-20", "2026-01-05")]      # noqa: E731
    assert len(C.accident_date_conflicts(r("Rear-end collision 12/30/2025."))) == 1
    assert len(C.accident_date_conflicts(r("Rear-end collision 03/14/2024, resolved."))) == 1
    assert C.accident_date_conflicts(r("Prior rear-end collision 03/14/2024, resolved.")) == []


def test_the_note_does_not_claim_that_nothing_names_a_collision_in_words_it_did_not_look_for():
    n = C.accident_date_note(STD("Annual physical."))
    assert "None describes" not in n["text"] and "read them" in n["text"]


def test_previously_had_an_event_is_history_but_previously_until_the_event_is_not():
    assert C.accident_date_conflicts(STD("Annual physical. Previously had an MVA, resolved.")) == []
    assert len(C.accident_date_conflicts(STD("Previously asymptomatic until the crash.", "ER"))) == 1


def test_prior_to_the_event_is_not_history_even_when_the_event_is_one_word():
    assert len(C.accident_date_conflicts(STD("Healthy prior to the crash.", "ER"))) == 1
    assert C.accident_date_conflicts(STD("Healthy. Prior crash, resolved.")) == []


def test_a_bare_year_never_exempts_only_an_explicit_prior_does():
    """T-141 r4 (reviewer Y1), superseded by D-061: no year, however old, exempts an accident word."""
    def rec(d, ex):
        return [R(1, d, "PCP", ex), R(2, d[:8] + "28", "PT", "Exam: ok."), INT(3, d[:8] + "29", d[:8] + "27")]
    for d, ex in (("2026-01-05", "Car accident in 2025, neck pain."), ("2026-06-05", "Rear-ended in 2025."), ("2026-03-04", "Car accident in 2024, resolved."),
                  ("2026-03-04", "Car accidents in 2019 and 2022.")):
        assert len(C.accident_date_conflicts(rec(d, ex))) == 1, ex
    assert C.accident_date_conflicts(rec("2026-03-04", "Prior car accident in 2024, resolved.")) == []
    assert C.accident_date_conflicts(rec("2026-03-04", "History per patient: car accidents in 2019 and 2022.")) == []


# T-141 r4 (section 7.4 bounded fix-up): the reviewer's 33 r3 variants (r3_variants.py). A pre-accident record is info-only ONLY when its accident wording is
# generic prior history that is negated or explicitly prior; any reference to THE accident or its mechanism is a date conflict even if other words are negated.
R3 = [
    ("N1 no prior accidents", "info", "Annual physical. No prior accidents."),
    ("N2 denies MVC", "info", "Annual physical. Denies MVC."),
    ("N3 denies any motor vehicle collision or injury", "info", "Annual physical. Denies any motor vehicle collision or injury."),
    ("N4 MVA in 2015", "conflict", "Annual physical. MVA in 2015, resolved."),
    ("N5 history of MVA 2015", "conflict", "Annual physical. History of MVA 2015."),
    ("N6 hx rear-end collision 2018", "conflict", "Annual physical. Hx rear-end collision 2018."),
    ("T1 no LOC after the accident", "conflict", "ER visit. No LOC after the accident. Neck pain."),
    ("T2 has not worked since the accident", "conflict", "Follow-up. Has not worked since the accident. Neck pain."),
    ("T3 no relief since the MVA", "conflict", "Follow-up. No relief of neck pain since the MVA."),
    ("T4 not wearing a seatbelt in the rear-end collision", "conflict", "ER visit. Patient was not wearing a seatbelt in the rear-end collision."),
    ("T5 no improvement since the crash", "conflict", "Follow-up. No improvement since the crash."),
    ("T6 no airbag deployment in the collision", "conflict", "ER visit. No airbag deployment in the collision. Neck pain."),
    ("T7 without fracture after the MVC", "conflict", "ER visit. Without fracture after the MVC."),
    ("T8 never lost consciousness during the crash", "conflict", "ER visit. Never lost consciousness during the crash."),
    ("T9 no other injuries; was in an MVA", "conflict", "ER visit. No other injuries; was in an MVA."),
    ("T10 negative for fracture after rear-end collision", "conflict", "ER visit. Negative for fracture after rear-end collision."),
    ("H1 History: rear-ended at a stoplight", "conflict", "ER visit. History: rear-ended at a stoplight. Neck pain."),
    ("H2 past week since the MVA", "conflict", "Chiro visit. Neck pain for the past week since the MVA."),
    ("H3 history of present illness: MVC today", "conflict", "ER visit. History of present illness: MVC today."),
    ("H4 earlier today MVA", "conflict", "ER visit. Earlier today the pt was in an MVA. Neck pain."),
    ("H5 PMH none; pt in MVC", "conflict", "ER visit. PMH none; pt in MVC this week."),
    ("H6 old man hit by a car", "conflict", "ER visit. Old man hit by a car crossing the street."),
    ("H7 years ago, worse after the collision", "conflict", "Chiro visit. Neck pain started years ago and worsened after the rear-end collision."),
    ("H8 last year, rear-ended this week", "conflict", "ER visit. Seen last year for knee, now rear-ended this week."),
    ("H9 prior to arrival MVC", "conflict", "ER visit. Prior to arrival the patient was in an MVC. Neck pain."),
    ("H10 at the previous visit she reported the MVA", "conflict", "Follow-up. At the previous visit she reported the MVA and neck pain."),
    ("H11 MVA remote past", "conflict", "Annual physical. MVA remote past, resolved."),
    ("Y2 rear-ended in November 2025", "conflict", "ER visit. Rear-ended in November 2025."),
    ("Y3 rear-ended in October 2025", "conflict", "ER visit. Rear-ended in October 2025."),
    ("B1 fall risk screen negative", "info", "Annual physical. Fall risk screen negative."),
    ("B2 impact of diabetes on diet", "info", "Annual physical. Impact of diabetes on diet counselled."),
    ("B3 injury prevention handout", "info", "Annual physical. Injury prevention handout given."),
]


@pytest.mark.parametrize("label,expected,ex", R3, ids=[r[0].split()[0] for r in R3])
def test_reviewer_r3_variants(label, expected, ex):
    recs = STD(ex, "ER")
    out, note = C.accident_date_conflicts(recs), C.accident_date_note(recs)
    assert ("conflict" if out else "info") == expected, label
    if expected == "info":
        assert note and note["count"] == 1


def test_reviewer_y1_bare_year_in_a_june_record_is_a_conflict():
    recs = [R(1, "2026-06-05", "ER", "Intake. Rear-ended in 2025."), R(2, "2026-06-12", "PT", "Exam: ok."), INT(3, "2026-06-20", "2026-06-09")]
    assert len(C.accident_date_conflicts(recs)) == 1


@pytest.mark.parametrize("sentence", [
    "No LOC after the accident.", "No improvement since the crash.", "Denies the accident.", "No pain during the collision.", "Never in the MVA.",
    "History: MVC.", "Hx: the accident.", "No history of the crash.", "Rear-end collision with whiplash.", "No pain with the collision.",
    "Without injury, the crash was minor.", "Not hurt, in the collision.",
])
def test_a_negator_or_history_word_does_not_exempt_a_reference_to_the_accident(sentence):
    """Negation and history scope over the event noun they modify, never across 'the', a preposition, a verb or a label colon."""
    assert len(C.accident_date_conflicts(STD(f"Seen at ER. {sentence}", "ER"))) == 1, sentence


@pytest.mark.parametrize("sentence", [
    "No prior accidents.", "Denies previous MVA.", "Prior accidents: No.", "Denies any accidents or injuries.", "No history of prior injury.", "Negative for whiplash.",
    "Free of injury.", "Previous accident with whiplash.", "Prior MVA with head injury.", "Previously had an MVA.", "Earlier MVC, resolved.", "Prior accident, resolved.", "Without trauma.", "Neg for injuries.",
])
def test_negated_or_explicitly_prior_generic_wording_is_an_earlier_visit(sentence):
    r = STD(f"Annual physical. {sentence}")
    assert C.accident_date_conflicts(r) == [], sentence
    assert C.accident_date_note(r)["count"] == 1


def test_the_connector_splits_a_clause_so_one_part_s_date_does_not_cover_the_other():
    assert len(C.accident_date_conflicts(STD("Seen 03/01/2024 for knee and rear-ended this week.", "ER"))) == 1
    assert len(C.accident_date_conflicts(STD("Neck pain started years ago but worsened after the crash.", "ER"))) == 1
    assert len(C.accident_date_conflicts(STD("Annual physical. Reports a car accident years ago, neck pain years ago."))) == 1      # D-061: "years ago" never exempts
    assert C.accident_date_conflicts(STD("Annual physical. Reports a previous car accident, neck pain years ago.")) == []


def test_the_note_does_not_assert_that_no_record_names_injury():
    n = C.accident_date_note(STD("Annual physical."))
    assert "No record names" not in n["text"] and "injury" not in n["text"] and "read them" in n["text"].lower() and n["count"] == 1
