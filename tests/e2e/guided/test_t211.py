"""T-211 (D-074): the app itself shows and explains the validation ladder. Real browser, fixture backend (curated set), real API; cases are made over the API and deleted afterwards.
Guarded: every Step 2 and Step 3 item shows "How this was checked" with three rows (code check, second AI check with its verdict and reason, you); a prepared answer says it was prepared by our team and then
checked; a disputed or failed check is shown in words (the trace is rewritten the way the server answers for one); the panel never hides the highlighted words or the primary action at 1440x900 and fits at 390px;
the header link on every screen opens "How each answer is checked" (about 150 words, the ladder picture, what is code and what is AI, the repo doc names); no console error anywhere."""
import json
import re
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided.test_shell_smoke import watch, go
from tests.e2e.guided.test_step2 import make, phone, sized, case, item, open_item, settle   # noqa: F401  (make and phone are fixtures)

VERDICTS = {"Agrees", "Disputes", "Could not check", "Not needed", "Not run"}


def rows(page):
    t = lambda k: page.get_by_test_id(k).inner_text()
    return t("how-code-text"), t("how-ai-text"), t("how-you-text")


def wait_loaded(page):
    expect(page.get_by_test_id("how-checked")).not_to_have_attribute("aria-busy", "true", timeout=10000)


def open_panel(page):
    """At 1440x900 the panel folds to its chips when it would push a highlighted word out of the record window; she opens it with one click (and it then stays open)."""
    if not page.get_by_test_id("how-code").is_visible():
        page.get_by_test_id("how-summary").click()
    expect(page.get_by_test_id("how-code")).to_be_visible()


def inside(outer, inner):
    return inner["y"] >= outer["y"] - 1 and inner["y"] + inner["height"] <= outer["y"] + outer["height"] + 1


# ------------------------------------------------------------------------------------------------ the three rows on every item

def test_every_item_of_steps_2_and_3_shows_code_check_second_ai_check_and_you(pw, make):
    tok = make(); c = case(tok)
    b, pg = sized(pw, 1440, 900)
    try:
        seen = watch(pg)
        steps = [("timeline", i["id"]) for g in ("entries", "undated_entries", "flags") for i in c[g]] + [("bills", a["id"]) for a in c["amounts"]]
        assert len(steps) >= 15
        for step, iid in steps:
            open_item(pg, tok, iid, step=step); wait_loaded(pg)
            expect(pg.get_by_test_id("how-summary")).to_be_visible()
            for k in ("how-chip-code", "how-chip-ai", "how-chip-you"):
                assert pg.get_by_test_id(k).count() == 1, (iid, k)
            open_panel(pg)
            code, ai, you = rows(pg)
            assert code.startswith(("Passed:", "Did not pass:", "No code check")), (iid, code)
            assert page_verdict(pg) in VERDICTS, (iid, page_verdict(pg))
            assert ai.strip() and "Checking" not in ai and "Checking" not in code, (iid, ai)
            assert you.strip() == "Waiting for you.", (iid, you)
            for k in ("how-code", "how-ai", "how-you"):
                expect(pg.get_by_test_id(k)).to_be_visible()
            y = pg.get_by_test_id("answer-yes").bounding_box(); assert y["y"] + y["height"] <= 900, f"{iid}: the primary action is below the fold"
            assert pg.evaluate("document.documentElement.scrollHeight <= window.innerHeight"), iid
        assert seen == [], seen
    finally:
        b.close()


def page_verdict(pg):
    return pg.get_by_test_id("how-verdict").inner_text()


def test_a_prepared_answer_says_it_was_prepared_and_then_checked_and_names_the_second_check(page, make):
    seen = watch(page)
    tok = make(); e = item(tok, "e1"); assert e["prepared"] is True
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    expect(page.get_by_test_id("how-prepared")).to_have_text("Prepared by our team; the second AI check then checked it against the quote.")
    code, ai, _ = rows(page)
    assert code.startswith("Passed:") and "word for word" in code, code
    assert page_verdict(page) == "Agrees" and "found every statement" in ai.lower(), ai
    assert page.get_by_test_id("how-ai-sub").inner_text().startswith("claude-haiku"), "the second check names its own model"
    page.get_by_test_id("how-all-checks").click()
    expect(page.get_by_test_id("how-all-list")).to_be_visible()
    assert page.get_by_test_id("how-all-list").locator("li").count() >= 5
    # an amount is code-made: no "prepared" line, but the same second check
    open_item(page, tok, "a1", step="bills"); wait_loaded(page); open_panel(page)
    assert page.get_by_test_id("how-prepared").count() == 0 and "amount appears in the record" in rows(page)[0]
    # a warning made by code needs no second check, and says why
    open_item(page, tok, "f_gap_r6_r7"); wait_loaded(page); open_panel(page)
    assert page_verdict(page) == "Not needed" and "worked out by code" in rows(page)[0]
    assert seen == [], seen


def test_your_decision_shows_in_the_you_row(page, make):
    seen = watch(page)
    tok = make(); open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "Waiting for you."
    page.get_by_test_id("answer-yes").click(); settle(page, 500)
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "You kept it in the letter."
    page.get_by_test_id("answer-no").click(); settle(page, 500)
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "You left it out of the letter."
    open_item(page, tok, "a1", step="bills"); page.get_by_test_id("answer-yes").click(); settle(page, 500)
    open_item(page, tok, "a1", step="bills"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "You counted it in the bill total."
    assert seen == [], seen


# ------------------------------------------------------------------------------------------------ a dispute or a failed check is shown in words

def rewrite_trace(page, fn):
    def h(route):
        r = route.fetch(); j = r.json(); fn(j); route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+/items/e2/trace$"), h)


def test_a_disputed_item_shows_disputes_with_the_servers_reason_and_a_failed_code_check_says_what_failed(page, make):
    seen = watch(page)
    tok = make()
    def fn(j):
        for s in j["steps"]:
            if s["id"] == "judge_1":
                s["status"] = "fail"; s["evidence"].update(judge_verdict="partially", judge_reason_code="DROPS_QUALIFIER", rationale="The summary leaves out a qualifier that the quote carries.")
            if s["id"] == "summary_tokens":
                s["status"] = "fail"; s["why"] = "The summary has a number that is not in the quote: 9."
    rewrite_trace(page, fn)
    open_item(page, tok, "e2"); wait_loaded(page); open_panel(page)
    code, ai, _ = rows(page)
    assert page_verdict(page) == "Disputes" and "leaves out a qualifier that the highlighted words carry" in ai, ai
    assert code.startswith("Did not pass:") and "number that is not in the highlighted words" in code, code
    expect(page.locator("[data-testid=how-chip-ai]")).to_have_text("AI: disputes"); expect(page.locator("[data-testid=how-chip-code]")).to_have_text("Code: not passed")
    assert seen == [], seen


def test_a_trace_that_cannot_be_read_says_so_and_the_item_still_works(page, make):
    tok = make()
    page.route(re.compile(r"/api/cases/[^/]+/items/e1/trace$"), lambda r: r.fulfill(status=500, json={"error": {"code": "x", "message": "x"}}))
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    code, ai, you = rows(page)
    assert "couldn't load" in code and "couldn't load" in ai and you == "Waiting for you."
    page.get_by_test_id("answer-yes").click(); settle(page, 500)
    assert page.get_by_test_id("card-line").get_attribute("data-item-id") != "e1" or page.get_by_test_id("done-heading").count()


# ------------------------------------------------------------------------------------------------ layout

def test_at_1440x900_the_panel_never_pushes_a_highlighted_word_or_the_primary_action_out_of_view(pw, make):
    tok = make(); b, pg = sized(pw, 1440, 900)
    try:
        seen = watch(pg)
        opened = 0
        for step, iid in (("timeline", "e1"), ("timeline", "e2"), ("timeline", "e4"), ("timeline", "f_gap_r6_r7"), ("timeline", "e6"), ("bills", "a1")):
            open_item(pg, tok, iid, step=step); wait_loaded(pg); settle(pg, 200)
            src = pg.get_by_test_id("card-source").bounding_box(); how = pg.get_by_test_id("how-checked").bounding_box()
            assert how["y"] >= src["y"] + src["height"] - 2, "the panel sits under the record, not over it"
            marks = pg.locator("[data-testid=card-source] mark")
            assert marks.count() >= 1
            for i in range(marks.count()):
                m = marks.nth(i).bounding_box()
                assert m["y"] >= src["y"] - 1 and m["y"] + m["height"] <= src["y"] + src["height"] + 1, f"{iid}: highlighted word {i} is in the record window"
            opened += pg.get_by_test_id("how-code").is_visible()
            expect(pg.get_by_test_id("how-summary")).to_be_visible()
            assert pg.get_by_test_id("answer-yes").is_visible() and pg.evaluate("document.documentElement.scrollHeight <= window.innerHeight")
        assert opened >= 1, "where there is room the rows are open without a click"
        assert seen == [], seen
    finally:
        b.close()


def test_at_390px_the_panel_is_a_strip_above_the_action_bar_closed_with_three_chips_and_opens_without_overflow(phone, make):
    seen = watch(phone)
    tok = make()
    for iid in ("e1", "f_r7_1"):
        open_item(phone, tok, iid); wait_loaded(phone)
        sm = phone.get_by_test_id("how-summary").bounding_box(); bar = phone.get_by_test_id("answer-yes").bounding_box()
        assert sm["y"] + sm["height"] <= bar["y"], f"{iid}: the strip is above the action bar with nothing scrolled"
        assert sm["y"] + sm["height"] <= 844 and sm["y"] >= 0
        assert phone.evaluate("document.querySelector('[data-testid=how-checked]').parentNode.getAttribute('data-testid')") == "actions"
    open_item(phone, tok, "e1"); wait_loaded(phone)
    for k, t in (("how-chip-code", "Code: passed"), ("how-chip-ai", "AI: agrees"), ("how-chip-you", "You: waiting")):
        assert phone.get_by_test_id(k).inner_text() == t
    assert phone.get_by_test_id("how-code").is_visible() is False
    y0 = phone.get_by_test_id("answer-yes").bounding_box()["y"]
    phone.get_by_test_id("how-summary").click()
    for k in ("how-code", "how-ai", "how-you"):
        expect(phone.get_by_test_id(k)).to_be_in_viewport()
    expect(phone.get_by_test_id("how-prepared")).to_be_visible()
    assert phone.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"), "no sideways scroll"
    ai = phone.get_by_test_id("how-ai").bounding_box(); assert ai["x"] + ai["width"] <= 390 + 1
    y = phone.get_by_test_id("answer-yes").bounding_box(); assert y["y"] == y0 and y["y"] + y["height"] <= 844, "opening moves nothing and the primary action is in view"
    assert seen == [], seen


# ------------------------------------------------------------------------------------------------ one statement from the judge's real state (r2)

def _step(status, verdict=None, why="", rationale=None, model=True):
    ev = {"model": {"role": "judge", "id": "claude-haiku-5-5"}} if model else {}
    if verdict: ev["judge_verdict"] = verdict
    if rationale: ev["rationale"] = rationale
    return {"steps": [{"id": "judge_4", "kind": "llm", "status": status, "why": why, "label": "second check", "evidence": ev}]}


# (name, trace, item.prepared) -> (word, chip, lead said?)
JUDGE_TABLE = [
    ("prepared, judge ran and agrees",        _step("pass", "supported", rationale="found every statement in the quote"), True,  "Agrees", "AI: agrees", True),
    ("live, judge ran and agrees",            _step("pass", "supported", rationale="found every statement in the quote"), False, "Agrees", "AI: agrees", False),
    ("prepared, judge ran and disputes",      _step("fail", "partially", rationale="the quote does not say this"),        True,  "Disputes", "AI: disputes", True),
    ("live, judge ran and disputes",          _step("fail", "unsupported", rationale="the quote does not say this"),      False, "Disputes", "AI: disputes", False),
    ("prepared, judge could not check",       _step("pass", "unsure", rationale="could not read it"),                     True,  "Could not check", "AI: could not check", True),
    ("prepared, no prepared answer, judge not run", _step("skipped", None, why="Not run: only the phrase list found this warning, so there is no prepared answer to double-check; it stays marked for review."), True,  "Not run", "AI: not run", False),
    ("live, judge not run (phrase list only)", _step("skipped", None, why="Not run: only the phrase list found this warning."),                                                  False, "Not run", "AI: not run", False),
    ("prepared, made by code, judge not needed", _step("skipped", None, why="Not needed: arithmetic over dates."),         True,  "Not needed", "AI: not needed", False),
    ("live, made by code, judge not needed",  _step("skipped", None, why="Not needed: arithmetic over dates."),           False, "Not needed", "AI: not needed", False),
    ("prepared, judge pending",               _step("pending", None, why="Waiting for the second check."),                True,  "Not run yet", "AI: not run yet", False),
    ("prepared, no judge step at all",        {"steps": []},                                                              True,  "Not run", "AI: not run", False),
    ("live, no trace",                        None,                                                                       False, "Not run", "AI: not run", False),
]


@pytest.mark.parametrize("name,trace,prepared,word,chip,lead", [r for r in JUDGE_TABLE], ids=[r[0] for r in JUDGE_TABLE])
def test_the_second_ai_row_is_one_statement_derived_from_the_judge_state(page, name, trace, prepared, word, chip, lead):
    page.goto(C.SERVER + "/"); page.wait_for_function("window.G && G.review && G.review.howJudge")
    j = page.evaluate("([t, p]) => G.review.howJudge(t, { prepared: p })", [trace, prepared])
    assert (j["word"], j["chip"], bool(j["lead"])) == (word, chip, lead), j
    # no row can say it checked and did not check: a lead only with a real verdict, and the text never contradicts the word
    said = (j["lead"] + " " + j["text"]).lower()
    if j["word"] in ("Not run", "Not run yet", "Not needed"):
        assert "then checked" not in said and not j["lead"], j
    if j["word"] in ("Agrees", "Disputes", "Could not check"):
        assert not said.lstrip().startswith("not run") and "no prepared answer" not in said, j


def test_f_r7_1_says_the_second_check_did_not_run_and_never_says_it_checked_a_prepared_answer(page, make):
    seen = watch(page)
    tok = make(); open_item(page, tok, "f_r7_1"); wait_loaded(page); open_panel(page)
    ai = page.get_by_test_id("how-ai-text").inner_text().lower()
    assert "then checked" not in ai and page.get_by_test_id("how-prepared").count() == 0, ai
    assert page_verdict(page) == "Not run" and page.get_by_test_id("how-chip-ai").inner_text() == "AI: not run"
    open_item(page, tok, "f_gap_r6_r7"); wait_loaded(page); open_panel(page)
    assert page_verdict(page) == "Not needed"
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    assert page_verdict(page) == "Agrees" and page.get_by_test_id("how-prepared").count() == 1
    assert seen == [], seen


# ------------------------------------------------------------------------------------------------ the page

@pytest.mark.parametrize("path_of", [lambda t: "/", lambda t: "/new", lambda t: f"/case/{t}/records", lambda t: f"/case/{t}/timeline", lambda t: f"/case/{t}/bills", lambda t: f"/case/{t}/letter"])
def test_every_screen_links_to_how_each_answer_is_checked(page, make, path_of):
    seen = watch(page)
    tok = make(); go(page, path_of(tok)); page.locator("#view[data-ready]").wait_for()
    link = page.get_by_test_id("link-how"); expect(link).to_be_visible(); expect(link).to_have_attribute("href", "/how-it-works")
    link.click(); expect(page).to_have_url(re.compile(r"/how-it-works$")); expect(page.get_by_test_id("page-title")).to_have_text("How each answer is checked")
    expect(page.get_by_test_id("link-how")).to_have_attribute("aria-current", "page")
    assert seen == [], seen


def explain_words(page):
    return len(re.findall(r"\w+", page.get_by_test_id("how-steps").inner_text()))


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_the_page_explains_the_ladder_shows_the_picture_and_names_code_and_ai(pw, w, h):
    b, pg = sized(pw, w, h)
    try:
        seen = watch(pg)
        go(pg, "/how-it-works"); pg.locator("#view[data-ready]").wait_for()
        assert 100 <= explain_words(pg) <= 200, explain_words(pg)
        text = pg.get_by_test_id("how-steps").inner_text()
        for must in ("Prepared by our team", "Code checks it", "A second AI checks it", "different model, with a different prompt", "You decide", "accept, edit or dismiss"):
            assert must in text, must
        note = pg.get_by_test_id("how-demo-note").inner_text()      # T-216 (UX M5): the demo says plainly that the second check's results were recorded, not run live
        assert "recorded when the demo was built" in note and "not run live" in note, note
        img = pg.get_by_test_id("how-ladder-img"); expect(img).to_be_visible()
        assert img.evaluate("e => e.complete && e.naturalWidth > 0"), "the validation-ladder picture loaded"
        assert (img.get_attribute("alt") or "").startswith("Validation ladder")
        body = pg.get_by_test_id("how-code-vs-ai").inner_text(); assert "Code only, never AI" in body and "AI, always checked" in body
        repo = pg.get_by_test_id("how-repo").inner_text()
        for name in ("docs/LLM_VS_CODE.md", "app/llm/prompts/", "evals/", "D-065", "D-066"):
            assert name in repo, name
        assert pg.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth"), "no sideways scroll"
        assert not re.search(r"\bAI draft\b|claude|sonnet", pg.get_by_test_id("how-page").inner_text(), re.I), "a prepared demo never calls the answers AI output"
        pg.get_by_test_id("how-back").click(); expect(pg.get_by_test_id("page-title")).to_have_text("Your cases")      # opened directly: Back goes to the cases
        assert seen == [], seen
    finally:
        b.close()


def test_the_picture_is_served_and_the_page_is_reachable_by_its_own_address(page):
    seen = watch(page)
    st, _ = C.api("GET", "/api/health"); assert st == 200
    go(page, "/how-it-works"); expect(page.get_by_test_id("how-page")).to_be_visible()
    r = page.request.get(C.SERVER + "/validation-ladder.svg"); assert r.status == 200 and "svg" in r.headers["content-type"] and "Validation ladder" in r.text()
    assert seen == [], seen


def test_back_returns_to_the_item_she_was_on(page, make):
    seen = watch(page)
    tok = make(); open_item(page, tok, "e2"); wait_loaded(page)
    page.get_by_test_id("link-how").click(); expect(page.get_by_test_id("how-page")).to_be_visible()
    page.get_by_test_id("how-back").click(); expect(page).to_have_url(re.compile(r"/timeline\?item=e2$"))
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e2")
    assert seen == [], seen


def test_t214_a_flag_only_code_found_says_so_on_its_tag_and_in_the_panel(page, make):
    seen = watch(page)
    tok = make(); f = item(tok, "f_r7_1")
    assert f["prepared"] is False and f["origin_label"] == "Found by code (phrase list)", f
    open_item(page, tok, "f_r7_1"); wait_loaded(page); open_panel(page)
    tags = page.locator("[data-testid=line-tag], [data-testid=line-tag2]").all_inner_texts()
    assert "Found by code (phrase list)" in tags and "Prepared answer" not in tags, tags
    assert page.get_by_test_id("how-origin").inner_text() == "Found by code (phrase list)." and page.get_by_test_id("how-prepared").count() == 0
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    tags = page.locator("[data-testid=line-tag], [data-testid=line-tag2]").all_inner_texts()
    assert "Prepared answer" in tags and page.get_by_test_id("how-origin").count() == 0, tags
    assert seen == [], seen
