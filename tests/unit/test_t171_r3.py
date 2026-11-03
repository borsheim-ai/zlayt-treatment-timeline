"""T-171 round 3 (adjuster r2 fail; final round): two items, test-first. The adjuster's new scenarios (artifacts/review-evidence/T-171-adjuster-r2/probe_r2.py, set 'new') are
restated here as data.
(1) A line with any payer or insurer name, or any payer word, is not countable, with a plain reason (not only the names a list happened to hold).
(2) Duplicate matching normalizes the service: word families, abbreviations (PT / physical therapy, pt / patient, xray / x-ray / radiograph) and a CPT code matched to its
    description when both appear in the case. Over-flagging costs one more named confirm; a missed repeat costs the letter total.
Code only (scripted call factory)."""
import pytest

from app.backend import amounts as AM
from tests.unit.test_t171_r2_countable import (BASE, SRC, TRUE, accepted_cents, amounts, count_all, doc, libclient, live, nc, post, single, _flag)  # noqa: F401

DATED = "Clinic, billing statement"

# ---------------------------------------------------------------- (1) payer / insurer names and payer words
INSURER_NAMES = ["BCBSTX", "BCBS of Texas", "Oscar", "Molina", "USAA", "Workers comp", "Workers' compensation", "Wellcare", "Ambetter", "Centene", "Optum", "Sedgwick",
                 "Zurich", "Texas Mutual", "Blue Cross", "HMO", "PPO", "Hartford", "AmFam", "Esurance", "Amerigroup", "Health Net", "Coventry", "MultiPlan", "Safeco",
                 "Gallagher Bassett", "Aetna", "Cigna", "UHC", "Humana", "TPA", "insurer", "insurance", "carrier", "the plan", "Medicare", "Medicaid"]


@pytest.mark.parametrize("name", INSURER_NAMES)
def test_any_insurer_name_on_the_line_makes_it_not_countable_with_a_plain_reason(name):
    r = nc(BASE + f" {name} therapy visit charge $600.00.", "$600.00")
    assert r["countable"] is False and r["reason"], (name, r)
    assert "insurer" in r["reason"].lower() or "payer" in r["reason"].lower() or "allowed" in r["reason"].lower() or "insurance" in r["reason"].lower(), (name, r)


PAYER_WORDS = {"repriced": "Repriced therapy visit charge $300.00.", "approved": "Approved therapy visit charge $300.00.", "negotiated": "Negotiated therapy visit charge $300.00.",
               "ucr": "Usual and customary therapy visit charge $300.00.", "fee_schedule": "Fee schedule therapy visit charge $300.00.", "eligible": "Eligible therapy visit charge $300.00.",
               "contractual": "Contractual therapy visit charge $300.00.", "allowed": "Allowed therapy visit charge $300.00.", "discounted": "Discounted therapy visit charge $300.00.",
               "in_network": "In-network therapy visit charge $300.00.", "network": "Network rate therapy visit charge $300.00.", "plan": "Plan therapy visit charge $300.00.",
               "covered": "Covered therapy visit charge $300.00."}
LIFETIME = {"since_first": "Therapy visit charges since first visit $1,100.00.", "so_far": "Exam and therapy charges so far $1,100.00.",
            "through_today": "Therapy charges through today $1,100.00.", "episode": "Therapy charges for the whole episode of care $1,100.00.",
            "course": "Charge for the entire course of therapy $1,100.00.", "all_therapy": "All therapy charges $1,100.00.", "visits_1_6": "Therapy charges for visits 1 to 6 $1,100.00.",
            "to_date": "Therapy charges to date $1,100.00.", "cumulative": "Cumulative therapy charges $1,100.00.", "running": "Running therapy charges $1,100.00.",
            "gross": "Gross therapy charges $1,100.00.", "billed_amount": "Billed amount for therapy visits $1,100.00.", "last_stmt": "Therapy care charges from last statement $1,100.00."}
ACCOUNT = {"lien": "Therapy visit charge under lien $1,100.00.", "collections": "Therapy visit charge sent to collections $1,100.00.", "deferred": "Deferred therapy visit charge $1,100.00.",
           "on_hold": "Therapy visit charge on hold $1,100.00.", "attorney": "Therapy visit charge billed to attorney $1,100.00."}
NEW = {f"ins_{n}": f"{n} therapy visit charge $600.00." for n in ("BCBSTX", "Oscar", "Workers comp", "USAA")}
NEW["ins_molina"] = "Molina repriced exam charge $190.00."
NEW.update({f"payer_{k}": v for k, v in PAYER_WORDS.items()})
NEW.update({f"life_{k}": v for k, v in LIFETIME.items()})
NEW.update({f"acct_{k}": v for k, v in ACCOUNT.items()})


@pytest.mark.parametrize("name", sorted(NEW))
def test_the_adjusters_unlisted_payer_lifetime_and_account_wordings_are_refused_and_the_total_stays(live, name):
    c, tok = live(single(NEW[name]))
    extra = [a for a in amounts(c, tok) if a["text"] not in ("$250.00", "$180.00", "$400.00")]
    assert extra, name
    for a in extra:
        assert a["countable"] is False and a["not_counted_reason"], (name, a["text"], a["not_counted_reason"])
        r = post(c, tok, a["id"], action="count", confirm="separate_charge")
        assert r.status_code == 422 and r.json()["error"]["code"] == "NOT_COUNTABLE", (name, a["text"], r.text)
    count_all(c, tok)
    for it in c.get(f"/api/cases/{tok}").json()["entries"]:
        post(c, tok, it["id"], action="accept")
    assert accepted_cents(c, tok) == TRUE, (name, accepted_cents(c, tok))


@pytest.mark.parametrize("line,fig", [
    ("Plan of care visit charge $400.00.", "$400.00"), ("Treatment plan visit charge $400.00.", "$400.00"), ("Therapy session charge $400.00.", "$400.00"),
    ("Exam charge $250.00 for the second visit.", "$250.00"), ("Follow-up visit charge $180.00.", "$180.00"),
])
def test_an_ordinary_itemized_service_line_is_still_countable(line, fig):
    assert nc("Itemized ledger. " + line, fig)["countable"] is True


# ---------------------------------------------------------------- (2) duplicate matching normalizes the service
REWORDED = {
    "dup_code_vs_desc": ("04/16/2026 97140 charge $150.00.", "Manual therapy charge $150.00.", 15000),
    "dup_desc_vs_code": ("04/16/2026 manual therapy charge $150.00.", "CPT 97140 charge $150.00.", 15000),
    "dup_abbrev_therex": ("04/16/2026 therapeutic exercise charge $120.00.", "Ther ex charge $120.00.", 12000),
    "dup_pt_vs_physical": ("04/16/2026 physical therapy visit charge $185.00.", "PT visit charge $185.00.", 18500),
    "dup_newpt_abbrev": ("04/16/2026 new patient exam charge $250.00.", "New pt exam charge $250.00.", 25000),
    "dup_word_order": ("04/16/2026 x-ray charge $180.00.", "Charge for x-ray of cervical spine $180.00.", 18000),
    "dup_xray_radiograph": ("04/16/2026 cervical x-ray charge $180.00.", "Cervical radiograph charge $180.00.", 18000),
    "dup_xray_joined": ("04/16/2026 cervical x-ray charge $180.00.", "Cervical xray charge $180.00.", 18000),
    "dup_office_visit_eandm": ("04/16/2026 office visit 99213 charge $165.00.", "Established patient office visit charge $165.00.", 16500),
    "dup_eval_vs_exam": ("04/16/2026 evaluation charge $250.00.", "Exam charge $250.00.", 25000),
    "dup_ov": ("04/16/2026 office visit charge $165.00.", "OV charge $165.00.", 16500),
    "dup_estim": ("04/16/2026 electrical stimulation charge $60.00.", "E-stim charge $60.00.", 6000),
    "dup_same_words": ("04/16/2026 manual therapy charge $150.00.", "Manual therapy charge $150.00.", 15000),
}


@pytest.mark.parametrize("name", sorted(REWORDED))
def test_an_undated_repeat_worded_differently_still_needs_the_duplicate_confirm(live, name):
    d1, u2, truth = REWORDED[name]
    c, tok = live(doc(("2026-04-16", DATED, "Billing statement. " + d1), ("2026-05-01", "", u2)))
    am = amounts(c, tok)
    first = next(a for a in am if a["kind"] == "charge")
    twin = next(a for a in am if a["kind"] != "charge")
    assert post(c, tok, first["id"], action="accept").status_code == 200
    twin = next(a for a in amounts(c, tok) if a["id"] == twin["id"])
    if not twin["countable"]:          # a line the code cannot read as a service line (no service noun: 'Ther ex', 'OV') is refused outright: it cannot count at all
        r = post(c, tok, twin["id"], action="count", confirm="separate_charge")
        assert r.status_code == 422 and r.json()["error"]["code"] == "NOT_COUNTABLE" and twin["not_counted_reason"], (name, r.text)
        assert accepted_cents(c, tok) == truth
        return
    assert twin["count_confirm"] and twin["count_confirm"]["flag"] == "likely_duplicate", (name, twin)
    d = _flag(post(c, tok, twin["id"], action="count", confirm="separate_charge"))
    assert d["flag"] == "likely_duplicate", d
    assert accepted_cents(c, tok) == truth


def test_a_reprint_with_abbreviated_wording_is_flagged_on_every_line(live):
    LED = "Fennimoor Spine Clinic, itemized ledger"
    c, tok = live(doc(("2026-06-15", LED, BASE), ("2026-06-30", LED + " (reprint)", "Itemized ledger. New pt exam charge $250.00; xray charge $180.00; ther visit charge $400.00.")))
    am = [a for a in amounts(c, tok) if a["countable"]]
    assert len(am) == 6 and all(a["count_confirm"] and a["count_confirm"]["flag"] == "likely_duplicate" for a in am), [(a["text"], a["count_confirm"]) for a in am]
    count_all(c, tok)
    assert accepted_cents(c, tok) <= TRUE


def test_a_restated_line_with_an_abbreviation_is_flagged_on_both_lines(live):
    c, tok = live(single("New pt exam charge $250.00 (restated)."))
    twins = [a for a in amounts(c, tok) if a["text"] == "$250.00"]
    assert len(twins) == 2 and all(t["count_confirm"] and t["count_confirm"]["flag"] == "likely_duplicate" for t in twins), twins


def _b(codes=(), words=(), dos=None):
    return {"dos": dos, "codes": frozenset(codes), "tokens": frozenset(words), "ok": False, "svc": True}


def _line(i, cents, basis, record_no=1, charge=False):
    return {"id": i, "record_no": record_no, "cents": cents, "basis": basis, "charge": charge, "line": f"line {i}"}


def test_a_code_matches_its_description_when_both_appear_in_the_case():
    # 97140 is stated with 'manual therapy' on one line of the case: a code-only line and a described line then meet by what the case itself says
    known = _line("k", 9000, _b(["97140"], ["manu", "ther"]), charge=True)
    assert AM.count_flag(_line("a", 15000, _b(["97140"])), [known, _line("b", 15000, _b(words=["manu", "ther"]), 2)])["flag"] == "likely_duplicate"
    # ... and a code the case describes as manual therapy is NOT asked about against an x-ray at the same price
    assert AM.count_flag(_line("a", 15000, _b(["97140"])), [known, _line("b", 15000, _b(words=["ray"]), 2)]) is None


def test_a_code_with_no_description_in_the_case_is_asked_about_against_a_described_line_at_the_same_amount():
    f = AM.count_flag(_line("a", 15000, _b(["97140"])), [_line("b", 15000, _b(words=["manu", "ther"]), 2)])
    assert f and f["flag"] == "likely_duplicate"
    assert AM.count_flag(_line("a", 15000, _b(["97140"])), [_line("b", 16000, _b(words=["manu", "ther"]), 2)]) is None
    assert AM.count_flag(_line("a", 15000, _b(["97140"], dos="2026-04-16")), [_line("b", 15000, _b(words=["manu"], dos="2026-04-23"), 2)]) is None


@pytest.mark.parametrize("a,b", [(["pt", "visi"], ["phys", "ther", "visi"]), (["new", "pt", "exam"], ["new", "pati", "exam"]), (["xray"], ["ray"]), (["radi"], ["ray"]),
                                 (["ther", "ex"], ["ther", "exer"]), (["ov"], ["offi", "visi"])])
def test_abbreviations_and_word_families_meet(a, b):
    assert AM.count_flag(_line("a", 100, _b(words=a)), [_line("b", 100, _b(words=b), 2)])


@pytest.mark.parametrize("a,b", [(["exam"], ["ray"]), (["manu", "ther"], ["ther", "exer"]), (["new", "exam"], ["ray", "cerv"]), (["visi"], ["ray"])])
def test_different_services_at_one_price_are_still_not_flagged(a, b):
    assert AM.count_flag(_line("a", 100, _b(words=a)), [_line("b", 100, _b(words=b), 2)]) is None
