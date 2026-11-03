"""T-174 MVP finish (designer round 2, reviews/MVP-ux-audit-r2.md): F8 the skip link and n go to the item "Do this first" names, F9 one open count on every surface, F13 a sticky section nav
and a Back to review control in Export, F14 leaving the sample preview creates no case, F15 every input error offers one action, F16 the 'Add a synthetic case' bar is a styled card that only
the overview shows, F20 the search box and the progress track use the tokens in dark mode, F21 a rate row gives one Not counted reason, N3 a placeholder keeps focus through a repaint.
New test ids (declared in tests/e2e/conftest.py, 'T-174'): section-nav, nav-overview, nav-timeline, nav-flags, nav-charges, nav-export, btn-back-to-review, btn-error-action, charge-detail.
Needs the fixture backend in local mode (a plain run starts its own)."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE, golden_text

TITLE = "Rivera v. Northgate (MVA 2026-01)"


@pytest.fixture
def rivera():
    st, c = api("POST", "/api/cases", {"sample": True, "title": TITLE}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")


def _page(pw, w, h, scheme="light"):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, permissions=["clipboard-read", "clipboard-write"])
    return b, ctx.new_page()


def _active_item(pg):
    return pg.evaluate("(() => { const a = document.activeElement, r = a && a.closest && a.closest('[data-item-id]'); return r ? r.getAttribute('data-item-id') : null; })()")


def _first_named(pg):
    box = pg.get_by_test_id("case-overview"); expect(box).to_have_attribute("data-do-first-item", re.compile(r".+"), timeout=15000)
    return box.get_attribute("data-do-first-item")


def _num(text, tail):
    m = re.search(r"(\d+)\s*" + tail, text); assert m, (text, tail)
    return int(m.group(1))


# ---- F8: one first item. The skip link and n go where Do this first goes.
def test_the_skip_link_and_n_go_to_the_item_do_this_first_names(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        first = _first_named(pg)
        entries = [i["id"] for i in api("GET", f"/api/cases/{rivera}")[1]["entries"]]
        assert first not in entries, "the sample case names a non-entry first, which is what makes the old 'top of the list' wrong"
        pg.get_by_test_id("skip-review").focus(); pg.keyboard.press("Enter")
        assert _active_item(pg) == first, (_active_item(pg), first)
        pg.get_by_test_id("entry-1").focus(); assert _active_item(pg) != first
        pg.keyboard.press("n")
        assert _active_item(pg) == first, (_active_item(pg), first)
        pg.get_by_test_id("btn-do-first").click(); assert _active_item(pg) == first
        # decide it: the line names a new item and n follows it
        pg.keyboard.press("a")
        expect(pg.get_by_test_id("case-overview")).not_to_have_attribute("data-do-first-item", first, timeout=15000)
        second = _first_named(pg)
        pg.get_by_test_id("entry-1").focus(); pg.keyboard.press("n")
        assert _active_item(pg) == second, (_active_item(pg), second)
    finally:
        b.close()


# ---- F9: one open count and one need-review count on every surface (hitl.needs_review_open is the server's own number)
def test_one_open_count_on_every_surface_with_an_edit_to_check(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        e1 = pg.get_by_test_id("entry-1"); e1.get_by_test_id("btn-accept").click(); expect(e1).to_have_attribute("data-review", "accepted")     # one accepted item: the export gate passes
        e = pg.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
        e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
        expect(e).to_have_attribute("data-review", "edited")
        m = re.match(r"(\d+) of (\d+) decided", pg.locator("#progress-text").inner_text()); assert m
        left = int(m.group(2)) - int(m.group(1)); needs = int(pg.locator("#progress-text").get_attribute("data-needs")); assert left > needs > 0
        pg.wait_for_timeout(1500)                                                                       # the list summary and the case checks refresh after the burst
        sm = next(c for c in api("GET", "/api/cases")[1]["cases"] if c["token"] == rivera)["hitl"]
        assert sm["needs_review_open"] == needs and sm["pending"] + sm["edits_to_check"] == left, (sm, needs, left)
        chip = pg.get_by_test_id("co-chip-can-export"); expect(chip).to_contain_text(f"{left} not reviewed", timeout=10000)
        expect(pg.get_by_test_id("need-review-count")).to_contain_text(f"{needs} ")
        assert _num(pg.get_by_test_id("case-verdict").text_content(), "not reviewed") == left
        assert _num(pg.get_by_test_id("case-summary-gate").inner_text(), "not reviewed") == left
        expect(pg.get_by_test_id("btn-start-review")).to_be_visible()
        # the list row says the same
        pg.get_by_test_id("btn-all-cases").click()
        row = pg.locator(f'[data-testid=cases-row][data-token="{rivera}"]'); expect(row).to_be_visible()
        expect(row.get_by_test_id("cases-chip-can-export")).to_contain_text(f"{left} not reviewed")
        expect(row.get_by_test_id("cases-chip-needs-review")).to_contain_text(f"{needs} ")
        # one name for one state: the filter is "Everything decided", the same words as the chip of a finished case
        expect(pg.get_by_test_id("cases-filter-ready")).to_contain_text("Everything decided")
        assert not re.search(r"Ready to send", pg.get_by_test_id("cases-overview").inner_text())
    finally:
        b.close()


# ---- F14: no ghost case
def _case_tokens():
    return {c["token"] for c in api("GET", "/api/cases")[1]["cases"]}


def test_backing_out_of_the_sample_preview_creates_no_case(pw):
    b, pg = _page(pw, 1440, 900)
    try:
        before = _case_tokens()
        pg.goto(BASE); pg.get_by_test_id("cases-list").wait_for(state="attached", timeout=15000)
        pg.get_by_test_id("btn-sample").click(); expect(pg.get_by_test_id("record-count")).to_be_visible(timeout=15000)
        pg.get_by_test_id("btn-all-cases").click()
        expect(pg.get_by_test_id("cases-overview")).to_be_visible()
        for _ in range(40):
            if _case_tokens() == before:
                break
            pg.wait_for_timeout(250)
        assert _case_tokens() == before, "the preview left a case behind"
        pg.wait_for_timeout(500)
        assert not any("sample preview" in (r or "").lower() for r in pg.get_by_test_id("cases-title").all_inner_texts())
        # Analyze keeps the case: it is real work from then on
        pg.get_by_test_id("btn-new-case").click(); pg.get_by_test_id("btn-sample").click(); expect(pg.get_by_test_id("record-count")).to_be_visible(timeout=15000)
        pg.get_by_test_id("btn-analyze").click(); expect(pg.get_by_test_id("timeline")).to_be_visible(timeout=60000)
        pg.get_by_test_id("btn-all-cases").click(); expect(pg.get_by_test_id("cases-overview")).to_be_visible(); pg.wait_for_timeout(1200)
        kept = _case_tokens() - before; assert len(kept) == 1, kept
        for t in kept:
            api("DELETE", f"/api/cases/{t}")
    finally:
        b.close()


# ---- F15: every error has one action
def _stub(pg, pattern, method, status, code, message):
    import json
    def h(route):
        if route.request.method == method:
            route.fulfill(status=status, content_type="application/json", body=json.dumps({"error": {"code": code, "message": message, "detail": {}}}))
        else:
            route.continue_()
    pg.route(pattern, h)


def test_a_failed_create_keeps_the_text_and_offers_try_again(pw):
    b, pg = _page(pw, 1440, 900)
    try:
        pg.goto(BASE); pg.get_by_test_id("input-text").wait_for()
        _stub(pg, "**/api/cases", "POST", 500, "internal", "Something went wrong. Try again.")
        text = golden_text("sample.txt")
        pg.get_by_test_id("input-text").fill(text); pg.get_by_test_id("btn-analyze").click()
        err = pg.get_by_test_id("error"); expect(err).to_be_visible(); expect(err).to_contain_text("Your text is still here")
        assert pg.get_by_test_id("input-text").input_value() == text
        expect(err.get_by_test_id("btn-error-action")).to_have_count(1); expect(err.get_by_test_id("btn-error-action")).to_have_text("Try again")
        pg.unroute_all(behavior="ignoreErrors")
        before = _case_tokens()
        err.get_by_test_id("btn-error-action").click(); expect(pg.get_by_test_id("record-count")).to_be_visible(timeout=15000)
        for t in _case_tokens() - before:
            api("DELETE", f"/api/cases/{t}")
    finally:
        b.close()


NOT_A_RECORDED_CASE = "=== Record 1 ===\nDate: 2026-01-09\nSource: Synthetic clinic note (SYNTHETIC)\nExcerpt: \"Patient seen for neck pain after a rear-end collision.\"\n"


def test_a_paste_the_demo_does_not_run_is_explained_with_real_actions(pw):
    """T-174 r2 F15: no stub. The real POST /api/cases refuses a paste that is not a recorded case (409 demo_mode_unsupported_input); the box then says so plainly and offers
    two things that work (open the sample, choose a library case) plus how to run live locally. No 'Edit the text' dead end."""
    b, pg = _page(pw, 1440, 900)
    try:
        pg.goto(BASE); pg.get_by_test_id("input-text").wait_for()
        before = _case_tokens()
        pg.get_by_test_id("input-text").fill(NOT_A_RECORDED_CASE); pg.get_by_test_id("btn-analyze").click()
        err = pg.get_by_test_id("error"); expect(err).to_contain_text("only runs", timeout=15000)
        expect(err).not_to_contain_text("Edit the text")
        expect(err.get_by_test_id("btn-error-action")).to_have_count(1); expect(err.get_by_test_id("btn-error-action")).to_have_text("Open the sample")
        expect(err.get_by_test_id("btn-error-library")).to_have_count(1); expect(err.get_by_test_id("btn-error-library")).to_have_text("Choose a library case")
        expect(err.get_by_test_id("error-live-note")).to_contain_text("ENABLE_LIVE=1")                                  # one line on how to run live locally
        assert _case_tokens() == before                                                                                  # the refusal created nothing
        err.get_by_test_id("btn-error-action").click()
        expect(pg.get_by_test_id("record-count")).to_contain_text("9 records", timeout=15000)                          # the sample's preview, ready to Analyze
        pg.get_by_test_id("btn-all-cases").click(); pg.wait_for_timeout(1500)
        for _ in range(40):
            if _case_tokens() == before:
                break
            pg.wait_for_timeout(250)
        assert _case_tokens() == before                                                                                  # and the preview is not left behind either
    finally:
        b.close()


def test_the_refused_paste_offers_the_library_by_keyboard(pw):
    b, pg = _page(pw, 390, 844)
    try:
        pg.goto(BASE); pg.get_by_test_id("input-text").wait_for()
        # the page decides whether to offer the library when the refusal is built, from the library list it has loaded by then; that list loads after first paint and is slow on a server
        # holding many cases, so wait for it before pasting (otherwise the refusal is built without the library button and the test races the page)
        pg.locator("[data-testid=library-list] button").first.wait_for(state="attached", timeout=30000)
        pg.get_by_test_id("input-text").fill(NOT_A_RECORDED_CASE); pg.get_by_test_id("btn-analyze").click()
        err = pg.get_by_test_id("error"); expect(err.get_by_test_id("btn-error-library")).to_be_visible(timeout=15000)
        for t in ("btn-error-action", "btn-error-library"):
            bb = err.get_by_test_id(t).bounding_box(); assert bb["x"] >= 0 and bb["x"] + bb["width"] <= 390, (t, bb)
        err.get_by_test_id("btn-error-library").focus(); pg.keyboard.press("Enter")
        expect(pg.get_by_test_id("library-list")).to_be_visible()                                                         # the 'Add a synthetic case' group is open
        assert pg.evaluate("!!document.activeElement.closest('[data-testid=library-list]')")                             # focus is on the first library case
    finally:
        b.close()


def test_leaving_by_reload_or_back_from_the_sample_preview_leaves_no_case(pw):
    """T-174 r2 F14: closing the page, reloading it or going Back out of the preview deletes the preview, like All cases does."""
    b, pg = _page(pw, 1440, 900)
    try:
        before = _case_tokens()
        for how in ("reload", "back"):
            pg.goto(BASE); pg.get_by_test_id("btn-sample").wait_for()
            if how == "back":
                pg.goto("about:blank"); pg.goto(BASE); pg.get_by_test_id("btn-sample").wait_for()
            pg.get_by_test_id("btn-sample").click(); expect(pg.get_by_test_id("record-count")).to_be_visible(timeout=15000)
            assert len(_case_tokens() - before) == 1
            if how == "reload":
                pg.reload()
            else:
                pg.go_back()
            for _ in range(40):
                if _case_tokens() == before:
                    break
                pg.wait_for_timeout(250)
            assert _case_tokens() == before, how
            pg.goto(BASE); pg.get_by_test_id("btn-sample").wait_for()
            assert pg.get_by_test_id("input-text").is_visible()                                                           # a reload lands on the empty form, not on a missing case
    finally:
        b.close()


def test_a_failed_run_start_offers_try_again(pw):
    b, pg = _page(pw, 1440, 900)
    try:
        pg.goto(BASE); pg.get_by_test_id("btn-sample").wait_for()
        before = _case_tokens()
        pg.get_by_test_id("btn-sample").click(); expect(pg.get_by_test_id("record-count")).to_be_visible(timeout=15000)
        _stub(pg, "**/api/cases/*/run", "POST", 500, "internal", "Something went wrong. Try again.")
        pg.get_by_test_id("btn-analyze").click()
        err = pg.get_by_test_id("error"); expect(err.get_by_test_id("btn-error-action")).to_have_text("Try again", timeout=15000)
        assert "Try again" not in err.locator(".error-text").inner_text()                                                   # the button says it once; the sentence does not repeat it
        pg.unroute_all(behavior="ignoreErrors")
        err.get_by_test_id("btn-error-action").click(); expect(pg.get_by_test_id("timeline")).to_be_visible(timeout=60000)
        pg.get_by_test_id("btn-all-cases").click(); pg.wait_for_timeout(1200)
        for t in _case_tokens() - before:
            api("DELETE", f"/api/cases/{t}")
    finally:
        b.close()


@pytest.mark.parametrize("what", ["empty", "toolong", "pdf"])
def test_the_other_input_errors_each_offer_one_action(pw, what, tmp_path):
    b, pg = _page(pw, 1440, 900)
    try:
        pg.goto(BASE); pg.get_by_test_id("input-text").wait_for()
        if what == "empty":
            pg.get_by_test_id("btn-analyze").click(); label = "Use the sample case"
        elif what == "toolong":
            mx = pg.evaluate("ZL.state.get().health.limits.max_chars")
            pg.get_by_test_id("input-text").fill("x" * (mx + 5)); pg.get_by_test_id("btn-analyze").click(); label = "Edit the text"
        else:
            f = tmp_path / "records.pdf"; f.write_bytes(b"%PDF-1.4 synthetic"); pg.get_by_test_id("file-input").set_input_files(str(f)); label = "Choose a .txt file"
        err = pg.get_by_test_id("error"); expect(err).to_be_visible()
        expect(err.get_by_test_id("btn-error-action")).to_have_count(1); expect(err.get_by_test_id("btn-error-action")).to_have_text(label)
    finally:
        b.close()


# ---- F16 / F20
def test_the_synthetic_case_bar_is_a_styled_card_on_the_overview_only(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        pg.goto(BASE); sw = pg.get_by_test_id("case-switcher"); expect(sw).to_be_visible(timeout=15000)
        m = pg.evaluate("""(() => { const s = document.querySelector('#case-switcher summary'), c = document.querySelector('#case-switcher'), cs = getComputedStyle(s), cc = getComputedStyle(c);
          return { pl: parseFloat(cs.paddingLeft), pt: parseFloat(cs.paddingTop), h: s.getBoundingClientRect().height, border: cc.borderTopWidth, radius: cc.borderTopLeftRadius, cursor: cs.cursor }; })()""")
        assert m["pl"] >= 12 and m["pt"] >= 8 and m["h"] >= 40 and m["border"] != "0px" and m["cursor"] == "pointer", m
        open_case(pg, rivera)
        expect(pg.get_by_test_id("case-switcher")).to_be_hidden()
        pg.get_by_test_id("btn-all-cases").click(); expect(pg.get_by_test_id("case-switcher")).to_be_visible()
    finally:
        b.close()


def test_dark_mode_search_and_progress_track_use_the_tokens(pw, rivera):
    b, pg = _page(pw, 1440, 900, "dark")
    try:
        pg.goto(BASE); expect(pg.get_by_test_id("cases-search")).to_be_visible(timeout=15000); pg.get_by_test_id("cases-row").first.wait_for()
        m = pg.evaluate("""(() => { const bg = (s) => getComputedStyle(document.querySelector(s)).backgroundColor, panel = getComputedStyle(document.querySelector('.card')).backgroundColor;
          const lum = (c) => { const v = c.match(/[\\d.]+/g).slice(0, 3).map(Number).map((x) => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
          const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
          const p = document.querySelector('.cv-row progress'), ps = getComputedStyle(p);
          return { search: bg('[data-testid=cases-search]'), sort: bg('[data-testid=cases-sort]'), title: bg('#case-title'), panel, track: ps.borderTopColor, trackW: ps.borderTopWidth, trackRatio: ratio(ps.borderTopColor, panel) }; })()""")
        assert m["search"] == m["sort"] == m["title"], m
        assert m["trackW"] != "0px" and m["trackRatio"] >= 3, m
    finally:
        b.close()


# ---- F21
def test_a_rate_row_gives_one_not_counted_reason(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        row = pg.locator("[data-testid=charges-panel] [data-amount-kind=rate]").first; row.scroll_into_view_if_needed()
        cell = row.locator("td.rv-c-status")
        assert len(re.findall(r"Not counted", cell.inner_text())) == 1, cell.inner_text()
        expect(cell.get_by_test_id("not-counted-reason")).to_have_count(1)
        row.get_by_test_id("btn-more").click()                                                          # the code's detail (rate, unit, what is missing) waits behind More
        expect(row.get_by_test_id("charge-detail")).to_contain_text("not stated")
    finally:
        b.close()


# ---- F13: section nav + a way back from Export
@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_the_section_nav_reaches_every_section_from_any_scroll_position(pw, rivera, w, h):
    b, pg = _page(pw, w, h)
    try:
        open_case(pg, rivera)
        nav = pg.get_by_test_id("section-nav"); bar = nav.locator(".section-nav-bar")
        assert nav.bounding_box()["height"] == 0, "the nav takes no room in the page flow, so the first screen keeps its budget"
        pg.evaluate("window.scrollTo(0, 600)"); pg.wait_for_timeout(200); expect(bar).to_be_visible()      # it shows once she has scrolled past the first screen
        assert pg.evaluate("document.documentElement.scrollWidth <= innerWidth"), "no horizontal scroll"
        for tid, sel in (("nav-flags", "#rv-flags-h"), ("nav-charges", "#rv-charges-h"), ("nav-timeline", "#h-timeline"), ("nav-overview", "#co-h")):
            pg.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)"); pg.wait_for_timeout(200)
            nb = bar.bounding_box(); assert nb["y"] >= 0 and nb["y"] < 140, nb                           # sticky: it is still on screen at the bottom of the page
            btn = nav.get_by_test_id(tid); btn.click(); pg.wait_for_timeout(500)
            r = pg.evaluate(f"(() => {{ const t = document.querySelector('{sel}').getBoundingClientRect(), n = document.querySelector('.section-nav-bar').getBoundingClientRect(); return {{ top: t.top, navBottom: n.bottom, h: innerHeight }}; }})()")
            assert r["top"] >= r["navBottom"] - 2 and r["top"] < r["h"] * 0.6, (tid, r)                  # the section starts right under the sticky chrome
            assert pg.evaluate(f"document.querySelector('{sel}') === document.activeElement"), tid                # focus is on the section's heading
            expect(btn).to_have_attribute("aria-current", "location")
        # counts: what is still open in the section
        for tid, key in (("nav-flags", "flags"), ("nav-charges", "amounts")):
            n = pg.evaluate(f"ZL.state.get().case.{key}.filter((i) => i.state !== 'rejected' && ZL.undecided(i)).length")
            assert n > 0 and re.search(rf"(?<!\d){n}(?!\d)", nav.get_by_test_id(tid).text_content()), (tid, n, nav.get_by_test_id(tid).text_content())
        if w < 700:
            for tid in ("nav-overview", "nav-timeline", "nav-flags", "nav-charges", "nav-export"):
                assert nav.get_by_test_id(tid).bounding_box()["height"] >= 43, tid
    finally:
        b.close()


def test_export_offers_back_to_review_as_its_first_control(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        e1 = pg.get_by_test_id("entry-1"); e1.get_by_test_id("btn-accept").click(); expect(e1).to_have_attribute("data-review", "accepted")     # one accepted item: Export opens
        row = pg.get_by_test_id("entry-4"); rid = row.get_attribute("data-item-id"); row.scroll_into_view_if_needed(); row.focus()
        pg.get_by_test_id("section-nav").get_by_test_id("nav-export").click()
        ex = pg.locator("#view-export"); expect(ex).to_be_visible(timeout=15000)
        first = pg.evaluate("(() => { const f = document.querySelector('#export-body').querySelector('button, a[href], input, [tabindex=\"0\"]'); return f && f.getAttribute('data-testid'); })()")
        assert first == "btn-back-to-review", first
        expect(pg.get_by_test_id("btn-back-to-review")).to_be_visible()
        pg.get_by_test_id("btn-back-to-review").click()
        expect(ex).to_be_hidden()
        assert _active_item(pg) == rid, (_active_item(pg), rid)                                         # she is back on the row she left, on screen
        f = pg.evaluate("(() => { const r = document.activeElement.getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight; })()"); assert f
        pg.get_by_test_id("btn-export").click(); expect(ex).to_be_visible(timeout=15000)               # Export again from the header; Back works the same
        pg.get_by_test_id("btn-back-to-review").click(); expect(ex).to_be_hidden()
    finally:
        b.close()


# ---- N3: a dismiss placeholder keeps focus through a repaint (the cause of the 1-in-2 failure of the charge-dismiss spec)
def test_the_placeholder_keeps_focus_when_the_panels_repaint(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        ch = pg.locator("[data-testid=charges-panel] [data-amount-kind=charge]").first; cid = ch.get_attribute("data-item-id")
        ch.scroll_into_view_if_needed(); ch.get_by_test_id("btn-dismiss").click()
        g = pg.locator(f'[data-testid=charges-panel] tbody [data-ghost-for="{cid}"]'); expect(g).to_be_visible()
        expect(g.get_by_test_id("btn-undo-dismiss")).to_be_focused()
        for _ in range(3):
            pg.evaluate("document.dispatchEvent(new CustomEvent('zl:panels'))"); pg.wait_for_timeout(120)
            expect(pg.locator(f'[data-ghost-for="{cid}"]').get_by_test_id("btn-undo-dismiss")).to_be_focused()
        f = pg.evaluate("(() => { const r = document.activeElement.getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight; })()"); assert f
    finally:
        b.close()


# ---- F15 (orchestrator): a failed case list says so in plain words and offers one Retry
def test_a_failed_case_list_shows_a_plain_message_and_a_retry_button(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        _stub(pg, "**/api/cases", "GET", 500, "internal", "boom")
        pg.goto(BASE)
        err = pg.get_by_test_id("cases-load-error"); expect(err).to_be_visible(timeout=15000)
        txt = err.inner_text(); assert "could not load your cases" in txt and not re.search(r"500|HTTP|boom|fetch", txt, re.I), txt
        expect(err.get_by_role("button")).to_have_count(1); expect(pg.get_by_test_id("cases-retry")).to_have_text("Try again")
        assert pg.get_by_test_id("cases-row").count() == 0
        pg.unroute_all(behavior="ignoreErrors")
        pg.get_by_test_id("cases-retry").click()
        expect(pg.get_by_test_id("cases-row").first).to_be_visible(timeout=15000); expect(err).to_be_hidden()
        # the same when the list fails after the page was already showing it (a refresh behind the scenes keeps the rows; the next visit to the overview offers Try again)
    finally:
        b.close()


# ---- T-175 r2: a row with status_error shows the server's message and Try again, never zeros or Can export
def test_a_status_error_row_shows_the_message_and_try_again_and_no_figures(pw, rivera):
    import json
    b, pg = _page(pw, 1440, 900)
    try:
        def h(route):
            if route.request.method != "GET":
                return route.continue_()
            r = route.fetch(); body = r.json()
            for c in body["cases"]:
                if c["token"] == rivera:
                    c.update(record_count=None, counts=None, progress=None, hitl=None, export_ready=False, next_action=None, status_error=True, status_error_message="We couldn't load this case's status")
            route.fulfill(response=r, body=json.dumps(body))
        pg.route("**/api/cases", h)
        pg.goto(BASE)
        row = pg.locator(f'[data-testid=cases-row][data-token="{rivera}"]'); expect(row).to_be_visible(timeout=15000)
        expect(row.get_by_test_id("cases-status-error")).to_contain_text("We couldn't load this case's status")
        expect(row.get_by_test_id("cases-status-retry")).to_have_text("Try again")
        txt = row.inner_text(); assert not re.search(r"Can export|Everything decided|0 of|need review|Analysis done", txt), txt
        assert row.locator("progress").count() == 0
        pg.unroute_all(behavior="ignoreErrors")
        row.get_by_test_id("cases-status-retry").click()
        expect(row.get_by_test_id("cases-status-error")).to_have_count(0, timeout=10000); expect(row.get_by_test_id("cases-decided")).to_be_visible()
    finally:
        b.close()


# ---- T-174 r2: a counted line reads as her own decision, not a warning
LIB11 = "case_lib11_priors_and_ledger"


@pytest.fixture
def lib11():
    st, c = api("POST", "/api/cases", {"library": LIB11})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_a_counted_line_says_counted_by_you_once_with_no_warning(pw, lib11, w, h):
    b, pg = _page(pw, w, h)
    try:
        a = next(x for x in api("GET", f"/api/cases/{lib11}")[1]["amounts"] if x["text"] == "$250.00")
        open_case(pg, lib11)
        row = pg.get_by_test_id("charges-panel").locator(f'[data-item-id="{a["id"]}"]').first; row.scroll_into_view_if_needed()
        row.get_by_test_id("btn-count-charge").click()
        dlg = pg.get_by_test_id("count-confirm"); expect(dlg).to_be_visible(); dlg.get_by_test_id("btn-count-confirm").click()
        row = pg.get_by_test_id("charges-panel").locator(f'[data-item-id="{a["id"]}"]').first
        expect(row).to_have_attribute("data-amount-kind", "charge"); expect(row).to_have_attribute("data-review", "accepted")
        status = row.locator("td.rv-c-status")
        chip = status.get_by_test_id("counted-by-you"); expect(chip).to_have_count(1); expect(chip).to_have_text("Counted by you")
        assert status.locator(".chip--warn").count() == 0 and status.locator(".rv-reason-line").count() == 0              # no amber box
        text = status.inner_text()
        assert "flag" not in text.lower(), text                                                                           # she was shown no flag
        assert len(re.findall(r"confirm", text, re.I)) == 1, text                                                          # her confirm, said once
        assert "You counted this line" not in text, text                                                                   # the server's longer sentence is not repeated beside it
        cell = status.bounding_box()
        for c in status.locator(".chip").all():
            bb = c.bounding_box(); assert bb["x"] + bb["width"] <= cell["x"] + cell["width"] + 0.5, (bb, cell)              # every chip fits its cell
        # a new case view (reload) reads the same
        open_case(pg, lib11)
        row = pg.get_by_test_id("charges-panel").locator(f'[data-item-id="{a["id"]}"]').first
        expect(row.get_by_test_id("counted-by-you")).to_have_text("Counted by you")
    finally:
        b.close()
