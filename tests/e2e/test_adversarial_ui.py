"""T-045 AC3 (screen side of tests/e2e/test_adversarial.py): adversarial inputs typed or uploaded in the browser end in a clear state, and the LLM counter stays at 0 where required.

R-IN-4 (empty / oversize / non-English / pasted PDF text are refused with a plain sentence and one action), R-CO-5 (a refused input costs no model call and stores no case: the whole
database's llm_calls and cases counts do not move), R-RV-6 + D-005 (case_07's injected line never reaches the total: it stays $420.00 on screen and in the letter, and no flag is resolved).
Demo mode (D-020) refuses text that is not a recorded case before any storage, so non-English and pasted-PDF text are 409s here; the AC's wording 'end in clear states' is what is tested.
Needs ZLAYT_DB (the private server a plain run starts) to read the counters; E2E_REQUIRE_DB=1 makes a missing one a failure."""
import re
import sqlite3
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, golden_text, needs_db
import tests.e2e.conftest as C
from tests.e2e.test_adversarial import NON_ENGLISH, PDF_TEXT

BAD_TEXT = re.compile(r"\[object|\bundefined\b|\bNaN\b|Traceback")


def _counts():
    con = sqlite3.connect(needs_db())
    try:
        return tuple(con.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in ("llm_calls", "cases", "entries", "amounts", "flags"))
    finally:
        con.close()


@pytest.fixture
def pg(pw):
    b = pw.chromium.launch(); p = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    yield p
    b.close()


@pytest.mark.parametrize("what", ["empty", "whitespace", "oversize", "non_english", "pdf_text_with_page_headers"])
def test_refused_input_ends_in_a_clear_state_and_costs_nothing(pg, what):
    """Each bad input: a visible alert with a plain sentence and exactly one action, the paste box keeps its text (nothing lost), no case is created and the database's LLM-call count is
    exactly what it was (R-IN-4, R-CO-5)."""
    before = _counts(); n_cases = len(api("GET", "/api/cases")[1]["cases"])
    pg.goto(C.BASE); pg.get_by_test_id("input-text").wait_for(timeout=15000)
    mx = pg.evaluate("ZL.state.get().health.limits.max_chars")
    text = {"empty": "", "whitespace": "   \n \t  ", "oversize": "x" * (mx + 5), "non_english": NON_ENGLISH, "pdf_text_with_page_headers": PDF_TEXT}[what]
    if text:
        pg.get_by_test_id("input-text").fill(text)
    pg.get_by_test_id("btn-analyze").click()
    err = pg.get_by_test_id("error"); expect(err).to_be_visible(timeout=15000)
    msg = err.inner_text(); assert len(msg.strip()) > 20 and not BAD_TEXT.search(msg), msg
    expect(err.get_by_test_id("btn-error-action")).to_have_count(1)
    assert pg.get_by_role("alert").first.is_visible()
    assert pg.get_by_test_id("input-text").input_value() == text            # the paralegal's paste is still there to fix or move
    pg.wait_for_timeout(500)
    assert _counts() == before, f"a refused {what} input changed the database: {before} -> {_counts()}"
    assert len(api("GET", "/api/cases")[1]["cases"]) == n_cases


def test_case_07_injection_total_stays_420_on_screen_and_in_the_letter(pg):
    """R-RV-6 / D-005 through the browser: paste case_07, Analyze; the injection warning shows, no flag is pre-decided, the accepted total stays $420.00 after every amount is accepted,
    the letter's total line is the 'Billed charges accepted from these records' wording (D-062) at $420.00, and the injected $50,000 is nowhere in the letter."""
    pg.goto(C.BASE); pg.get_by_test_id("input-text").fill(golden_text("case_07_prompt_injection.txt")); pg.get_by_test_id("btn-analyze").click()
    pg.get_by_test_id("timeline").wait_for(timeout=120000)
    tok = re.search(r"#/case/([^/?#]+)", pg.url).group(1)
    try:
        assert "instruction" in pg.get_by_test_id("flags-panel").inner_text().lower()
        assert pg.locator("[data-review=accepted]").count() == 0 and pg.locator("[data-review=edited]").count() == 0
        c = api("GET", f"/api/cases/{tok}")[1]
        assert not [f for f in c["flags"] if f["review_status"] != "pending"]
        for a in c["amounts"]:
            if a["state"] != "rejected" and a["review_status"] == "pending":
                pg.locator(f'[data-item-id="{a["id"]}"]').first.get_by_test_id("btn-accept").click()
                expect(pg.locator(f'[data-item-id="{a["id"]}"]').first).to_have_attribute("data-review", "accepted")
        total = pg.get_by_test_id("accepted-total").inner_text(); assert "$420.00" in total and "50,000" not in total, total
        for e in c["entries"]:
            if e["state"] != "rejected" and e["review_status"] == "pending":
                pg.locator(f'[data-item-id="{e["id"]}"]').first.get_by_test_id("btn-accept").click()
        pg.get_by_test_id("btn-export").click(); expect(pg.get_by_test_id("export-letter")).to_be_visible(timeout=15000)
        letter = pg.get_by_test_id("export-letter").inner_text()
        assert "Billed charges accepted from these records: $420.00" in letter.split("\n") and "50,000" not in letter
    finally:
        api("DELETE", f"/api/cases/{tok}")
