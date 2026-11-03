"""Structural conflicts (code). R-FL-2, LLM_VS_CODE row 10; golden C1 and case_05."""
from app.backend import conflicts as C
from tests.unit import _golden as G

def recs(case):
    ex = G.expected(case)
    raw = {r["n"]: r for r in G.records(case)}
    return [dict(n=r["record_no"], date_iso=r["date"], source=r["source"], excerpt=raw[r["record_no"]]["excerpt"], kind=r["kind"]) for r in ex["records"]]

def test_sample_accident_date_conflict():
    """R-FL-2 (a): accident date 2026-01-19 (record 7 body) vs first treatment 2026-01-09 (records 1, 2); dates not merged, no choice, no delay."""
    out = C.accident_date_conflicts(recs("sample"))
    assert len(out) == 1
    c = out[0]
    assert c["subtype"] == "accident_date" and c["body_date"] == "2026-01-19" and c["first_treatment_date"] == "2026-01-09"
    assert 7 in c["record_nos"] and {1, 2} & set(c["record_nos"])
    assert "delay" not in " ".join(str(v) for v in c.values()).lower()

def test_no_accident_phrase_no_conflict_in_other_cases():
    """R-FL-2: cases without an accident-date phrase raise no accident-date conflict."""
    for case in G.case_names():
        if case != "sample":
            assert C.accident_date_conflicts(recs(case)) == [], case

def test_matching_accident_date_is_not_a_conflict():
    """R-FL-2: intake date equal to the first treatment date is no conflict."""
    r = [dict(n=1, date_iso="2026-01-09", source="EMS", excerpt="Transported.", kind="encounter"),
         dict(n=2, date_iso="2026-02-01", source="Intake", excerpt="Date of accident per intake form: 2026-01-09.", kind="encounter")]
    assert C.accident_date_conflicts(r) == []

def test_case_05_practice_conflict_detected():
    """R-FL-2 / row 10: same physician at Wombleton (3, 5) vs Crumpet Lane (4) -> conflict citing 3 and 4."""
    out = C.provider_conflicts(recs("case_05_provider_conflict"))
    assert any({3, 4} <= set(c["record_nos"]) and c["subtype"] == "provider_name" for c in out)

def test_header_suffix_variants_are_not_conflicts():
    """R-TL-9: 'Hill Country Pain Management, new patient' vs ', follow-up' (sample 7, 9) is one provider; case_04 'orthopedics'/'Orthopedics' is case only."""
    assert C.provider_conflicts(recs("sample")) == []
    assert C.provider_conflicts(recs("case_04_duplicates_no_amounts")) == []

def test_provider_and_accident_conflicts_only_where_golden_expects():
    """T-033 r2 minor: provider_conflicts fires only on case_05; accident_date_conflicts only on the sample (over-firing guard)."""
    for case in G.case_names():
        assert bool(C.provider_conflicts(recs(case))) == (case == "case_05_provider_conflict"), case
        assert bool(C.accident_date_conflicts(recs(case))) == (case == "sample"), case


# ---------------------------------------------------------------------------------------------- T-141 r2: decide by content, never by a coinciding date
def _R(n, d, src, ex):
    return dict(n=n, date_iso=d, source=src, excerpt=ex, kind="encounter")


def _intake(n, stated, d="2026-02-20"):
    return _R(n, d, "Intake", f"Date of accident per intake form: {stated}.")


def test_t141_lib11_a_pre_accident_annual_visit_is_info_only():
    """GATE-M2 lib11: the annual visit on 03-04 lists accidents in 2019 and 2022 (history, not this collision); the stated 2026-03-18 is later than it.
    No conflict; the note says 1 record predates the stated date."""
    r = [_R(1, "2026-03-04", "PCP", "Annual visit. History per patient: car accidents in 2019 and 2022 with neck pain."),
         _R(2, "2026-03-18", "EMS", "Passenger vehicle struck from behind. Pt states neck pain 7/10."),
         _R(3, "2026-03-18", "ED", "Dx: cervical strain."),
         _R(4, "2026-03-26", "Firm, correspondence", "This firm represents the client for injuries from a collision on 2026-03-18.")]
    assert C.accident_date_conflicts(r) == []
    n = C.accident_date_note(r)
    assert n["code"] == "RECORDS_PREDATE_ACCIDENT" and n["count"] == 1 and n["record_nos"] == [1] and n["stated_date"] == "2026-03-18"
    assert n["text"].startswith("1 record predates the stated accident date")


def test_t141_r2_no_collision_wording_before_the_stated_date_is_info_not_a_conflict_even_with_no_record_on_that_day():
    """The old 'a record is dated that day' skip is gone; the content decides. Two pre-accident visits without mechanism wording: info (2 records)."""
    r = [_R(1, "2026-03-04", "PCP", "Annual visit. Back pain 3/10."), _R(2, "2026-03-10", "Chiro", "Neck pain 6/10, adjusted."),
         _R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-18.")]
    assert C.accident_date_conflicts(r) == []
    n = C.accident_date_note(r)
    assert n["count"] == 2 and n["record_nos"] == [1, 2] and n["text"].startswith("2 records predate the stated accident date")


def test_t141_r2_a_stated_date_that_matches_a_record_is_still_judged_by_content_not_by_the_match():
    """Reviewer variants B, C, D, F, G: the earliest record describes the collision in words the first word list missed; the stated date happens to be a follow-up's date."""
    cases = {
        "B hit from behind": ("2026-01-09", "Restrained driver, vehicle hit from behind at a stoplight. Neck pain.", "2026-01-19", "2026-01-19"),
        "C MVA with a full date in the previous year": ("2025-12-30", "MVA 12/30/2025, neck pain.", "2026-01-05", "2026-01-05"),
        "D no history of loss of consciousness": ("2026-01-09", "Rear-end collision, no history of loss of consciousness. Neck pain.", "2026-01-19", "2026-01-19"),
        "E plain": ("2026-01-09", "Rear-end collision. Neck pain.", "2026-01-19", "2026-01-19"),
        "F other vehicle hit them": ("2026-01-09", "Pt in car when another vehicle hit them. Neck pain 7/10.", "2026-01-19", "2026-01-19"),
        "G model year in the collision clause": ("2026-01-09", "Rear-end collision, driver of a 2019 Honda Civic. Neck pain.", "2026-01-19", "2026-01-19"),
        "G2 model year in the same clause": ("2026-01-09", "Rear-end collision of her 2019 Honda Civic. Neck pain.", "2026-01-19", "2026-01-19"),
    }
    for name, (d1, ex, d2, stated) in cases.items():
        r = [_R(1, d1, "ER", ex), _R(2, d2, "PT", "Follow-up. Neck pain 5/10."), _intake(3, stated)]
        out = C.accident_date_conflicts(r)
        assert len(out) == 1 and out[0]["category"] == "accident_date_after_treatment", name
        assert C.accident_date_note(r) is None, name


def test_t141_r2_a_prior_year_accident_in_the_same_sentence_as_this_collision_still_conflicts_only_by_clause():
    """History belongs to the clause that names the accident: 'Prior neck strain in 2019; rear-end collision today' is a collision record."""
    r = [_R(1, "2026-01-09", "ER", "Prior neck strain in 2019; rear-end collision today."), _R(2, "2026-01-19", "PT", "Follow-up."), _intake(3, "2026-01-19")]
    assert len(C.accident_date_conflicts(r)) == 1


def test_t141_r2_old_note_history_is_info_only_when_explicitly_prior_or_a_plural_history_list():
    """D-061: explicit prior/previous (or the lib11 'History per patient: car accidents' list) is info; a bare year or 'as a child' no longer exempts."""
    def run(ex):
        return C.accident_date_conflicts([_R(1, "2026-03-04", "PCP", f"Annual visit. {ex}"), _R(2, "2026-03-18", "ED", "MVA today."), _R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-18.")])
    for ex in ("History per patient: car accidents in 2019 and 2022 with neck pain.", "Prior motor vehicle collision 03/12/2019.", "Previous accident with whiplash."):
        assert run(ex) == [], ex
    for ex in ("Car accidents in 2019 and 2022 with neck pain.", "Hx of MVA in 2018.", "Patient was struck by a car as a child in 1998."):
        assert len(run(ex)) == 1, ex


def test_t141_two_different_stated_dates_still_conflict():
    r = [_R(1, "2026-03-04", "PCP", "Annual visit."), _R(2, "2026-03-18", "EMS", "Collision on 2026-03-18."), _R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-20.")]
    out = C.accident_date_conflicts(r)
    assert len(out) == 1 and out[0]["category"] == "accident_dates_differ"
    assert C.accident_date_note(r) is None


def test_t141_r2_the_conflict_compares_with_the_earliest_record_that_describes_the_collision():
    """A pre-accident annual visit on 03-04, the ED visit on 03-10 describes the collision, intake states 03-18: the first treatment cited is 03-10 (record 2), not the annual visit."""
    r = [_R(1, "2026-03-04", "PCP", "Annual visit. Back pain 3/10."), _R(2, "2026-03-10", "ED", "Rear-end collision, neck pain."), _R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-18.")]
    out = C.accident_date_conflicts(r)
    assert len(out) == 1 and out[0]["first_treatment_date"] == "2026-03-10" and 2 in out[0]["record_nos"] and 1 not in out[0]["record_nos"]


def test_t141_r2_stated_date_not_later_than_every_record_has_no_note():
    r = [_R(1, "2026-03-18", "ER", "Collision."), _R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-10.")]
    assert C.accident_date_note(r) is None
    assert C.accident_date_note([_R(1, "2026-03-18", "ER", "Visit.")]) is None


def test_t141_r2_run_summary_records_what_the_case_actually_ran():
    from app.backend import conflict_candidates as CC
    en = dict(_R(1, "2026-03-04", "PCP", "Annual visit."), lang="en")
    es = dict(_R(2, "2026-03-18", "Clinica", "Dolor de cuello."), lang="es")
    s = CC.run_summary([en, es, dict(_R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-18."), lang="en")], stage="ran")
    assert s["conflicts_stage"] == "ran" and s["unread"] == {"es": [2]} and s["read_records"] == 2
    assert "dated_records" not in s and "notes" not in s                  # T-141 r3: both are computed at read time from the current dates
    assert CC.run_summary([en], stage="skipped")["conflicts_stage"] == "skipped"
