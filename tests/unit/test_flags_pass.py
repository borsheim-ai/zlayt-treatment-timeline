"""Flag pass wiring beyond the golden floor: grounding, agreement, J3/J4, failures. Added by backend for T-036. R-FL-3..5, R-FL-7, ADR-008."""
from app.backend import flags as F
from app.llm import audited as AU, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall

EX = G.expected("sample")

def rec(n, case="sample", ex=EX):
    r = G.record(case, n)
    return dict(n=n, source=r["source"], excerpt=r["excerpt"], date_iso=ex["records"][n - 1]["date"])

R8 = rec(8)
HEDGE = "Findings may represent degenerative change; correlate clinically."

def test_ungrounded_model_flag_is_rejected_not_repaired():
    """R-FL-5: a model quote not verbatim in its record -> rejected; the text is left as the model wrote it."""
    c = FakeCall({"flags": {"flags": [dict(type="causation", category="speculative_language", excerpt="Findings suggest old degenerative change.")]}})
    out = F.run_flag_pass(R8, call=c)
    bad = [f for f in out if f["origin"] == "llm"]
    assert bad and bad[0]["state"] == "rejected" and "GROUNDING_EXCERPT_NOT_VERBATIM" in bad[0]["reasons"]
    assert bad[0]["excerpt"] == "Findings suggest old degenerative change."

def test_wrong_category_for_type_is_rejected():
    """ADR-013: a category outside the closed list for its type -> rejected SCHEMA_INVALID."""
    c = FakeCall({"flags": {"flags": [dict(type="causation", category="degenerative_language", excerpt="C5-C6 disc protrusion with mild right foraminal narrowing.")]}})
    out = F.run_flag_pass(R8, call=c)
    assert any(f["state"] == "rejected" and "SCHEMA_INVALID" in f["reasons"] for f in out)

def test_model_and_lexicon_agree_then_j4_decides():
    """AC5: agreed flag is verified only if J4 agrees; disagree/unsure/unavailable -> needs_review."""
    llm = [dict(type="causation", category="speculative_language", excerpt=HEDGE)]
    for verdict, code in (("agree", None), ("disagree", "JUDGE_DISAGREES"), ("unsure", "JUDGE_UNSURE")):
        fl = F.run_flag_pass(R8, call=FakeCall({"flags": {"flags": llm}}))
        both = [f for f in fl if f["origin"] == "both"]
        assert both and all("LEXICON_ONLY" not in f["reasons"] and "LLM_ONLY" not in f["reasons"] for f in both)
        F.judge_flags(fl, call=FakeCall({"j4": {"verdict": verdict, "reason_code": "NONE"}}))
        f = [x for x in fl if x["origin"] == "both"][0]
        assert (f["state"] == "verified") if code is None else (f["state"] == "needs_review" and code in f["reasons"])
    fl = F.run_flag_pass(R8, call=FakeCall({"flags": {"flags": llm}}))
    F.judge_flags(fl, call=FakeCall({"j4": AU.LLMFailed("x")}))
    assert "JUDGE_UNAVAILABLE" in [x for x in fl if x["origin"] == "both"][0]["reasons"]

def test_lexicon_only_flags_get_no_judge_call():
    """Row 12: a phrase-list-only flag stays LEXICON_ONLY needs_review and is not sent to J4."""
    fl = F.run_flag_pass(R8, call=FakeCall({"flags": {"flags": []}}))
    c = FakeCall({"j4": {"verdict": "agree", "reason_code": "NONE"}})
    F.judge_flags(fl, call=c)
    assert c.steps() == [] and all(f["state"] == "needs_review" and "LEXICON_ONLY" in f["reasons"] for f in fl)

def test_model_outage_keeps_lexicon_flags_with_reason():
    """Row 9: LLM failure/fixture miss -> lexicon flags survive with LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS."""
    for exc, code in ((AU.LLMFailed("x"), "LLM_FAILED_AFTER_RETRIES"), (P.FixtureMiss("x"), "FIXTURE_MISS")):
        fl = F.run_flag_pass(R8, call=FakeCall({"flags": exc}))
        assert fl and all(code in f["reasons"] for f in fl)

def test_conflict_pass_grounds_both_quotes_and_j3_decides():
    """T-094: plan-vs-actual across records 4 and 6 is proposed by code; J3 'conflict' verifies, 'benign' sends it to the could-not-verify tray."""
    recs = [rec(n) for n in range(1, 10)]
    out = F.run_conflict_pass(recs, call=FakeCall({"j3": {"verdict": "conflict", "reason_code": "PLAN_VS_ACTUAL"}}))
    assert len(out) == 1 and out[0]["record_nos"] == [4, 6] and out[0]["state"] == "verified" and "12 visits" in out[0]["explanation"]
    assert out[0]["excerpt"] == "Plan of care: 12 visits." and out[0]["excerpt_b"] == "Discharged from PT after two missed appointments."
    assert all(e["start"] is not None for e in out[0]["evidence"])
    out = F.run_conflict_pass(recs, call=FakeCall({"j3": {"verdict": "benign", "reason_code": "DIFFERENT_VISITS"}}))
    assert out[0]["state"] == "rejected" and "JUDGE_DISAGREES" in out[0]["reasons"]

def test_conflict_pass_has_no_model_search_so_no_incomplete_warning():
    """T-094 replaces the T-036 'conflict pass failed' warning: nothing is searched by a model, a failed J3 leaves the code candidate needs_review."""
    for exc, code in ((AU.LLMFailed("x"), "JUDGE_UNAVAILABLE"), (P.FixtureMiss("x"), "JUDGE_UNAVAILABLE")):
        out = F.run_conflict_pass([rec(n) for n in range(1, 10)], call=FakeCall({"j3": exc, "conflicts": exc}))
        assert len(out) == 1 and out[0]["type"] == "conflict" and out[0]["state"] == "needs_review" and code in out[0]["reasons"]
    assert F.run_conflict_pass([rec(1)], call=FakeCall({"conflicts": AU.LLMFailed("x")})) == []

def test_templates_quote_the_record_and_never_say_objective():
    """Review T-036 blocker: no flag title/explanation uses 'objective'; neutral wording for hedges and other-cause mentions."""
    from app.backend import flag_templates as FT
    for cat in FT.TYPE_OF:
        if FT.TYPE_OF[cat] in ("pre_existing", "causation"):
            t, e = FT.render(FT.TYPE_OF[cat], cat, provider="P", date="2026-01-02", quote="Cervical ROM full, no spasm noted.")
            assert "objective" not in (t + e).lower()
            assert "could be used" not in e and "suggesting another cause" not in e

def test_no_flag_carries_a_self_report_chip():
    """D-040: no code or model labels who is speaking, so every flag (including record 9's patient-statement flag) is a plain record flag."""
    for n in (7, 9):
        fl = F.lexicon_flags(rec(n))
        assert fl and all(f["source_kind"] == "record" for f in fl)

def test_no_flag_is_ever_accepted_and_none_is_labelled_by_speaker():
    """Invariant: every flag starts pending; D-040: record 9's flag has source_kind record."""
    fl = F.run_flag_pass(rec(9), call=FakeCall({"flags": {"flags": []}}))
    assert fl and all(f["review_status"] == "pending" for f in fl)
    assert all(f["source_kind"] == "record" for f in fl)

def test_flag_prompt_has_no_model_prose_fields_and_one_block():
    """Row 16: only type/category/excerpt cross the schema; the objective_negative category never becomes a UI title with that word."""
    from app.backend import schemas
    assert set(schemas.FlagOutput.model_fields) == {"type", "category", "excerpt", "excerpt_b"}
    assert all("objective_negative" not in f["title"] + f["explanation"] for f in F.lexicon_flags(rec(2)))


def test_no_template_ends_with_double_period():
    from app.backend import flag_templates as FT
    t, e = FT.render("pre_existing", "pre_existing", provider="P", date="2026-01-02", quote="Cervical ROM full.")
    assert ".”." not in e


def test_pipeline_makes_no_conflicts_call_and_a_failed_j3_is_a_visible_item_state(tmp_path):
    """T-094: the conflicts stage is code candidates + J3; there is no model search to fail. A J3 that fails leaves the candidate needs_review (JUDGE_UNAVAILABLE)."""
    from tests.unit._fakes import run_sample, sample_script
    out, call = run_sample(tmp_path, call=FakeCall(sample_script(j3=AU.LLMFailed("down"))))
    assert "conflicts" not in call.steps() and "CONFLICT_PASS_INCOMPLETE" not in [w["code"] for w in out["warnings"]]
    cx = [f for f in out["flags"] if f["type"] == "conflict" and f["category"] == "treatment_plan_vs_actual"]
    assert len(cx) == 1 and cx[0]["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in cx[0]["reasons"]


def test_d032_objective_negative_is_context_only_and_scene_facts_need_the_phrase_list():
    """D-032: normal/negative findings never become flags (either signal); a model scene_facts flag on a plain mechanism sentence is dropped."""
    r = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. X-ray negative for fracture. Ankle exam normal. Full cervical ROM.", date_iso="2026-06-01")
    llm = [dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),
           dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed.")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    assert not [f for f in out if f["state"] != "rejected"]                     # never a flag
    assert [f["category"] for f in out] == ["scene_facts", "objective_negative"] and out[0]["reasons"][0] == "LLM_ONLY"       # T-113 / D-053: the scene_facts proposal is a tray item, not a silent drop
    assert out[1]["reasons"] == ["FILTERED_BY_RULE"] and out[1]["state"] == "rejected"                                         # T-126 / D-057: the filtered proposal is listed, collapsed
    r2 = dict(r, excerpt="Ambulatory at scene, refused transport. Minimal damage to vehicle.")
    out = F.run_flag_pass(r2, call=FakeCall({"flags": {"flags": []}}))
    assert out and all(f["category"] == "scene_facts" and f["origin"] == "lexicon" for f in out)

def test_prior_condition_sentence_does_not_also_raise_alternative_cause():
    """One fact, one flag: case_06 'lifting injury several years ago' stays a pre_existing flag only."""
    r = rec(2, "case_06_subtle_pre_existing", G.expected("case_06_subtle_pre_existing"))
    cats = {f["category"] for f in F.lexicon_flags(r)}
    assert "alternative_cause" not in cats and "pre_existing" in cats


def test_d040_grounding_has_no_speaker_label_function():
    """D-040 (supersedes D-033/D-035/D-037): nothing in code decides who is speaking, so the chip helpers are gone and no module sets patient_report."""
    import pathlib
    from app.backend import grounding as GR
    assert not hasattr(GR, "has_self_report") and not hasattr(GR, "patient_report_spans")
    for p in pathlib.Path(F.__file__).parent.glob("*.py"):
        assert 'source_kind="patient_report"' not in p.read_text() and '"source_kind": "patient_report"' not in p.read_text(), p.name


def test_d040_every_excerpt_is_a_plain_record_excerpt():
    """Mixed, EMS, family and patient-subject excerpts all come out as source_kind record (the old NO_TAG/YES_TAG rows now assert no chip)."""
    from app.backend import present
    for t in ["Patient states symptoms began after the January collision.", "Pt c/o neck pain 7/10.", "EMS reports neck pain 7/10.",
              "Wife complains of neck pain.", "Patient states pain began after the collision, wife reports headaches.", "Subjective: pain 6/10."]:
        r = dict(n=1, source="Clinic", excerpt=t, date_iso="2026-06-01")
        assert all(f["source_kind"] == "record" for f in F.run_flag_pass(r, call=FakeCall({"flags": {"flags": []}})))
        row = dict(id="e1", state="needs_review", state_reasons=[], review_status="pending", edited=None, record_ids=["r1"], date_iso="2026-06-01",
                   provider="Clinic", summary="x", excerpt=t, excerpt_start=0, excerpt_end=len(t), ladder={})
        assert present.entry_view(row, {})["source_kind"] == "record"


def test_d038_credibility_phrases_raise_a_flag_with_the_sentence_excerpt():
    """D-038: Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent effort raise a lexicon flag (own category)."""
    phrases = ["3/5 Waddell signs positive.", "Subjective complaints out of proportion to exam findings.", "Symptom magnification noted.",
               "Non-physiologic sensory loss in the left arm.", "Inconsistent effort on strength testing."]
    for s in phrases:
        r = dict(n=1, source="IME", excerpt=s, date_iso="2026-06-01")
        out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": []}}))
        assert len(out) == 1, s
        f = out[0]
        assert f["category"] == "credibility_language" and f["type"] == "causation" and f["origin"] == "lexicon" and f["excerpt"] == s
        assert f["review_status"] == "pending" and "normal or absent" not in (f["title"] + f["explanation"]).lower()


def test_d038_other_normal_findings_stay_context_only_even_beside_a_credibility_phrase():
    """D-032 still holds: normal exam, negative imaging and 'no objective findings' raise nothing; a credibility sentence next to them does."""
    r = dict(n=1, source="IME", excerpt="X-ray negative for fracture. Ankle exam normal. Full cervical ROM. No objective findings.", date_iso="2026-06-01")
    assert F.run_flag_pass(r, call=FakeCall({"flags": {"flags": []}})) == []
    r2 = dict(r, excerpt=r["excerpt"] + " Waddell signs positive.")
    out = F.run_flag_pass(r2, call=FakeCall({"flags": {"flags": []}}))
    assert [f["category"] for f in out] == ["credibility_language"] and out[0]["excerpt"] == "Waddell signs positive."


def test_d038_negated_credibility_phrase_raises_nothing():
    r = dict(n=1, source="IME", excerpt="No Waddell signs.", date_iso="2026-06-01")
    assert F.run_flag_pass(r, call=FakeCall({"flags": {"flags": []}})) == []


def test_d038_hedged_credibility_sentence_keeps_its_own_credibility_flag():
    r = dict(n=1, source="IME", excerpt="Possible symptom magnification noted.", date_iso="2026-06-01")
    cats = {f["category"] for f in F.run_flag_pass(r, call=FakeCall({"flags": {"flags": []}}))}
    assert "credibility_language" in cats


def _cred(text):
    r = dict(n=1, source="IME", excerpt=text, date_iso="2026-06-01")
    return [f for f in F.run_flag_pass(r, call=FakeCall({"flags": {"flags": []}})) if f["category"] == "credibility_language"]


def test_d038_only_allow_listed_clean_negations_are_silent():
    """D-043: a sentence that is wholly one of the short clean-negation forms raises nothing (case and trailing punctuation vary)."""
    for s in ["No Waddell signs.", "no waddell signs", "Waddell signs negative.", "WADDELL SIGNS NEGATIVE",
              "0/5 Waddell signs.", "Effort consistent.", "Good effort.", "Full effort!", "Waddell signs not performed.", "Waddell signs not tested.",
              "Dr. Waddell examined the patient."]:
        assert _cred(s) == [], s


def test_d038_everything_else_with_a_credibility_term_flags():
    """D-043: any second clause, contrast word, side qualifier, comma, semicolon or extra words flags. Strings from the three T-067 reviews."""
    for s in ["Waddell signs negative, no symptom magnification.", "Pain is not out of proportion to the injury.", "No non-physiologic sensory loss.",
              "Waddell testing negative at all sites.", "Waddell signs not present.", "Waddell signs: none.", "No inconsistent effort.",
              "Effort was not inconsistent.", "Pain behavior not out of proportion.", "Pain not out of proportion.", "Without symptom magnification.",
              "Patient denies symptom magnification.", "Symptom magnification was ruled out.", "No evidence of symptom magnification.",
              "Malingering ruled out.", "Malingering was not suspected.", "Symptom magnification was not noted.", "Waddell tests were not administered.",
              "Waddell testing was not conducted.", "Waddell signs were not repeated.", "Waddell signs were not positive.", "No Waddell signs present.",
              "Waddell signs negative or equivocal.", "Waddell signs inconclusive.", "Waddell signs: no positive findings.",
              "Waddell testing has not been performed.", "Waddell signs negative on the left.", "No Waddell signs on the left.",
              "Waddell signs negative; positive straight leg raise.", "Waddell signs negative, straight leg raise positive.",
              "Effort was not consistent across trials.", "Effort is not consistent on grip.",
              "Patient exhibits pain behaviors during examination.", "Possible symptom magnification, ruled out later.",
              # T-067 r5 trim: forms outside D-043's list flag
              "Negative Waddell signs.", "Waddell signs were negative.", "0/5 Waddell", "Waddell signs: 0/5.", "No symptom magnification.",
              "No symptom-magnification."]:
        out = _cred(s)
        assert len(out) >= 1, s


def test_d038_family_variants_flag_with_the_sentence_excerpt():
    """T-067 r2 blocker 2: word order, inflection, hyphenation and Waddell phrasing of the same families."""
    for s in ["Effort is inconsistent during grip testing.", "Effort was inconsistent across repeated trials.", "The effort displayed was inconsistent.",
              "Inconsistent effort.", "inconsistent effort noted", "Submaximal effort noted.", "Sub-maximal effort on grip.", "Effort was poor.",
              "Magnifying symptoms noted.", "Patient is magnifying her symptoms.", "Pain behavior out of proportion.",
              "Pain behavior out of proportion to the injury.", "Waddell testing positive at 3 of 5 sites.", "Waddell 3 of 5 positive.",
              "3/5 Waddell signs positive.", "Symptom-magnification noted on exam.", "Non-organic physical signs present.",
              "Physical exam findings are non physiologic.", "Symptoms appear exaggerated.", "Findings concerning for malingering."]:
        out = _cred(s)
        assert len(out) == 1 and out[0]["excerpt"] == s and out[0]["review_status"] == "pending", s


def test_d038_negative_sentence_beside_a_positive_one_flags_only_the_positive_sentence():
    out = _cred("Waddell signs negative. Effort is inconsistent during grip testing.")
    assert [f["excerpt"] for f in out] == ["Effort is inconsistent during grip testing."]


def test_d038_credibility_template_is_neutral():
    out = _cred("Waddell signs positive.")
    text = (out[0]["title"] + out[0]["explanation"]).lower()
    assert "defense" not in text and "questions" not in text and "credibility" in text


def test_d038_mixed_result_waddell_sentence_flags_in_either_order():
    """D-043 (T-067 r3 blockers): mixed-result sentences flag whichever result comes first, with the whole sentence as the excerpt."""
    for s in ["Waddell signs negative on the left, positive on the right.", "Waddell signs negative on the left but positive on the right.",
              "Waddell signs positive on the right and negative on the left.", "Waddell signs positive on the right, negative on the left.",
              "Waddell signs: negative on the left, positive on the right.", "Waddell signs absent on the left but present on the right.",
              "Waddell signs negative, 3/5 on retest.", "No Waddell signs on the left, positive on the right.",
              "Waddell testing was not performed, but signs positive.", "3/5 Waddell.", "Waddell signs negative per Dr. Smith, positive later.",
              "Positive Waddell signs on the left, negative on the right.", "Positive Waddell signs on the left but negative on the right.",
              "Positive Waddell testing on the left, negative on the right.", "Abnormal Waddell signs on the left, negative on the right.",
              "Negative Waddell signs on the left, positive on the right.", "Waddell signs positive on the left, negative on the right.",
              "Waddell signs negative on the left and negative on the right.", "Waddell signs negative on the left, negative on the right.",
              "Negative Waddell signs on the left, negative on the right.", "No Waddell signs on the left, negative on the right."]:
        out = _cred(s)
        assert out and any(f["excerpt"] == s for f in out), s
    # a semicolon ends the sentence unit, so the clean-looking first half still flags (it is not the whole sentence)
    assert _cred("Waddell signs negative; positive on the right.")
    assert _cred("Subjective complaints out of proportion to exam findings; Waddell signs negative.")


def test_d043_semicolon_and_line_break_are_clause_separators_and_excerpt_is_the_full_sentence():
    """T-067 r4 blocker + major: ';' and line breaks do not end the credibility sentence; the flag quotes the whole period-delimited sentence."""
    from app.backend import grounding, sentences
    for s in ["Straight leg raise positive; Waddell signs negative.", "Positive on the right; no Waddell signs.",
              "Straight leg raise positive; Waddell testing was not done.", "Straight leg raise positive\nWaddell signs negative.",
              "Positive on the right\nno Waddell signs.", "Straight leg raise positive;\nWaddell signs negative.",
              "Waddell signs negative; straight leg raise positive.", "Waddell signs negative\nstraight leg raise positive.",
              "Waddell testing was not done; positive on the right.", "Waddell signs positive on the right; negative on the left.",
              "Subjective complaints out of proportion to exam findings; Waddell signs negative.",
              "Waddell signs positive on the left, no symptom magnification.", "No Waddell signs; Waddell signs negative."]:
        out = _cred(s)
        assert len(out) == 1 and out[0]["excerpt"] == s, s
        assert grounding.normalize(out[0]["excerpt"]) in grounding.normalize(s)
        assert sentences.is_whole_units(s, out[0]["excerpt"]), s
    # preceding and following sentences are not pulled in; a period still ends the sentence
    rec = "Gait antalgic. Straight leg raise positive; Waddell signs negative. Plan: PT."
    out = _cred(rec)
    assert [f["excerpt"] for f in out] == ["Straight leg raise positive; Waddell signs negative."]
    assert _cred("Straight leg raise positive. Waddell signs negative.") == []
    assert _cred("Waddell signs negative!") == []


def test_d038_clean_negation_allow_list_does_not_hide_a_neighbouring_credibility_sentence():
    out = _cred("No Waddell signs. Effort was not consistent across trials.")
    assert [f["excerpt"] for f in out] == ["Effort was not consistent across trials."]


def test_t092_allow_list_is_the_d043_forms_plus_t111_single_clause_not_done():
    """T-067 r5 C01-C10 kept 'was/were', other nouns, colon, spaced 0 / 5 and 'signs not done' flagging. T-111 re-admits only the
    single-clause 'Waddell testing not performed/done.' form (see test_t111_*); everything else in this list still flags."""
    for s in ["Waddell testing was not done.", "No Waddell testing.", "Waddell testing negative.", "Waddell signs were not performed.",
              "Waddell signs not done.", "No Waddell criteria.", "0 / 5 Waddell signs.", "Waddell signs: negative.", "Waddell testing: not performed."]:
        out = _cred(s)
        assert len(out) == 1 and out[0]["excerpt"] == s, s
    for s in ["No Waddell signs.", "Waddell signs negative.", "0/5 Waddell signs.", "Effort consistent.", "Good effort.", "Full effort.",
              "Waddell signs not tested.", "Waddell signs not performed.", "Waddell testing not performed.", "Waddell testing not done."]:
        assert _cred(s) == [], s


def test_t111_single_clause_not_performed_or_not_done_is_silent():
    """T-111 (D-043 'Not tested/not performed' reading): one clause 'Waddell testing not performed.' / 'not done.', 'Waddell signs not tested.'
    or 'Not tested.' raises nothing, whatever the case, spacing or trailing punctuation. Each form is paired with a flagging
    variant below so the silence is shown to come from the allow-list, not from a missed term."""
    for s in ["Waddell testing not performed.", "Waddell testing not done.", "WADDELL TESTING NOT DONE", "waddell testing not performed!",
              "Waddell  testing   not done.", "Waddell testing not done", "Waddell testing not performed?", "Waddell signs not tested.",
              "Not tested.", "not tested", "NOT TESTED!"]:
        assert _cred(s) == [], s
    assert _cred("Waddell testing not performed, but pain persisted.") and _cred("Waddell signs not tested, but pain persisted.")


def test_t111_second_clause_contrast_side_or_extra_word_still_flags_the_sentence():
    """T-111: the same forms flag as soon as a second clause, contrast word, side qualifier or extra word joins them (D-043)."""
    cases = ["Waddell testing not performed, but pain persisted.", "Waddell testing not done; straight leg raise positive.",
             "Waddell testing not performed on the left.", "Waddell testing not done (claimant declined).",
             "Waddell testing not performed however.", "Waddell testing not done, though symptom magnification noted.",
             "Waddell testing not performed and Waddell signs negative.", "Waddell testing not performed at the IME.",
             "Waddell testing not done yet.", "Waddell testing not performed or reported.", "Waddell signs not tested, but pain behaviour noted.",
             "Not tested, but symptom magnification noted.", "Waddell testing not performed; no symptom magnification.",
             "Waddell testing not done\nstraight leg raise positive."]
    for s in cases:
        out = _cred(s)
        assert out and all(f["excerpt"] == s for f in out), s
    out = _cred("Waddell testing not performed. Symptom magnification noted.")
    assert [f["excerpt"] for f in out] == ["Symptom magnification noted."]


def test_t111_r2_reversed_and_counted_waddell_forms_flag_and_bare_count_after_a_waddell_sentence_flags():
    """T-111 r2 (claims-adjuster probes): every word order of a Waddell result flags the whole sentence; a bare 'N/5 positive' flags when the
    sentence right before it is a Waddell sentence; the single-clause not-performed form stays silent."""
    for s in ["Positive Waddell signs.", "Positive Waddell.", "Waddell 3/5 positive.", "3 of 5 Waddell signs.", "Waddell's signs positive.",
              "Waddell\u2019s signs positive.", "Waddell-signs positive.", "Negative Waddell signs."]:
        out = _cred(s)
        assert len(out) == 1 and out[0]["excerpt"] == s, s
    out = _cred("Waddell testing not performed. 3/5 positive.")
    assert [f["excerpt"] for f in out] == ["3/5 positive."]
    out = _cred("Waddell testing not performed. Positive Waddell.")
    assert [f["excerpt"] for f in out] == ["Positive Waddell."]
    assert [f["excerpt"] for f in _cred("Waddell testing not performed.\n3 of 5 positive.")] == ["3 of 5 positive."]
    for s in ["3/5 positive.", "Waddell testing not performed.", "Waddell testing not done.", "Straight leg raise positive. 3/5 positive.",
              "Waddell testing not performed. Straight leg raise positive. 3/5 positive."]:
        assert _cred(s) == [], s


def test_t092_model_flag_overlapping_a_credibility_sentence_keeps_the_whole_sentence_excerpt():
    """T-067 r5 F01: a model clause never replaces the credibility flag's whole-period-sentence excerpt (origin still 'both')."""
    text = "Straight leg raise positive; Waddell signs negative."
    r = dict(n=1, source="IME", excerpt=text, date_iso="2026-06-01")
    for quote in ("Waddell signs negative.", text, "Straight leg raise positive"):
        llm = [dict(type="causation", category="credibility_language", excerpt=quote)]
        fl = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
        cred = [f for f in fl if f["category"] == "credibility_language" and f["origin"] == "both"]
        assert len(cred) == 1, (quote, [(f["category"], f["origin"], f["excerpt"]) for f in fl])
        assert cred[0]["excerpt"] == text and cred[0]["evidence"][0]["text"] == text, quote
        assert (cred[0]["evidence"][0]["start"], cred[0]["evidence"][0]["end"]) == (0, len(text)), quote


def test_t092_hedge_run_never_quotes_a_neighbour_sentence_into_a_credibility_flag():
    """T-067 r5 D01: the credibility flag quotes only its own sentence even when the neighbour is hedge wording."""
    out = _cred("Findings may represent degenerative change. Possible symptom magnification noted.")
    assert [f["excerpt"] for f in out] == ["Possible symptom magnification noted."]
    out = _cred("Possible symptom magnification noted. Findings may represent degenerative change.")
    assert [f["excerpt"] for f in out] == ["Possible symptom magnification noted."]


def test_a_model_proposed_conflict_is_a_tray_item_not_a_silent_drop():
    """T-113 / D-053 (T-109 r2 finding): the per-record pass used to filter model conflicts out at the schema step. The proposal is now a could-not-verify tray
    item (rejected, LLM_ONLY, the model's quotes kept), never a flag; the model's category/quote text is not used as a title."""
    r = dict(n=4, source="Capital PT", excerpt="Plan of care: 12 visits. Patient attended 3.", date_iso="2026-01-23")
    llm = [dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.", excerpt_b="Discharged after two missed appointments."),
           dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.", excerpt_b="Discharged after two missed appointments."),
           dict(type="conflict", category="not_a_category", excerpt="Plan of care: 12 visits.")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    cx = [f for f in out if f["type"] == "conflict"]
    assert len(cx) == 2 and all(f["state"] == "rejected" and f["reasons"][0] == "LLM_ONLY" and f["origin"] == "llm" for f in cx)
    good = next(f for f in cx if f["category"] == "treatment_plan_vs_actual")
    assert good["excerpt"] == "Plan of care: 12 visits." and good["excerpt_b"] == "Discharged after two missed appointments." and "Unrecognised" not in good["title"]
    assert any("SCHEMA_INVALID" in f["reasons"] for f in cx if f["category"] == "not_a_category")
    ungrounded = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": [dict(llm[0], excerpt="Twelve visits were planned.")]}}))
    assert ungrounded[0]["state"] == "rejected" and "GROUNDING_EXCERPT_NOT_VERBATIM" in ungrounded[0]["reasons"]


def test_a_model_conflict_reaches_the_case_tray_and_never_the_flag_list(tmp_path):
    from app.backend import present
    from app.backend import pipeline as PL
    from app.db import db as DB
    from tests.unit._fakes import sample_script, which_record
    extra = dict(type="conflict", category="other_fact_mismatch", excerpt="Plan of care: 12 visits.", excerpt_b="Discharged from PT after two missed appointments.")
    flags = lambda user: {"flags": [extra]} if which_record(user) == [4] else {"flags": []}
    conn = DB.connect(str(tmp_path / "c.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=flags)), now=lambda: 1.0)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    t = [x for x in v["tray"] if x["kind"] == "flag" and x["flag"]["type"] == "conflict" and x["flag"]["category"] == "other_fact_mismatch"]
    assert len(t) == 1 and t[0]["reasons"][0] == "LLM_ONLY" and t[0]["state"] == "rejected" and t[0]["id"] not in v["review"]["queue"]
    assert not [f for f in v["flags"] if f["category"] == "other_fact_mismatch"]


def test_tray_items_come_last_so_no_recorded_judge_prompt_changes():
    """A flag's id (f_r<n>_<k>) is its position in the list and is inside the judge prompt (the nonce), so a newly kept tray item must not renumber the others."""
    r = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. Patient had a prior cervical strain in 2022. X-ray negative.", date_iso="2026-06-01")
    llm = [dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed."),
           dict(type="pre_existing", category="pre_existing", excerpt="Patient had a prior cervical strain in 2022."),
           dict(type="conflict", category="other_fact_mismatch", excerpt="X-ray negative.", excerpt_b="x")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    states = [f["state"] == "rejected" for f in out]
    assert states == sorted(states) and states.count(True) == 2 and not states[0]


def test_a_tray_proposal_listed_before_a_kept_flag_does_not_take_its_place():
    """T-113 r2 F4: scene_facts (tray) is proposed BEFORE an AI-only kept flag; the kept flag must still be first, or its id f_r<n>_<k> (inside the judge prompt) shifts.
    Mutant: dropping the tray-last reorder in run_flag_pass gives [scene_facts, pre_existing]."""
    r = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. Pain 6/10.", date_iso="2026-06-01")
    llm = [dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed."),
           dict(type="pre_existing", category="pre_existing", excerpt="Pain 6/10."),
           dict(type="conflict", category="other_fact_mismatch", excerpt="Pain 6/10.", excerpt_b="Cyclist struck by a car at low speed.")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    assert [(f["category"], f["state"] == "rejected") for f in out] == [("pre_existing", False), ("scene_facts", True), ("other_fact_mismatch", True)]


def test_a_model_proposed_conflict_says_why_it_is_in_the_tray_and_does_not_blame_the_phrase_list():
    """T-113 r2 F5: conflicts never come from the phrase list; the only rule is that a pair the software's own rules pick can be a conflict."""
    r = dict(n=4, source="Capital PT", excerpt="Plan of care: 12 visits. Patient attended 3.", date_iso="2026-01-23")
    llm = [dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.", excerpt_b="Patient attended 3."),
           dict(type="causation", category="scene_facts", excerpt="Patient attended 3.")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    cx = next(f for f in out if f["type"] == "conflict")
    assert cx["reasons"][0] == "LLM_ONLY" and "phrase list" not in cx["why"].lower() and "fixed rules" in cx["why"]
    sf = next(f for f in out if f["category"] == "scene_facts")
    assert "phrase list" in sf["why"]            # a scene_facts proposal really is a phrase-list miss: its sentence is unchanged
    from app.backend import flags as FL
    j = FL.judge_flags([dict(cx, state="needs_review", reasons=["LLM_ONLY"], why="x")], call=FakeCall({}))
    assert "phrase list" not in j[0]["why"].lower()


def test_a_tray_item_that_was_never_judged_does_not_carry_judge_unavailable():
    """T-122: a model-only scene_facts / conflict tray item is not sent to a judge by design (LLM_ONLY, not code-confirmed). It must carry its real reason only;
    the compose default 'judge unavailable' would be counted by the eval as a judge that did not run."""
    r = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. X-ray negative.", date_iso="2026-06-01")
    llm = [dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed."),
           dict(type="conflict", category="other_fact_mismatch", excerpt="X-ray negative.", excerpt_b="x")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    assert len(out) == 2
    for f in out:
        assert f["state"] == "rejected" and f["reasons"][0] == "LLM_ONLY" and "JUDGE_UNAVAILABLE" not in f["reasons"] and "JUDGE_UNAVAILABLE" not in f["why"].upper().replace(" ", "_")
        assert f["_stage"]["judge"] is None and not (f["ladder"].get("judge") or {}).get("verdict")


def test_case_05_has_no_judge_unavailable_item():
    """T-122: the golden case_05 tray flag f_r1_1 (scene_facts, LLM_ONLY) was the one item the eval counted as judge-unavailable."""
    from evals import run as ER
    from app.backend import pipeline as PL
    out = PL.run_case(G.raw("case_05_provider_conflict"), "fixture") if hasattr(PL, "run_case") else None
    assert out is not None and ER.judge_unavailable_in(out) == 0
