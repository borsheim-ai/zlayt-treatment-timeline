"""Running total of accepted charges. R-CH-3, R-EX-8 (D-019), LLM_VS_CODE row 8; golden totals."""
import pytest
from app.backend import totals as T

def amt(cents, cls="charge", status="accepted"):
    return dict(cents=cents, cls=cls, review_status=status)

def test_sample_accepted_total_is_8390():
    """R-CH-3: ER $6,240 + MRI $2,150 accepted = 839000 cents; the $185 rate is not added."""
    t = T.totals([amt(624000), amt(215000), amt(18500, "rate", "accepted")])
    assert t["accepted_cents"] == 839000

def test_dismissing_er_charge_drops_to_2150():
    """R-CH-3: dismissed charges leave the total."""
    assert T.totals([amt(624000, status="dismissed"), amt(215000)])["accepted_cents"] == 215000

def test_pending_detected_is_separate_and_not_a_total():
    """R-CH-3: 'Detected, not yet accepted' is reported apart from accepted."""
    t = T.totals([amt(624000, status="pending"), amt(215000)])
    assert t["accepted_cents"] == 215000 and t["detected_pending_cents"] == 624000

@pytest.mark.parametrize("cls", ["rate", "estimate", "damages", "unclear"])
def test_only_charge_class_counts(cls):
    """R-CH-3: rate/estimate/damages/unclear never add, even if accepted."""
    assert T.totals([amt(10000, cls)])["accepted_cents"] == 0

def test_edited_status_counts():
    """R-EX-1: accepted and edited items count; pending and dismissed do not."""
    assert T.totals([amt(100, status="edited")])["accepted_cents"] == 100

def test_unclear_items_listed_not_totaled():
    """R-CH-3 / row 8: non-charge accepted amounts appear in unclear_items."""
    assert len(T.totals([amt(18500, "rate")])["unclear_items"]) == 1

def test_integer_cents_no_float_drift():
    """Row 8: money is whole cents; 0.1+0.2 style drift is impossible."""
    assert T.totals([amt(10), amt(20)])["accepted_cents"] == 30 and isinstance(T.totals([amt(10)])["accepted_cents"], int)
