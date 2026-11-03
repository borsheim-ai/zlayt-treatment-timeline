"""T-133 (T-120 r3 / T-132 leftovers, lexicon only): (1) the denial forms deny / denies / denied / denying are negation words everywhere the lexicon lists
negation (the NegEx-style guard, the field answer, the added_qualifier negation_word family that grounding reads); declined / declines stay care refusals.
(2) a bare 'History ... notable/significant for X' raises the prior-condition flag, including after a history-source attribution ('History provided by wife,
notable for lumbar strain'), while an attribution-only sentence and non-patient histories stay quiet. Deterministic code, no model."""
import re

import pytest

from app.backend import flags as FL, grounding as G, lexicon, lexicon_scan as LS

DENY = ("deny", "denies", "denied", "denying")


def _prior(text):
    return [h for h in LS.scan(text) if h["flag_type"] == "pre_existing"]


def _quotes(text):
    return sorted({text[h["unit_start"]:h["unit_end"]] for h in _prior(text)})


# 1. denial forms ------------------------------------------------------------------------------------------------------------------------------------------------
def test_every_denial_form_is_a_negation_cue_and_a_negation_word():
    neg = lexicon.load()["negation"]
    for w in DENY:
        assert w in neg["pre_cues"], w
        assert G.is_negation_word(w), w
        assert G.has_negation(f"Patient {w} numbness."), w
    assert re.match(neg["field_answer"], "? Deny.", re.I)


def test_declined_is_not_a_negation_cue():
    # 'declined ambulance transport' / 'declined ESI' are care refusals the scene_facts and missed_care entries must keep raising
    neg = lexicon.load()["negation"]
    assert not {"declined", "declines"} & set(neg["pre_cues"])
    assert not G.is_negation_word("declined")
    r = {"n": 1, "id": "r1", "source": "EMS", "date_iso": "2026-01-09", "excerpt": "Patient declined ambulance transport."}
    assert [f["category"] for f in FL.lexicon_flags(r)] == ["scene_facts"]


@pytest.mark.parametrize("text", [
    "Patient and wife deny prior neck injury.",
    "Patient denying prior neck injury.",
    "Patient denies prior neck injury.",
    "Prior neck injury denied.",
    "Prior injuries? Deny.",
])
def test_a_denied_prior_injury_raises_no_prior_flag(text):
    assert _prior(text) == [], _prior(text)


def test_the_same_sentence_without_the_denial_flags():
    # control: it is the denial word, not the sentence shape, that keeps the cases above quiet
    assert _prior("Patient and wife report prior neck injury.")
    assert _prior("Patient describing prior neck injury.")


def test_without_denying_in_pre_cues_the_denying_sentence_flags(monkeypatch):
    # mutant: drop 'denying' from the cue list and the guard no longer suppresses it (the test above would fail)
    neg = dict(lexicon.load()["negation"])
    neg["pre_cues"] = [c for c in neg["pre_cues"] if c != "denying"]
    real = lexicon.load()
    monkeypatch.setattr(LS.lexicon, "load", lambda: dict(real, negation=neg))
    assert _prior("Patient denying prior neck injury.")


def test_grounding_reads_deny_as_a_negation_in_the_quote_and_the_summary():
    # the quote's 'deny' is a negation a summary may not drop, and a summary may not add one the quote lacks
    assert "negation" in G.dropped_qualifiers("Numbness.", "Patient and wife deny numbness.")
    assert "negation" not in G.dropped_qualifiers("Patient and wife deny numbness.", "Patient and wife deny numbness.")
    assert "deny" in G.new_tokens("Patient and wife deny numbness.", "Numbness reported.")
    assert "denying" in G.new_tokens("Denying numbness.", "Numbness.")
    assert G.negation_words("Patient and wife deny numbness; denying weakness.") == ["deny", "denying"]


def test_a_deny_summary_carries_the_quotes_attribution():
    # r2 F2: attribution_word has deny / denying, so a summary that says 'deny' keeps the quote's 'Patient reports' (no self_report drop);
    # removing them from attribution_word makes these return ['self_report']
    assert G.dropped_qualifiers("Deny numbness.", "Patient reports numbness.") == []
    assert G.dropped_qualifiers("Patient and wife deny numbness.", "Patient reports numbness.") == []
    assert G.dropped_qualifiers("Denying numbness.", "Patient reports numbness.") == []


def test_every_denial_form_has_an_opened_source_in_the_lexicon():
    # r2 F4: denied/denies/denying from NegEx, all four (deny included) from the pyConText lexical KB; the yaml names both paths
    import pathlib
    y = (pathlib.Path(lexicon.__file__).resolve().parents[1] / "llm" / "lexicon.yaml").read_text()
    assert "chapmanbe/negex/master/genConText/negex_triggers.txt" in y
    assert "chapmanbe/pyConTextNLP/master/KB/lexical_kb_05042016.yml" in y


# 2. bare 'History ... notable/significant for' -----------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("text,quote", [
    ("History provided by wife, notable for lumbar strain.", "History provided by wife, notable for lumbar strain."),          # the T-120 staff probe
    ("History significant for diabetes.", "History significant for diabetes."),
    ("History provided by wife; notable for lumbar strain.", "History provided by wife; notable for lumbar strain."),          # T-132 extension form
    ("History obtained via interpreter, significant for chronic low back pain.", "History obtained via interpreter, significant for chronic low back pain."),
    ("Pain 6/10. History is notable for a 2019 lumbar strain. Plan PT.", "History is notable for a 2019 lumbar strain."),
    ("Medical history remarkable for prior neck surgery.", "Medical history remarkable for prior neck surgery."),
    ("History is significant for prior assault.", "History is significant for prior assault."),                                          # r2 F1 acceptance
    ("History reviewed with patient, notable for lumbar strain after a 2019 MVA.", "History reviewed with patient, notable for lumbar strain after a 2019 MVA."),  # a dated earlier MVA is not the index cue
])
def test_bare_history_notable_for_raises_the_prior_condition_flag(text, quote):
    assert _quotes(text) == [quote], _quotes(text)
    assert "history_significant_for" in {h["id"] for h in _prior(text)}


def test_the_hit_is_the_history_word_so_the_attribution_gate_applies():
    # lexicon_scan strips the history-source attribution only for a hit that IS a history word (T-120 r3); the condition phrase is a look-ahead
    h = [x for x in _prior("History provided by wife, notable for lumbar strain.") if x["id"] == "history_significant_for"][0]
    assert h["text"] == "History" and LS._HISTORY_WORD.match(h["text"])


def test_it_is_one_flag_with_the_condition_in_the_quote():
    r = {"n": 1, "id": "r1", "source": "ER", "date_iso": "2026-01-09", "excerpt": "Pain 7/10. History provided by wife, notable for lumbar strain."}
    pre = [f for f in FL.lexicon_flags(r) if f["type"] == "pre_existing"]
    assert len(pre) == 1 and pre[0]["excerpt"] == "History provided by wife, notable for lumbar strain." and pre[0]["category"] == "pre_existing"


def test_with_pmh_significant_for_it_joins_the_same_flag():
    r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": "Past medical history significant for cervical radiculopathy."}
    pre = [f for f in FL.lexicon_flags(r) if f["type"] == "pre_existing"]
    assert len(pre) == 1 and set(pre[0]["lexicon_ids"]) == {"pmh_significant_for", "history_significant_for"}


@pytest.mark.parametrize("text", [
    "History provided by wife.",                                             # attribution only
    "History obtained from patient's son, who interpreted.",
    "Family history significant for diabetes.",                              # not the patient
    "Social history notable for tobacco use.",
    "Interval history significant for improved sleep.",                      # since the last visit
    "History of present illness notable for neck pain after the MVA.",       # HPI header
    "History and physical notable for cervical tenderness.",
    "History obtained from patient, exam notable for paraspinal spasm.",     # an exam finding, not history
    "History: rear-ended at a light, notable for neck pain.",                # the index accident
    "History provided by wife. Exam notable for spasm.",                     # the condition phrase is in another sentence
    "History notable for: none.",                                            # field answer
    "History significant for no prior injuries.",                            # suppressor
    "Denies history significant for neck injury.",                           # negation guard
])
def test_these_history_sentences_raise_no_history_significant_for_hit(text):
    assert "history_significant_for" not in {h["id"] for h in _prior(text)}, _prior(text)


# 3. r2 F1: the HPI is not a past history (reviews/T-133-staff-engineer-r2.md) ---------------------------------------------------------------------------------
HPI = [
    "History: 45-year-old male, significant for neck pain.",
    "History: patient was a passenger, significant for neck pain.",
    "Chief complaint and history: notable for neck pain.",
    "History obtained from patient, notable for neck pain since the crash.",
    "History - significant for neck pain.",
    "History: significant for neck pain.",
    "History of present illness: 45-year-old male, notable for neck pain.",
    "HISTORY OF PRESENT ILLNESS: significant for neck pain after the MVA.",
    "History of present illness: significant for lumbar strain.",
    "Chief complaint: neck pain. History of present illness: significant for stiffness.",
    "History is significant for neck pain that began today.",
    "History notable for neck pain following the collision.",
    "History, 34 y/o female driver, notable for neck pain.",
]


@pytest.mark.parametrize("text", HPI)
def test_an_hpi_header_or_narrative_raises_no_prior_condition_flag(text):
    r = {"n": 1, "id": "r1", "source": "ER", "date_iso": "2026-01-09", "excerpt": text}
    assert [f for f in FL.lexicon_flags(r, 2026) if f["type"] == "pre_existing"] == [], text
    assert "history_significant_for" not in {h["id"] for h in LS.scan(text, 2026)}


def test_without_the_header_guard_the_hpi_header_flags(monkeypatch):
    # mutant: drop the "History:" header exclusion and the bare header form flags again (the test above would fail)
    real = LS._entries()
    pat = next(e for e, _, _ in real if e["id"] == "history_significant_for")["pattern"]
    assert r"(?!\s*[:\-])" in pat
    import re as _re
    mut = tuple((e, _re.compile(pat.replace(r"(?!\s*[:\-])", ""), _re.I | _re.M) if e["id"] == "history_significant_for" else rx, sup) for e, rx, sup in real)
    monkeypatch.setattr(LS, "_entries", lambda: mut)
    assert "history_significant_for" in {h["id"] for h in LS.scan("History: significant for neck pain.", 2026)}


# 4. r2 F3: a flag's quote always shows the condition ------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("text,condition", [
    ("Pain 7/10. History provided by wife; notable for lumbar strain. Plan PT.", "notable for lumbar strain"),
    ("History per interpreter; significant for cervical fusion.", "significant for cervical fusion"),
    ("History obtained from the patient's son; notable for prior neck injury.", "notable for prior neck injury"),
])
def test_a_semicolon_is_crossed_only_after_an_attribution_and_the_quote_shows_the_condition(text, condition):
    r = {"n": 1, "id": "r1", "source": "ER", "date_iso": "2026-01-09", "excerpt": text}
    pre = [f for f in FL.lexicon_flags(r, 2026) if f["type"] == "pre_existing"]
    assert len(pre) == 1 and condition in pre[0]["excerpt"], pre


@pytest.mark.parametrize("text", ["History reviewed; notable for pain on cough.", "Pain 6/10. History reviewed; notable for pain on cough."])
def test_a_non_attribution_semicolon_is_not_crossed_so_no_conditionless_quote(text):
    # the T-132 unit extension only extends attribution-only units; crossing here would quote "History reviewed;" with no condition
    r = {"n": 1, "id": "r1", "source": "ER", "date_iso": "2026-01-09", "excerpt": text}
    assert [f for f in FL.lexicon_flags(r, 2026) if f["type"] == "pre_existing"] == []


# 5. r3 F1: a QUALIFIED history header is past history and still flags; only a bare "History:" / "History -" header is the HPI ----------------------------------
QUALIFIED = [
    "Past history: significant for lumbar strain.",
    "Medical history: significant for diabetes.",
    "Surgical history: notable for L4-5 laminectomy.",
    "Past medical history: significant for diabetes.",
    "Prior history: notable for cervical strain.",
    "Previous history - significant for lumbar strain.",
]


@pytest.mark.parametrize("text", QUALIFIED)
def test_a_qualified_history_header_still_flags_with_the_full_sentence(text):
    r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": text}
    pre = [f for f in FL.lexicon_flags(r, 2026) if f["type"] == "pre_existing"]
    assert len(pre) == 1 and pre[0]["excerpt"] == text, pre
    assert "history_significant_for" in {h["id"] for h in LS.scan(text, 2026)}


def test_without_the_qualifier_exemption_the_qualified_headers_lose_the_flag(monkeypatch):
    # mutant: make the header guard apply to every history word (the f939ccb regression) and the qualified headers go quiet
    real = LS._entries()
    pat = next(e for e, _, _ in real if e["id"] == "history_significant_for")["pattern"]
    guard = r"(?:(?<=[a-z][ \t]history)(?<!\band[ \t]history)|(?!\s*[:\-]))"
    assert guard in pat
    import re as _re
    mut = tuple((e, _re.compile(pat.replace(guard, r"(?!\s*[:\-])"), _re.I | _re.M) if e["id"] == "history_significant_for" else rx, sup) for e, rx, sup in real)
    monkeypatch.setattr(LS, "_entries", lambda: mut)
    assert not any("history_significant_for" in {h["id"] for h in LS.scan(t, 2026)} for t in QUALIFIED)


R3_HPI = [   # reviews/T-133-staff-engineer-r3.md HPI01-HPI15 and the r2 F1 sentences
    "History: rear-ended at a light, notable for neck pain.", "History - 52 year old female, significant for headache.",
    "History: restrained driver, notable for neck pain after MVA.", "History: pt seen today, notable for neck pain.",
    "History: presents with neck pain, notable for stiffness.", "History reviewed; notable for pain on cough.",
    "History reviewed with patient; notable for neck stiffness.", "History: MVA on 1/9, notable for neck pain.",
    "History: 45 yo M, notable for neck pain from crash.", "History: the patient states she was rear-ended, significant for neck pain.",
    "History obtained from patient, exam notable for paraspinal spasm.", "Patient reports neck pain. History: notable for stiffness since yesterday.",
    "History of present illness notable for neck pain after the MVA.", "History of present illness: notable for neck pain since the crash.",
    "History: 37-year-old woman, notable for lumbar pain after a fall at work.",
    "History: 45-year-old male, significant for neck pain.", "History: patient was a passenger, significant for neck pain.",
    "Chief complaint and history: notable for neck pain.", "History obtained from patient, notable for neck pain since the crash.",
]


@pytest.mark.parametrize("text", R3_HPI)
def test_the_reviewer_hpi_probes_stay_quiet(text):
    assert "history_significant_for" not in {h["id"] for h in LS.scan(text, 2026)}, text


# 6. r3 F2 (scope cut, pinned): a ';' after a NON-attribution phrase is not crossed. The flag's quote is its unit, and the T-132 extension (backend) only extends an
# attribution-only unit, so crossing would quote "History reviewed;" with no condition. Recorded as a scope-cut proposal on the card for the orchestrator.
@pytest.mark.parametrize("text", ["History reviewed; significant for diabetes.", "History reviewed with patient; notable for neck stiffness."])
def test_scope_cut_a_non_attribution_semicolon_form_does_not_flag(text):
    assert "history_significant_for" not in {h["id"] for h in LS.scan(text, 2026)}


# 7. r3 F4 (decision recorded in the entry rationale, pinned): the patient as the named source is treated like any other source (the wife): the sentence still flags
# unless a presentation / index-accident cue keeps it quiet ("since the crash").
@pytest.mark.parametrize("text,flags_", [
    ("History obtained from patient, notable for neck pain.", True),
    ("History per patient: significant for lumbar strain.", True),
    ("History provided by wife, notable for lumbar strain.", True),
    ("History obtained from patient, notable for neck pain since the crash.", False),
])
def test_the_patient_as_source_is_treated_like_any_other_source(text, flags_):
    assert ("history_significant_for" in {h["id"] for h in LS.scan(text, 2026)}) is flags_


# 8. r3: against the parent commit and r1, no prior-condition flag is lost except the HPI over-flags (and the pinned scope-cut semicolon form) ---------------------
PARENT, R1 = "e79c3aa^", "e79c3aa"      # e79c3aa is the T-133 r1 commit; its parent has no history_significant_for entry


def _corpus():
    import json
    import pathlib
    root = pathlib.Path(lexicon.__file__).resolve().parents[2]
    out = set(QUALIFIED) | set(R3_HPI) | set(HPI)
    for e in lexicon.load()["entries"]:
        for k in ("hit", "miss", "negated"):
            out.update(e.get("examples", {}).get(k, []))
    for line in (root / "evals" / "lexicon_heldout.jsonl").read_text().splitlines():
        if line.strip():
            out.add(json.loads(line)["text"])
    for f in sorted((root / "evals" / "golden").glob("*.txt")):
        out.update(l.strip() for l in f.read_text().splitlines() if l.strip())
    out.update([
        "Hx obtained via patient's son, who interpreted, denies neck pain.", "Patient and wife deny prior neck injury.", "Patient denying prior neck injury.",
        "PMH: significant for lumbar strain.", "Hx: significant for lumbar strain.", "History: significant for lumbar strain.",
        "Past medical history significant for cervical radiculopathy.", "History provided by wife; notable for lumbar strain.",
        "History obtained from patient, notable for neck pain.", "History per patient: significant for neck pain.", "History (per patient): notable for neck pain.",
    ])
    return sorted(out)


def _prior_flags_at(sha, corpus, monkeypatch):
    import subprocess
    import pathlib
    import yaml
    root = pathlib.Path(lexicon.__file__).resolve().parents[2]
    try:
        y = subprocess.run(["git", "show", f"{sha}:app/llm/lexicon.yaml"], cwd=root, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip(f"git object {sha} not available (archive or shallow clone)")
    data = yaml.safe_load(y)
    with monkeypatch.context() as m:
        m.setattr(lexicon, "load", lambda: data)
        LS._entries.cache_clear()
        try:
            return _prior_flag_set(corpus)
        finally:
            LS._entries.cache_clear()


def _prior_flag_set(corpus):
    out = set()
    for t in corpus:
        r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": t}
        out |= {(t, f["excerpt"]) for f in FL.lexicon_flags(r, 2026) if f["type"] == "pre_existing"}
    return out


def test_no_prior_condition_flag_on_the_parent_is_lost(monkeypatch):
    corpus = _corpus()
    before = _prior_flags_at(PARENT, corpus, monkeypatch)
    now = _prior_flag_set(corpus)
    assert before, "baseline produced no flags"
    # the only intended loss: a denial form the parent did not read as a negation (T-133 point 1)
    intended = {"Patient denying prior neck injury."}
    lost = {t for t, _ in before - now}
    assert lost == intended, sorted(lost)


def test_against_r1_only_the_hpi_over_flags_and_the_scope_cut_form_are_lost(monkeypatch):
    corpus = _corpus()
    before = _prior_flags_at(R1, corpus, monkeypatch)
    now = _prior_flag_set(corpus)
    # HPI over-flags, the bare 'History:' header (an HPI header by rule) and the pinned scope-cut semicolon form
    allowed = set(R3_HPI) | set(HPI) | {"History reviewed; significant for diabetes.", "History reviewed with patient; notable for neck stiffness."}
    bare_header = re.compile(r"(?:^|[.!?]\s+|\band\s+)history\s*[:\-]", re.I)       # by rule: a bare 'History:' / 'History -' header is the HPI
    lost = {t for t, _ in before - now if t not in allowed and not bare_header.search(t)}
    assert not lost, sorted(lost)
    assert {t for t, _ in now if t in QUALIFIED} == set(QUALIFIED)


# 9. r4 F1: a bare 'History:' header on its OWN LINE is the HPI whatever the previous line ends with (the qualifier look-behind must not cross a newline) ----------
OWN_LINE = [
    "Patient seen in clinic\nHistory: significant for neck pain.",
    "Chief complaint: neck pain\nHistory: 45-year-old male, notable for neck pain.",
    "Rear-ended at a light\r\nHistory - significant for headache.",
    "Seen today for follow up\n\nHistory: notable for stiffness.",
]


@pytest.mark.parametrize("text", OWN_LINE)
def test_a_bare_history_header_on_its_own_line_stays_quiet(text):
    r = {"n": 1, "id": "r1", "source": "ER", "date_iso": "2026-01-09", "excerpt": text}
    assert "history_significant_for" not in {h["id"] for h in LS.scan(text, 2026)}, text
    assert [f for f in FL.lexicon_flags(r, 2026) if f["type"] == "pre_existing"] == [], text


@pytest.mark.parametrize("text,quote", [
    ("Patient seen in clinic\nPast history: significant for lumbar strain.", "Past history: significant for lumbar strain."),
    ("Chief complaint: neck pain\nMedical history: significant for diabetes.", "Medical history: significant for diabetes."),
])
def test_a_qualified_header_on_its_own_line_still_flags(text, quote):
    r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": text}
    pre = [f for f in FL.lexicon_flags(r, 2026) if f["type"] == "pre_existing"]
    assert len(pre) == 1 and pre[0]["excerpt"] == quote, pre


def test_with_a_newline_crossing_look_behind_the_own_line_header_flags(monkeypatch):
    # mutant: the 6fa8ecc guard (\s in the look-behind) lets the own-line header flag, so the test above would fail
    real = LS._entries()
    pat = next(e for e, _, _ in real if e["id"] == "history_significant_for")["pattern"]
    import re as _re
    mpat = pat.replace(r"(?<=[a-z][ \t]history)(?<!\band[ \t]history)", r"(?<=[a-z]\shistory)(?<!\band\shistory)")
    assert mpat != pat
    mut = tuple((e, _re.compile(mpat, _re.I | _re.M) if e["id"] == "history_significant_for" else rx, sup) for e, rx, sup in real)
    monkeypatch.setattr(LS, "_entries", lambda: mut)
    assert "history_significant_for" in {h["id"] for h in LS.scan(OWN_LINE[0], 2026)}
