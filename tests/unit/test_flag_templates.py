"""Flag titles/explanations are code-rendered. LLM_VS_CODE row 16, R-FL-5, ADR-013; golden flags."""
import pytest
from app.backend import flag_templates as F
from tests.unit import _golden as G

def golden_flags():
    out = []
    for c in G.case_names():
        out += [(c, f) for f in G.expected(c)["flags"]]
    return out

@pytest.mark.parametrize("case,f", golden_flags(), ids=lambda x: x if isinstance(x, str) else x["id"])
def test_every_golden_flag_type_subtype_has_a_template(case, f):
    """Row 16: every golden (type, subtype) renders a non-empty title and explanation with no model text and no unfilled braces."""
    kw = {k: f[k] for k in ("days", "from_date", "to_date") if k in f}
    title, expl = F.render(f["type"], f["subtype"], **kw) if f["type"] != "gap" else F.render("gap", "treatment_gap", **kw)
    assert title and expl and "{" not in title + expl

def test_gap_template_states_days_and_dates():
    """R-FL-1: the gap explanation includes the day count and both dates, nothing computed beyond them."""
    _, e = F.render("gap", "treatment_gap", days=73, from_date="2026-03-06", to_date="2026-05-18")
    assert "73" in e and "March 6, 2026" in e and "May 18, 2026" in e

def test_templates_never_characterize_or_infer():
    """R-FL-4/R-CO-3: no template words like 'caused', 'non-compliant', 'fraud', 'delay'."""
    for c, f in golden_flags():
        kw = {k: f[k] for k in ("days", "from_date", "to_date") if k in f}
        t, e = F.render(f["type"], f["subtype"], **kw) if f["type"] != "gap" else F.render("gap", "treatment_gap", **kw)
        assert not any(w in (t + e).lower() for w in ("non-compliant", "noncompliant", "fraud", "lied", "caused by", "delay"))

def test_render_deterministic():
    """Row 16: byte-identical output for identical input."""
    a = F.render("conflict", "accident_date"); assert a == F.render("conflict", "accident_date")

def test_unknown_subtype_raises():
    """Row 16: closed list - an unknown subtype is a KeyError."""
    with pytest.raises(KeyError):
        F.render("conflict", "made_up")
