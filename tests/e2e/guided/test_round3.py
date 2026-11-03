"""T-181 round 3 (phone only): at 390x844 the highlighted words are inside the record window whenever a tick box shows, and a refused edit's message is never behind the sticky action bar.
Every assertion is on bounding boxes (inside the viewport, inside its own card, above the bar's top edge), without scrolling anything first."""
import json
import os

import pytest
from playwright.sync_api import expect

from tests.e2e.guided.test_round2 import LIB10, phone, item, make, open_item   # noqa: F401  (make is a fixture)

BOXES = """() => {
  const R = (el) => { if (!el) return null; const r = el.getBoundingClientRect(); return { top: r.top, bottom: r.bottom, left: r.left, right: r.right, h: r.height }; };
  const q = (s) => document.querySelector('[data-testid=' + s + ']');
  const body = q('card-source'), mark = body && body.querySelector('mark, .sent.on');
  return { vw: innerWidth, vh: innerHeight, bar: R(q('actions')), src: R(body), mark: R(mark), line: R(q('line-text')), head: R(q('line-head')), card: R(q('card-line')),
           chk: R(q('check-compare')), foot: R(q('card-foot')), scrollTop: body ? body.scrollTop : null, scrollH: body ? body.scrollHeight : null, lineH: mark ? parseFloat(getComputedStyle(mark).lineHeight) || 24 : 24 };
}"""


def shot(page, name):
    d = os.environ.get("R3_SHOTS")
    if d:
        page.screenshot(path=os.path.join(d, name + ".png"))


def boxes(page):
    return page.evaluate(BOXES)


def inside_viewport(b, r, name):
    assert r is not None, (name, b)
    assert r["top"] >= 0 and r["bottom"] <= b["vh"] and r["left"] >= 0 and r["right"] <= b["vw"], (name, r, b["vw"], b["vh"])


def not_under_bar(b, r, name):
    assert r["bottom"] <= b["bar"]["top"] + 0.5, (name, "is under the action bar", r, b["bar"])


def show_the_mark(b):
    """the first highlighted mark is whole inside the record window, with about one more line of the record under it (or the record ends there)"""
    m, s = b["mark"], b["src"]
    assert m is not None, "no highlighted words in the record window"
    assert m["top"] >= s["top"] - 0.5 and m["bottom"] <= s["bottom"] + 0.5, ("the mark is outside the record window", m, s)
    inside_viewport(b, m, "mark"); not_under_bar(b, m, "mark")
    assert s["bottom"] - s["top"] - m["h"] >= b["lineH"] - 1, ("the window has less than one line of the record to spare beside the mark", m, s)


@pytest.mark.parametrize("w,h", [(390, 844), (375, 667)])
def test_a_disputed_line_shows_its_highlighted_words_in_the_record_window_without_scrolling(pw, make, w, h):
    tok = make(LIB10); b, page = phone(pw, w, h)
    try:
        open_item(page, tok, "e1")
        expect(page.get_by_test_id("check-compare")).to_be_visible()
        page.wait_for_timeout(300)
        bx = boxes(page)
        print("DISPUTED", w, h, json.dumps(bx)); shot(page, f"disputed-{w}x{h}")
        show_the_mark(bx)
    finally:
        b.close()


def test_a_line_just_reworded_shows_its_highlighted_words_and_the_whole_line_above_the_bar(pw, make):
    tok = make(); e1 = item(tok, "e1"); b, page = phone(pw)
    try:
        open_item(page, tok, "e1")
        page.get_by_test_id("btn-third").click()
        page.get_by_test_id("edit-summary").fill(e1["summary"].replace("alert and oriented; ", ""))
        page.get_by_test_id("answer-yes").click()
        expect(page.get_by_test_id("check-compare")).to_be_visible()
        page.wait_for_timeout(300)
        bx = boxes(page); print("EDITED", json.dumps(bx)); shot(page, "edited")
        show_the_mark(bx)
        c, ln, hd = bx["card"], bx["line"], bx["head"]
        assert ln["top"] >= hd["bottom"] - 1 and ln["bottom"] <= c["bottom"] + 1, ("the line is behind the card header or cut off", ln, hd, c)
        assert bx["chk"]["bottom"] <= c["bottom"] + 1, ("the tick box is cut off", bx["chk"], c)
        inside_viewport(bx, bx["chk"], "tick box"); not_under_bar(bx, bx["chk"], "tick box")
    finally:
        b.close()


@pytest.mark.parametrize("w,h", [(390, 844), (375, 667)])
def test_a_refused_edit_shows_its_message_above_the_action_bar(pw, make, w, h):
    tok = make(); e1 = item(tok, "e1"); b, page = phone(pw, w, h)
    try:
        open_item(page, tok, "e1")
        page.get_by_test_id("btn-third").click()
        page.get_by_test_id("edit-summary").fill(e1["summary"].replace("complained of ", ""))
        page.get_by_test_id("answer-yes").click()
        foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved.")
        page.wait_for_timeout(300)
        r = page.evaluate("""() => { const f = document.querySelector('[data-testid=card-foot]'), r = f.getBoundingClientRect(), bar = document.querySelector('[data-testid=actions]').getBoundingClientRect(),
            card = document.querySelector('[data-testid=card-line]').getBoundingClientRect(), hit = document.elementFromPoint(r.left + r.width / 2, r.top + Math.min(r.height / 2, 12));
          return { foot: [r.top, r.bottom, r.left, r.right], bar: bar.top, card: [card.top, card.bottom], vh: innerHeight, vw: innerWidth, hitInFoot: !!hit && f.contains(hit), hit: hit ? hit.outerHTML.slice(0, 120) : null, text: f.innerText }; }""")
        print("REFUSED", json.dumps(r)); shot(page, "refused2")
        assert "complained of" in r["text"], r
        assert r["foot"][0] >= 0 and r["foot"][3] <= r["vw"] and r["foot"][1] <= r["bar"] + 0.5 and r["foot"][1] <= r["vh"], ("the refusal is under the action bar or off the screen", r)
        if h >= 760:
            assert r["foot"][1] <= r["card"][1] + 1 and r["foot"][0] >= r["card"][0] - 1, ("the refusal is outside the visible part of its card", r)
        assert r["hitInFoot"], ("something else covers the refusal", r)
        assert item(tok, "e1")["summary"] == e1["summary"], "nothing was saved"
    finally:
        b.close()
