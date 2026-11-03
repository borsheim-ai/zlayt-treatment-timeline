"""T-204 (frontend; D-065, D-069): a prepared answer is never described as the AI's wording, not even for the moment before the server's sentence arrives.
The classic review row paints a fallback sentence for "quote re-picked, second check has no answer" and for "accepted, export blocked"; for an item that is a prepared answer (item.prepared)
the fallback is the prepared twin. The test holds the trace requests, so the first paint is observable, reads it, releases them, and reads the swapped-in server sentence. A MutationObserver
also records every text those nodes ever held, so a flash between two reads cannot hide. Second test: the demo's refused-paste message is rebuilt when the library list loads late.
r2 (staff review): a fourth test walks the whole classic UI for the prepared sample (rail, AI-check panel, Why panels, flags, charges, tray, export gate, audit) with a document-wide observer and fails on any
AI-attributing phrase that is not the real second-check wording. No fixed waits: every wait is on a condition. No new test ids."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e import conftest as C
from tests.e2e.conftest import api, BASE
from tests.e2e.test_edit_to_check import edited_quote, _row, _accept_something_else   # noqa: F401  (edited_quote is a fixture)
from tests.e2e.test_mvp_finish import NOT_A_RECORDED_CASE

AI = re.compile(r"\bAI\b|\bmodel\b|claude|sonnet|haiku|opus", re.I)
WATCH = """(() => {
  window.__seen = [];
  const SEL = '[data-testid=edit-check-hint],[data-testid=edit-compare-prompt],[data-testid=compare-export-note]';
  const scan = () => document.querySelectorAll(SEL).forEach((n) => { const t = n.textContent; if (t && !window.__seen.includes(t)) window.__seen.push(t); });
  new MutationObserver(scan).observe(document, { subtree: true, childList: true, characterData: true });
  setInterval(scan, 20);
})();"""


def _hold(page):
    held = []
    page.route(re.compile(r"/api/cases/[^/]+(/items/[^/]+)?/trace$"), lambda route: held.append(route))
    return held


def _until(page, cond, what, timeout=15.0):
    """Wait on a condition, polling through the page's own animation frames (no fixed sleep)."""
    import time
    end = time.monotonic() + timeout
    while not cond():
        assert time.monotonic() < end, "timed out waiting for " + what
        page.evaluate("new Promise((r) => requestAnimationFrame(r))")


def _release(page, held, wait_for_one=True):
    """Release every held route. With wait_for_one (the default for the first release of a test) it first waits until the page has actually issued a held request."""
    if wait_for_one:
        _until(page, lambda: bool(held), "a held request")
    while held:
        held.pop().continue_()


def test_a_prepared_item_paints_no_ai_wording_before_or_after_the_server_sentence(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    assert next(x for x in C.api("GET", f"/api/cases/{t['tok']}")[1]["entries"] if x["id"] == t["id"])["prepared"] is True, "the setup: a prepared answer"
    page.add_init_script(WATCH)
    held = _hold(page)
    try:
        page.reload(); page.get_by_test_id("timeline").wait_for()
        row = _row(page, t["id"])
        hint = row.get_by_test_id("edit-check-hint"); expect(hint).to_be_visible()
        first = hint.inner_text()
        assert not AI.search(first), first                                        # first paint: the server has not answered yet
        assert "prepared wording" in first and "second check has no answer" in first, first
        row.focus(); page.keyboard.press("a")
        prompt = row.get_by_test_id("edit-compare-prompt"); expect(prompt).to_be_visible()
        assert not AI.search(prompt.inner_text()), prompt.inner_text()
        assert "will be blocked" in prompt.inner_text() and "prepared wording" in prompt.inner_text()
        _release(page, held)                                                       # the swap, item sentence
        why = next(s for s in api("GET", f"/api/cases/{t['tok']}/items/{t['id']}/trace")[1]["steps"] if s["id"] == "human")["why"]
        expect(prompt).to_contain_text(why)
        assert why and not AI.search(why) and not AI.search(prompt.inner_text()), prompt.inner_text()
        assert not AI.search(hint.inner_text()), hint.inner_text()
        held = _hold(page)                                                         # hold the case trace again for the blocker sentence
        row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
        note = row.get_by_test_id("compare-export-note"); expect(note).to_be_visible()
        assert not AI.search(note.inner_text()), note.inner_text()                # the blocker sentence has not arrived yet
        assert "second check still has no answer" in note.inner_text()
        _release(page, held)                                                       # the swap, blocker sentence
        expect(note).to_contain_text("Nothing prepared goes into the letter")
        assert not AI.search(note.inner_text()), note.inner_text()
        seen = page.evaluate("window.__seen")
        assert seen, "the observer saw nothing"
        assert not [s for s in seen if AI.search(s)], [s for s in seen if AI.search(s)]   # not for a moment, on any of the three nodes
    finally:
        _release(page, held, wait_for_one=False)


def test_the_refused_paste_message_follows_the_library_when_it_loads_late(page):
    """T-174 r2 F15 / T-204: the message offers 'Choose a library case' only where the library is on the page. If the list arrives after the refusal was painted, the message is built again."""
    held = []
    page.route(re.compile(r"/api/library$"), lambda route: held.append(route))
    try:
        page.goto(BASE); page.get_by_test_id("input-text").wait_for()
        page.get_by_test_id("input-text").fill(NOT_A_RECORDED_CASE); page.get_by_test_id("btn-analyze").click()
        err = page.get_by_test_id("error"); expect(err).to_contain_text("only runs the recorded sample case", timeout=15000)
        assert held, "the library request was held"
        expect(err.get_by_test_id("btn-error-library")).to_have_count(0)
        _release(page, held)
        expect(err.get_by_test_id("btn-error-library")).to_have_text("Choose a library case", timeout=15000)
        expect(err).to_contain_text("sample and library cases")
        expect(err).not_to_contain_text("only runs the recorded sample case,")
        expect(err.get_by_test_id("btn-error-action")).to_have_text("Open the sample")
        err.get_by_test_id("btn-error-library").click()
        expect(page.get_by_test_id("library-list")).to_be_visible()
    finally:
        _release(page, held, wait_for_one=False)


def test_an_unrelated_error_is_not_replaced_when_the_library_loads(page):
    """The rebuild is for the refusal only: a different message (here, no text to read) stays as it is when the list arrives."""
    held = []
    page.route(re.compile(r"/api/library$"), lambda route: held.append(route))
    try:
        page.goto(BASE); page.get_by_test_id("input-text").wait_for()
        page.get_by_test_id("btn-analyze").click()
        err = page.get_by_test_id("error"); expect(err).to_contain_text("There is no text to read")
        # the late event the rebuild would hang on: wait for the library answer and for the page's own zl:switcher event (a listener registered after the app's, so it fires last), then one more frame
        page.evaluate("window.__sw = false; document.addEventListener('zl:switcher', () => { window.__sw = true; })")
        _release(page, held); _until(page, lambda: page.evaluate("window.__sw === true"), "the zl:switcher event")
        page.evaluate("new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))")
        expect(err).to_contain_text("There is no text to read"); expect(err.get_by_test_id("btn-error-library")).to_have_count(0)
    finally:
        _release(page, held, wait_for_one=False)


# ---- the whole classic UI, one prepared case (T-204 r2) ----------------------------------------------------------------------------------------------------------------------------------
# What the observer collects: the text of every node and element that is ever added or changed, every title / aria-label, and (every 40 ms) the page's visible text. Nothing is filtered in the page.
WATCH_ALL = """(() => {
  window.__all = new Set();
  const add = (t) => { if (t) { t = t.replace(/\\s+/g, ' ').trim(); if (t) window.__all.add(t); } };
  const ATTRS = ['title', 'aria-label', 'placeholder', 'alt'];
  const el = (n) => {
    if (n.nodeType === 3) { add(n.data); if (n.parentElement) add(n.parentElement.textContent.length < 700 ? n.parentElement.textContent : ''); return; }
    if (n.nodeType !== 1) return;
    if (n.textContent.length < 700) add(n.textContent);
    ATTRS.forEach((a) => add(n.getAttribute(a)));
    n.querySelectorAll('*').forEach((c) => { ATTRS.forEach((a) => add(c.getAttribute(a))); });
  };
  const scan = () => {
    if (!document.body) return;
    document.body.innerText.split('\\n').forEach(add);
    document.querySelectorAll('[title],[aria-label]').forEach((c) => ATTRS.forEach((a) => add(c.getAttribute(a))));
  };
  const mo = new MutationObserver((ms) => ms.forEach((m) => {
    if (m.type === 'attributes') add(m.target.getAttribute(m.attributeName));
    else if (m.type === 'characterData') el(m.target);
    else { m.addedNodes.forEach(el); if (m.target.nodeType === 1 && m.target.textContent.length < 700) add(m.target.textContent); }
  }));
  mo.observe(document, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ATTRS });
  setInterval(scan, 40);
  window.__scanAll = scan;
})();"""

# The second check is a real AI step (api.md T-177 r3): these phrases are about the judge and may say AI or model. Everything else that is left after they are removed must not name an AI, a model or a model's name.
SECOND_CHECK = [re.compile(p, re.I) for p in (
    r"second (AI )?(check|model)", r"another model", r"AI[- ]?checks?\b", r"AI-checked", r"checked by (AI|[\w.:/-]+)", r"how the AI was checked", r"AI quality checks",
    # the second check's own verdict words, as whole phrases (T-204 r3: no open verb list: "the AI said / found / read / disagree" about a prepared answer is exactly the leak)
    r"\b(the )?AI (objected|agreed|did not check|could not (check|decide))", r"The AI did not give an answer you can rely on\.",
    r"The AI found the draft (only partly |not )?supported by the quote\.", r"The AI reads this differently from the draft\.", r"no AI judge looked at this item",
    r"no AI model can answer", r"not (written )?by an AI model", r"\(not AI\)", r"(model )?claude-haiku-[\w.-]+",       # the judge's own model id, and the "(not AI)" of a code step
    r"independent of the (drafting )?model",
    # the calibration line: the server's measured statement from evals/reports/calibration.json, this sentence only
    r"matched the record \d+/\d+ times in testing on the claude-cli backend \(\d+ golden cases, small sample\)\.",
)]
LEAK = re.compile(r"\bAI\b|\bmodel|claude|sonnet|haiku|opus", re.I)


def _leaks(seen):
    out = []
    for t in seen:
        rest = t
        for p in SECOND_CHECK:
            rest = p.sub(" ", rest)
        m = LEAK.search(rest)
        if m:
            out.append(t[:300])
    return sorted(set(out), key=len)[:40]


def _clean_seen(page):
    page.evaluate("window.__scanAll()")
    return page.evaluate("[...window.__all]")


def test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai(page, edited_quote):
    """A prepared sample, an accepted entry whose quote she changed (held by the second check), the whole classic UI walked with a document-wide observer: the case rail, its legend and every step,
    the AI-check panel (collapsed, opened, with the held item in it), a Why panel and Audit, flags, charges, the tray, the export gate. Any phrase that names an AI or a model, other than about the real
    second check, fails. Before this the rail and the panel said 'kept the AI's summary' (staff review T-204 r1)."""
    from tests.e2e.test_stepper import open_rail, open_judges
    t = edited_quote; _accept_something_else(t)
    assert next(x for x in C.api("GET", f"/api/cases/{t['tok']}")[1]["entries"] if x["id"] == t["id"])["prepared"] is True, "the setup: a prepared answer"
    page.add_init_script(WATCH_ALL)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); row.focus(); page.keyboard.press("a")
    expect(row.get_by_test_id("edit-compare-prompt")).to_be_visible()
    row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
    expect(row.get_by_test_id("compare-export-note")).to_be_visible()
    # a fresh load: the held item is now in the gate, so the rail, the panel and the export message are painted from the server's case
    page.reload(); page.get_by_test_id("timeline").wait_for()
    cs = open_rail(page)
    held_blockers = cs.get_by_test_id("gate-blocker"); expect(held_blockers.first).to_be_visible()
    assert "prepared wording" in cs.inner_text(), cs.inner_text()                  # the rail says it in the prepared words, not just says nothing
    steps = cs.get_by_test_id("case-step")
    for i in range(steps.count()):                                                  # every step of the rail, with its details opened where it has them
        for d in steps.nth(i).locator("details").all():
            if not d.evaluate("n => n.open"):
                d.locator("summary").first.click()
    jp = open_judges(page)
    assert "prepared wording" in jp.inner_text(), jp.inner_text()
    for d in jp.locator("details").all():
        if not d.evaluate("n => n.open"):
            d.locator("summary").first.click()
    from tests.e2e.conftest import reveal
    for tid in ("entry-why", "btn-audit"):                                          # Why this status and Audit on the prepared row
        loc = reveal(row.get_by_test_id(tid))
        if loc.count():
            loc.first.click()
            page.locator("dialog[open], #why-modal:visible, [data-testid=audit-panel]:visible").first.wait_for()
            page.keyboard.press("Escape")
    for panel in ("flags-panel", "charges-panel"):
        p = page.get_by_test_id(panel)
        if p.count():
            btn = reveal(p.get_by_test_id("btn-trace"))
            if btn.count():
                btn.first.click(); page.get_by_test_id("item-stepper").wait_for(); page.keyboard.press("Escape")
    tray_box = page.get_by_test_id("rejected-tray")
    if tray_box.count():
        tray_box.scroll_into_view_if_needed()
    seen = _clean_seen(page)
    assert len(seen) > 50, "the observer saw too little: " + str(len(seen))
    assert page.get_by_test_id("tag-ai-draft").count() == 0, "a prepared case paints no 'draft' (AI) tag"
    assert not _leaks(seen), "\n".join(_leaks(seen))


def test_the_leak_check_itself_catches_the_old_wording():
    """The allow-list only forgives second-check phrases: the r1 sentences, and a model name, still fail it."""
    assert _leaks(["You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote."])
    assert _leaks(["The model's attempt (not used): x"]) and _leaks(["Drafted by claude-sonnet-4"]) and _leaks(["Run the AI steps again"])
    # r3 (staff review r2): the AI-check panel's own labels for a prepared flag disagreement, and any backend other than the measured one, are leaks
    assert _leaks(["The AI said: The prepared answers did not include it."]) and _leaks(["The phrase list and the AI disagree"]) and _leaks(["Where code and the AI read an item differently (1 item)"])
    assert _leaks(["The AI found it."]) and _leaks(["Verified items matched the record 82/83 times in testing on the claude-api backend (10 golden cases, small sample)."]) and _leaks(["Summaries and warnings are drafted by AI and checked by code; you decide every item."])
    assert not _leaks(["The phrase list and the prepared answers disagree", "The prepared answers said: The prepared answers did not include it.", "Where code and the prepared answers read an item differently (1 item)",
                       "Code checks passed, the second AI check objected", "The second AI check said: The AI found the draft not supported by the quote.",
                       "Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample)."])
    assert not _leaks(["The second AI check found this not supported by the quote.", "Prepared by our team (not by an AI model), checked by claude-haiku-4-5.", "How the AI was checked",
                       "You changed the quote on an accepted entry and kept the prepared wording, and the second AI check has no answer on the new quote."])


# ---- r3 (staff review r2): the plain sample's AI-check panel, the guided footer before health, the rerun button label ------------------------------------------------------------------
def _open_every_detail(page):
    page.evaluate("document.querySelectorAll('details').forEach((d) => { d.open = true; })")


def test_the_plain_prepared_samples_ai_check_panel_names_the_prepared_answers(page, sample_case):
    """No edits, no held item: the unedited prepared sample. Its flag disagreement (the phrase list found it, the prepared answers did not include it) is said in the prepared answers' name,
    in the chip, the row's evidence, the Technical detail and the group heading, and the document-wide walk (no open verb list) finds no AI wording beyond the second check's own."""
    from tests.e2e.test_stepper import open_rail, open_judges
    dis = api("GET", f"/api/cases/{sample_case}/judges")[1]["disagreements"]
    assert [d for d in dis if d["type"] == "sources_disagree"], "the setup: the plain sample has a phrase-list versus prepared-answers disagreement: " + str(dis)
    page.add_init_script(WATCH_ALL)
    C.open_case(page, sample_case)
    open_rail(page); jp = open_judges(page); _open_every_detail(page)
    txt = jp.inner_text()
    assert "Where code and the prepared answers read an item differently" in txt, txt
    assert "The phrase list and the prepared answers disagree" in txt and "The prepared answers said:" in txt and "The prepared answers did not include it." in txt, txt
    assert not re.search(r"the AI said|and the AI (disagree|read)|AI disagree", txt, re.I), txt
    seen = _clean_seen(page)
    assert len(seen) > 50, "the observer saw too little: " + str(len(seen))
    assert not _leaks(seen), "\n".join(_leaks(seen))


def test_a_rerun_button_on_a_prepared_case_says_checks_not_ai_steps(page, sample_case):
    """Staff review r2 mutant B: the case rail's RERUN action button label was never painted by the walk. A route stub gives the grounding step a RERUN next action (the fixture backend never does)."""
    from tests.e2e.test_stepper import open_rail

    def _trace(route):
        d = route.fetch().json()
        g = next(x for x in d["steps"] if x["id"] == "grounding")
        g["status"] = "pending"; g["next_action"] = {"code": "RERUN", "text": "Run the steps again.", "target": {}}
        route.fulfill(json=d)
    page.route(re.compile(r"/api/cases/[^/]+/trace$"), _trace)
    page.add_init_script(WATCH_ALL)
    C.open_case(page, sample_case)
    cs = open_rail(page); _open_every_detail(page)
    btn = cs.locator("[data-action-code=RERUN]")
    _until(page, lambda: btn.count() > 0, "the RERUN action button")
    assert btn.first.inner_text() == "Run the checks again", btn.first.inner_text()
    seen = _clean_seen(page)
    assert not [s for s in seen if "AI steps" in s], [s for s in seen if "AI steps" in s]
    assert not _leaks(seen), "\n".join(_leaks(seen))


def test_the_guided_ui_paints_no_ai_wording_for_the_prepared_sample_before_or_after_health(pw):
    """Staff review r2 major: until /api/health answered, the footer said 'drafted by AI' on every guided screen. Now: a neutral line first, the prepared sentence after, and a document-wide walk
    of home, step 1 (the draft done screen), step 2, step 3 and step 4 for the prepared sample finds no AI wording beyond the second check's own."""
    from tests.e2e.guided._helpers import browser, make_case
    tok = make_case("t204 r3 guided", run=True, decide=True)
    br, page = browser(pw, 1440, 900)
    held = []
    page.route(re.compile(r"/api/health$"), lambda route: held.append(route))
    try:
        page.add_init_script(WATCH_ALL)
        page.goto(C.SERVER + f"/case/{tok}/timeline", wait_until="domcontentloaded")
        _until(page, lambda: bool(held), "the held health request")
        _until(page, lambda: page.get_by_test_id("footer-note").count() > 0, "the footer")
        before = page.get_by_test_id("footer-note").inner_text()
        assert before and not AI.search(before) and "prepared" not in before.lower(), before            # a neutral line: nothing about who wrote the answers
        assert page.get_by_test_id("demo-badge").count() == 0
        while held:
            held.pop().continue_()
        page.unroute_all(behavior="ignoreErrors")
        _until(page, lambda: "Prepared by our team" in page.get_by_test_id("footer-note").inner_text(), "the prepared footer sentence")
        after = page.get_by_test_id("footer-note").inner_text()
        assert not re.search(r"drafted by AI", after), after
        page.goto(C.SERVER + "/"); page.get_by_test_id("brand").wait_for(); _open_every_detail(page)
        for path in ("records", "timeline", "bills", "letter"):
            page.goto(C.SERVER + f"/case/{tok}/{path}")
            _until(page, lambda: page.get_by_test_id("footer-note").count() > 0 and page.evaluate("document.body.innerText.length") > 400, "the " + path + " page")
            _open_every_detail(page)
            page.evaluate("new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))")
        # a fresh sample case drafted from step 1: the done screen carries the server's banner and the prepared badge
        st, nc = api("POST", "/api/cases", {"sample": True, "title": "t204 r3 step1"}); assert st == 201
        page.goto(C.SERVER + f"/case/{nc['token']}/records")
        page.get_by_test_id("btn-draft").click(); expect(page.get_by_test_id("draft-done")).to_be_visible(timeout=30000)
        _open_every_detail(page)
        seen = _clean_seen(page)
        assert len(seen) > 100, "the observer saw too little: " + str(len(seen))
        assert not [s for s in seen if re.search(r"drafted by AI|AI draft\b", s)], [s for s in seen if re.search(r"drafted by AI|AI draft\b", s)]
        assert not _leaks(seen), "\n".join(_leaks(seen))
    finally:
        while held:
            held.pop().continue_()
        br.close()
