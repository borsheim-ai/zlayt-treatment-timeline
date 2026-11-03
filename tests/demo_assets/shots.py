"""T-184 final screenshots of every state in docs/GUIDED_UI_SPEC.md, 1440x900 and 390x844, from a `git archive` copy of one commit running in demo mode.
Usage: .venv/bin/python tests/demo_assets/shots.py [--rev HEAD] [--stage main|letter|all] [--out artifacts/screenshots/final]
Stages: `main` = everything except the letter screens; `letter` = Your cases (with a finished case), Step 4 (ready, numbered, pending, blocked), run LAST because the letter text may still change.
Every shot is a real page of the real app. Four states cannot happen on the curated demo set and are produced by answering the page's own request with a stub, named in CAPTIONS:
loading (slow list), list error (500), drafting (status poll says running), stopped (case says failed). Nothing else is stubbed."""
import argparse
import json
import pathlib
import subprocess
import sys
import textwrap
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from playwright.sync_api import sync_playwright, expect  # noqa: E402
from tests.demo_assets import common as K  # noqa: E402

LIB02, LIB09, LIB10, LIB11 = "case_lib02_slip_fall_prior_knee", "case_lib09_spanish_interpreter_espalda", "case_lib10_eob_ub04_cms1500", "case_lib11_priors_and_ledger"
SIZES = {"1440": (1440, 900), "390": (390, 844)}
STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
CAP = {}     # name -> caption, filled by the states below


class Run:
    def __init__(self, pw, base, db, src, out):
        self.pw, self.base, self.db, self.src, self.out = pw, base, db, src, out
        self.done = []

    def api(self, m, p, b=None):
        return K.api(self.base, m, p, b)

    def case(self, title=None, lib=None, run=True):
        return K.make_case(self.base, title, lib, run)

    def decide(self, tok, groups=("entries", "undated_entries", "flags", "amounts"), skip=()):
        c = self.api("GET", f"/api/cases/{tok}")[1]
        for g in groups:
            for i in c[g]:
                if i["id"] in skip or i.get("state") == "rejected":
                    continue
                body = {"action": "accept"}
                if self.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", body)[0] == 422:
                    body["compared"] = True
                    st, r = self.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", body)
                    assert st == 200, (i["id"], st, r)

    def tray_entry(self, tok, rid):
        """Put one record's line into the could-not-check tray the way the pipeline does when a record has no usable answer (copied from tests/e2e/conftest.py::tray_entry_for_record)."""
        code = textwrap.dedent(f"""
            import sys, time; sys.path.insert(0, '.')
            from app.db import db as DB
            from app.backend import generator, pipeline as PL, store
            conn = DB.connect({self.db!r}); case = DB.get_case(conn, {tok!r})
            recs = store.load_records(conn, {tok!r}, case['raw_text']); rec = next(r for r in recs if f"r{{r['n']}}" == {rid!r})
            f = generator.failure_entry(rec, [rec['n']], 'FIXTURE_MISS'); old = DB.get_item(conn, f['id'], {tok!r})
            f['ladder']['backend'] = (old.get('ladder') or {{}}).get('backend')
            DB.update_item(conn, f['id'], now=time.time(), case={tok!r}, **PL._row('entry', PL._clean(f))); conn.close(); print(f['id'])""")
        return subprocess.check_output([K.PY, "-c", code], cwd=self.src, text=True).strip()

    def go(self, page, path):
        page.goto(self.base + path)
        page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=20000)

    def item(self, page, tok, iid=None, step="timeline"):
        self.go(page, f"/case/{tok}/{step}" + (f"?item={iid}" if iid else ""))
        page.get_by_test_id("card-line").wait_for()

    def shoot(self, name, caption, states, widths=("1440", "390"), scheme="light"):
        """states(page, w) prepares the page; the shot is saved as <name>-<w>.png."""
        for w in widths:
            vw, vh = SIZES[w]
            br = self.pw.chromium.launch()
            ctx = br.new_context(viewport={"width": vw, "height": vh}, color_scheme=scheme, permissions=["clipboard-read", "clipboard-write"])
            page = ctx.new_page(); errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            try:
                states(page, w)
                page.wait_for_timeout(500)
                fn = f"{name}-{w}.png"; page.screenshot(path=str(self.out / fn))
                self.done.append((fn, caption))
                print("shot", fn, "ERRORS " + str(errs) if errs else "", flush=True)
            finally:
                br.close()


def main_stage(R):
    # ---- Your cases: empty first (fresh database), loading, error
    R.shoot("01-home-empty", "Your cases, before any case exists. The page says what a case is and offers two buttons: Start a new case and Open the sample case.",
            lambda p, w: R.go(p, "/"))

    def loading(p, w):
        def slow(route):
            if route.request.method != "GET":
                return route.continue_()
            time.sleep(8); route.continue_()
        p.route("**/api/cases", slow); p.goto(R.base + "/"); p.get_by_test_id("cases-loading").wait_for()
    R.shoot("02-home-loading", "Your cases while the list is on its way: three grey placeholder cards the size of the real ones, so nothing jumps when they fill. (The slow answer is simulated for this picture.)", loading, widths=("1440",))

    def herr(p, w):
        p.route("**/api/cases", lambda r: r.fulfill(status=500, json={"error": {"code": "server_error", "message": "The server had a problem."}}) if r.request.method == "GET" else r.continue_())
        R.go(p, "/")
    R.shoot("03-home-error", "Your cases when the list can't be loaded: a plain sentence and a Try again button. (The server error is simulated for this picture.)", herr, widths=("1440",))

    # ---- Step 1 before the case exists
    def new_paste(p, w):
        R.go(p, "/new"); p.get_by_test_id("input-name").fill("Jordan Rivera (sample)")
    R.shoot("04-step1-add", "Step 1, Add records, before the case exists. Name the case, then pick one of three ways in: paste text, upload a file, or use the sample case.", new_paste)

    def new_sample(p, w):
        R.go(p, "/new"); p.get_by_test_id("tile-sample").click()
    R.shoot("05-step1-add-sample", "Step 1 with the sample case chosen. The box below the tiles keeps its size and says what the sample is. Read the records is now available.", new_sample, widths=("1440",))

    # ---- Step 1 with a real case
    tok_found = R.case("Records found, not drafted yet", run=False)
    R.shoot("07-step1-found", "Step 1, records found. The nine records of the sample case are listed with their dates and sources. The next button is Draft the timeline.",
            lambda p, w: R.go(p, f"/case/{tok_found}/records"))

    def drafting(p, w):
        tok = R.case("Drafting", run=False)
        calls = {"n": 0}

        def case(route):
            j = route.fetch().json(); j["status"] = "running"; route.fulfill(json=j)

        def status(route):
            route.fulfill(json={"token": tok, "status": "running", "stage": "verify", "stages": STAGES, "progress": {"done": 2, "total": 8, "label": "x"}, "counts": {}, "error": None})
        p.route(f"**/api/cases/{tok}", case); p.route(f"**/api/cases/{tok}/status", status)
        R.go(p, f"/case/{tok}/records"); p.get_by_test_id("stage-list").wait_for()
    R.shoot("08-step1-drafting", "Step 1 while the timeline is being drafted: a checklist of eight plain stages with the current one marked. In this demo the lines come from answers our team prepared. (The running state is simulated for this picture because the demo finishes instantly.)", drafting, widths=("1440",))

    def drafted(p, w):
        tok = R.case("Drafted", run=False); R.go(p, f"/case/{tok}/records"); p.get_by_test_id("btn-draft").click(); p.get_by_test_id("draft-done").wait_for(timeout=20000)
    R.shoot("09-step1-done", "Step 1 done, after the real Draft the timeline click: how many timeline items and bill amounts are ready to check, and the button Go to step 2.", drafted)

    def failed(p, w):
        tok = R.case("Stopped", run=True)

        def case(route):
            j = route.fetch().json(); j["status"] = "failed"
            j["error"] = {"code": "run_partial", "message": "The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.", "interrupted": True, "records": [2, 7]}
            route.fulfill(json=j)
        p.route(f"**/api/cases/{tok}", case); R.go(p, f"/case/{tok}/records"); p.get_by_test_id("draft-failed").wait_for()
    R.shoot("10-step1-stopped", "Step 1 when drafting stopped: the server's own sentence, which records got no line, and a Run it again button. (The stopped run is simulated for this picture.)", failed, widths=("1440",))

    # ---- Step 2
    tok2 = R.case("Jordan Rivera (sample)")
    R.shoot("11-step2-entry", "Step 2, one timeline line at a time. Left: the record with the quoted words highlighted. Right: the line to check and the plain reason it passed the checks. The question sits next to two equal answers.",
            lambda p, w: R.item(p, tok2, "e4"))

    tok10 = R.case("Disputed line", lib=LIB10)
    if (R.src / "app" / "frontend" / "guided" / "how.js").exists():       # T-211 (D-074): the check panel and the explainer page, when this commit has them
        def panel(p, w):
            R.item(p, tok2, "e4"); d = p.get_by_test_id("how-checked")
            if d.evaluate("e => e.tagName === 'DETAILS' && !e.open"):
                d.evaluate("e => { e.open = true }")
            d.scroll_into_view_if_needed(); p.wait_for_timeout(300)
        R.shoot("11b-step2-how-checked", "Step 2 with the How this was checked panel open: what the code found, then one statement from the second AI check (prepared by our team, then checked against the quote, with its verdict and why), then the reader's own decision. Three checks, in that order.", panel)

        def panel_disputed(p, w):
            R.item(p, tok10, "e1"); d = p.get_by_test_id("how-checked")
            if d.evaluate("e => e.tagName === 'DETAILS' && !e.open"):
                d.evaluate("e => { e.open = true }")
            d.scroll_into_view_if_needed(); p.wait_for_timeout(300)
        R.shoot("11c-step2-how-checked-disputed", "The same panel on a line the second AI check only partly supported: the verdict (Disputes) and its reason are shown in one statement, and the decision is still the reader's.", panel_disputed)
        R.shoot("11d-how-it-works", "The page How each answer is checked, linked from the top of every screen: code first, then the second AI check, then the person decides.", lambda p, w: R.go(p, "/how-it-works"))

    def saved(p, w):
        R.item(p, tok2, "e4"); p.get_by_test_id("answer-yes").click(); p.get_by_test_id("btn-undo").wait_for()
    R.shoot("12-step2-saved", "Step 2 right after a Yes. The next line is open in the same boxes, and the line under the buttons says what was saved, with an Undo button.", saved)

    def fix(p, w):
        R.item(p, tok2, "e5"); p.get_by_test_id("btn-third").click(); p.wait_for_timeout(300)
    R.shoot("13-step2-fix", "Step 2, Fix the wording. The line becomes a text box. Whole sentences in the record can be tapped to change which words are the quote.", fix)

    def fix_refused(p, w):
        R.item(p, tok2, "e5"); p.get_by_test_id("btn-third").click(); p.get_by_test_id("edit-summary").fill("Right shoulder pain 9/10 after the crash on May 4.")
        p.get_by_test_id("answer-yes").click(); p.wait_for_timeout(600)
    R.shoot("14-step2-fix-refused", "Step 2, a wording the checks refuse. The message says which number is not in the highlighted quote. The text stays in the box and nothing is saved.", fix_refused, widths=("1440",))

    R.shoot("15-step2-warning", "Step 2, a warning for the attorney. It is explained in plain words with the record words that support it. A grey Found by code tag shows the warning came from a program, not from a prepared AI answer. The question is whether the attorney should be told. Warnings go in the notes, never in the letter.",
            lambda p, w: R.item(p, tok2, "f_cx1"))
    R.shoot("16-step2-gap", "Step 2, a break in treatment. The gap length (73 days) was counted by code, and the tag says Found by code. Its second-AI line reads Not needed, because code made the warning. The records on both sides of the gap are shown with their dates highlighted.",
            lambda p, w: R.item(p, tok2, "f_gap_r6_r7"))

    def note(p, w):
        R.item(p, tok2, "f_r3_1"); p.get_by_test_id("btn-third").click(); p.wait_for_timeout(300)
    R.shoot("17-step2-warning-note", "Step 2, Add a note to a warning. A text box opens in the card, with Save note and Cancel.", note, widths=("1440",))

    R.shoot("18-step2-disputed", "Step 2, a line the second check only partly supported. Yes is disabled until the reader ticks that she read the line against the highlighted words herself.",
            lambda p, w: R.item(p, tok10, "e1"))

    def disputed_ticked(p, w):
        R.item(p, tok10, "e1"); p.get_by_test_id("check-compare").check(); p.wait_for_timeout(200)
    R.shoot("19-step2-disputed-ticked", "The same line after the box is ticked. Yes, this matches is now available.", disputed_ticked, widths=("1440",))

    tok_c = R.case("Could not check", run=True); tid = R.tray_entry(tok_c, "r4")
    R.shoot("20-step2-cannot-check", "Step 2, a line we couldn't check. The reason is given and nothing is highlighted. These items are optional. (For this picture the demo's prepared answer for record 4 was removed, so the page shows what it does when an answer is missing.)",
            lambda p, w: R.item(p, tok_c, tid))

    def write(p, w):
        R.item(p, tok_c, tid); p.get_by_test_id("answer-yes").click(); p.get_by_test_id("sentence").first.click(); p.wait_for_timeout(300)
        p.get_by_test_id("edit-line").fill("Neck range of motion reduced about 40%.")
    R.shoot("21-step2-write", "Step 2, Write it myself. She picks whole sentences from the record and types her own line. Save my line sends it through the same checks.", write)

    tok2b = R.case("Warning not confirmed", lib=LIB02); tray = R.api("GET", f"/api/cases/{tok2b}")[1]["tray"]
    R.shoot("22-step2-cannot-confirm-warning", "Step 2, a warning the second check couldn't confirm. It cannot go in the notes. The reader can leave it out or tell the attorney herself.",
            lambda p, w: R.item(p, tok2b, tray[0]["id"]))

    tok9 = R.case("Date to pick", lib=LIB09); und = R.api("GET", f"/api/cases/{tok9}")[1]["undated_entries"]
    R.shoot("23-step2-date", "Step 2, a date to pick. The record's date could be read two ways, so no date is chosen for her. The page offers both readings, month first and day first, and marks one as suggested with the reason.",
            lambda p, w: R.item(p, tok9, und[0]["id"]))

    tok2d = R.case("Jordan Rivera (sample), timeline checked"); R.decide(tok2d, groups=("entries", "undated_entries", "flags"))
    R.shoot("24-step2-done", "Step 2 done: a big check, the counts of what was kept, left out and flagged for the attorney, and one row per item with its answer and a Change button.",
            lambda p, w: R.go(p, f"/case/{tok2d}/timeline"))

    def steps_open(p, w):
        R.item(p, tok2, "e1"); p.get_by_test_id("btn-steps").click(); p.wait_for_timeout(300)
    R.shoot("25-step2-steps-open", "The step list on a phone. It folds into one line to leave room for the record, and opens with a tap to show all four steps.", steps_open, widths=("390",))

    def dark(p, w):
        R.item(p, tok2, "e4")
    R.shoot("26-step2-entry-dark", "Step 2 in dark mode, which follows the computer's setting.", dark, widths=("1440",), scheme="dark")

    # ---- Step 3
    tok3 = R.case("Bills")
    R.shoot("27-step3-charge", "Step 3, one bill amount at a time. The record shows the figure; the question is whether this charge counts toward the bill total. The charge line carries a fillable blank, date of service [__________], with the record date in parentheses, and a yellow note says the letter takes no service date from the records and the reader fills the blank. The total so far is in the title row.",
            lambda p, w: R.item(p, tok3, "a1", step="bills"))
    R.shoot("28-step3-never", "Step 3, an amount that is never added to the total (here a rate). The reason is given, and the choice is only whether to list it in the notes for the attorney.",
            lambda p, w: R.item(p, tok3, "a2", step="bills"))

    tok11 = R.case("Ledger", lib=LIB11); cnt = [a for a in R.api("GET", f"/api/cases/{tok11}")[1]["amounts"] if a["countable"]]

    def count(p, w):
        R.item(p, tok11, cnt[0]["id"], step="bills")
    R.shoot("29-step3-count", "Step 3, an amount that is not counted yet but could be. The reason it was not counted is given, with a note that the second check thought it may be a billed charge. Yes, count it stays disabled until she ticks the boxes that say she checked it.", count)

    def count_ticked(p, w):
        count(p, w)
        for b in p.locator("[data-testid=card-foot] input[type=checkbox]").all():
            b.check()
        p.wait_for_timeout(200)
    R.shoot("30-step3-count-ticked", "The same amount with the confirm box ticked. Yes, count it is now available.", count_ticked, widths=("1440",))

    tok3d = R.case("Bills checked")
    R.decide(tok3d, groups=("amounts",))
    R.shoot("31-step3-done", "Step 3 done: the bill total as the letter will print it, and three plain lists: counted, not counted by her, and never counted. Each counted charge shows the date-of-service blank and its record date.",
            lambda p, w: R.go(p, f"/case/{tok3d}/bills"))

    # ---- demo refusal on the public-mode server is shot by video stage; here the classic page
    R.shoot("32-classic", "The older review screen, kept at /classic for people who want every control on one page.", lambda p, w: (p.goto(R.base + "/classic"), p.wait_for_timeout(1500)), widths=("1440",))


def letter_stage(R):
    # Your cases with several cases at different steps (local mode lists every case on this computer): made first so the list holds exactly these four
    tok_ok = R.case("Jordan Rivera (sample)"); R.decide(tok_ok)
    R.case("Waiting to draft", run=False)
    t_half = R.case("Half checked"); R.decide(t_half, groups=("entries",))
    t_bills = R.case("Timeline checked, bills left"); R.decide(t_bills, groups=("entries", "undated_entries", "flags"))
    R.shoot("44-home-cases", "Your cases with several cases at different steps. Each card shows its four steps, a Next line that says exactly what to do, and one Continue button.",
            lambda p, w: R.go(p, "/"))

    def finished(p, w):
        R.go(p, "/"); p.get_by_test_id("btn-continue").last.scroll_into_view_if_needed(); p.evaluate("document.querySelectorAll('*').forEach(e => { if (e.scrollHeight > e.clientHeight + 40 && getComputedStyle(e).overflowY !== 'visible') e.scrollTop = e.scrollHeight })"); p.evaluate("window.scrollTo(0, document.body.scrollHeight)"); p.wait_for_timeout(300)
    R.shoot("44b-home-finished", "Your cases, scrolled down to Finished. A case whose letter is ready moves here and says Letter ready, with a button that opens the letter.", finished)

    def rename(p, w):
        R.go(p, "/"); p.get_by_test_id("btn-rename").first.click(); p.wait_for_timeout(300)
    R.shoot("45-home-rename", "Your cases, renaming a case. The title turns into a box inside the same card, with Save and Cancel.", rename, widths=("1440",))

    def delete(p, w):
        R.go(p, "/"); p.get_by_test_id("btn-delete").first.click(); p.wait_for_timeout(300)
    R.shoot("46-home-delete", "Your cases, deleting a case. The card's bottom row asks first: Delete this case and all its answers, with Yes, delete and Keep it.", delete, widths=("1440",))

    # Step 4: the part that may still change
    R.shoot("40-step4-letter", "Step 4, Get your letter. The letter is on the left, ready to paste into a demand letter; each charge line in it carries the fillable blank date of service [__________], and the bar says the [Ex. __ / Bates __] blanks are hers to fill. The notes for the attorney, marked do not send, are on the right. Copy and Download buttons sit under each.",
            lambda p, w: R.go(p, f"/case/{tok_ok}/letter"))

    def cfg(p, w):
        R.go(p, f"/case/{tok_ok}/letter"); p.get_by_test_id("cfg-exhibit").fill("4"); p.get_by_test_id("cfg-bates-prefix").fill("RIV"); p.get_by_test_id("cfg-bates-start").fill("1")
        p.get_by_test_id("btn-save-cfg").click(); p.wait_for_timeout(800)
    R.shoot("41-step4-letter-numbered", "Step 4 after typing an exhibit number and a Bates prefix. The numbers are filled into the letter's source tags.", cfg, widths=("1440",))

    tok_p = R.case("Undecided items"); c = R.api("GET", f"/api/cases/{tok_p}")[1]
    R.api("POST", f"/api/cases/{tok_p}/review/batch", {"action": "accept", "item_ids": [e["id"] for e in c["entries"]]})
    R.shoot("42-step4-pending", "Step 4 with items still undecided. The letter shows what would be sent now, and copying needs one tick that says she knows those items stay out.",
            lambda p, w: R.go(p, f"/case/{tok_p}/letter"))
    tok_b = R.case("Nothing decided")
    R.shoot("43-step4-blocked", "Step 4 when nothing has been answered. The letter can't be made, the page says why in the server's own words, and a button goes to the step that fixes it.",
            lambda p, w: R.go(p, f"/case/{tok_b}/letter"))



def public_stage(R):
    """Server B (public demo mode: no case list; other text refused)."""
    R.shoot("47-step1-add-demo", "Step 1 in the public demo. Paste and Upload are shown but switched off, with the reason in plain words (this demo can only read the sample case and our test cases). The sample case is already chosen.",
            lambda p, w: R.go(p, "/new"))
    R.shoot("48-home-demo-empty", "Your cases in the public demo. There is no list of other people's cases; this browser lists only the cases it started.", lambda p, w: R.go(p, "/"), widths=("1440",))


def write_manifest(out, done, sha):
    pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--rev", default="HEAD"); ap.add_argument("--stage", default="all"); ap.add_argument("--out", default=str(K.ROOT / "artifacts" / "screenshots" / "final")); ap.add_argument("--captions", default=str(K.ROOT / "artifacts" / "CAPTIONS.md"))
    a = ap.parse_args(); a_caps = a.captions; out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    src, sha = K.archive(a.rev); print("archive", sha, src, flush=True)
    done = []
    with sync_playwright() as pw:
        if a.stage in ("main", "all"):
            with K.server(src, local=True) as (base, db):
                R = Run(pw, base, db, src, out); main_stage(R); done += R.done
        if a.stage in ("letter", "all"):
            with K.server(src, local=True) as (base, db):
                R = Run(pw, base, db, src, out); letter_stage(R); done += R.done
        if a.stage in ("public", "all"):
            with K.server(src, local=False) as (base, db):
                R = Run(pw, base, db, src, out); public_stage(R); done += R.done
    mf = out / "_captions.json"
    old = json.loads(mf.read_text()) if mf.exists() else {"shots": {}}
    shots = old["shots"] if isinstance(old.get("shots"), dict) else {}
    for fn, cap in done:
        shots[fn] = {"caption": cap, "commit": sha[:7]}
    mf.write_text(json.dumps({"shots": shots}, indent=1))
    lines = ["# Screenshot captions", "",
             "Every picture is a real page of the app, running in demo mode from a clean copy of one commit (listed per picture), at 1440x900 (desktop) or 390x844 (phone). Files are in `artifacts/screenshots/final/`.",
             "In the demo the sample lines and warnings were prepared by our team (D-065), checked by code and by a second AI model. Where a picture needed a state the demo cannot reach on its own (a slow list, a server error, a drafting run in progress, a stopped run, a line with no prepared answer), the caption says so.", ""]
    for fn in sorted(shots):
        lines.append(f"- `{fn}` ({shots[fn]['commit']}): {shots[fn]['caption']}")
    pathlib.Path(a_caps).write_text("\n".join(lines) + "\n")
    print("commit", sha, "shots", len(done))
