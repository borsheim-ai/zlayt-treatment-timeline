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
    ("R16", "conflict", "Car accident in March 2025, resolved.", "ER"),
    ("R17", "conflict", "Struck by a car last year.", "ER"),
    ("R18", "conflict", "Injured in October 2025.", "ER"),
    ("R19", "conflict", "Injury in October 2025.", "ER"),
    ("R20", "conflict", "LOC in October 2025.", "ER"),
    ("R21", "conflict", "Whiplash in October 2025.", "ER"),
    ("R22", "conflict", "Pedestrian struck in 2022.", "ER"),
    ("R23", "conflict", "Impact to the left side last year.", "ER"),
    ("R24", "conflict", "Rear-ended in October 2025.", "ER"),
    ("R25", "conflict", "Rear-ended in 2021, resolved.", "ER"),
    ("R26", "conflict", "Rear-ended in November 2025.", "ER"),
    ("R27", "conflict", "Hit by a car 2 days ago.", "ER"),
    ("R28", "conflict", "Hit from behind at a stoplight in October 2025.", "ER"),
    ("R29", "conflict", "Hit from behind this week.", "ER"),
    ("R30", "conflict", "Collisions in October 2025.", "ER"),
    ("R31", "conflict", "Two collisions last week.", "ER"),
    ("R32", "conflict", "Two MVAs last week.", "ER"),
    ("R33", "conflict", "Two MVCs in October 2025.", "ER"),
    ("R34", "conflict", "Pedestrians struck in October 2025.", "ER"),
    ("R35", "conflict", "Impact noted in October 2025.", "ER"),
    ("R36", "conflict", "Wreck in October 2025.", "ER"),
    ("R37", "conflict", "Side-swiped last year.", "ER"),
    ("R38", "conflict", "Car accident in 2019 and 2022.", "ER"),
    ("H1", "conflict", "History: MVC.", "PCP"),
    ("H2", "conflict", "History: rear-ended.", "PCP"),
    ("H3", "conflict", "History of MVA 2015.", "PCP"),
    ("H4", "conflict", "Hx rear-end collision 2018.", "PCP"),
    ("H5", "conflict", "PMH: MVA 2015.", "PCP"),
    ("H6", "conflict", "History per patient: car accident in 2022.", "PCP"),
    ("H7", "conflict", "History: collision 2015.", "PCP"),
    ("H8", "conflict", "Past MVA 2015.", "PCP"),
    ("H9", "conflict", "Remote MVA 2015.", "PCP"),
    ("H10", "conflict", "Old MVC, resolved.", "PCP"),
    ("H11", "conflict", "MVA remote past, resolved.", "PCP"),
    ("H12", "conflict", "History per patient: MVC in 2019 and 2022.", "PCP"),
    ("H13", "conflict", "History: rear-ended at a stoplight.", "PCP"),
    ("H14", "conflict", "History of MVC 2018.", "PCP"),
    ("E1", "info", "No prior accidents.", "ER"),
    ("E2", "info", "Denies previous MVA.", "ER"),
    ("E3", "info", "Prior accidents: No.", "ER"),
    ("E4", "info", "Previously had an MVA.", "ER"),
    ("E5", "info", "Prior MVC in October 2025.", "ER"),
    ("E6", "info", "Earlier MVA, resolved.", "ER"),
    ("E7", "info", "History per patient: car accidents in 2019 and 2022 with neck pain.", "PCP"),
    ("E8", "info", "History per patient: MVAs in 2019 and 2022.", "PCP"),
    ("E9", "info", "No prior accidents or injuries.", "ER"),
    ("E10", "info", "Denies any accidents or injuries.", "ER"),
    ("E11", "info", "Annual visit, flu shot given. Weight stable.", "PCP"),
    ("E12", "info", "Prior MVA, resolved.", "ER"),
    ("P1", "conflict", "History per patient: car accidents in 2019 and 2022; accident last week.", "PCP"),
    ("P2", "conflict", "History per patient: car accidents in 2019 and 2022 and an accident last week.", "PCP"),
    ("P3", "conflict", "History per patient: car accidents in 2019 and 2022 and rear-ended in October 2025.", "PCP"),
    ("P4", "conflict", "History per patient: car accidents in 2019 and 2022, rear-ended in October 2025.", "PCP"),
    ("P5", "conflict", "History per patient: car accidents in 2019 and 2022. This accident happened 01/03/2026.", "PCP"),
    ("P6", "conflict", "History per patient: car accidents in 2019 and 2022 and the accidents this month.", "PCP"),
    ("P7", "conflict", "History per patient: car accidents in 2019 and 2022 and two accidents this month.", "PCP"),
    ("P8", "conflict", "History per patient: car accidents in 2019 and 2022; the two accidents were this week.", "PCP"),
    ("P9", "conflict", "History per patient: car accidents in 2019 and 2022 (rear-ended last year).", "PCP"),
    ("P10", "conflict", "History per patient: car accidents in 2019 and 2022 — rear-ended last year.", "PCP"),
    ("P11", "conflict", "History per patient: car accidents in 2019 and 2022; rear-end collision in October 2025.", "PCP"),
    ("P12", "conflict", "History per patient: car accidents in 2019 and 2022, collisions this month.", "PCP"),
    ("P13", "conflict", "History per patient: car accidents in 2019 and 2022. MVAs this month.", "PCP"),
    ("P14", "conflict", "History per patient: car accidents in 2019 and 2022. Hit from behind this week.", "PCP"),
    ("P15", "conflict", "History per patient: car accidents in 2019 and 2022 and the rear-end collision in 2026.", "PCP"),
    ("P16", "conflict", "History per patient: car accidents with whiplash since 01/03/2026.", "PCP"),
    ("P17", "conflict", "History per patient: MVC in 2019 and 2022.", "PCP"),
    ("P18", "conflict", "History per patient: car accidents in 2019 and 2022. Pedestrian hit this month.", "PCP"),
    ("P19", "conflict", "History per patient: car accidents in 2019 and 2022 and was rear-ended.", "PCP"),
    ("P20", "conflict", "History of car accidents in 2019 and 2022, rear-ended this week.", "PCP"),
    ("L1", "conflict", "Denies prior accidents and rear-ended in October 2025.", "ER"),
    ("L2", "conflict", "No prior accidents and rear-ended in October 2025.", "ER"),
    ("L3", "conflict", "Previous MVA or rear-ended in October 2025.", "ER"),
    ("L4", "conflict", "Prior accidents or collision in October 2025.", "ER"),
    ("L5", "conflict", "No injury or rear-ended in October 2025.", "ER"),
    ("L6", "conflict", "Negative for whiplash and struck by a car in October 2025.", "ER"),
    ("L7", "conflict", "No prior accidents with rear-end collision in October 2025.", "ER"),
    ("L8", "conflict", "No prior accidents for rear-end collision in October 2025.", "ER"),
    ("L9", "conflict", "Prior accident and rear-ended this week.", "ER"),
    ("L10", "conflict", "Prior accidents and the accident of 01/03/2026.", "ER"),
    ("C1", "conflict", "Prior accidents: No. Rear-ended in October 2025.", "ER"),
    ("C2", "conflict", "Denies previous MVA. MVC last year.", "ER"),
    ("Q1", "conflict", "History per patient: car accidents in 2019 and 2022. Accidents this month.", "PCP"),
    ("Q2", "conflict", "History per patient: car accidents in 2019 and 2022, accidents this month.", "PCP"),
    ("Q3", "conflict", "History per patient: accidents in 2019 and 2022 with the accidents this month.", "PCP"),
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
