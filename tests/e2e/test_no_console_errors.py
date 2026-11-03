"""T-154 (lesson from commit 6379c0b): a ReferenceError inside the render path stopped every panel from drawing, and nothing in CI noticed because the specs that ran against the
dirty working tree were green. This is the pre-commit frontend smoke, so it is strict:
- every registered side panel (ZL.registerPanel callers in app/frontend) must mount its root element `[data-panel=<name>]` and draw content, on the sample case and on one library case;
- no uncaught page error, no console error, no failed request ('Failed to load resource' counts), and no error that reached window.onerror / unhandledrejection (hooked from before the app
  loads, so an error the app catches and re-raises, or a rejected promise nobody awaits, still fails the spec);
- no panel-error notice (the UI's own sign that one panel threw; ZL.panelFailed).
T-162 r3: with the panels listed by name, a throw in any one of them (not only the charges panel) fails here, which the first version of this spec did not."""
import os
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import BASE, api, open_case

# data-panel names, one per ZL.registerPanel/RV.registerPanel call in app/frontend (batch, audit, charges, export-settings, flags, manual). tests/unit/test_e2e_contract.py
# does not know this list, so test_every_registered_panel_is_listed greps the frontend for the registrations and fails if one is missing here.
PANELS = ("batch", "audit", "charges", "export-settings", "flags", "manual")
LIB = "case_lib06_lop_billed_vs_adjusted"

HOOK = """
window.__zlErrors = [];
window.addEventListener("error", (e) => window.__zlErrors.push("window.onerror: " + (e.message || e.error)));
window.addEventListener("unhandledrejection", (e) => window.__zlErrors.push("unhandledrejection: " + (e.reason && e.reason.message || e.reason)));
"""


def _watch(page):
    """pageerror + console.error from Playwright, and window.onerror / unhandledrejection from a hook installed before any app script runs (read with _hooked)."""
    seen = []
    page.add_init_script(HOOK)
    page.on("pageerror", lambda e: seen.append("pageerror: " + str(e)))
    page.on("console", lambda m: seen.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    return seen


def _hooked(page):
    return page.evaluate("window.__zlErrors || []")


@pytest.fixture
def library_case():
    st, c = api("POST", "/api/cases", {"library": LIB})
    if st not in (200, 201):
        if os.environ.get("E2E_REQUIRE_DB") == "1":
            pytest.fail("library cases need ZLAYT_MODE=local")
        pytest.skip("library cases need ZLAYT_MODE=local")
    tok = c["token"]
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")


def _loads_clean(page, tok, what):
    seen = _watch(page)
    page.goto(f"{BASE}/#/")
    page.wait_for_load_state("networkidle")
    open_case(page, tok)
    for name in PANELS:
        panel = page.locator(f'[data-panel="{name}"]')
        expect(panel, f"side panel {name!r} did not mount its root element on {what}").to_have_count(1)
        if name == "batch":   # a host section: its output is the Accept-all bar in the Timeline toolbar
            expect(page.locator(".toolbar > .rv-batchbar"), f"the batch panel drew no Accept-all bar on {what}").to_have_count(1)
        elif name != "manual":   # manual is a host section too: it adds its control to unclear and missing-entry cards and has no text of its own on a case without any
            expect(panel, f"side panel {name!r} mounted but drew nothing on {what}").to_have_text(re.compile(r"\S"))
    expect(page.get_by_test_id("panel-error"), "a side panel reported that it threw").to_have_count(0)
    assert not page.get_by_test_id("run-error").count() or not page.get_by_test_id("run-error").is_visible(), page.get_by_test_id("run-error").inner_text()
    page.wait_for_load_state("networkidle")
    seen += _hooked(page)
    assert not seen, f"the page logged errors while loading {what}:\n" + "\n".join(seen)


def test_the_sample_case_loads_with_every_panel_mounted_and_no_errors(page, sample_case):
    _loads_clean(page, sample_case, "the sample case")


def test_a_library_case_loads_with_every_panel_mounted_and_no_errors(page, library_case):
    _loads_clean(page, library_case, "a library case")


def test_every_registered_panel_is_listed():
    """A new panel must be added to PANELS, or this smoke stays blind to it (the T-162 r2 finding: 4 of 7 panels were unwatched)."""
    root = os.path.join(os.path.dirname(__file__), "..", "..", "app", "frontend")
    registered = set()
    # only the scripts the classic page loads: a stale file left in a reused directory (a deleted narrative.js, T-181 r2 reviewer) is not a panel
    loaded = re.findall(r'<script src="([^"/]+\.js)"', open(os.path.join(root, "index.html")).read())
    assert loaded, "index.html loads no scripts"
    for f in loaded:
        registered |= set(re.findall(r'RV\.registerPanel\("([a-z-]+)"', open(os.path.join(root, f)).read()))
    assert registered == set(PANELS), f"registered panels {sorted(registered)} differ from PANELS {sorted(PANELS)}"


def test_a_key_press_on_a_review_row_raises_no_console_error(page, sample_case):
    """The keydown handler is the other place a stray undefined name hides: press each single-key shortcut that changes nothing (j, k, o is skipped: it opens a drawer) on a focused row."""
    seen = _watch(page)
    open_case(page, sample_case)
    row = page.locator("[data-item-id]").first
    row.scroll_into_view_if_needed(); row.focus()
    for k in ("j", "k", "j", "?"):
        page.keyboard.press(k)
    page.keyboard.press("Escape")
    page.keyboard.press("a")   # accepts the focused item or says why it cannot: either way no script error
    page.wait_for_timeout(500)
    seen += _hooked(page)
    assert not seen, "the page logged errors on key presses:\n" + "\n".join(seen)
