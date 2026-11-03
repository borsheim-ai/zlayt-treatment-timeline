"""T-112 / D-054: code removes the clauses of an AI summary that its own quote does not support, before the judge sees it.
Pure-function cases (including faithful paraphrases that must NOT be trimmed), then the generator wiring: the judge sees the trimmed summary, the removal is in
the item trace, nothing supported -> could-not-verify tray, human-written summaries and translated records are never trimmed. Fake model calls, no key, no network."""
import pytest

from app.backend import generator as GN, ingest, summary_trim as T, trace, why
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, sample_script, which_record

PAIN = "Patient reports left wrist pain 6/10."


def test_case_02_example_removes_only_the_splint_clause():
    r = T.trim("Initial consult; left wrist pain 6/10; splint fitted.", PAIN)
    assert r["changed"] and r["supported"]
    assert r["text"] == "Initial consult; left wrist pain 6/10."
    assert r["removed"] == ["splint fitted"]
    assert r["notes"] == ["removed from the summary: not in the quote: 'splint fitted'"]


def test_everything_unsupported_leaves_nothing():
    r = T.trim("Splint fitted.", PAIN)
    assert r["text"] == "" and r["removed"] == ["Splint fitted"] and not r["supported"]


# Faithful paraphrases: the quote says the same thing in other words. Nothing is removed, byte for byte (T-112 r2, staff-engineer major 1).
FAITHFUL = [
    # the two the reviewer found first, then the rest of his hard pairs
    ("Dizziness reported.", "Pt dizzy since crash."),
    ("Patient ambulating with a cane.", "Walks with cane."),
    ("Dizziness and blurred vision.", "Dizzy, vision blurry."),
    ("Patient is anxious and tearful.", "Anxiety, crying at exam."),
    ("Numbness and tingling in fingers.", "Paresthesias in digits."),
    ("Patient vomited twice.", "Emesis x2."),
    ("Sleeping poorly.", "Insomnia due to pain."),
    ("Taking Tylenol.", "Acetaminophen PRN."),
    ("Patient is nauseated.", "Reports nausea and vomiting."),
    ("Walking with a limp.", "Gait antalgic."),
    ("Bruising on the arm.", "Contusion of the forearm."),
    ("Reports trouble sleeping.", "Sleep disturbance noted."),
    ("Patient crying during the exam.", "Tearful at visit."),
    ("Neck stiffness.", "Cervical stiffness."),
    ("Took ibuprofen at home.", "Advil taken at home."),
    ("Back pain on bending.", "Low back pain with flexion."),
    ("Pain improving.", "Pain is better."),
    ("Headache daily.", "Daily headaches."),
    ("Patient lightheaded.", "Feels dizzy."),
    ("Sent home with pain medication.", "Discharged; Rx tramadol."),
    # the earlier faithful set
    ("Patient reports left wrist pain with swelling and tenderness.", "Pt c/o L wrist pain 6/10, swelling and tenderness noted."),
    ("Neck pain 5/10.", "Cervical pain 5/10 with spasm."),
    ("Physical therapy twice weekly for six weeks.", "PT 2x/week for 6 weeks."),
    ("Rear-end collision, restrained driver.", "MVA; restrained driver struck from behind."),
    ("Left shoulder x-ray showed no fracture.", "XR left shoulder: no acute fracture or dislocation."),
    ("Injections were given to the lumbar spine.", "Lumbar injection performed."),
    ("Referred to orthopedics for evaluation.", "Referral to ortho for assessment."),
    ("MRI lumbar spine ordered.", "MRI of the lumbar spine was ordered."),
    ("Pain improving, now 3/10.", "Pain is improving; currently rated 3/10."),
    ("Discharged home with prescriptions.", "Discharged home; prescribed meds."),
    ("Loss of consciousness at the scene.", "Brief LOC at scene."),
    # more: numbers, sides, negations and dates written another way
    ("Pain is six out of ten.", "Pain 6/10."),
    ("Follow-up in two weeks.", "F/U 2 wks."),
    ("Right knee pain.", "Rt knee pain after the fall."),
    ("Both wrists sore.", "Bilateral wrist pain."),
    ("Seen on March 4.", "Visit 03/04/2026."),
    ("No broken bones on the x-ray.", "X-ray: no acute fracture."),
    ("Spine x-ray normal.", "Cervical spine films unremarkable."),
    ("Denies numbness.", "Patient denies numbness or tingling."),
    ("Pain not relieved by rest.", "Pain persists at rest."),
    ("Tenderness over the neck muscles.", "Cervical paraspinal tenderness."),
    ("Walker used for balance.", "Ambulates with walker."),
    ("Left hand numb.", "L fingers numb."),
    ("Chest wall pain.", "Pain over the ribs."),
    ("Shoulder pain with overhead reach.", "Rotator cuff tenderness; pain on overhead reach."),
    ("Prescribed muscle relaxant.", "Rx Flexeril 10 mg."),
    ("Ankle swelling.", "Swollen ankle."),
    ("Concussion symptoms.", "Post-concussive symptoms."),
    ("Emergency transport by ambulance.", "Transported by EMS."),
]


@pytest.mark.parametrize("summary,excerpt", FAITHFUL)
def test_faithful_paraphrases_are_not_trimmed(summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["text"] == summary and not r["changed"] and r["removed"] == [], r


def test_the_two_reported_overtrims_stay_whole():
    assert T.trim("Dizziness reported.", "Pt dizzy since crash.")["changed"] is False
    r = T.trim("Patient ambulating with a cane.", "Walks with cane.")
    assert r["text"] == "Patient ambulating with a cane." and r["text"] != "A cane."


def test_the_label_vouches_for_body_part_side_and_modality_but_not_for_treatment():
    s = "Right knee MRI shows medial meniscus tear."
    q = "Medial meniscus tear."
    assert T.trim(s, q)["changed"] and not T.trim(s, q, "Tamsin Imaging, right knee MRI")["changed"]
    r = T.trim("Surgery recommended.", "Persistent pain.", "Dr. Voss, orthopedic surgery, clinic")
    assert r["text"] == "" and r["removed"] == ["Surgery recommended"]


# Clauses that DO add salient new content (procedure, device, drug, body part, diagnosis, number, date, side, negation): removed whole.
UNSUPPORTED = [
    ("Left wrist pain 6/10; splint fitted.", PAIN, "Left wrist pain 6/10.", ["splint fitted"]),
    ("Left wrist pain 6/10; MRI ordered.", PAIN, "Left wrist pain 6/10.", ["MRI ordered"]),
    ("Left wrist pain 6/10; surgery recommended.", PAIN, "Left wrist pain 6/10.", ["surgery recommended"]),
    ("Left wrist pain 6/10; cast applied.", PAIN, "Left wrist pain 6/10.", ["cast applied"]),
    ("Left wrist pain 6/10; referred to neurosurgeon.", PAIN, "Left wrist pain 6/10.", ["referred to neurosurgeon"]),
    ("Left wrist pain 6/10; hospitalized overnight.", PAIN, "Left wrist pain 6/10.", ["hospitalized overnight"]),
    ("Left wrist pain 6/10; prescribed Flexeril.", PAIN, "Left wrist pain 6/10.", ["prescribed Flexeril"]),
    ("Left wrist pain 6/10; Tylenol given.", PAIN, "Left wrist pain 6/10.", ["Tylenol given"]),
    ("Left wrist pain 6/10; epidural injection.", PAIN, "Left wrist pain 6/10.", ["epidural injection"]),
    ("Left wrist pain 6/10; neck pain.", PAIN, "Left wrist pain 6/10.", ["neck pain"]),
    ("Left wrist pain 6/10; shoulder swelling.", PAIN, "Left wrist pain 6/10.", ["shoulder swelling"]),
    ("Left wrist pain 6/10; fracture noted.", PAIN, "Left wrist pain 6/10.", ["fracture noted"]),
    ("Left wrist pain 6/10; sprain.", PAIN, "Left wrist pain 6/10.", ["sprain"]),
    ("Left wrist pain 6/10; concussion.", PAIN, "Left wrist pain 6/10.", ["concussion"]),
    ("Left wrist pain 6/10; radiculopathy.", PAIN, "Left wrist pain 6/10.", ["radiculopathy"]),
    ("Left wrist pain 6/10; depression.", PAIN, "Left wrist pain 6/10.", ["depression"]),
    ("Left wrist pain 6/10; for 4 weeks.", PAIN, "Left wrist pain 6/10.", ["for 4 weeks"]),
    ("Left wrist pain 6/10; seen in March.", PAIN, "Left wrist pain 6/10.", ["seen in March"]),
    ("Left wrist pain 6/10; no splint needed.", PAIN, "Left wrist pain 6/10.", ["no splint needed"]),
    ("Left wrist pain 6/10; splint fitted to the wrist.", PAIN, "Left wrist pain 6/10.", ["splint fitted to the wrist"]),        # shares 'wrist' but adds a device
    ("Left wrist pain 6/10; wrist splint applied.", PAIN, "Left wrist pain 6/10.", ["wrist splint applied"]),
    ("Left wrist pain 6/10; patient referred to surgeon for wrist.", PAIN, "Left wrist pain 6/10.", ["patient referred to surgeon for wrist"]),
    ("Back pain, splint fitted.", "Fell on back.", "Back pain.", ["splint fitted"]),
    ("CT scan ordered.", "MRI scan of brain.", "", ["CT scan ordered"]),
    ("Cervical strain.", "Neck pain after crash.", "", ["Cervical strain"]),
    ("Initial consult; splint fitted.", PAIN, "Initial consult.", ["splint fitted"]),          # 'Initial consult' adds nothing salient: it stays, the judge checks it
    ("Patient seen; splint fitted.", PAIN, "", ["splint fitted"]),                          # what is left has no content word
    ("Orthodontic braces tightened.", PAIN, "", ["Orthodontic braces tightened"]),
]


@pytest.mark.parametrize("summary,excerpt,text,removed", UNSUPPORTED)
def test_clauses_with_salient_new_content_are_removed(summary, excerpt, text, removed):
    r = T.trim(summary, excerpt)
    assert r["removed"] == removed and r["text"] == text, r
    assert r["changed"] and r["supported"] == bool(text)


@pytest.mark.parametrize("summary,excerpt", [
    ("Pain 3/10, improving.", "Pain 4/10, improving."),            # R-TL-10: a changed score stays and is flagged needs_review by D-034, not silently dropped
    ("Right wrist pain.", "Left wrist pain."),                     # D-047 flags the side
    ("No wrist numbness.", "Wrist numbness reported."),            # D-047 flags the negation
    ("Pain 9/10 at night.", PAIN),
])
def test_a_changed_value_on_the_quotes_own_topic_stays_for_the_code_checks_to_flag(summary, excerpt):
    from app.backend import grounding
    assert not T.trim(summary, excerpt)["changed"]
    assert grounding.check_summary(summary, excerpt)


def test_a_capitalized_name_is_not_a_body_part():
    s = "Law firm letter to Fennimoor Spine Clinic states the firm represents the client."
    assert not T.trim(s, "This firm represents the client for injuries.")["changed"]
    assert T.trim("Letter sent; spine clinic visit.", "This firm represents the client.")["removed"] == ["spine clinic visit"]


def test_a_trim_never_leaves_a_fragment():
    """T-128 r3 fix-up: ' with ' is not a clause boundary, so 'MRI ordered with a cane.' is one clause: it is removed whole (the tray), never cut to 'A cane.'."""
    r = T.trim("MRI ordered with a cane.", "Walks with cane.")
    assert r["text"] == "" and r["removed"] == ["MRI ordered with a cane"] and not r["supported"]
    for summary, excerpt, text, _ in UNSUPPORTED:
        t = T.trim(summary, excerpt)["text"]
        assert not t or t[0].isupper() and t.split()[0].lower() not in ("a", "an", "the", "with", "and", "of", "to")


def test_no_change_returns_the_summary_byte_for_byte():
    s = "  Wrist pain 6/10 ;  swelling noted .  "
    assert T.trim(s, "Wrist pain 6/10. Swelling noted.")["text"] == s


def test_numbers_sides_and_negations_are_salient_when_the_quote_lacks_them():
    assert T.trim("Left splint fitted.", "Left wrist pain 6/10.")["text"] == ""
    assert T.trim("No fracture.", "Wrist pain 6/10.")["text"] == ""
    r = T.trim("Wrist pain 6/10; 4 weeks.", "Wrist pain 6/10.")
    assert r["text"] == "Wrist pain 6/10." and r["removed"] == ["4 weeks"]
    assert T.trim("Right wrist pain.", "Left wrist pain.")["changed"] is False       # about the quote's own topic: kept, the D-047 code check flags the side


def test_a_denial_is_kept_when_the_quote_has_a_negation_even_if_no_word_matches():
    s = "Diagnosis of cervical strain; patient denies loss of consciousness."
    q = "Dx: cervical strain. Denies LOC per patient."
    assert T.trim(s, q)["text"] == s
    assert T.trim("Denies radiating pain.", "Denies numbness.")["text"] == "Denies radiating pain."
    r = T.trim("Wrist pain 6/10; no splint was fitted.", "Wrist pain 6/10.")
    assert r["removed"] == ["no splint was fitted"]


def test_clause_without_content_words_is_neutral_and_kept():
    r = T.trim("6/10; wrist pain", "Wrist pain 6/10.")
    assert r["text"] == "6/10; wrist pain" and not r["changed"]
    r = T.trim("Patient seen; splint fitted.", "Wrist pain 6/10.")
    assert r["text"] == "" and r["removed"] == ["splint fitted"]


def test_middle_clause_removed_keeps_the_stronger_separator():
    r = T.trim("Wrist pain 6/10; swelling noted, splint fitted.", "Wrist pain 6/10 with swelling noted.")
    assert r["text"] == "Wrist pain 6/10; swelling noted." and r["removed"] == ["splint fitted"]            # a removed tail drops its own (weaker) separator
    assert not T.trim("Wrist pain 6/10, splint fitted; swelling noted.", "Wrist pain 6/10 with swelling noted.")["changed"]     # T-128 r3: a middle removal is not made
    assert not T.trim("Wrist pain and splint fitted and swelling.", "Wrist pain and swelling.")["changed"]      # ' and ' after a removed clause: not left behind (T-128 r2)


def test_and_with_joins_are_clause_boundaries():
    r = T.trim("Wrist pain with numbness and cast applied.", "Wrist pain with numbness.")
    assert r["text"] == "Wrist pain with numbness." and r["removed"] == ["cast applied"]


def test_no_split_inside_numbers_or_abbreviations():
    assert [c for c, _ in T.split_clauses("Seen by Dr. Lee, approx. 6.5 weeks, $1,200 billed.")] == ["Seen by Dr. Lee", "approx. 6.5 weeks", "$1,200 billed"]
    assert [c for c, _ in T.split_clauses("First. Second; third")] == ["First", "Second", "third"]


def test_removal_never_edits_a_kept_clause():
    s = "Left wrist pain 6/10 (worse at night); splint fitted"
    r = T.trim(s, "Left wrist pain 6/10 (worse at night).")
    assert r["text"].startswith("Left wrist pain 6/10 (worse at night)") and "splint" not in r["text"].lower()


def test_trim_is_deterministic_and_pure():
    a = [T.trim("Initial consult; left wrist pain 6/10; splint fitted.", PAIN) for _ in range(3)]
    assert a[0] == a[1] == a[2]


def test_the_module_imports_no_llm_code():
    import pathlib
    src = pathlib.Path(T.__file__).read_text()
    assert "app.llm" not in src and "import requests" not in src


# ---------------------------------------------------------------- T-112 r3: the reviewer's probes as tests
# staff-engineer r2 probes, verbatim: 20 hard faithful pairs, 40 faithful pairs that expand an abbreviation or use a synonym, 28 unsupported clauses that MUST still trim.
REVIEWER_HARD_FAITHFUL_20 = [
    ('Dizziness reported.', 'Pt dizzy since crash.'),
    ('Patient ambulating with a cane.', 'Walks with cane.'),
    ('Unable to bend or lift.', 'Cannot bend, cannot lift.'),
    ('Limping on the right leg.', 'Limp noted on right leg.'),
    ('Bruising across the chest.', 'Ecchymosis across chest wall.'),
    ('Patient is anxious and tearful.', 'Anxiety, crying at exam.'),
    ('Difficulty sleeping due to pain.', 'Pain disturbs sleep.'),
    ('Numbness and tingling in fingers.', 'Paresthesias in digits.'),
    ('Patient is employed as a roofer.', 'Works as roofer.'),
    ('Pain medication refilled.', 'Refill of analgesic.'),
    ('Range of motion reduced.', 'ROM decreased.'),
    ('Patient vomited twice.', 'Emesis x2.'),
    ('Wrist swollen and bruised.', 'Wrist swelling, bruise.'),
    ('Complains of nausea.', 'Nauseous.'),
    ('Tenderness over lumbar spine.', 'Lumbar tender to palpation.'),
    ('Sleeping poorly.', 'Insomnia due to pain.'),
    ('Attended therapy.', 'Rehab visit attended.'),
    ('Driver was struck from behind.', 'Rear-ended while driving.'),
    ('Dizziness and blurred vision.', 'Dizzy, vision blurry.'),
    ('Taking Tylenol.', 'Acetaminophen PRN.'),
]

REVIEWER_ABBREVIATION_FAITHFUL_40 = [
    ('Laceration repaired with sutures.', 'Lac closed w/ 4 sutures.'),
    ('Laceration to the chin.', 'Chin lac.'),
    ('Degenerative changes in the spine.', 'DJD of lumbar spine.'),
    ('Disc herniation at L5.', 'HNP L5-S1.'),
    ('Whiplash injury.', 'Whiplash associated disorder.'),
    ('Epidural steroid injection given.', 'ESI performed.'),
    ('Home exercise program given.', 'HEP reviewed.'),
    ('Bruising on the thigh.', 'Ecchymosis, left thigh.'),
    ('Pain in both legs.', 'BLE pain.'),
    ('Arm pain.', 'Pain in upper extremity.'),
    ('Broken collarbone.', 'Clavicle fx.'),
    ('Torn rotator cuff.', 'Rotator cuff tear.'),
    ('Knee brace provided.', 'Knee brace dispensed.'),
    ('Crutches provided.', 'Given crutches.'),
    ('Wrist in a splint.', 'Wrist splinted.'),
    ('Arm in a sling.', 'Sling applied to L arm.'),
    ('Neck collar placed.', 'C-collar applied.'),
    ('Stitches placed in the scalp.', 'Scalp lac repaired, 6 sutures.'),
    ('Blood work ordered.', 'Labs ordered.'),
    ('CT of the head was negative.', 'CT head: no acute findings.'),
    ('MRI showed a disc bulge.', 'MRI: L4-5 disc bulge.'),
    ('Ultrasound of the abdomen was normal.', 'US abdomen unremarkable.'),
    ('Stomach pain.', 'Abd pain.'),
    ('Pain in the tailbone.', 'Coccyx tenderness.'),
    ('Sprained ankle.', 'Ankle sprain, grade 2.'),
    ('Strained back muscles.', 'Lumbar strain.'),
    ('Depressed mood.', 'Depression screen positive.'),
    ('Anxiety after the crash.', 'Anxious post-MVA.'),
    ('Sent to the hospital by ambulance.', 'Transported to ER via EMS.'),
    ('Admitted overnight for observation.', 'Admit for obs.'),
    ('Told to rest and use ice.', 'Rest, ice, compression, elevation.'),
    ('Given a shot of ketorolac.', 'Toradol IM given.'),
    ('Taking naproxen twice daily.', 'Aleve BID.'),
    ('Recommend physical therapy.', 'PT recommended.'),
    ('Heel pain.', 'Plantar heel tenderness.'),
    ('Jaw pain.', 'TMJ tenderness.'),
    ('Pelvic pain.', 'Pain over the hip and groin.'),
    ('Teeth were chipped.', 'Dental trauma, chipped tooth.'),
    ('Patient has a headache and stiff neck.', 'HA, neck stiffness.'),
    ('Told to follow up if worse.', 'RTC prn worsening.'),
]

REVIEWER_UNSUPPORTED_28 = [
    ('Wrist pain 6/10; physical therapy started.', 'Wrist pain 6/10.'),
    ('Knee pain; started gabapentin.', 'Knee pain after fall.'),
    ('Neck pain; left shoulder pain.', 'Neck pain 5/10.'),
    ('Back pain; diagnosed with diabetes.', 'Back pain 5/10.'),
    ('Chronic headache; knee brace given.', 'Chronic headache daily.'),
    ('Wrist pain, ankle swelling.', 'Wrist pain 4/10.'),
    ('Neck pain and crutches provided.', 'Neck pain.'),
    ('Chest pain; ECG ordered.', 'Chest pain.'),
    ('Hip pain; epidural injection given.', 'Hip pain 5/10.'),
    ('Back pain; herniated disc.', 'Back pain 5/10.'),
    ('Neck pain; whiplash.', 'Neck pain.'),
    ('Shoulder pain; rotator cuff tear.', 'Shoulder pain.'),
    ('Ankle pain; ultrasound performed.', 'Ankle pain.'),
    ('Arm pain; sling applied.', 'Arm pain.'),
    ('Leg pain; ibuprofen prescribed.', 'Leg pain.'),
    ('Back pain; scheduled for surgery.', 'Back pain.'),
    ('Foot pain; patient admitted.', 'Foot pain.'),
    ('Head injury; CT scan negative.', 'Head injury.'),
    ('Neck pain; concussion.', 'Neck pain.'),
    ('Wrist pain; sprain.', 'Wrist pain.'),
    ('Wrist pain; laceration on forearm.', 'Wrist pain.'),
    ('Jaw pain; depression.', 'Jaw pain.'),
    ('Back pain; stitches placed.', 'Back pain.'),
    ('Knee pain; Tylenol given.', 'Knee pain.'),
    ('Back pain; muscle relaxant prescribed.', 'Back pain.'),
    ('Neck pain and arthritis.', 'Neck pain.'),
    ('Neck pain and infection.', 'Neck pain.'),
    ('Hand pain with swelling of the elbow.', 'Hand pain.'),
]


@pytest.mark.parametrize("summary,excerpt", REVIEWER_HARD_FAITHFUL_20 + REVIEWER_ABBREVIATION_FAITHFUL_40 + [
    ("Sutured laceration on forehead.", "Forehead lac repaired with 5 sutures."),
])
def test_reviewer_faithful_pairs_survive_whole(summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["text"] == summary and not r["changed"] and r["removed"] == [], r


@pytest.mark.parametrize("summary,excerpt", REVIEWER_UNSUPPORTED_28)
def test_reviewer_unsupported_clauses_are_still_trimmed(summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["changed"] and r["removed"], r
    assert not r["text"] or r["text"] != summary


def test_the_reviewer_sets_have_the_counted_sizes():
    assert (len(REVIEWER_HARD_FAITHFUL_20), len(REVIEWER_ABBREVIATION_FAITHFUL_40), len(REVIEWER_UNSUPPORTED_28)) == (20, 40, 28)


# General clinical abbreviations (not only the ones the reviewer listed): the summary spells it out, the quote abbreviates it, or the other way round.
ABBREVIATIONS = [
    ("Rheumatoid arthritis flare.", "RA flare."), ("Osteoarthritis of the knee.", "OA of knee."), ("Trigger point injection given.", "TPI done."),
    ("Rotator cuff repair surgery.", "RCR performed."), ("Total knee arthroplasty.", "TKA of the knee."), ("Open reduction and internal fixation.", "ORIF of the ankle."),
    ("Acetaminophen given.", "APAP given."), ("Antibiotics prescribed.", "Abx prescribed."), ("Chest pain.", "CP on exertion."),
    ("Right lower extremity numbness.", "RLE numbness."), ("Left arm weakness.", "LUE weakness."), ("Leg weakness.", "LE weakness."),
    ("Lacerations to the hand.", "Lacs of hand."), ("Chest x-ray normal.", "CXR normal."), ("Home exercise program reviewed.", "HEP reviewed."),
    ("Cervical collar applied.", "C collar applied."),
    # the abbreviation is in the SUMMARY, the quote spells it out
    ("DJD of the spine.", "Degenerative changes in the spine."), ("ESI given.", "Epidural steroid injection given."), ("BLE pain.", "Pain in both legs."),
    ("Lac closed with sutures.", "Laceration repaired with sutures."), ("US abdomen normal.", "Ultrasound of the abdomen was normal."),
    ("Toradol IM given.", "Given a shot of ketorolac."),
]


@pytest.mark.parametrize("summary,excerpt", ABBREVIATIONS)
def test_clinical_abbreviations_are_expanded_both_ways(summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["text"] == summary and not r["changed"], r


def test_an_abbreviation_does_not_vouch_for_a_different_thing():
    """Expanding abbreviations must not over-support: US is ultrasound, not CT; ESI is an injection, not surgery; LE is a leg, not an arm."""
    assert T.trim("CT abdomen ordered.", "US abdomen unremarkable.")["removed"] == ["CT abdomen ordered"]
    assert T.trim("Knee surgery recommended.", "ESI performed.")["removed"] == ["Knee surgery recommended"]
    assert T.trim("Arm splint applied.", "LE weakness.")["removed"] == ["Arm splint applied"]
    assert T.trim("Back pain; ESI given.", "Back pain.")["removed"] == ["ESI given"]
    assert T.trim("Knee pain; US performed.", "Knee pain.")["removed"] == ["US performed"]


# ' with ' is NOT a clause boundary (T-128 r3 fix-up): a with-phrase is removed with its head, or kept with it.
def test_a_with_phrase_is_one_clause_so_a_bare_noun_is_never_left_behind():
    r = T.trim("Laceration repaired with sutures.", "Sutures placed in the clinic.")
    assert r["text"] == "" and r["removed"] == ["Laceration repaired with sutures"]                   # the whole clause is unsupported ('laceration'): the tray, never 'Sutures.'
    assert T.trim("Fracture reduced with traction.", "Traction applied.")["text"] != "Traction."
    assert len(T.split_clauses("Wrist pain with numbness; neck pain consistent with sprain.")) == 2           # the split is at ; only


def test_a_with_phrase_inside_a_kept_clause_is_kept_and_a_removed_tail_clause_takes_its_own_with_phrase():
    r = T.trim("Back pain; diagnosed with diabetes.", "Back pain 5/10.")
    assert r["text"] == "Back pain." and r["removed"] == ["diagnosed with diabetes"], r
    r = T.trim("Neck pain with stiffness; surgery recommended.", "Neck pain with stiffness.")
    assert r["text"] == "Neck pain with stiffness." and r["removed"] == ["surgery recommended"]
    assert T.trim("Pain with radiculopathy.", "Pain 5/10.")["text"] == ""                              # one clause, unsupported: the tray


import re as _re
_PART = _re.compile(r"(?:[a-z]+(?:ed|ing)|given|consistent|due|secondary|related|compatible|suggestive|positive|up)$", _re.I)
REVIEWER_WITH_TAILS = [      # reviews/T-128-staff-engineer-r3.md finding 1: each used to become 'X consistent.', 'X treated.' ...
    ("Neck pain consistent with sprain.", "Neck pain."), ("Neck pain treated with injection.", "Neck pain."), ("Neck pain managed with ibuprofen.", "Neck pain."),
    ("Back pain relieved with ibuprofen.", "Back pain."), ("Neck pain diagnosed with sprain.", "Neck pain."), ("Findings consistent with disc bulge.", "Findings."),
    ("Neck pain evaluated with MRI.", "Neck pain."), ("Left knee pain worked up with X-ray.", "Left knee pain."),
    ("Neck pain treated conservatively with physical therapy.", "Neck pain."),
]


@pytest.mark.parametrize("summary,excerpt", REVIEWER_WITH_TAILS)
def test_the_reviewers_with_tails_are_removed_whole_never_left_as_a_stranded_participle(summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["text"] == "" and r["removed"] == [summary.rstrip(".")], r
    assert not r["text"] or not _PART.search(r["text"].rstrip(". "))


def test_a_negation_flip_on_the_quotes_own_topic_stays_and_the_contract_says_so():
    """Minor 4 (r2): the contract promises only judge 1 and the human for a negation; the D-047 token check cannot see a flip when the quote has the same negation word elsewhere."""
    from app.backend import grounding
    s, q = "No cervical strain.", "X-ray: no acute fracture. Cervical strain."
    assert not T.trim(s, q)["changed"] and grounding.new_tokens(s, q) == []
    import pathlib
    api = (pathlib.Path(__file__).resolve().parents[2] / "memory" / "contracts" / "api.md").read_text()
    assert "only guaranteed to reach judge 1 and the paralegal" in api and "No cervical strain." in api
    assert "only guaranteed to reach judge 1 and the human" in (T.__doc__ or "")


def test_the_eval_report_counts_what_code_trimmed(tmp_path):
    """Minor 3 (r2): evals.run.summary_trim_counts is pinned: one trimmed entry, 3 clauses removed in all, one tray placeholder."""
    import evals.run as ER
    from app.backend import pipeline as PL

    def extract(user):
        n = which_record(user)[0]
        s, q = SUMS[n]
        if n == 1:
            return dict(summary=s.rstrip(".") + "; splint fitted and cast applied.", excerpt=q)
        if n == 2:
            return dict(summary="Orthodontic braces tightened.", excerpt=q)
        return dict(summary=s, excerpt=q)
    conn = DB.connect(str(tmp_path / "c.sqlite"))
    cid = DB.create_case(conn, RAW, now=1.0)
    out = PL.run_pipeline(conn, cid, RAW, call=FakeCall(sample_script(extract=extract)), now=lambda: 1.0)
    assert ER.summary_trim_counts(out) == {"items_trimmed": 1, "clauses_removed": 3, "tray_placeholders": 1}
    conn2 = DB.connect(str(tmp_path / "d.sqlite"))
    clean = PL.run_pipeline(conn2, DB.create_case(conn2, RAW, now=1.0), RAW, call=FakeCall(sample_script()), now=lambda: 1.0)
    assert ER.summary_trim_counts(clean) == {"items_trimmed": 0, "clauses_removed": 0, "tray_placeholders": 0}


# ---------------------------------------------------------------- generator wiring
RAW = G.raw("sample")
ING = ingest.ingest(RAW)
RECS, GROUPS = ING["records"], ING["groups"]
BY = {r["n"]: r for r in RECS}
SUMS = golden_summaries()


def _script(extra_clause=None, replace_with=None):
    def extract(user):
        n = which_record(user)[0]
        s, q = SUMS[n]
        if n == 1 and replace_with is not None:
            return dict(summary=replace_with, excerpt=q)
        if n == 1 and extra_clause:
            return dict(summary=s.rstrip(".") + "; " + extra_clause, excerpt=q)
        return dict(summary=s, excerpt=q)
    return {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}}


def test_judge_sees_the_trimmed_summary_and_the_trace_says_what_was_removed():
    call = FakeCall(_script("splint fitted and cast applied."))
    ents, rej, fails = GN.extract_entries(RECS, GROUPS, call=call, case_text=RAW)
    GN.judge_entries(ents, BY, call=call, case_text=RAW)
    e1 = next(e for e in ents if e["seq"] == 1)
    assert "splint" not in e1["summary"].lower() and "cast" not in e1["summary"].lower()
    assert e1["summary"].rstrip(".") .startswith(SUMS[1][0].rstrip(".")[:20])
    tr = e1["ladder"]["summary_trim"]
    assert tr["rule"] == "D-054" and tr["removed"] and all(n.startswith("removed from the summary: not in the quote: '") for n in tr["notes"])
    assert "splint" in tr["original_summary"] and e1["ladder"]["generator"]["output"]["summary"] == tr["original_summary"]        # the model's own output is kept for audit
    j1 = [u for u in call.prompts("j1") if "splint" in u.lower() or "cast applied" in u.lower()]
    assert j1 == [], "the judge must see the trimmed summary only"
    assert e1["state"] == "verified" and not rej and not fails


def test_untrimmed_entries_have_no_trim_record():
    call = FakeCall(_script())
    ents, _, _ = GN.extract_entries(RECS, GROUPS, call=call, case_text=RAW)
    assert all("summary_trim" not in e["ladder"] for e in ents)


def test_nothing_supported_goes_to_the_tray_with_the_removals():
    call = FakeCall(_script(replace_with="Orthodontic braces tightened."))
    ents, rej, fails = GN.extract_entries(RECS, GROUPS, call=call, case_text=RAW)
    assert [f["failure"] for f in fails] == ["SUMMARY_NOT_IN_QUOTE"] and fails[0]["record_no"] == 1
    assert 1 not in [e["seq"] for e in ents]
    t = GN.failure_entry(BY[1], [1], fails[0]["failure"], fails[0]["detail"])
    assert t["state"] == "rejected" and t["reasons"] == ["SUMMARY_NOT_IN_QUOTE"] and t["summary"] is None
    assert t["ladder"]["failure"] == "SUMMARY_NOT_IN_QUOTE" and t["ladder"]["summary_trim"]["removed"] == ["Orthodontic braces tightened"]
    assert t["ladder"]["generator"]["output"]["summary"] == "Orthodontic braces tightened."
    assert why.why("SUMMARY_NOT_IN_QUOTE")


def test_non_verbatim_quote_is_still_rejected_by_grounding_not_trimmed():
    call = FakeCall({"extract": lambda u: dict(summary="Splint fitted.", excerpt="Not in the record at all."), "j1": {"verdict": "supported", "reason_code": "NONE"}})
    ents, rej, fails = GN.extract_entries(RECS, GROUPS, call=call, case_text=RAW)
    assert not fails and len(rej) == 9 and all("summary_trim" not in e["ladder"] for e in rej)


def test_translated_records_are_not_trimmed():
    """A Spanish quote cannot stem-match an English translation; D-050 already makes every translated item needs_review."""
    from tests.unit.test_spanish_records import MIXED, _es_script, _record
    rec = _record()
    e = GN.extract_one(rec, [2], call=FakeCall(_es_script(summary="Splint fitted on arrival.")), case_text=MIXED)
    assert "failure" not in e and "summary_trim" not in e["ladder"] and e["state"] != "verified"


def test_human_written_summaries_are_never_trimmed(tmp_path):
    """D-047 refuses an unsupported human summary; the trimmer runs in the generator only. Behavior, not a grep: edit a summary to carry an unsupported clause."""
    from app.backend import pipeline as PL, review as RV
    conn = DB.connect(str(tmp_path / "h.sqlite"))
    cid = DB.create_case(conn, RAW, now=1.0)
    call = FakeCall(sample_script(extract=_script()["extract"]))
    out = PL.run_pipeline(conn, cid, RAW, call=call, now=lambda: 1.0)
    e1 = next(e for e in out["entries"] if e["seq"] == 1)
    assert "summary_trim" not in (e1.get("ladder") or {})
    mine = e1["summary"].rstrip(".") + "; splint fitted."
    RV.apply_review(conn, cid, e1["id"], {"action": "edit", "edits": {"summary": mine}}, call=call, now=lambda: 2.0)
    row = next(i for i in DB.list_items(conn, cid, "entry") if i["id"] == e1["id"])
    assert (row["edited"] or {}).get("summary") == mine
    assert "summary_trim" not in (row["ladder"] or {})


def test_pipeline_puts_an_emptied_summary_in_the_tray_without_an_error_and_traces_it(tmp_path):
    from app.backend import pipeline as PL
    conn = DB.connect(str(tmp_path / "t.sqlite"))
    cid = DB.create_case(conn, RAW, now=1.0)
    call = FakeCall(sample_script(extract=_script(replace_with="Orthodontic braces tightened.")["extract"]))
    out = PL.run_pipeline(conn, cid, RAW, call=call, now=lambda: 1.0)
    tray = [i for i in out["tray"] if "r1" in i.get("record_ids", [])]
    assert len(tray) == 1 and tray[0]["reasons"] == ["SUMMARY_NOT_IN_QUOTE"] and tray[0]["state"] == "rejected"
    assert not [e for e in out["errors"] if e.get("record_no") == 1]
    assert 1 not in [e["seq"] for e in out["entries"]]
    # a trimmed (not emptied) entry shows the removal as its own trace step
    call = FakeCall(sample_script(extract=_script("splint fitted.")["extract"]))
    conn2 = DB.connect(str(tmp_path / "t2.sqlite"))
    cid2 = DB.create_case(conn2, RAW, now=1.0)
    out2 = PL.run_pipeline(conn2, cid2, RAW, call=call, now=lambda: 1.0)
    e1 = next(e for e in out2["entries"] if e["seq"] == 1)
    tr = trace.item_trace(conn2, cid2, e1["id"])
    steps = {s["id"]: s for s in tr["steps"]}
    assert "summary_trimmed" in steps and steps["summary_trimmed"]["kind"] == "code" and steps["summary_trimmed"]["rule"] == "D-054"
    assert "removed from the summary: not in the quote: 'splint fitted'" in steps["summary_trimmed"]["why"]
    assert list(steps).index("summary_trimmed") == list(steps).index("extracted") + 1


# ---------------------------------------------------------------- T-112 r2: the 'not a duplicate' split and the tray item's trace
def _split_with_unsupported_summary(tmp_path):
    from app.backend import review as RV
    from tests.unit.test_manual_and_split import CASE, seeded_case4
    conn, cid, _ = seeded_case4(tmp_path)

    def extract(u):
        n = which_record(u, CASE)[0]
        s = G.record(CASE, n)["excerpt"].split(". ")[0].rstrip(".") + "."
        return dict(summary="Orthodontic braces tightened.", excerpt=s)
    merged = next(e for e in DB.list_items(conn, cid, "entry") if "r2" in e["record_ids"])
    out = RV.not_duplicate(conn, cid, merged["id"], "r2", call=FakeCall(sample_script(extract=extract)))
    return conn, cid, out


def test_not_a_duplicate_split_sends_an_emptied_summary_to_the_tray_with_the_right_reason(tmp_path):
    conn, cid, out = _split_with_unsupported_summary(tmp_path)
    tray = [i for i in DB.list_items(conn, cid, "entry") if i["record_ids"] == ["r2"]]
    assert len(tray) == 1 and tray[0]["state"] == "rejected" and tray[0]["state_reasons"] == ["SUMMARY_NOT_IN_QUOTE"]
    w = [x for x in out["warnings"] if x["code"] == "SUMMARY_NOT_IN_QUOTE"]
    assert len(w) == 1 and w[0]["item_id"] == tray[0]["id"]
    assert "could not draft" not in w[0]["message"] and "removed every part of the AI's summary" in w[0]["message"] and "tray" in w[0]["message"]


def test_the_tray_items_trace_does_not_claim_the_quote_failed_the_word_for_word_check(tmp_path):
    conn, cid, _ = _split_with_unsupported_summary(tmp_path)
    tray = next(i for i in DB.list_items(conn, cid, "entry") if i["record_ids"] == ["r2"])
    tr = trace.item_trace(conn, cid, tray["id"])
    steps = {s["id"]: s for s in tr["steps"]}
    assert steps["extracted"]["status"] == "fail" and "removed from the summary" in steps["extracted"]["why"]
    assert not [s for s in tr["steps"] if s["id"] == "excerpt_verbatim" and s["status"] == "fail"]
    skipped = [s for s in tr["steps"] if s["status"] == "skipped"]
    assert skipped and all("word-for-word" not in s["why"] and "summary" in s["why"] for s in skipped)


# ---- T-128 round 2 (reviews/T-128-staff-engineer.md): fragments are impossible by construction, not by a word list ------------------------------------------
# Structural rule (orchestrator direction): (1) the FIRST clause is never removed - if it is unsupported nothing is trimmed and the whole summary goes to the judge (a
# summary whose every clause is unsupported still goes to the tray); (2) the kept prefix (the clauses before the first removal) has at least 2 content words; (3) a
# kept clause that was joined to a removed one by ',' ' and ' or ' with ' is not left behind (only ';' or a sentence end lets a clause stand alone).
FRAGMENTS = [   # (summary, quote): every one of these used to leave a fragment; the trim now leaves the whole summary to judge 1
    ("Pain in the neck and back.", "Back pain."), ("Pain in the neck and shoulder.", "Shoulder pain."),
    ("Knee surgery recommended, due to torn meniscus.", "Torn meniscus."), ("MRI ordered, which showed a torn meniscus.", "Torn meniscus."),
    ("Cast applied, including a sling.", "Sling provided."), ("Splint applied and was advised to rest.", "Advised to rest."),
    # the reviewer's fresh set (reviews/T-128-staff-engineer.md section 2)
    ("Pain in the neck and lower back.", "Lower back pain."), ("Pain in the neck and right shoulder.", "Right shoulder pain."),
    ("Wrist fracture and surgery.", "Surgery."), ("MRI ordered, pending insurance approval.", "MRI approved."),
    ("Knee surgery recommended, requiring six weeks of crutches.", "Crutches for six weeks."), ("Ankle sprain, likely from the fall.", "Fall."),
    ("Back pain, worse with sitting.", "Sitting."), ("Epidural injection given, after which pain eased.", "Pain eased."),
    ("Shoulder surgery performed, leading to a sling.", "Sling worn."), ("Physical therapy started, plus home exercises.", "Home exercises."),
]


@pytest.mark.parametrize("summary,excerpt", FRAGMENTS)
def test_a_trim_never_leaves_a_fragment_the_whole_summary_goes_to_the_judge(summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["text"] == summary and not r["changed"] and r["removed"] == [], r


@pytest.mark.parametrize("summary,excerpt,want", [      # unsupported TAIL clauses still trim: the kept text is a prefix of whole clauses (T-128 r3)
    ("Neck pain; surgery recommended.", "Neck pain.", "Neck pain."),
    ("Neck pain; surgery recommended; MRI ordered.", "Neck pain.", "Neck pain."),
    ("Neck pain. Surgery recommended.", "Neck pain.", "Neck pain."),
    ("Neck pain; discharged home; MRI ordered.", "Neck pain. Discharged home.", "Neck pain; discharged home."),
    ("Back pain; ibuprofen advised; injection given.", "Back pain. Ibuprofen advised.", "Back pain; ibuprofen advised."),
    ("Pain in the neck and back.", "Neck pain.", "Pain in the neck."),
    ("Initial consult; left wrist pain 6/10; splint fitted.", "Patient reports left wrist pain 6/10.", "Initial consult; left wrist pain 6/10."),
    ("Back pain; follow-up visit. Ultrasound done.", "Back pain. Follow-up visit.", "Back pain; follow-up visit."),
])
def test_unsupported_later_clauses_still_trim_when_a_whole_clause_is_left(summary, excerpt, want):
    r = T.trim(summary, excerpt)
    assert r["changed"] and r["text"] == want, r


MIDDLE_REMOVALS = [      # a kept clause would follow a removed one: the whole summary goes to judge 1 (T-128 r3, suffix only)
    ("Wrist pain; cast applied; discharged home.", "Wrist pain. Discharged home."),
    ("Neck pain; MRI ordered. Was prescribed ibuprofen.", "Neck pain. Ibuprofen prescribed."),
    ("Neck pain. Surgery recommended. Also reports headaches.", "Neck pain. Headaches."),
    ("Back pain; injection given. Is improving.", "Back pain. Improving."),
    ("Ankle pain; X-ray taken; no fracture.", "Ankle pain. No fracture."),
    # the reviewer's round-2 set (reviews/T-128-staff-engineer-r2.md section 3): each used to leave a dependent or mis-attached tail
    ("Neck pain; injection given; resulting in relief.", "Neck pain. Relief."), ("Wrist pain; splint applied; which helped.", "Wrist pain."),
    ("Neck pain; cast applied; however, improving.", "Neck pain."), ("Shoulder pain; surgery performed; due to torn labrum.", "Shoulder pain. Torn labrum."),
    ("Back pain; ultrasound done; thereafter, improvement.", "Back pain."), ("Back pain; epidural given; as a result, less pain.", "Back pain."),
    ("Wrist fracture; cast applied; including follow-up.", "Wrist fracture."), ("Neck pain; ibuprofen prescribed; 3 times daily.", "Neck pain. 3 times daily."),
    ("Neck pain; physical therapy started; for six weeks.", "Neck pain."), ("Knee pain; brace issued; as needed.", "Knee pain."),
    ("Neck pain; surgery recommended; discharged home; MRI ordered.", "Neck pain. Discharged home."),      # the LAST clause is removed too, but not the one before it
    ("Head injury; CT ordered; negative.", "Head injury. Negative."), ("Hip pain; X-ray taken; unremarkable.", "Hip pain. Unremarkable."),
]


@pytest.mark.parametrize("summary,excerpt", MIDDLE_REMOVALS)
def test_a_clause_is_removed_only_when_every_clause_after_it_is_removed_too(summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["text"] == summary and not r["changed"] and r["removed"] == [], r


def test_the_first_clause_is_never_removed():
    r = T.trim("Was seen at the ER; surgery recommended.", "Seen at ER.")
    assert not r["changed"]                                                                  # nothing is removed before the first clause stands
    r = T.trim("Surgery recommended; neck pain.", "Neck pain.")
    assert not r["changed"] and r["removed"] == []                                           # an unsupported FIRST clause: whole summary to the judge
    r = T.trim("Splint fitted.", PAIN)
    assert r["text"] == "" and r["removed"] == ["Splint fitted"]                             # nothing at all supported: the tray, as before
    r = T.trim("Splint fitted; cast applied.", PAIN)
    assert r["text"] == "" and not r["supported"]


def test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed():
    assert not T.trim("Pain; splint fitted.", "Fell on back. Pain.")["changed"]
    assert not T.trim("Headache; knee brace given.", "Headache daily.")["changed"]
    assert T.trim("Back pain; radiculopathy suspected.", "Back pain 5/10.")["text"] == "Back pain."      # two content words: fine
    assert not T.trim("Pain; splint fitted; swelling noted; cast applied.", "Pain. Swelling noted.")["changed"]          # the prefix is what comes before the FIRST removal, not the last
    assert T.trim("Pain; swelling noted; splint fitted.", "Pain. Swelling noted.")["text"] == "Pain; swelling noted."    # 'Pain; swelling noted' is two content words before the first removal
    assert T.trim("Wrist pain; splint fitted.", PAIN)["text"] == "Wrist pain."


def test_a_clause_joined_to_a_removed_one_by_comma_and_or_with_is_not_left_behind():      # still true, now a special case of the suffix rule
    for s, q in [("Knee pain; MRI ordered, pending approval.", "Knee pain."), ("Knee pain; MRI ordered and was advised to rest.", "Knee pain. Advised to rest."),
                 ]:
        assert not T.trim(s, q)["changed"], s
    assert not T.trim("Knee pain; surgery recommended; pending approval.", "Knee pain. Pending approval.")["changed"]     # ';' no longer lets a clause follow a removed one


# ---- mutants that survived the T-112 r3 review ------------------------------------------------------------------------------------------------------------------
def test_lower_case_us_and_im_are_ordinary_words_and_do_not_vouch_for_ultrasound_or_injection():
    r = T.trim("Neck pain; ultrasound performed.", "Neck pain; he told us it hurts.")
    assert r["text"] == "Neck pain." and r["removed"] == ["ultrasound performed"]
    r = T.trim("Back pain; injection given.", "Back pain. Im in pain.")
    assert r["text"] == "Back pain." and r["removed"] == ["injection given"]
    assert not T.trim("Neck pain; ultrasound performed.", "Neck pain; US performed.")["changed"]             # upper case is the abbreviation
    assert not T.trim("Back pain; injection given.", "Back pain. IM given.")["changed"]


def test_the_record_label_vouches_for_a_body_part_but_not_for_a_diagnosis_or_treatment():
    label = "Valley Imaging, cervical spine MRI"
    assert T.trim("Neck pain.", "MRI findings.", label)["changed"] is False
    assert T.trim("Neck pain.", "MRI findings.")["text"] == ""                                      # without the label the body part is new
    assert T.trim("Neck sprain.", "MRI findings.", label)["text"] == ""                              # the label does not vouch for a diagnosis
    assert T.trim("Neck pain; surgery recommended.", "MRI findings.", "Valley Imaging, cervical spine surgery")["removed"] == ["surgery recommended"]


def test_negation_like_words_in_the_quote_keep_a_summary_negation_in_front_of_the_judge():
    assert T.trim("Wrist pain; denies numbness.", "Wrist pain. X-ray unremarkable.")["changed"] is False
    assert T.trim("Wrist pain; denies numbness.", "Wrist pain. Strength unchanged.")["changed"] is False
    r = T.trim("Wrist pain; denies numbness.", "Wrist pain. X-ray done.")
    assert r["text"] == "Wrist pain." and r["removed"] == ["denies numbness"]


# One pair per abbreviation-table entry: deleting the entry makes the faithful pair trim (T-112 r3 table sweep: tha, acdf, lle, bue, rue, u/s, UE survived).
ENTRY_PAIRS = [   # the term sits in a LATER clause: the first clause is never removed (T-128 r2), so a deleted entry shows as a removed second clause
    ("tha", "Neck pain; hip replacement surgery.", "Neck pain. THA."), ("tha", "Neck pain; THA.", "Neck pain. Hip replacement surgery."),
    ("acdf", "Back pain; neck fusion surgery.", "Back pain. ACDF."), ("acdf", "Back pain; ACDF.", "Back pain. Neck fusion surgery."),
    ("lle", "Neck pain; left leg weakness.", "Neck pain. LLE weakness."), ("lle", "Neck pain; LLE weakness.", "Neck pain. Left leg weakness."),
    ("rle", "Neck pain; right leg weakness.", "Neck pain. RLE weakness."),
    ("bue", "Back pain; both arms weakness.", "Back pain. BUE weakness."), ("bue", "Back pain; BUE weakness.", "Back pain. Both arms weakness."),
    ("rue", "Neck pain; right arm weakness.", "Neck pain. RUE weakness."), ("rue", "Neck pain; RUE weakness.", "Neck pain. Right arm weakness."),
    ("lue", "Neck pain; left arm weakness.", "Neck pain. LUE weakness."),
    ("u/s", "Back pain; ultrasound performed.", "Back pain. U/S performed."), ("u/s", "Back pain; U/S performed.", "Back pain. Ultrasound performed."),
    ("UE", "Neck pain; arm numbness.", "Neck pain. UE numbness."), ("UE", "Neck pain; UE numbness.", "Neck pain. Arm numbness."),
    ("orif", "Back pain; wrist surgery.", "Back pain. ORIF wrist."), ("orif", "Back pain; ORIF wrist.", "Back pain. Open reduction internal fixation of wrist."),
    ("rcr", "Neck pain; shoulder surgery.", "Neck pain. RCR performed."), ("rcr", "Neck pain; RCR performed.", "Neck pain. Rotator cuff repair performed."),
]


@pytest.mark.parametrize("entry,summary,excerpt", ENTRY_PAIRS)
def test_each_abbreviation_table_entry_is_pinned_by_a_faithful_pair(entry, summary, excerpt):
    r = T.trim(summary, excerpt)
    assert r["text"] == summary and not r["changed"], (entry, r)


@pytest.mark.parametrize("entry,summary,excerpt", [t for t in ENTRY_PAIRS if t[0].lower() in t[2].lower()])
def test_without_its_table_entry_the_pair_is_trimmed(entry, summary, excerpt, monkeypatch):
    """Mutation check in the suite: delete the entry and the faithful pair must change, so a deleted entry cannot pass unnoticed."""
    import re
    table = T._ABBR_CASE if entry in T._ABBR_CASE else T._ABBR
    monkeypatch.setitem(table, entry, "zzqx")                                                       # the entry no longer expands to its words
    if table is T._ABBR_CASE:
        monkeypatch.setattr(T, "_ABBR_CASE_RX", re.compile(r"(?<![A-Za-z0-9/])(" + "|".join(T._ABBR_CASE) + r")(?![A-Za-z0-9/])"))
    r = T.trim(summary, excerpt)
    assert r["changed"], (entry, r)


# ---- T-128 r2 / T-105 r2 leftover: negation and side words come from the lexicon (grounding.view), not from private lists in summary_trim ----------------------------
def test_negation_words_are_the_lexicons_not_a_private_list():
    import pathlib
    src = pathlib.Path(T.__file__).read_text()
    import re
    assert not re.search(r"^(?:_NEG|_NEG_WORDS|_SIDE_WORDS)\s*=", src, re.M)
    # 'absence of' / 'lacks' / 'free of' are lexicon negation words (negation_extra): a summary clause that adds one the quote does not have is new content
    for s in ("Neck pain; absence of numbness.", "Neck pain; lacks radiation.", "Neck pain; free of numbness."):
        r = T.trim(s, "Neck pain.")
        assert r["changed"] and r["text"] == "Neck pain.", (s, r)
    assert not T.trim("Neck pain; absence of numbness.", "Neck pain. Exam unremarkable.")["changed"]        # the quote has a negative finding
    assert not T.trim("Neck pain; absence of numbness.", "Neck pain. No numbness.")["changed"]
    assert not T.trim("Neck pain; denies fever.", "Neck pain. Absence of radiation.")["changed"]       # the quote's own 'absence of' is a lexicon negation word
    assert T.trim("Neck pain; denies fever.", "Neck pain. Radiation to the arm.")["changed"]
    # a side word comes from the lexicon too
    assert T.trim("Neck pain; bilaterally tender.", "Neck pain.")["changed"]


# ---- T-128 r3: the n't contraction branch and the quote's sides (reviews/T-128-staff-engineer-r2.md minor 3) --------------------------------------------------
@pytest.mark.parametrize("clause", ["couldn't sleep", "didn't miss work", "can't lift", "wasn't tender", "doesn't radiate"])
def test_a_contraction_negation_the_quote_lacks_is_new_content(clause):
    r = T.trim(f"Neck pain; {clause}.", "Neck pain.")
    assert r["changed"] and r["text"] == "Neck pain." and r["removed"] == [clause], r
    assert not T.trim(f"Neck pain; {clause}.", "Neck pain. Exam normal.")["changed"]               # a negative finding in the quote vouches (judge 1 decides)
    assert not T.trim(f"Neck pain; {clause}.", "Neck pain. Patient did not sleep, no radiation.")["changed"]


def test_the_quotes_own_side_word_supports_a_summary_side():
    assert not T.trim("Neck pain; left arm numbness.", "Neck pain. Left arm numbness.")["changed"]
    assert T.trim("Neck pain; left shoulder pain.", "Neck pain. Shoulder pain.")["changed"] is False       # about the quote's own topic: the D-047 check flags the side
    assert T.trim("Neck pain; left arm splint.", "Neck pain. Right arm exam.")["text"] == "Neck pain."        # the quote says right, not left: new
    assert not T.trim("Neck pain; left arm splint.", "Neck pain. Splint to L arm.")["changed"]                # 'L' in the quote counts as left
