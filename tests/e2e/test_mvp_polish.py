"""T-166 MVP polish (frontend half of the UX audit, reviews/MVP-ux-audit.md): F2 one-row header that never covers the source pane, F3 excerpts and charge quotes never clipped,
F4 Save and accept, F5 a dismissed row leaves a six-second placeholder and focus stays on screen, F6 the keyboard loop moves on (a, d, n, x), F7 no test or developer wording and no Audit link
on a row, and the P1s that are frontend only: F9 one open count in the live message, F10 'all agreed' only when it is true, F11 at most five visible controls per row, F12 Undo asks before
it throws her wording away.
New test ids (declared in tests/e2e/conftest.py, 'T-166'): dismiss-ghost, btn-undo-dismiss, btn-show-excerpt, btn-save-accept, discard-confirm, btn-discard-edit, btn-keep-edit, btn-more,
entry-more-panel, flag-more-panel, charge-more-panel, charge-quote. Needs the fixture backend (a plain run starts its own)."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

TITLE = "Rivera v. Northgate (MVA 2026-01)"
BAD_WORDS = re.compile(r"fixture|golden|prompt|JUDGE_|FIXTURE_|server answered|Request failed|cached demo|curated", re.I)


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


def _page(pw, w, h):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, permissions=["clipboard-read", "clipboard-write"])
    return b, ctx.new_page()


def _decided(page):
    m = re.match(r"(\d+) of (\d+) decided", page.locator("#progress-text").inner_text()); assert m
    return int(m.group(1)), int(m.group(2))


def _in_view(page):
    return page.evaluate("""(() => { const a = document.activeElement; if (!a || a === document.body) return null; const r = a.getBoundingClientRect();
      return { top: r.top, bottom: r.bottom, h: innerHeight, ok: r.top >= 0 && r.bottom <= innerHeight && r.height > 0, tag: a.tagName, tid: a.getAttribute('data-testid') }; })()""")


# ---- F2: one row header, the source pane starts below it
@pytest.mark.parametrize("scroll", [0, 2000])
def test_header_is_one_row_and_the_source_pane_starts_below_it(pw, rivera, scroll):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        e = pg.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
        e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
        expect(e).to_have_attribute("data-review", "edited")      # an edit to check makes the progress line its longest
        pg.evaluate(f"window.scrollTo(0, {scroll})"); pg.wait_for_timeout(300)
        m = pg.evaluate("""(() => { const h = document.querySelector('.app-header').getBoundingClientRect(), p = document.querySelector('.sbs-pane'), pr = p && p.getBoundingClientRect(),
          name = document.querySelector('#case-name'), tools = document.querySelector('.header-tools').getBoundingClientRect();
          return { hh: h.height, hb: h.bottom, pane: pr && getComputedStyle(p).display !== 'none' ? pr.top : null, sw: document.documentElement.scrollWidth, name: name.textContent, toolsTop: tools.top, headTop: h.top }; })()""")
        assert m["hh"] <= 60, m
        assert m["pane"] is not None and m["pane"] >= m["hb"] + 8 - 1, m
        assert m["sw"] <= 1440 and m["name"] == TITLE, m
        assert m["toolsTop"] < m["hb"] - 10, m                       # Export and the other tools are on the same row, not dropped under the name
    finally:
        b.close()


def test_header_fits_on_a_phone_and_names_the_case(pw, rivera):
    b, pg = _page(pw, 390, 844)
    try:
        open_case(pg, rivera)
        assert pg.evaluate("document.documentElement.scrollWidth") <= 391
        expect(pg.get_by_test_id("case-name")).to_have_attribute("title", TITLE)
        expect(pg.get_by_test_id("btn-export")).to_be_visible()
    finally:
        b.close()


# ---- F3: nothing is clipped while a row needs a decision, and a charge row always shows its own amount
@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_charge_quotes_and_pending_excerpts_are_not_clipped(pw, rivera, w, h):
    b, pg = _page(pw, w, h)
    try:
        open_case(pg, rivera)
        quotes = pg.locator("[data-testid=charge-quote]"); assert quotes.count() >= 3
        bad = quotes.evaluate_all("els => els.filter(e => e.scrollHeight > e.clientHeight + 1 || !e.querySelector('mark')).map(e => e.textContent)")
        assert not bad, bad
        row = pg.locator('[data-testid="amount-$2,150"]').first
        assert "$2,150" in row.locator("[data-testid=charge-quote] mark").first.inner_text()
        assert row.locator("[data-testid=charge-quote]").evaluate("e => e.scrollHeight <= e.clientHeight + 1")
        clipped = pg.locator('.entry[data-entry-id][data-review="pending"] .excerpt').evaluate_all("els => els.filter(e => e.scrollHeight > e.clientHeight + 1).map(e => e.textContent)")
        assert not clipped, clipped
        assert pg.locator('[data-testid=charge-quote]').evaluate_all("els => els.filter(e => /^\\u2026|\\u2026$/.test(e.textContent.trim())).length") == 0   # no ellipsis added by the page
    finally:
        b.close()


def test_a_decided_row_shows_one_line_and_a_button_under_the_quote_that_shows_the_rest(page, rivera):
    open_case(page, rivera)
    row = page.get_by_test_id("entry-1"); row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
    more = row.get_by_test_id("btn-show-excerpt"); expect(more).to_be_visible()
    ex = row.get_by_test_id("entry-excerpt"); eb, mb = ex.bounding_box(), more.bounding_box()
    assert mb["y"] >= eb["y"] + eb["height"] - 1, (eb, mb)                       # directly under the quote
    more.click(); expect(more).to_have_text("Show less")
    assert ex.evaluate("e => e.scrollHeight <= e.clientHeight + 1")
    page.get_by_test_id("entry-2").get_by_test_id("btn-accept").click()
    expect(page.get_by_test_id("entry-2").get_by_test_id("btn-show-excerpt")).to_be_visible()
    expect(page.get_by_test_id("entry-4").get_by_test_id("btn-show-excerpt")).to_be_hidden()   # an undecided row already shows its whole quote


# ---- F4: edit, then one button saves and accepts; the whole quote is on screen next to the edit
def test_edit_shows_the_whole_quote_and_save_and_accept_is_one_click(page, rivera):
    open_case(page, rivera)
    e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted.")
    expect(e.get_by_test_id("btn-save-accept")).to_be_visible()
    assert e.get_by_test_id("entry-excerpt").evaluate("x => x.scrollHeight <= x.clientHeight + 1")
    e.get_by_test_id("btn-save-accept").click()
    expect(e).to_have_attribute("data-review", re.compile("accepted|edited"))
    expect(e).not_to_have_attribute("data-edit-check", re.compile(".*"))               # nothing left to compare: one click did both
    assert "Persistent neck pain 6/10 with daily headaches noted." in e.get_by_test_id("entry-summary").inner_text()


def test_plain_save_still_leaves_the_edit_to_compare(page, rivera):
    open_case(page, rivera)
    e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited")
    if e.get_attribute("data-edit-check") is not None:                                    # the fixture backend has no second check: she still has to say she compared it
        expect(e.get_by_test_id("btn-accept")).to_contain_text("I compared it with the quote")
        assert e.get_by_test_id("entry-excerpt").evaluate("x => x.scrollHeight <= x.clientHeight + 1")


# ---- F5: dismiss leaves a placeholder in the row's slot and focus never leaves the screen
@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_pointer_dismiss_leaves_an_undo_placeholder_in_place(pw, rivera, w, h):
    b, pg = _page(pw, w, h)
    try:
        open_case(pg, rivera)
        ids = pg.locator("[data-testid=queue] > article").evaluate_all("els => els.map(e => e.getAttribute('data-item-id'))")
        row = pg.get_by_test_id("entry-5"); rid = row.get_attribute("data-item-id"); at = ids.index(rid)
        row.scroll_into_view_if_needed(); row.get_by_test_id("btn-dismiss").click()
        ghost = pg.locator(f'[data-ghost-for="{rid}"]'); expect(ghost).to_be_visible(); expect(ghost).to_contain_text("Dismissed")
        after = pg.locator("[data-testid=queue] > *").evaluate_all("els => els.map(e => e.getAttribute('data-item-id') || (e.hasAttribute('data-ghost-for') ? 'GHOST' : null))")
        assert after[at] == "GHOST" and after[at - 1] == ids[at - 1] and after[at + 1] == ids[at + 1], (ids, after)    # in the row's own slot
        pg.wait_for_timeout(300)
        f = _in_view(pg); assert f and f["ok"] and f["tid"] == "btn-undo-dismiss", f
        ghost.get_by_test_id("btn-undo-dismiss").click()
        expect(ghost).to_have_count(0)
        back = pg.locator("[data-testid=queue] > article").evaluate_all("els => els.map(e => e.getAttribute('data-item-id'))")
        assert back == ids                                                                                  # Undo restores the row where it was
        expect(pg.locator(f'[data-testid=queue] [data-item-id="{rid}"]')).to_have_attribute("data-review", "pending")
    finally:
        b.close()


def test_the_placeholder_collapses_into_the_dismissed_group_after_six_seconds(page, rivera):
    open_case(page, rivera)
    row = page.get_by_test_id("entry-5"); rid = row.get_attribute("data-item-id"); row.get_by_test_id("btn-dismiss").click()
    expect(page.locator(f'[data-ghost-for="{rid}"]')).to_be_visible()
    page.wait_for_timeout(5000); expect(page.locator(f'[data-ghost-for="{rid}"]')).to_be_visible()      # still there at 5 s
    expect(page.locator(f'[data-ghost-for="{rid}"]')).to_have_count(0, timeout=3500)                    # gone by 6 s
    expect(page.locator(f'[data-testid=dismissed-queue] [data-item-id="{rid}"]')).to_have_count(1)
    f = _in_view(page)
    assert f is None or f["ok"], f                                                                         # a focus lost with the placeholder lands on screen or on the page, never below the fold


def test_keyboard_dismiss_moves_to_the_next_item_on_screen_and_keeps_a_placeholder(page, rivera):
    open_case(page, rivera)
    row = page.get_by_test_id("entry-5"); rid = row.get_attribute("data-item-id"); row.scroll_into_view_if_needed(); row.focus()
    page.keyboard.press("d")
    expect(page.locator(f'[data-ghost-for="{rid}"]')).to_be_visible()
    page.wait_for_timeout(300)
    f = _in_view(page); assert f and f["ok"], f
    assert page.evaluate("(() => { const a = document.activeElement; return !!a.closest('[data-item-id]') && a.closest('[data-item-id]').getAttribute('data-item-id') !== '%s'; })()" % rid)


def test_dismissing_a_flag_and_a_charge_leaves_a_placeholder_in_their_panels(page, rivera):
    open_case(page, rivera)
    flag = page.locator("[data-testid=flags-panel] [data-flag-type=conflict]").first; fid = flag.get_attribute("data-item-id")
    flag.scroll_into_view_if_needed(); flag.get_by_test_id("btn-dismiss").click()
    g = page.locator(f'[data-testid=flags-panel] [data-ghost-for="{fid}"]'); expect(g).to_be_visible(); expect(g).to_contain_text("Dismissed")
    expect(g.get_by_test_id("btn-undo-dismiss")).to_be_focused()
    f = _in_view(page); assert f and f["ok"], f
    ch = page.locator("[data-testid=charges-panel] [data-amount-kind=charge]").first; cid = ch.get_attribute("data-item-id")
    ch.scroll_into_view_if_needed(); ch.get_by_test_id("btn-dismiss").click()
    g2 = page.locator(f'[data-testid=charges-panel] tbody [data-ghost-for="{cid}"]'); expect(g2).to_be_visible()
    expect(g2.get_by_test_id("btn-undo-dismiss")).to_be_focused()                                            # T-174 N3: focus moves one frame after the placeholder appears; measure after it has
    f = _in_view(page); assert f and f["ok"], f
    g2.get_by_test_id("btn-undo-dismiss").click(); expect(g2).to_have_count(0)
    expect(page.locator(f'[data-testid=charges-panel] [data-item-id="{cid}"]').first).to_have_attribute("data-review", "pending")


# ---- F6: the keyboard loop never dead-ends
def test_a_alone_decides_every_item_across_lists_and_no_press_is_a_no_op(pw, rivera):
    b, pg = _page(pw, 1440, 900)
    try:
        open_case(pg, rivera)
        pg.get_by_test_id("btn-start-review").click()
        seen_lists = set()
        for n in range(60):
            d0, total = _decided(pg)
            if d0 == total:
                break
            a0 = pg.evaluate("document.activeElement && document.activeElement.getAttribute('data-item-id')")
            seen_lists.add(pg.evaluate("(() => { const r = document.activeElement && document.activeElement.closest('[data-item-id]'); const g = r && r.closest('[data-group], [data-testid=queue]'); return g ? (g.getAttribute('data-group') || g.getAttribute('data-testid')) : null; })()"))
            pg.keyboard.press("a")
            if pg.locator("[data-testid=charge-confirm][open]").count():                 # a flagged charge asks first; confirming it is her decision
                pg.get_by_test_id("btn-charge-confirm").click()
            for _ in range(40):                                                          # the press must change the count or the focused item
                pg.wait_for_timeout(50)
                if _decided(pg)[0] != d0 or pg.evaluate("document.activeElement && document.activeElement.getAttribute('data-item-id')") != a0:
                    break
            else:
                pytest.fail(f"press {n + 1} of a did nothing (decided {d0}, focus {a0})")
        d, total = _decided(pg); assert d == total, (d, total)
        assert len(seen_lists) >= 3, seen_lists                                          # it crossed from the timeline into the flags and the charges
    finally:
        b.close()


def test_a_at_the_end_of_a_list_moves_to_the_next_list_without_deciding_it(page, rivera):
    open_case(page, rivera)
    tids = page.locator("[data-testid=queue] > article").evaluate_all("els => els.map(e => e.getAttribute('data-testid'))")
    for t in tids[:-1]:
        page.get_by_test_id(t).get_by_test_id("btn-accept").click()
    page.wait_for_timeout(300)
    last = page.get_by_test_id(tids[-1]); last.scroll_into_view_if_needed(); last.focus()
    d0, _ = _decided(page); page.keyboard.press("a"); page.wait_for_timeout(700)
    assert _decided(page)[0] == d0 + 1                                                   # the key decided its own item and nothing else
    where = page.evaluate("""(() => { const r = document.activeElement.closest('[data-item-id]'); const g = r && r.closest('[data-group], [data-testid=queue]');
      return r ? { review: r.getAttribute('data-review'), inQueue: !!(g && g.getAttribute('data-testid') === 'queue') } : null; })()""")
    assert where and not where["inQueue"] and where["review"] == "pending", where          # moved on to the next list, and did not decide the item it landed on
    assert "Next:" in page.locator("#rv-live").inner_text()
    assert _in_view(page)["ok"]


def test_n_jumps_to_the_first_open_item_and_x_to_export_and_both_are_in_the_sheet(page, rivera):
    open_case(page, rivera)
    last = page.locator("[data-testid=charges-panel] [data-item-id]").last; last.scroll_into_view_if_needed(); last.focus()
    page.keyboard.press("n"); page.wait_for_timeout(200)
    first = page.evaluate("document.activeElement.getAttribute('data-item-id')")
    assert first and page.locator(f'[data-testid=queue] [data-item-id="{first}"]').count() + page.locator(f'[data-item-id="{first}"]').count() >= 1
    assert _in_view(page)["ok"]
    page.keyboard.press("x"); expect(page.get_by_test_id("btn-export")).to_be_focused()
    last.focus(); page.keyboard.press("?"); sheet = page.get_by_test_id("shortcuts-list"); expect(sheet).to_be_visible()
    t = sheet.inner_text(); assert re.search(r"(^|\n)n\n", t) and re.search(r"(^|\n)x\n", t), t


def test_n_and_x_do_nothing_from_the_page_body(page, rivera):
    open_case(page, rivera)
    page.evaluate("document.activeElement && document.activeElement.blur()")
    d0 = _decided(page)
    page.keyboard.press("n"); page.keyboard.press("x"); page.wait_for_timeout(200)
    assert _decided(page) == d0 and page.evaluate("document.activeElement === document.body")


# ---- F7: nothing a paralegal reads is test or developer wording; Audit is behind More on every row
def test_no_test_or_developer_wording_on_the_case_page_or_in_the_exports(page, rivera):
    open_case(page, rivera)
    for tid in ("entry-1", "entry-2"):
        page.get_by_test_id(tid).get_by_test_id("btn-accept").click()
    expect(page.locator("#badge")).to_have_text(re.compile(r"^(Demo: recorded AI answers|Demo: sample answers prepared by our team|)$"))
    text = page.evaluate("document.body.innerText")
    assert not BAD_WORDS.search(text), BAD_WORDS.search(text).group(0)
    page.get_by_test_id("btn-export").click()
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    for tid in ("export-letter", "export-notes"):
        t = page.get_by_test_id(tid).inner_text()
        assert not re.search(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b", t) and not BAD_WORDS.search(t), (tid, t[:200])


def test_overview_has_no_test_wording_and_an_error_says_what_to_do(page):
    page.route(re.compile(r"/api/cases$"), lambda r: r.fulfill(status=500, json={"error": {"code": "internal", "message": ""}}) if r.request.method == "GET" else r.continue_())
    page.goto(BASE + "/"); page.wait_for_timeout(1500)
    t = page.evaluate("document.body.innerText")
    assert not BAD_WORDS.search(t) and "500" not in t, t


def test_audit_waits_behind_more_on_entries_flags_and_charges(page, rivera):
    open_case(page, rivera)
    for loc in (page.get_by_test_id("entry-1"), page.locator("[data-testid=flags-panel] [data-item-id]").first, page.locator("[data-testid=charges-panel] [data-amount-kind=charge]").first):
        loc.scroll_into_view_if_needed()
        expect(loc.get_by_test_id("btn-audit")).to_be_hidden()
        more = loc.get_by_test_id("entry-toggle") if loc.get_attribute("data-testid") == "entry-1" else loc.get_by_test_id("btn-more")
        more.click(); expect(more).to_have_attribute("aria-expanded", "true")
        expect(loc.get_by_test_id("btn-audit")).to_be_visible()
        more.click(); expect(loc.get_by_test_id("btn-audit")).to_be_hidden()


# ---- F11: at most five visible controls on an undecided row or card
def test_a_row_or_card_shows_at_most_five_controls(page, rivera):
    open_case(page, rivera)
    sel = "button:visible, a:visible"
    for loc in (page.get_by_test_id("entry-4"), page.locator("[data-testid=flags-panel] [data-flag-type=conflict]").first, page.locator("[data-testid=charges-panel] [data-amount-kind=charge]").first):
        n = loc.locator(sel).count(); assert n <= 5, (n, loc.locator(sel).evaluate_all("els => els.map(e => e.textContent.trim())"))
        for name in ("Accept", "Edit", "Dismiss"):
            if loc.get_attribute("data-flag-type") or loc.get_attribute("data-amount-kind"):
                continue
            expect(loc.get_by_role("button", name=re.compile("^" + name))).to_be_visible()
        expect(loc.get_by_test_id("btn-source")).to_be_visible()


# ---- F12: Undo asks before it discards her wording
def test_undo_on_an_edited_row_asks_first_and_keep_leaves_the_wording(page, rivera):
    open_case(page, rivera)
    e = page.get_by_test_id("entry-3"); new = "Persistent neck pain 6/10 with daily headaches noted."
    e.get_by_test_id("btn-edit").click(); e.get_by_test_id("edit-summary").fill(new); e.get_by_test_id("btn-save-accept").click()
    expect(e).to_have_attribute("data-review", re.compile("accepted|edited"))
    e.get_by_test_id("btn-reset").click()
    box = e.get_by_test_id("discard-confirm"); expect(box).to_be_visible(); expect(e.get_by_test_id("btn-keep-edit")).to_be_focused()
    assert new in e.get_by_test_id("entry-summary").inner_text()                           # nothing was sent yet
    e.get_by_test_id("btn-keep-edit").click(); expect(box).to_have_count(0)
    assert new in e.get_by_test_id("entry-summary").inner_text()
    e.focus(); page.keyboard.press("r"); expect(e.get_by_test_id("discard-confirm")).to_be_visible()      # the r key asks too
    page.keyboard.press("Escape"); expect(e.get_by_test_id("discard-confirm")).to_have_count(0)
    assert new in e.get_by_test_id("entry-summary").inner_text()
    e.get_by_test_id("btn-reset").click(); e.get_by_test_id("btn-discard-edit").click()
    expect(e).to_have_attribute("data-review", "pending")
    assert new not in e.get_by_test_id("entry-summary").inner_text()


def test_undo_on_a_plain_accept_does_not_ask(page, rivera):
    open_case(page, rivera)
    e = page.get_by_test_id("entry-1"); e.get_by_test_id("btn-accept").click(); expect(e).to_have_attribute("data-review", "accepted")
    e.get_by_test_id("btn-reset").click(); expect(e).to_have_attribute("data-review", "pending")
    expect(e.get_by_test_id("discard-confirm")).to_have_count(0)


# ---- F9 / F10: one open count; "all agreed" only when it is true
def test_the_live_message_and_the_header_agree_on_what_is_left(page, rivera):
    open_case(page, rivera)
    page.get_by_test_id("entry-1").get_by_test_id("btn-accept").click(); page.wait_for_timeout(400)
    m = re.search(r"(\d+) (?:item is|items are|left to review)", page.locator("#rv-live").inner_text()) or re.search(r"(\d+) left", page.locator("#rv-live").inner_text())
    d, total = _decided(page); assert m and int(m.group(1)) == total - d, (page.locator("#rv-live").inner_text(), d, total)
    e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited"); page.wait_for_timeout(400)
    d, total = _decided(page)
    m = re.search(r"(\d+) left to review", page.locator("#rv-live").inner_text())
    if m:
        assert int(m.group(1)) == total - d, (page.locator("#rv-live").inner_text(), d, total)


def test_the_ai_check_summary_does_not_say_all_agreed_when_an_edit_was_not_checked(page, rivera):
    open_case(page, rivera)
    e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited"); page.wait_for_timeout(800)
    if e.get_attribute("data-edit-check") is None:
        pytest.skip("this backend verified the edit")
    assert "all agreed" not in page.get_by_test_id("judge-summary").inner_text()
