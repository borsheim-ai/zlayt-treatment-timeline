"""T-091: speaker attribution v2 (app/backend/speaker.py) against the adversarial set. Module is disabled (D-040); this is the gate.

The jsonl holds every attack string from the four T-061 claims-adjuster rounds plus 40+ new ones. The gate is 100%: a single
wrong label fails the test. A second, generated grid checks the safety property directly (a mixed excerpt is never labelled
patient or other, whatever the connector, the second speaker or the reporting verb).
"""
import itertools
import json
from pathlib import Path

import pytest

from app.backend import speaker

SET = Path(__file__).resolve().parents[2] / "evals" / "adversarial" / "speaker_attribution.jsonl"
ROWS = [json.loads(line) for line in SET.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_set_shape():
    assert len(ROWS) == len({r["id"] for r in ROWS})
    assert sum(r["src"].startswith("t061") for r in ROWS) >= 60
    assert sum(r["src"] == "new" for r in ROWS) >= 40
    assert {r["expect"] for r in ROWS} == {"patient", "other", "unknown"}
    for g in ("spanish", "line_breaks_quotes", "pronouns_family", "punctuation_variants", "mixed_grid"):
        assert any(r["group"] == g for r in ROWS), g


def test_gate_100_percent_on_adversarial_set():
    wrong = [(r["id"], r["expect"], speaker.attribute(r["text"]).label, r["text"]) for r in ROWS
             if speaker.attribute(r["text"]).label != r["expect"]]
    assert not wrong, f"{len(wrong)}/{len(ROWS)} wrong: {wrong[:5]}"


def test_no_unsafe_patient_label_anywhere():
    """The costly error class: expected not-patient, labelled patient."""
    unsafe = [r["id"] for r in ROWS if r["expect"] != "patient" and speaker.attribute(r["text"]).label == "patient"]
    assert unsafe == []


@pytest.mark.parametrize("p", ["Patient states neck pain", "Pt reports headaches", "Per patient, pain began at the scene"])
def test_generated_mixed_grid_never_patient_or_other(p):
    speakers = ["wife", "his wife", "EMS", "the pastor", "landlord", "Mrs. Ortiz", "Maria", "Dr. Smith", "he", "she", "they",
                "a friend", "the tow driver", "su esposa", "roommate", "witness"]
    verbs = ["reports", "says", "states", "notes", "thinks", "claims", "told me", "insists", "reporting", "mentioned", "texted"]
    conns = [", ", "; ", ": ", " — ", " - ", " & ", " / ", ". ", "\n", " plus ", " as ", " while ", " but ", " and ", " (", " [",
             " | ", " however, ", " with ", " per ", " also ", " y "]
    for c, s, v in itertools.product(conns, speakers, verbs):
        text = f"{p}{c}{s} {v} headaches began at the scene."
        assert speaker.attribute(text).label == "unknown", text
        flipped = f"{s} {v} headaches began at the scene{c}{p[0].lower() + p[1:]}."
        assert speaker.attribute(flipped).label == "unknown", flipped


def test_disabled_by_default_d040():
    assert speaker.ENABLED is False
    assert speaker.chip_label("Patient states neck pain.") is None


def test_label_is_always_one_of_three_and_never_raises():
    for t in ["", None, "\x00", "((((", "\n\n\n", "a" * 5000, "Patient states " * 300, "‮patient states neck pain"]:
        assert speaker.attribute(t).label in speaker.LABELS
