"""T-116 round 5 (D-055): a paperwork-headed record warns whatever its text says. Treatment words (diagnosis lines, 'performed', 'seen by')
never suppress the warning, the alternative, the conditional flag or the accident-baseline caveat. Reviewer probes from
artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py, -packet-dx-line.py and -baseline.py. Fixture backend, no network."""
import pathlib

import pytest

from app.backend import conflicts as CF
from app.backend import gaps as GP
from app.backend import ingest as I

ROOT = pathlib.Path(__file__).resolve().parents[2]
HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
V = "Neck pain 5/10. Improved range of motion. Continue home exercise."
PAPER = [
    ("Capital PT, billing statement", "Statement of account. Dx: M54.2 cervicalgia. CPT 97110 x4. Balance due $740."),
    ("Capital PT, billing statement", "Statement of account. Services performed 03/01/2026 and 03/08/2026. Balance due $740."),
    ("Capital PT, billing statement", "Statement of account. Balance due $740."),
    ("Capital PT, intake form", "Have you been seen by a physician for this problem? Yes. Pain diagram completed."),
    ("Capital PT, intake form", "Patient-completed intake form. Date of birth, insurance, emergency contact."),
    ("Capital PT, records request", "Please produce all records of treatment performed on this patient 03/01/2026 through 04/10/2026."),
    ("Capital PT, affidavit of records custodian", "I certify the attached records are true copies. Services were performed on the dates shown."),
    ("Quoinmere Mutual Health Plan, EOB", "Explanation of benefits. Diagnosis: M54.2. Allowed amount $120."),
]


def pk(items):
    return HDR + "".join(f"=== Record {i} ===\nDate: {d}\nSource: {s}\nExcerpt: \"{e}\"\n\n" for i, (d, s, e) in enumerate(items, 1))


def flags_of(items):
    return GP.gap_flags(I.ingest(pk(items))["records"])


@pytest.mark.parametrize("src,txt", PAPER)
def test_eight_paperwork_variants_show_the_span_and_the_alternative(src, txt):
    (mid,) = flags_of([("2026-03-01", "Capital PT, visit 1", V), ("2026-03-20", src, txt), ("2026-04-10", "Capital PT, visit 3", V)])
    assert (mid["days"], mid["conditional"], [w["side"] for w in mid["endpoint_warnings"]]) == (40, True, ["inside"])
    assert mid["endpoint_warnings"][0]["alternative_days"] == 40
    (end,) = flags_of([("2026-03-01", "Capital PT, visit 1", V), ("2026-04-10", src, txt)])
    assert (end["days"], bool(end.get("conditional")), [w["side"] for w in end["endpoint_warnings"]]) == (40, False, ["end"])


def test_lib06_keeps_its_35_day_flag_with_a_diagnosis_line_on_the_billing_record():
    t = (ROOT / "evals/library/case_lib06_lop_billed_vs_adjusted.txt").read_text(encoding="utf-8")
    i = t.index("=== Record 4 ==="); j = t.index('Excerpt: "', i); k = t.index('"\n', j + 10)
    for text in (t, t[:k] + " Diagnosis: M25.511 pain in right shoulder." + t[k:]):
        fl = GP.gap_flags(I.ingest(text)["records"])
        assert any(f["days"] == 35 and f["conditional"] and (f["from_date"], f["to_date"]) == ("2026-05-13", "2026-06-17") for f in fl)


def test_accident_baseline_never_calls_a_paperwork_headed_record_the_first_recorded_treatment():
    for txt in ("Patient-completed intake form. Date of accident: 2026-01-15.",
                "Patient-completed intake form. Date of accident: 2026-01-15. Have you been seen by a physician for this problem? Yes."):
        t = HDR + (f"=== Record 1 ===\nDate: 2026-01-12\nSource: Capital PT, intake form\nExcerpt: \"{txt}\"\n\n"
                   "=== Record 2 ===\nDate: 2026-01-20\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%.\"\n")
        (c,) = CF.accident_date_conflicts(I.ingest(t)["records"])
        assert "first recorded treatment" not in c["explanation"]
        assert "looks like paperwork" in c["explanation"]
