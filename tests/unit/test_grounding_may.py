"""The month 'May' is not the hedge word 'may' (T-030 follow-up, found by backend-4)."""
import pytest
from app.backend import grounding as g


@pytest.mark.parametrize("excerpt", ["On May 18, 2026 the patient was seen for neck pain.", "May 29 MRI: C5-C6 disc protrusion.", "Seen in May 2026."])
def test_month_may_in_the_excerpt_is_not_a_qualifier(excerpt):
    assert g.hedge_ids(excerpt) == set()
    assert g.dropped_qualifiers("Seen for neck pain.", excerpt) == []


def test_modal_may_in_the_excerpt_is_a_qualifier():
    ex = "Findings may represent degenerative change."
    assert g.hedge_ids(ex) and g.dropped_qualifiers("Degenerative change was seen.", ex) == ["hedge"]


@pytest.mark.parametrize("summary", ["MRI on May 18, 2026 showed degenerative change.", "In May 2026 degenerative change was seen.", "May 29: degenerative change."])
def test_month_may_in_the_summary_does_not_carry_a_dropped_hedge(summary):
    """A summary that only mentions the month must still be flagged for dropping 'may represent'."""
    assert g.dropped_qualifiers(summary, "Findings may represent degenerative change.") == ["hedge"]


@pytest.mark.parametrize("summary", ["Findings may represent degenerative change.", "May represent degenerative change.", "Findings might be degenerative."])
def test_modal_may_in_the_summary_carries_the_hedge(summary):
    assert g.dropped_qualifiers(summary, "Findings may represent degenerative change.") == []
