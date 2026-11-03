"""T-181 (D-068) guided shell smoke: every route loads with no console errors, and the chrome (banner, header, step bar) never moves.
The guided app is served at the root of the server (real paths: /, /new, /case/<token>/records|timeline|bills|letter); the old screen is at /classic (tests/e2e keeps guarding it).
Shell test ids: banner-synthetic, app-header, demo-badge (the pill; absent when not a demo), btn-theme, step-bar, step-1..step-4 (links; aria-current=step on the open one; a locked step is a span with
aria-disabled), view (the page container; data-ready=1 once the page's first paint is done; data-route=<name>), page-title (the h1, set by each page), page-error, btn-retry, link-home, footer-note, case-title,
btn-your-cases. Step builders: use these helpers (go, rect, watch) from this module in their own specs."""
import urllib.request
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C

HOOK = """
window.__errs = [];
window.addEventListener("error", (e) => window.__errs.push("window.onerror: " + (e.message || e.error)));
window.addEventListener("unhandledrejection", (e) => window.__errs.push("unhandledrejection: " + (e.reason && e.reason.message || e.reason)));
"""
CHROME = ("[data-testid=banner-synthetic]", "[data-testid=app-header]", "[data-testid=step-bar]")
LABELS = ["1 Add records", "2 Check the timeline", "3 Check the bills", "4 Get your letter"]


def watch(page, allow_404=()):
    """pageerror, console.error, failed requests (an asset 404 counts) and window.onerror / unhandledrejection (a hook that runs before any page script). Returns the list to assert empty."""
    seen = []
    page.add_init_script(HOOK)
    page.on("pageerror", lambda e: seen.append("pageerror: " + str(e)))
    page.on("console", lambda m: seen.append("console." + m.type + ": " + m.text) if m.type == "error" and not any(a in m.text for a in allow_404) else None)
    page.on("response", lambda r: seen.append(f"http {r.status}: {r.url}") if r.status >= 400 and not any(a in r.url for a in allow_404) else None)
    page.on("requestfailed", lambda r: seen.append("requestfailed: " + r.url) if "ERR_ABORTED" not in (r.failure or "") else None)      # a fetch the app aborted on purpose when she moved on is not a failure
    return seen


def go(page, path="/"):
    page.goto(C.SERVER + path)
    page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000)


def rect(page, sel):
    return page.evaluate("(s) => { const r = document.querySelector(s).getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round); }", sel)


def chrome(page):
    return {s: rect(page, s) for s in CHROME}


def case_paths(tok):
    return [f"/case/{tok}/{p}" for p in ("records", "timeline", "bills", "letter")]


def test_every_route_loads_with_no_console_errors(page, sample_case):
    seen = watch(page)
    for path in ["/", "/new"] + case_paths(sample_case) + [f"/case/{sample_case}/timeline?item=e3"]:
        go(page, path)
        page.wait_for_timeout(250)
        assert page.get_by_test_id("page-title").first.inner_text().strip(), path
        assert "Synthetic data only" in page.get_by_test_id("banner-synthetic").inner_text()
        assert page.get_by_test_id("app-header").is_visible() and page.get_by_test_id("footer-note").count() == 1
        assert page.get_by_test_id("page-error").count() == 0, path
        assert (page.evaluate("window.__errs") or []) == [], path
    assert seen == [], seen


def test_banner_demo_label_and_footer_follow_health_answers(page):
    go(page)
    hl = C.api("GET", "/api/health")[1]
    badge = page.get_by_test_id("demo-badge")
    if hl["demo_mode"]:
        label = "Demo: sample answers prepared by our team" if hl["answers"] == "prepared" else "Demo: recorded AI answers"
        expect(badge).to_have_text(label)
        note = page.get_by_test_id("footer-note").inner_text()
        if hl["answers"] == "prepared":      # D-065 (amended T-177 r2): say whose answers these are, and that a second AI model checked them
            assert label in note and "not written by an AI model" in note and "A second AI model then checked each answer against its quote." in note
            assert "not written by an AI model" in badge.get_attribute("title")
        else:
            assert label in note and "real AI answers recorded earlier" in note
    else:
        expect(badge).to_have_count(0)


def test_step_bar_per_route(page, sample_case):
    go(page)
    expect(page.get_by_test_id("step-bar")).to_be_hidden()
    expect(page.get_by_test_id("btn-theme")).to_be_visible()
    go(page, "/new")
    for n in (1, 2, 3, 4):
        s = page.get_by_test_id(f"step-{n}")
        assert (s.get_attribute("aria-current") == "step") == (n == 1)
        assert (s.get_attribute("aria-disabled") == "true") == (n > 1), n
    assert page.get_by_test_id("case-title").inner_text() == "New case"
    for n, path in enumerate(case_paths(sample_case), 1):
        go(page, path)
        labels = [page.get_by_test_id(f"step-{k}").locator(".st-label .long").inner_text() for k in (1, 2, 3, 4)]
        assert labels == LABELS
        for k in (1, 2, 3, 4):
            s = page.get_by_test_id(f"step-{k}")
            assert (s.get_attribute("aria-current") == "step") == (k == n), (path, k)
            assert s.get_attribute("aria-disabled") is None and s.evaluate("e => e.tagName") == "A"
        assert page.get_by_test_id("page-title").first.is_visible()
    # a ready sample case: step 1 done, its steps 2 and 3 carry the counts the data rules give, step 4 is not yet
    go(page, case_paths(sample_case)[0])
    status = [page.get_by_test_id(f"step-{k}").locator(".st-status").inner_text() for k in (1, 2, 3, 4)]
    case = C.api("GET", f"/api/cases/{sample_case}")[1]
    s2 = [i for i in case["entries"] + case["undated_entries"] + case["flags"] if i["state"] != "rejected"]
    s3 = [i for i in case["amounts"] if i["state"] != "rejected"]
    assert status[0] == "Done" and status[1] == f"{len(s2)} of {len(s2)} left" and status[2] == f"{len(s3)} amounts" and status[3] == "Not yet", status
    assert page.get_by_test_id("case-title").inner_text() == case["title"]


def test_chrome_never_moves_between_pages_layouts_or_scrolling(page, sample_case):
    seen = watch(page)
    go(page, case_paths(sample_case)[0])
    first = chrome(page)
    assert first["[data-testid=banner-synthetic]"][1] == 0 and first["[data-testid=app-header]"][1] == first["[data-testid=banner-synthetic]"][3]
    assert first["[data-testid=step-bar]"][1] == first["[data-testid=app-header]"][1] + first["[data-testid=app-header]"][3]
    for n in (2, 3, 4, 1, 3):                    # by clicking the bar, as a person would: page layout, frame layout, page, page, frame
        page.get_by_test_id(f"step-{n}").click()
        expect(page.get_by_test_id(f"step-{n}")).to_have_attribute("aria-current", "step")
        page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
        assert chrome(page) == first, n
    expect(page.locator("body")).to_have_class("frame")
    go(page, case_paths(sample_case)[3])         # a page-layout page: the chrome is sticky, so it stays when the page scrolls
    page.evaluate("document.querySelector('main').append(Object.assign(document.createElement('div'), { className: 'spacer-test' })); document.querySelector('.spacer-test').style.height = '4000px'")
    page.mouse.wheel(0, 1500); page.wait_for_timeout(200)
    assert page.evaluate("window.scrollY") > 500
    assert chrome(page) == first, "the chrome moved when the page scrolled"
    assert seen == [], seen


def test_the_frame_fits_the_window_and_pages_have_no_sideways_scroll(page, sample_case):
    for w, h in ((1280, 800), (390, 844)):
        page.set_viewport_size({"width": w, "height": h})
        for path in ["/"] + case_paths(sample_case):
            go(page, path)
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"sideways scroll at {w}: {path}"
            if path.endswith(("timeline", "bills")):
                assert page.evaluate("document.documentElement.scrollHeight <= window.innerHeight"), f"the frame scrolls the document at {w}: {path}"
                assert rect(page, ".actions")[1] + rect(page, ".actions")[3] == h, f"the action bar is not at the bottom at {w}: {path}"
        b = rect(page, "[data-testid=step-bar]"); assert b[3] > 0
        for n in (1, 2, 3, 4):
            sb = page.get_by_test_id(f"step-{n}").bounding_box(); assert sb and sb["x"] >= 0 and sb["x"] + sb["width"] <= w, (w, n, sb)


def test_links_route_without_a_reload_and_back_and_deep_links_work(page, sample_case):
    seen = watch(page)
    go(page, case_paths(sample_case)[0])
    page.evaluate("window.__marker = 42")
    page.get_by_test_id("step-3").click()
    expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "bills")
    assert page.url.endswith(f"/case/{sample_case}/bills") and page.evaluate("window.__marker") == 42, "a click must not reload the page"
    page.get_by_test_id("step-4").click()
    expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "letter")
    page.go_back(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "bills")
    page.go_back(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "records")
    assert page.evaluate("window.__marker") == 42
    page.get_by_test_id("btn-your-cases").click()
    expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "home"); expect(page.get_by_test_id("step-bar")).to_be_hidden()
    go(page, f"/case/{sample_case}/timeline?item=e3")                 # a reload of a deep link lands on the same screen
    assert page.locator("[data-testid=view]").get_attribute("data-route") == "timeline" and page.evaluate("location.search") == "?item=e3"
    go(page, f"/case/{sample_case}")                                  # a bare case link opens step 1
    assert page.url.endswith(f"/case/{sample_case}/records")
    assert seen == [], seen


def test_bad_links_and_unknown_cases_are_plain(page):
    seen = watch(page, allow_404=("/api/cases/",))
    go(page, "/nonsense/here")
    assert "couldn't find that page" in page.get_by_test_id("page-title").inner_text()
    page.get_by_test_id("link-home").click(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "home")
    go(page, "/case/does-not-exist/timeline")
    assert "no longer here" in page.get_by_test_id("page-title").inner_text()
    body = page.locator("body").inner_text()
    assert "Failed to fetch" not in body and "404" not in body
    expect(page.get_by_test_id("link-home")).to_be_visible(); expect(page.get_by_test_id("step-bar")).to_be_visible()
    assert [s for s in seen if "does-not-exist" not in s and "Failed to load resource" not in s] == [], seen


def test_theme_button_switches_between_light_and_dark(page):
    page.emulate_media(color_scheme="light")
    go(page); page.evaluate("localStorage.removeItem('zl.guided.theme')"); page.reload(); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
    light = page.evaluate("getComputedStyle(document.body).backgroundColor")
    expect(page.get_by_test_id("btn-theme")).to_have_text("Dark mode")
    page.get_by_test_id("btn-theme").click()
    assert page.evaluate("document.documentElement.getAttribute('data-theme')") == "dark"
    expect(page.get_by_test_id("btn-theme")).to_have_text("Light mode")
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") != light
    page.reload(); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
    assert page.evaluate("document.documentElement.getAttribute('data-theme')") == "dark", "the pick is remembered"
    page.evaluate("localStorage.removeItem('zl.guided.theme')"); page.emulate_media(color_scheme="dark"); page.reload(); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
    assert page.evaluate("getComputedStyle(document.body).backgroundColor") != light, "dark follows the OS"


def test_step_rules_in_the_browser(page):
    go(page)
    out = page.evaluate("""() => {
      const it = (s, extra) => Object.assign({ state: "verified", review_status: s }, extra || {});
      const S = (c, here) => G.steps.states(c, here).map((s) => s.state + ":" + s.status);
      return {
        ingested: S({ status: "ingested", entries: [] }),
        running: S({ status: "running", entries: [] }),
        failedItems: S({ status: "failed", entries: [it("pending")] }),
        failedNone: S({ status: "failed", entries: [] }),
        fresh: S({ status: "ready", entries: [it("pending"), it("accepted")], flags: [it("pending")], amounts: [it("pending"), it("pending")], review: {} }, 2),
        editToCheck: S({ status: "ready", entries: [it("edited", { edit_to_check: true })], amounts: [], review: {} }, 2),
        rejectedIgnored: S({ status: "ready", entries: [it("accepted"), it("pending", { state: "rejected" })], amounts: [it("accepted")], review: { ready_to_export: true } }, 3),
        leftBehind: S({ status: "ready", entries: [it("pending")], amounts: [it("pending")], review: {} }, 4),
        summary: S({ status: "ready", progress: { entries: { decided: 9, total: 9 }, flags: { decided: 8, total: 10 }, amounts: { decided: 4, total: 4 } }, export_ready: false }),
        summaryReady: S({ status: "ready", progress: { entries: { decided: 9, total: 9 }, flags: { decided: 10, total: 10 }, amounts: { decided: 4, total: 4 } }, export_ready: true }),
      };
    }""")
    L = "locked:After step 1"
    assert out["ingested"] == ["todo:Not started", L, L, L]
    assert out["running"][0] == "todo:Drafting" and out["running"][1:] == [L, L, L]
    assert out["failedItems"][0] == "attn:Run again" and out["failedItems"][1] == "todo:1 of 1 left", "a stopped run with items opens steps 2-3"
    assert out["failedNone"] == ["attn:Run again", L, L, L]
    assert out["fresh"] == ["done:Done", "todo:2 of 3 left", "todo:2 amounts", "todo:Not yet"]
    assert out["editToCheck"][1] == "todo:1 of 1 left", "an edit still to check is undecided"
    assert out["rejectedIgnored"] == ["done:Done", "done:Done", "done:Done", "todo:Ready"]
    assert out["leftBehind"][1] == "attn:1 of 1 left" and out["leftBehind"][2] == "attn:1 amount", "a step left with undecided items needs a look"
    assert out["summary"][1] == "todo:2 of 19 left" and out["summary"][2] == "done:Done" and out["summary"][3] == "todo:Not yet"
    assert out["summaryReady"] == ["done:Done", "done:Done", "done:Done", "todo:Ready"]


def test_the_api_wrapper_turns_failures_into_plain_messages(page):
    go(page)
    out = page.evaluate("""async () => {
      const r = {};
      try { await G.api.getCase("does-not-exist"); } catch (e) { r.missing = [e instanceof G.ApiError, e.status, e.message]; }
      const real = window.fetch; window.fetch = () => Promise.reject(new TypeError("Failed to fetch"));
      try { await G.api.cases(); } catch (e) { r.offline = [e instanceof G.ApiError, e.status, e.message]; }
      window.fetch = () => Promise.resolve(new Response("<html>boom</html>", { status: 500 }));
      try { await G.api.cases(); } catch (e) { r.server = [e instanceof G.ApiError, e.status, e.message]; }
      window.fetch = real;
      return r;
    }""")
    for k, (is_err, status, msg) in out.items():
        assert is_err, k
        assert not any(bad in msg for bad in ("Failed to fetch", "boom", "<html", "500", "404", "Request failed")), (k, msg)
    assert out["offline"][1] == 0 and out["server"][1] == 500 and out["missing"][1] == 404
    assert out["offline"][2].startswith("We couldn't reach")


def test_a_page_that_throws_shows_a_plain_error_block_with_a_way_home(page, sample_case):
    seen = watch(page)
    go(page, f"/case/{sample_case}/timeline")
    page.evaluate("void (window.G.pages.bills = async () => { throw new window.G.ApiError(0, null); })")
    page.get_by_test_id("step-3").click()
    expect(page.get_by_test_id("page-error")).to_contain_text("We couldn't reach the app")
    expect(page.get_by_test_id("btn-retry")).to_be_visible(); expect(page.get_by_test_id("link-home")).to_be_visible(); expect(page.get_by_test_id("step-bar")).to_be_visible()
    assert seen == [], seen


def test_the_server_sends_the_csp_and_serves_classic_next_to_guided(page):
    for path in ("/", "/new", "/case/x/timeline", "/classic/", "/classic"):
        with urllib.request.urlopen(C.SERVER + path, timeout=10) as r:
            assert "script-src 'self'" in r.headers["Content-Security-Policy"], path
    try:
        urllib.request.urlopen(C.SERVER + "/api/nope", timeout=10); raise AssertionError("an unknown /api path must stay a 404")
    except urllib.error.HTTPError as e:
        assert e.code == 404 and "json" in e.headers["Content-Type"]
    seen = watch(page)
    page.goto(C.SERVER + "/classic"); page.get_by_test_id("btn-sample").wait_for(timeout=15000)
    assert seen == [], seen
    assert page.get_by_test_id("banner-synthetic").is_visible() and page.locator("#view").count() == 0, "/classic is the old screen"


def test_footer_and_chrome_never_print_the_word_null(page, sample_case):
    """replaceChildren(a, null) writes the text "null": the footer (no retention sentence in demo mode) and the rest of the chrome must not."""
    for path in ("/", "/new", f"/case/{sample_case}/records"):
        go(page, path)
        for sel in ("#footer", "#header", "[data-testid=banner-synthetic]", "[data-testid=step-bar]"):
            assert "null" not in page.locator(sel).inner_text().lower().split(), (path, sel)
        assert page.get_by_test_id("footer-note").count() == 1 and page.locator("#footer").evaluate("e => e.childNodes.length") == (2 if C.api("GET", "/api/health")[1]["demo_mode"] is False else 1)
