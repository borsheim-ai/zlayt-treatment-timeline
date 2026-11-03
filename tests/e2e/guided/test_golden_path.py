"""T-181 (D-068) README golden path, smoke: in demo mode a first-time visitor opens `/`, clicks Open the sample case, drafts it and lands on Step 2 with an entry on screen.
Public/demo mode has no case list (GET /api/cases is 404 by design, spec 3.3), so the browser starts with an empty list and Home offers the sample. The route stub below makes the shared
local-mode test server answer like the public one. Step 2 itself is Builder B's page: this test needs it to show the entry text."""
import re
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided._helpers import api, browser, jbody, err
from tests.e2e.guided.test_shell_smoke import watch


def test_demo_sample_reachable_from_root(pw):
    br, page = browser(pw, 1440, 900)
    tok = None
    try:
        page.route("**/api/cases", lambda r: jbody(r, 404, err("not_found", "Not found.")) if r.request.method == "GET" else r.continue_())
        page.goto(C.SERVER + "/")
        page.get_by_test_id("btn-sample-case").click(timeout=10000)               # Open the sample case
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=10000)
        tok = page.url.split("/case/")[1].split("/")[0]
        page.get_by_test_id("btn-draft").click()                                   # Draft the timeline (instant on the prepared set)
        expect(page.get_by_test_id("draft-done")).to_be_visible(timeout=15000)
        page.get_by_test_id("btn-next-step").click()                               # Go to step 2: Check the timeline
        expect(page).to_have_url(re.compile(r"/case/[^/]+/timeline$"), timeout=10000)
        expect(page.get_by_test_id("page-title")).to_have_text("Check the timeline")
        first = api("GET", f"/api/cases/{tok}")[1]["entries"][0]["summary"][:30]
        expect(page.locator("body")).to_contain_text(first, timeout=10000)          # at least one entry is on screen
    finally:
        if tok:
            api("DELETE", f"/api/cases/{tok}")
        br.close()
