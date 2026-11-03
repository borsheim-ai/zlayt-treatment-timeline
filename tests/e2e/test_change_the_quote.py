"""T-108: "Change the quote" completes end to end on the sample, against the REAL backend (needs ZLAYT_DB, the SQLite file of the server under test, to put
a bad quote into the store the way a stale or imported state would). The picker's sentence units carry no `Excerpt: "` wrapper, no quote marks and no header
lines, so picking whole sentences rebuilds a quote the save route accepts; the refused Accept is lifted by it.
No new test ids: btn-accept, accept-refused, btn-accept-refused-quote, excerpt-editor, excerpt-unit, btn-save-excerpt, excerpt-error (all declared in conftest)."""
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case
from tests.e2e.test_code_check_refusal import _break_quote, _entry, row_of


def _entry_with_a_picker(tok):
    c = api("GET", f"/api/cases/{tok}")[1]
    recs = {r["id"]: r for r in c["records"]}
    for e in c["entries"]:
        r = recs[e["record_ids"][0]]
        if e["state"] == "verified" and e["date"] and e["review_status"] == "pending" and len(e["record_ids"]) == 1 and len(r["sentences"]) >= 2:
            return e, r
    pytest.fail("no entry with a quote picker on the sample")


def test_sample_units_carry_no_wrapper_and_rebuild_every_entry_quote(sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    recs = {r["id"]: r for r in c["records"]}
    raw_of = lambda r, s: r["text"][s["start"] - r["char_start"]:s["end"] - r["char_start"]]
    for r in c["records"]:
        for s in r["sentences"]:
            assert s["text"] == raw_of(r, s) and not s["text"].startswith(("Excerpt", "Date:", "Source:", "===")) and '"' not in s["text"], s["text"]
    for e in c["entries"] + c["undated_entries"]:
        if len(e["record_ids"]) != 1:
            continue
        r = recs[e["record_ids"][0]]
        run = [s for s in r["sentences"] if s["start"] >= e["excerpt_start"] and s["end"] <= e["excerpt_end"]]
        assert run and r["text"][run[0]["start"] - r["char_start"]:run[-1]["end"] - r["char_start"]] == e["excerpt"], "the units rebuild the AI's own quote"


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_change_the_quote_saves_and_lifts_the_refusal(pw, sample_case, w, h):
    e, rec = _entry_with_a_picker(sample_case)
    orig = e["excerpt"]
    _break_quote(sample_case, e["id"])
    assert _entry(sample_case, e["id"])["excerpt"] != orig
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        open_case(pg, sample_case); row = row_of(pg, e["id"]); row.scroll_into_view_if_needed()
        row.get_by_test_id("btn-accept").click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        box.get_by_test_id("btn-accept-refused-quote").click()
        ed = row.get_by_test_id("excerpt-editor"); expect(ed).to_be_visible()
        units = ed.get_by_test_id("excerpt-unit")
        texts = [t.strip() for t in ed.locator("li").all_inner_texts()]
        assert texts and all(not t.startswith(("Excerpt", "Date:", "Source:")) and '"' not in t for t in texts), texts
        # pick the sentences that make up the original quote (the picker preselects the stored span; the broken quote started mid-sentence, so it is the whole-sentence run)
        want = [s["text"] for s in rec["sentences"] if s["start"] >= e["excerpt_start"] and s["end"] <= e["excerpt_end"]]
        for i in range(units.count()):
            on = texts[i] in want
            if units.nth(i).is_checked() != on:
                units.nth(i).click()
        ed.get_by_test_id("btn-save-excerpt").click()
        expect(ed.get_by_test_id("excerpt-error")).to_be_hidden()
        for _ in range(40):
            if _entry(sample_case, e["id"])["excerpt"] == orig:
                break
            pg.wait_for_timeout(250)
        got = _entry(sample_case, e["id"])
        assert got["excerpt"] == orig and got["review_status"] == "edited", (got["excerpt"], got["review_status"])
        # the saved quote passes the code checks again: the item can now be accepted without a CODE_CHECK_FAILED refusal
        st, body = api("POST", f"/api/cases/{sample_case}/items/{e['id']}/review", {"action": "accept"})
        assert st == 200, (st, body)
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()
