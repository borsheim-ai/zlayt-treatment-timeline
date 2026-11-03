"""T-177 / D-065 (GATE-M3 product-manager blocker): the demo never shows a hand-checked (curated) answer as the AI's.
Acceptance test (the PM's), curated set (the default private server, FIXTURE_SET=curated): no element names 'AI draft' or 'recorded AI answers' for a curated item; the badge says the answers were
prepared by the team and its tooltip says the team prepared them and a second AI model checked them; /items/e1/trace's generator step is not claude-sonnet-5-5 and names a prepared answer; /audit rows for the generator carry
model 'hand-checked (qa)'. Recorded set (a second private server, no FIXTURE_SET): the labels say AI and the model ids are real.
New test ids (declared in tests/e2e/conftest.py, 'T-177'): tag-prepared, tag-ai-draft, audit-prepared."""
import json
import os
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

import pytest
from playwright.sync_api import expect
from tests.e2e import conftest as _C
from tests.e2e.conftest import api, open_case, reveal, ROOT, BASE

def _classic():
    return _C.BASE[len(getattr(_C, "SERVER", _C.BASE)):]      # "/classic" once the old screen moved there (D-068), "" before; a private server is opened at base + CLASSIC
PREPARED = "hand-checked (qa)"
WHY = "Prepared answer (hand-checked by the team for the demo)"      # D-069: the "standing in for the AI draft" tail is gone; only the badge tooltip may say AI
TOOLTIP = "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."      # T-177 r2 F2: points at nothing that is not there


def _ready(call, tok):
    for _ in range(300):
        s = call("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def curated_case():
    st, c = api("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(api, tok)
    yield tok
    api("DELETE", f"/api/cases/{tok}")


@pytest.fixture(scope="module")
def recorded_server():
    """A private app on its own port with the recorded (real model answers) fixture set: FIXTURE_SET unset."""
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-rec-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", ZLAYT_DB=os.path.join(tmp, "rec.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None); env.pop("FIXTURE_SET", None); env.pop("LLM_FIXTURE_DIR", None); env.pop("ENABLE_LIVE", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    for _ in range(80):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
        except Exception:
            assert proc.poll() is None, "the recorded-set server exited"
            time.sleep(.5)
    else:
        proc.kill(); pytest.fail("the recorded-set server did not start")

    def call(method, path, body=None):
        req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    yield base, call
    proc.terminate()
    try: proc.wait(timeout=10)
    except Exception: proc.kill()
    log.close()


def _open_why(page, n):
    reveal(page.get_by_test_id(f"entry-{n}").get_by_test_id("entry-why")).click()
    page.get_by_test_id("item-stepper").wait_for()
    return page.get_by_test_id("item-stepper")


# ---- the PM's acceptance test: API half (curated)
def test_curated_trace_and_audit_say_prepared(curated_case):
    tok = curated_case
    tr = api("GET", f"/api/cases/{tok}/items/e1/trace")[1]
    gen = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert gen["evidence"]["model"]["id"] != "claude-sonnet-5-5" and gen["evidence"]["model"]["id"] == PREPARED and gen["evidence"]["model"]["prepared"] is True
    assert gen["why"] == WHY and "prepared answer" in gen["why"].lower()
    audit = api("GET", f"/api/cases/{tok}/audit")[1]["calls"]
    gens = [c for c in audit if c["role"] == "generator"]
    assert gens and all(c["model"] == PREPARED and c["prepared"] is True for c in gens), [(c["step"], c["model"]) for c in gens]
    assert not any(c["model"] == "claude-sonnet-5-5" for c in gens)
    item = api("GET", f"/api/cases/{tok}/items/e1")[1]["item"]
    assert item["prepared"] is True and item["ladder"]["generator"]["model"] == PREPARED
    assert api("GET", "/api/health")[1]["answers"] == "prepared"


# ---- the PM's acceptance test: page half (curated)
def test_curated_page_never_calls_a_prepared_answer_ai(page, curated_case):
    open_case(page, curated_case)
    badge = page.locator("#badge")
    expect(badge).to_have_text("Demo: sample answers prepared by our team")
    assert badge.get_attribute("title") == TOOLTIP
    entries = page.locator("[data-testid^=entry-][data-entry-id]")
    n = entries.count(); assert n >= 9
    assert page.get_by_test_id("tag-prepared").count() == n and page.get_by_test_id("tag-ai-draft").count() == 0
    assert page.get_by_test_id("tag-prepared").first.inner_text() == "Prepared answer"
    text = page.evaluate("document.body.innerText")
    assert "AI draft" not in text and "recorded AI answers" not in text, re.findall(r".{20}(?:AI draft|recorded AI answers).{20}", text)
    assert page.locator("[title*='Drafted by AI'], [aria-label*='AI draft']").count() == 0
    assert "drafted by AI" not in page.locator("#banner-ai").inner_text() and "prepared by our team" in page.locator("#banner-ai").inner_text()
    st = _open_why(page, 1)
    gen = st.get_by_test_id("step").first
    assert gen.get_by_test_id("step-kind").inner_text() == "Prepared answer"
    body = st.inner_text()
    assert WHY in body
    assert "AI draft" not in body and "claude-sonnet-5-5" not in body and "The AI read this record" not in body


def test_curated_audit_drawer_marks_the_prepared_rows(page, curated_case):
    open_case(page, curated_case)
    reveal(page.get_by_test_id("entry-1").get_by_test_id("btn-audit")).click()
    page.get_by_test_id("audit-drawer").wait_for()
    drawer = page.get_by_test_id("audit-drawer")
    expect(drawer.get_by_test_id("audit-prepared").first).to_have_text("Prepared answer")
    assert PREPARED in drawer.inner_text() and "claude-sonnet-5-5" not in drawer.inner_text()


# ---- recorded set: the labels say AI
def test_recorded_set_labels_say_ai(pw, recorded_server):
    base, call = recorded_server
    st, c = call("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); tok = c["token"]
    assert call("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(call, tok)
    assert call("GET", "/api/health")[1]["answers"] == "recorded"
    tr = call("GET", f"/api/cases/{tok}/items/e1/trace")[1]
    gen = next(s for s in tr["steps"] if s["id"] == "extracted")
    assert gen["evidence"]["model"]["id"] == "claude-sonnet-5-5" and gen["evidence"]["model"]["prepared"] is False
    assert gen["why"] == "The AI read this record and proposed a one-line summary and a quote."
    calls = call("GET", f"/api/cases/{tok}/audit")[1]["calls"]
    assert calls and not any(x["prepared"] or x["model"] == PREPARED for x in calls)
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    try:
        pg.goto(f"{base}{_classic()}/#/case/{tok}"); pg.get_by_test_id("timeline").wait_for(timeout=15000)
        expect(pg.locator("#badge")).to_have_text("Demo: recorded AI answers")
        assert pg.get_by_test_id("tag-prepared").count() == 0 and pg.get_by_test_id("tag-ai-draft").count() >= 1
        assert "prepared by our team" not in pg.evaluate("document.body.innerText")
        st_ = _open_why(pg, 1)
        assert st_.get_by_test_id("step").first.get_by_test_id("step-kind").inner_text() == "AI draft"
    finally:
        b.close()


# ---- T-177 round 2 (staff-engineer F1/F2/F3/F5): every surface, curated and recorded
def _scan(page):
    """Everything the page holds for a reader: all text (open or closed panels) and every title / aria-label, as one string."""
    return page.evaluate("""() => { const out = [document.documentElement.textContent];
      document.querySelectorAll('[title],[aria-label]').forEach(e => out.push(e.getAttribute('title') || '', e.getAttribute('aria-label') || ''));
      return out.join(' | '); }""")


def _open_judges(page):
    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
    if not jp.locator("details.zj-det").evaluate("d => d.open"):
        jp.get_by_test_id("judge-summary").click()
    jp.get_by_test_id("judge-totals").wait_for()
    return jp


def test_curated_judge_panel_does_not_name_a_drafting_model(page, curated_case):
    open_case(page, curated_case)
    jp = _open_judges(page)
    line = jp.get_by_test_id("judge-model-line").inner_text()
    assert "claude-sonnet-5-5" not in line and "Drafted by" not in line, line
    assert "prepared by our team" in line.lower() and "not by an AI model" in line and "claude-haiku-5-5" in line, line
    label = jp.get_by_test_id("judge-label").inner_text()
    assert "first AI" not in label and "AI's drafts" not in label and "answers our team prepared" in label and "second AI model" in label, label
    assert "not a verdict" in label


def test_curated_every_surface_is_free_of_the_drafting_model(page, curated_case):
    """The judge panel, the Why dialog (stepper and recorded ladder), the audit drawer, tooltips and the banner, all open at once: no 'claude-sonnet', no 'Drafted by AI', no 'AI draft'."""
    open_case(page, curated_case)
    _open_judges(page)
    _open_why(page, 1)
    ladder = page.get_by_test_id("why-ladder")
    assert ladder.count() == 1
    assert ladder.get_by_test_id("why-generator").text_content() == PREPARED, ladder.get_by_test_id("why-generator").text_content()   # no prompt version: no prompt made it
    dts = ladder.locator("dt").all_text_contents()
    assert "Drafted by" not in dts and "Prepared by" in dts and "AI draft" not in dts and "Prepared answer" in dts
    page.keyboard.press("Escape")
    reveal(page.get_by_test_id("entry-1").get_by_test_id("btn-audit")).click()
    drawer = page.get_by_test_id("audit-drawer"); drawer.wait_for()
    drawer.get_by_test_id("audit-prepared").first.wait_for()
    gen_rows = drawer.get_by_test_id("audit-call").filter(has=page.get_by_test_id("audit-prepared"))
    assert gen_rows.count() >= 1
    for i in range(gen_rows.count()):
        t = gen_rows.nth(i).inner_text()
        assert "extract_v1" not in t and "hash" not in t and "sent to the model" not in t, t      # no prompt made a prepared answer
    text = _scan(page)
    for bad in ("claude-sonnet", "Drafted by AI", "drafted by AI", "AI draft", "recorded AI answers", "The AI's own answers"):
        assert bad not in text, (bad, re.findall(r".{30}" + re.escape(bad) + ".{30}", text)[:3])


def test_recorded_judge_panel_still_names_the_drafting_model(pw, recorded_server):
    base, call = recorded_server
    st, c = call("POST", "/api/cases", {"sample": True, "title": "Rivera v. Northgate (MVA 2026-01)"}); tok = c["token"]
    assert call("POST", f"/api/cases/{tok}/run", {})[0] == 202
    _ready(call, tok)
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1280, "height": 900}).new_page()
    try:
        pg.goto(f"{base}{_classic()}/#/case/{tok}"); pg.get_by_test_id("timeline").wait_for(timeout=15000)
        jp = _open_judges(pg)
        line = jp.get_by_test_id("judge-model-line").inner_text()
        assert "Drafted by claude-sonnet-5-5" in line and "claude-haiku-5-5" in line and "prepared" not in line.lower(), line
        assert "first AI's drafts" in jp.get_by_test_id("judge-label").inner_text()
        _open_why(pg, 1)
        ladder = pg.get_by_test_id("why-ladder")
        gt = ladder.get_by_test_id("why-generator").text_content()      # the Recorded ladder is a closed <details>: read its text, not its rendering
        assert "claude-sonnet-5-5" in gt and "extract_v1" in gt, gt
        dts = ladder.locator("dt").all_text_contents()
        assert "Drafted by" in dts and "AI draft" in dts
        assert "second AI model" in pg.locator("#banner-ai").inner_text() or "drafted by AI" in pg.locator("#banner-ai").inner_text()
    finally:
        b.close()
