# Subagent: QA: recapture demo assets (QA: recapture demo assets)

Source: `agent-aa2dfcc4fcb64829c.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T13:30:56.848Z

You are a QA worker in /Users/arsis/zlayt-pm-project on T-184 (demo assets). Re-capture at the gate commit f6d5c19. Since the first capture, the letter's charge lines became fillable blanks (T-202), the judge panel changed (T-211 r2), and the code-found flag label changed (T-214).

Run `.venv/bin/python tests/demo_assets/shots.py --stage all` and `.venv/bin/python tests/demo_assets/video.py`; they archive HEAD and stop their own PIDs. Make sure HEAD is f6d5c19, or check out nothing and pass the commit if the scripts allow it.

Update artifacts/CAPTIONS.md and artifacts/NARRATION.md wherever the screens changed:
- the letter blank;
- the panel wording;
- "Found by code".

The video stays at 180 s or less. Commit only artifacts/ and the scripts if you changed them, with a temp index and `git commit`. Add a note on T-184 with the commit and reply in 1 line.

### User / tool · 2026-11-03T13:30:56.857Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:30:59.103Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/agent-memory/qa/project_demo_assets.md"
}
````

### User / tool · 2026-11-03T13:30:59.110Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:30:59.848Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short | head -20 && ls tests/demo_assets artifacts | head -50"
}
````

### User / tool · 2026-11-03T13:30:59.997Z

**tool result**
````
f6d5c19
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
artifacts:
CAPTIONS.md
NARRATION.md
demo.webm
m0-smoke
mockups
review-evidence
screenshots
t119-r3-e2e-full.txt
t119-r3-mutB.txt
tmp
unit-count-33e88c6.txt

tests/demo_assets:
common.py
script.py
shots.py
video.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:02.516Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/qa/project_demo_assets.md; git log --oneline -3; sed -n 1,60p tests/demo_assets/shots.py; python3 tools/board.py show T-184 | tail -30"
}
````

### User / tool · 2026-11-03T13:31:02.660Z

**tool result**
````
---
name: demo-assets-recipe
description: How T-184 screenshots, video and narration are produced (tests/demo_assets), re-run commands, and pitfalls
metadata:
  type: project
---

Scripts in tests/demo_assets: common.py (git archive of a rev, server on a free port, stops its own PID), shots.py (stages main/letter/public), video.py + script.py (beats with narration; NARRATION.md is generated from the same beats, so words and clicks cannot drift).
Re-run on a new commit: `.venv/bin/python tests/demo_assets/shots.py --stage all` then `.venv/bin/python tests/demo_assets/video.py` (each ~2-3 min; run in background and poll the log).

**Pitfalls.** Library cases (disputed, date, countable) need ZLAYT_MODE=local, so screenshots use a local server and the video a public one. The sample has no disputed item. Jumping to `?item=` skips earlier items, so the fast loop must click "Go to the first one" on the done page. In public mode Paste/Upload tiles are disabled (shoot /new, do not try to paste). Never `pkill -f` or `pgrep -f` on a script name from a Bash monitor: it matches the monitor itself and the hook blocks pkill. No ffmpeg/ffprobe: read webm duration from the EBML Duration element; seeking a Playwright webm in a <video> hangs, so take beat stills (screenshot at the end of each beat) instead.
**Why:** video must be <=180 s and narration must match the screen; D-065 wording is mandatory.
f6d5c19 feat(frontend): T-214 a flag only code found shows its origin label, not the Prepared answer tag; the how-checked panel says the same
d15c9ab fix(backend): flags found only by code are not prepared answers (T-214)
b50952d feat(backend): T-202 r7 D-073 fallback applied: the letter and Step 3 print the fillable blank on every charge line, no service date extracted; letter_check requires the blank form; reader kept as service_date.read (SCOPE_CUTS 28)
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
milestone: "M4"
role: "qa"
status: "in_review"
priority: "P0"
depends_on: ["T-181"]
created_by: "orchestrator"
created_at: "2026-11-02T21:00:13Z"
updated_at: "2026-11-03T13:13:35Z"
claimed_by: "qa"
claimed_at: "2026-11-03T04:31:53Z"
rounds: 0
commits: ["cda2856"]
reviews: []
ac:
  - {"n": 1, "text": "screenshots cover every state in docs/GUIDED_UI_SPEC.md with captions; demo.webm <=180 s shows Your cases -> 4 steps -> letter; narration script timed to the video", "done": true, "evidence": "artifacts/screenshots/final/ (72 pngs, all GUIDED_UI_SPEC states at 1440x900, key states at 390x844) + artifacts/CAPTIONS.md; artifacts/demo.webm 167.6 s (Duration header) Your cases -> Steps 1-4 -> downloaded letter, incl. How-checked panel and How-it-works page; artifacts/NARRATION.md timed from the same beats (tests/demo_assets/script.py). Captured at 4e4ff36"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T21:00:16Z orchestrator: assigned: qa
- 2026-11-03T04:31:53Z qa: claimed
- 2026-11-03T04:35:12Z qa: Orchestrator: T-211 adds a How this was checked panel and a How each answer is checked page; final capture waits for T-211. Scripts in tests/demo_assets/ (common.py, shots.py; video.py next) archive HEAD so a re-run on the new commit is one command. Video + narration will pause on one item's panel and on the How-it-works page, and explain code check, second AI check, you decide.
- 2026-11-03T05:15:32Z qa: AC 1 checked: artifacts/screenshots/final/ (72 pngs, all GUIDED_UI_SPEC states at 1440x900, key states at 390x844) + artifacts/CAPTIONS.md; artifacts/demo.webm 167.6 s (Duration header) Your cases -> Steps 1-4 -> downloaded letter, incl. How-checked panel and How-it-works page; artifacts/NARRATION.md timed from the same beats (tests/demo_assets/script.py). Captured at 4e4ff36
- 2026-11-03T05:15:33Z qa: moved in_progress -> in_review
- 2026-11-03T13:13:35Z orchestrator: review dispatched: product-manager-reviewer + installer-reviewer (queued: the D-074 double-check after T-202 fallback and T-211 land)

## Handoff
What changed: tests/demo_assets/{common,shots,video,script}.py; artifacts/screenshots/final (72 shots, 0 page errors), CAPTIONS.md, demo.webm (167.6 s), NARRATION.md (427 words, per-beat times). Commit cda2856. Captured at 4e4ff36 (HEAD of T-211, T-202 r6 included; T-202 still in_review, so the letter/charge-date lines may change). Re-run, one command each: .venv/bin/python tests/demo_assets/shots.py --stage letter ; .venv/bin/python tests/demo_assets/video.py (both archive HEAD, run in a clean copy on their own port and stop their PID). How verified: every shot written by the real app in demo mode from git archive; beat stills of the video viewed against the narration; sample/demo mode is public (no case list) for the video, local mode (case list + test-case library) for screenshots. Simulated states, named in captions: slow list, list 500, drafting, stopped run, and the could-not-check line (prepared answer removed from the DB copy). Not shown: flagged-charge confirm (no real case has one), PDF/OCR errors, disputed line in the video (sample has none; it is in screenshots from lib10). What surprised me: the sample has no disputed item, jumping straight to a warning skips earlier items so the loop must follow Go to the first one; the video is 16-19 MB (no LFS in this repo).
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:05.774Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/tmp && (.venv/bin/python tests/demo_assets/shots.py --stage all > /tmp/x 2>&1; cp /tmp/x artifacts/tmp/shots.log 2>/dev/null; echo done) 2>&1 | tail -3; tail -15 /tmp/x",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-03T13:31:05.834Z

**tool result**
````
Command running in background with ID: bkpz8ua12. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bkpz8ua12.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:08.496Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p tests/demo_assets/script.py | head -150; wc -l artifacts/CAPTIONS.md artifacts/NARRATION.md"
}
````

### User / tool · 2026-11-03T13:31:08.610Z

**tool result**
````
"""T-184: the scripted walk-through (what is clicked, and the words Chris reads over it). One place, so the narration cannot drift from the picture:
video.py plays it and NARRATION.md is generated from the same beats with their measured times. Edit the words here, then re-run video.py."""
import pathlib
import re
import time

BEATS_VERSION = 1
WPS = 2.6        # words per second of a calm read-aloud

NARR = {
    "home": "This is Your cases, the home page. The yellow bar says the data is synthetic, and the blue label says the sample answers were prepared by our team. I have no cases yet, so I open the sample.",
    "records": "Step 1 found the nine records in the sample case. I press Draft the timeline.",
    "drafted": "In this demo the summaries and warnings were prepared by our team ahead of time. They were not written by an AI just now, and nothing is sent to an AI while this demo runs. Nineteen timeline items and four bill amounts are ready for me to check.",
    "item": "Step 2 shows one item at a time. On the left is the record, with the quoted words highlighted. On the right is the line to check.",
    "checks": "Three checks stand between a line and the letter. First, code checks that the quote is in the record word for word, and that every number matches. Second, a different AI model checks the line against its quote. Third, me. Nothing moves on until I answer.",
    "panel": "Under the line, a panel shows how it was checked: what the code found, what the second AI check said and why, and then my own decision.",
    "answer": "I read the highlighted words, then say Yes, this matches. The next item opens in the same boxes, and I can undo.",
    "howpage": "This page, linked at the top of every screen, explains how each answer is checked. Code first, then the second AI check, then me. The AI never has the last word.",
    "warning": "A warning is for the attorney. It goes in the notes for her, never in the letter. I decide whether she should be told.",
    "rest": "To save time I will say yes to the rest. In real use I would read each one.",
    "step2done": "Step 2 is done. Every item has an answer.",
    "bills": "Step 3 is the bill amounts. Code finds them and adds them up. I decide whether each charge counts toward the total.",
    "never": "Some amounts, like this rate, are never added to the total. The page says so.",
    "step3done": "Step 3 is done. The total is added up by code, not by an AI.",
    "letter": "Step 4. The letter is on the left. The notes for the attorney, marked do not send, are on the right. I copy the letter, then download it.",
    "download": "This is the file I downloaded. It is plain text, ready to paste into a demand letter.",
    "close": "Back on Your cases, this one now says Letter ready. Everything here was a prepared answer. The AI's own results are in the evaluation report.",
}


def done_loop(R, page, step_done_id="done-page", limit=40):
    """Say yes to every remaining item, quickly (the rest of a step)."""
    for _ in range(limit):
        if page.get_by_test_id(step_done_id).count():
            first = page.get_by_test_id("btn-first-undecided")
            if not first.count():
                return
            R.tap(first, 0.3); page.get_by_test_id("card-line").wait_for(); continue      # the jump to the warning skipped the lines before it: go back to them
        for b in page.locator("[data-testid=card-foot] input[type=checkbox]").all():
            if b.is_visible():
                b.check()
        yes = page.get_by_test_id("answer-yes")
        yes.wait_for(state="visible", timeout=10000)
        R.tap(yes, dwell=0.05, steps=6)
        page.wait_for_timeout(260)


def has_t211(page):
    return page.get_by_test_id("how-checked").count() > 0


def open_panel(page):
    d = page.get_by_test_id("how-checked")
    if d.evaluate("e => e.tagName === 'DETAILS' && !e.open"):
        d.evaluate("e => { e.open = true }")


def play(R, page, base, vid_dir):
    page.goto(base + "/"); page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=20000)
    R.beat("home", lambda: (R.pause(4), R.tap(page.get_by_test_id("btn-sample-case"), 1.0)))
    page.get_by_test_id("btn-draft").wait_for()
    R.beat("records", lambda: (R.pause(1.5), R.tap(page.get_by_test_id("btn-draft"), 0.8)))
    page.get_by_test_id("draft-done").wait_for(timeout=20000)
    R.beat("drafted", lambda: R.pause(1))
    tok = page.url.split("/case/")[1].split("/")[0]

    def to_step2():
        R.tap(page.get_by_test_id("btn-next-step"), 0.6); page.get_by_test_id("card-line").wait_for()
    R.beat("item", to_step2)
    t211 = has_t211(page)
    R.beat("checks", lambda: R.pause(0.5))
    if t211:
        R.beat("panel", lambda: (open_panel(page), R.pause(0.5)))

        def how():
            R.tap(page.get_by_test_id("link-how"), 0.6); page.get_by_test_id("view").wait_for(); R.pause(2)
        R.beat("howpage", how)
        page.go_back(); page.get_by_test_id("card-line").wait_for()
    R.beat("answer", lambda: (R.tap(page.get_by_test_id("answer-yes"), 0.8), page.get_by_test_id("btn-undo").wait_for()))
    R.beat("warning", lambda: (page.goto(f"{base}/case/{tok}/timeline?item=f_gap_r6_r7"), page.get_by_test_id("card-line").wait_for()))
    R.beat("rest", lambda: done_loop(R, page))
    R.beat("step2done", lambda: R.pause(0.5))

    def to_step3():
        R.tap(page.get_by_test_id("btn-next-step"), 0.6); page.get_by_test_id("card-line").wait_for()
    R.beat("bills", lambda: (to_step3(), R.pause(1.2), R.tap(page.get_by_test_id("answer-yes"), 0.5), page.wait_for_timeout(500)))
    R.beat("never", lambda: (page.goto(f"{base}/case/{tok}/bills?item=a2"), page.get_by_test_id("card-line").wait_for()))
    done_loop(R, page)
    R.beat("step3done", lambda: R.pause(0.5))

    def to_letter():
        R.tap(page.get_by_test_id("btn-next-step"), 0.6); page.get_by_test_id("letter-text").wait_for()
        page.wait_for_timeout(1500)
    dl = {}

    def copy_and_download():
        R.tap(page.get_by_test_id("btn-copy-letter"), 0.6); R.pause(1.0)
        with page.expect_download() as d:
            R.tap(page.get_by_test_id("btn-download-letter"), 0.6)
        dl["path"] = vid_dir / "letter.txt"; d.value.save_as(dl["path"])
    R.beat("letter", lambda: (to_letter(), copy_and_download()))

    def show_file():
        page.goto("file://" + str(dl["path"]))
        page.add_style_tag(content="body{background:#fff;margin:0} pre{font:19px/1.55 ui-monospace,Menlo,monospace;white-space:pre-wrap;max-width:1180px;margin:24px auto;padding:0 24px;color:#111}")
        R.pause(1)
    R.beat("download", show_file)

    def home():
        page.goto(base + "/"); page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=20000)
    R.beat("close", home)


SCREEN = {
    "home": "Your cases with no cases yet, then the sample is opened.", "records": "Step 1: the nine records of the sample case; Draft the timeline is pressed.",
    "drafted": "Step 1 done: 19 timeline items and 4 bill amounts ready.", "item": "Step 2, the first item: the record with the quote highlighted, and the line to check.",
    "checks": "The same item, with its plain reason and the question and two answers.", "panel": "The panel under the line: what the code found, what the second AI check said, and your decision.",
    "howpage": "The How each answer is checked page, then back to the item.", "answer": "Yes, this matches is pressed; the next item opens; the Saved line shows an Undo button.",
    "warning": "A break-in-treatment warning (73 days between records 6 and 7) with both records highlighted.", "rest": "Quick yes-clicks through the remaining timeline items and warnings.",
    "step2done": "Step 2 done: the counts and one row per item with its answer.", "bills": "Step 3: the first charge; Yes, count it is pressed; the bill total so far changes.",
    "never": "Step 3: an amount that is never counted (a rate), with its reason.", "step3done": "Step 3 done: the total line as the letter will print it, and the lists.",
    "letter": "Step 4: the letter and the notes for the attorney; Copy letter and Download letter are pressed.", "download": "The downloaded .txt file opened in the browser.",
    "close": "Your cases again, with the finished case showing Letter ready.",
}


def fmt(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def write_narration(path, log, total, sha):
    words = sum(len(t.split()) for _, _, _, t in log)
    rows = "\n".join(f"| {fmt(s)}-{fmt(e)} | {t} |" for _, s, e, t in log)
    path = pathlib.Path(path)
    screen = "\n".join(f"- {fmt(st)}: {SCREEN[k]}" for k, st, _, _ in log)
    path.write_text(f"""# Narration script for artifacts/demo.webm

Read this in your own voice. The times are measured from the recording (about {total:.0f} seconds in all, {words} words, at a calm pace of about {WPS} words a second; allow a second either way).
Captured from commit `{sha[:7]}`. Per D-065 the demo runs on prepared answers: the summaries and warnings were prepared by our team, then checked by code and by a second AI model, and nothing new is sent to an AI while the demo runs.
Say "prepared by our team", not "the AI wrote this", whenever you talk about the sample lines.

| Time | Say |
|---|---|
{rows}

What is on the screen at each point:

{screen}
""")
      77 artifacts/CAPTIONS.md
      45 artifacts/NARRATION.md
     122 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:10.692Z

**tool call — Bash**
````
{
 "command": "tail -12 /tmp/x; git status --short artifacts | head; rm -f artifacts/tmp/shots.log; (.venv/bin/python tests/demo_assets/video.py > /tmp/v 2>&1; echo finished >> /tmp/v) ",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-03T13:31:10.752Z

**tool result**
````
Command running in background with ID: b40q1wl3t. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b40q1wl3t.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:18.576Z

**tool call — Bash**
````
{
 "command": "tail -12 /tmp/x; git status --short artifacts | head"
}
````

### User / tool · 2026-11-03T13:31:18.699Z

**tool result**
````
 M artifacts/screenshots/guided/home-1440.png
 M artifacts/screenshots/guided/home-390.png
 M artifacts/screenshots/guided/home-empty-1440.png
 M artifacts/screenshots/guided/step1-drafting-1440.png
 M artifacts/screenshots/guided/step1-failed-1440.png
 M artifacts/screenshots/guided/step1-found-390.png
 M artifacts/screenshots/guided/step2-date-1440.png
 M artifacts/screenshots/guided/step2-date-390.png
 M artifacts/screenshots/guided/step2-disputed-1440.png
 M artifacts/screenshots/guided/step2-disputed-390.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:21.344Z

**tool call — Bash**
````
{
 "command": "git status --short artifacts | awk '{print $2}' | cut -d/ -f1-3 | sort | uniq -c; ls -la --time-style=full-iso artifacts/screenshots/guided | head -4; ls -la --time-style=full-iso artifacts/screenshots/final | head -5; date; cat /tmp/x | head"
}
````

### User / tool · 2026-11-03T13:31:21.489Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:23.552Z

**tool call — Bash**
````
{
 "command": "git status --short artifacts/screenshots/final artifacts/CAPTIONS.md artifacts/NARRATION.md artifacts/demo.webm | wc -l; git status --short artifacts/screenshots/final | head -3;  git status --short artifacts | grep -v review-evidence | grep -v screenshots/guided | head"
}
````

### User / tool · 2026-11-03T13:31:23.705Z

**tool result**
````
       0
?? artifacts/screenshots/t060-after-_espalda-1440-full.png
?? artifacts/screenshots/t060-after-_espalda-1440-top.png
?? artifacts/screenshots/t060-after-_espalda-390-full.png
?? artifacts/screenshots/t060-after-_espalda-390-top.png
?? artifacts/screenshots/t060-after-sample-1440-full.png
?? artifacts/screenshots/t060-after-sample-1440-top.png
?? artifacts/screenshots/t060-after-sample-390-full.png
?? artifacts/screenshots/t060-after-sample-390-top.png
?? artifacts/screenshots/t060-before-_espalda-1440-full.png
?? artifacts/screenshots/t060-before-_espalda-1440-top.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:26.157Z

**tool call — Bash**
````
{
 "command": "ls -la /tmp/x; ls artifacts/screenshots/final | wc -l; ls -la --time-style=full-iso artifacts/screenshots/final | sed -n 2,4p; date; git status --short artifacts/screenshots/final | wc -l; git check-ignore -v artifacts/screenshots/final/x.png; grep -n \"out\\b\\|--out\\|default\" tests/demo_assets/shots.py | head"
}
````

### User / tool · 2026-11-03T13:31:26.320Z

**tool result**
````
total 2848
drwxr-xr-x@  17 arsis  wheel     544 Nov  2 11:59 .
drwxrwxrwt  590 root   wheel   18880 Nov  3 07:31 ..
-rw-r--r--@   1 arsis  wheel     187 Nov  2 04:08 41e42a2978854c340fcf3f43360478c22289d982857f3abc73377b804535ad59.json
-rw-r--r--@   1 arsis  wheel     239 Nov  1 22:40 S
-rw-r--r--@   1 arsis  wheel  179021 Nov  2 04:30 a.png
-rw-r--r--@   1 arsis  wheel  217268 Nov  2 04:28 b.png
-rw-r--r--@   1 arsis  wheel  202832 Nov  2 04:32 c.png
-rw-r--r--@   1 arsis  wheel    5617 Nov  2 07:34 case_list.py
-rw-r--r--@   1 arsis  wheel   14055 Nov  2 08:54 conflicts.py
-rw-r--r--@   1 arsis  wheel  151037 Nov  2 04:42 f.png
-rw-r--r--@   1 arsis  wheel   71009 Nov  2 04:32 m.png
-rw-r--r--@   1 arsis  wheel   81014 Nov  2 04:35 mob.png
-rw-r--r--@   1 arsis  wheel  247849 Nov  2 04:42 s1.png
-rw-r--r--@   1 arsis  wheel  253218 Nov  2 04:42 s2.png
lrwxr-xr-x@   1 arsis  wheel     238 Nov  2 04:30 sp -> /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
-rw-r--r--@   1 arsis  wheel     249 Nov  2 04:24 sp.sh
-rw-r--r--@   1 arsis  wheel     422 Nov  2 11:59 unit.out
      73
ls: unrecognized option `--time-style=full-iso'
usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
Tue Nov  3 07:31:26 CST 2026
       0
2:Usage: .venv/bin/python tests/demo_assets/shots.py [--rev HEAD] [--stage main|letter|all] [--out artifacts/screenshots/final]
25:    def __init__(self, pw, base, db, src, out):
26:        self.pw, self.base, self.db, self.src, self.out = pw, base, db, src, out
62:        page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=20000)
78:                page.wait_for_timeout(500)
79:                fn = f"{name}-{w}.png"; page.screenshot(path=str(self.out / fn))
132:        tok = R.case("Drafted", run=False); R.go(p, f"/case/{tok}/records"); p.get_by_test_id("btn-draft").click(); p.get_by_test_id("draft-done").wait_for(timeout=20000)
156:            d.scroll_into_view_if_needed(); p.wait_for_timeout(300)
163:            d.scroll_into_view_if_needed(); p.wait_for_timeout(300)
172:        R.item(p, tok2, "e5"); p.get_by_test_id("btn-third").click(); p.wait_for_timeout(300)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:31.251Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python tests/demo_assets/shots.py --stage all > $S/shots.log 2>&1; echo exit $? >> $S/shots.log; tail -15 $S/shots.log; echo; tail -5 /tmp/v",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-03T13:31:31.315Z

**tool result**
````
Command running in background with ID: b7wvejt31. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b7wvejt31.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:38.380Z

**tool call — Bash**
````
{
 "command": "ls -ld /tmp/v; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b40q1wl3t.output | tail"
}
````

### User / tool · 2026-11-03T13:31:38.465Z

**tool result**
````
-rw-r--r--@ 1 arsis  wheel  151 Nov  3 07:31 /tmp/v
 M artifacts/screenshots/guided/home-1440.png
 M artifacts/screenshots/guided/home-390.png
 M artifacts/screenshots/guided/home-empty-1440.png
 M artifacts/screenshots/guided/step1-drafting-1440.png
 M artifacts/screenshots/guided/step1-failed-1440.png
 M artifacts/screenshots/guided/step1-found-390.png
 M artifacts/screenshots/guided/step2-date-1440.png
 M artifacts/screenshots/guided/step2-date-390.png
 M artifacts/screenshots/guided/step2-disputed-1440.png
 M artifacts/screenshots/guided/step2-disputed-390.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:42.628Z

**tool call — Monitor**
````
{
 "command": "until grep -q \"^exit\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots.log 2>/dev/null && grep -q finished /tmp/v; do sleep 5; done; echo both done",
 "description": "wait for shots and video runs",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-03T13:31:42.642Z

**tool result**
````
Monitor started (task b23qs825y, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:46.338Z

**tool call — Bash**
````
{
 "command": "cat artifacts/CAPTIONS.md | cut -c1-400"
}
````

### User / tool · 2026-11-03T13:31:46.423Z

**tool result**
````
# Screenshot captions

Every picture is a real page of the app, running in demo mode from a clean copy of one commit (listed per picture), at 1440x900 (desktop) or 390x844 (phone). Files are in `artifacts/screenshots/final/`.
In the demo the sample lines and warnings were prepared by our team (D-065), checked by code and by a second AI model. Where a picture needed a state the demo cannot reach on its own (a slow list, a server error, a drafting run in progress, a stopped run, a line with no prepared answer), the caption says so.

- `01-home-empty-1440.png` (4e4ff36): Your cases, before any case exists. The page says what a case is and offers two buttons: Start a new case and Open the sample case.
- `01-home-empty-390.png` (4e4ff36): Your cases, before any case exists. The page says what a case is and offers two buttons: Start a new case and Open the sample case.
- `02-home-loading-1440.png` (4e4ff36): Your cases while the list is on its way: three grey placeholder cards the size of the real ones, so nothing jumps when they fill. (The slow answer is simulated for this picture.)
- `03-home-error-1440.png` (4e4ff36): Your cases when the list can't be loaded: a plain sentence and a Try again button. (The server error is simulated for this picture.)
- `04-step1-add-1440.png` (4e4ff36): Step 1, Add records, before the case exists. Name the case, then pick one of three ways in: paste text, upload a file, or use the sample case.
- `04-step1-add-390.png` (4e4ff36): Step 1, Add records, before the case exists. Name the case, then pick one of three ways in: paste text, upload a file, or use the sample case.
- `05-step1-add-sample-1440.png` (4e4ff36): Step 1 with the sample case chosen. The box below the tiles keeps its size and says what the sample is. Read the records is now available.
- `07-step1-found-1440.png` (4e4ff36): Step 1, records found. The nine records of the sample case are listed with their dates and sources. The next button is Draft the timeline.
- `07-step1-found-390.png` (4e4ff36): Step 1, records found. The nine records of the sample case are listed with their dates and sources. The next button is Draft the timeline.
- `08-step1-drafting-1440.png` (4e4ff36): Step 1 while the timeline is being drafted: a checklist of eight plain stages with the current one marked. In this demo the lines come from answers our team prepared. (The running state is simulated for this picture because the demo finishes instantly.)
- `09-step1-done-1440.png` (4e4ff36): Step 1 done, after the real Draft the timeline click: how many timeline items and bill amounts are ready to check, and the button Go to step 2.
- `09-step1-done-390.png` (4e4ff36): Step 1 done, after the real Draft the timeline click: how many timeline items and bill amounts are ready to check, and the button Go to step 2.
- `10-step1-stopped-1440.png` (4e4ff36): Step 1 when drafting stopped: the server's own sentence, which records got no line, and a Run it again button. (The stopped run is simulated for this picture.)
- `11-step2-entry-1440.png` (4e4ff36): Step 2, one timeline line at a time. Left: the record with the quoted words highlighted. Right: the line to check and the plain reason it passed the checks. The question sits next to two equal answers.
- `11-step2-entry-390.png` (4e4ff36): Step 2, one timeline line at a time. Left: the record with the quoted words highlighted. Right: the line to check and the plain reason it passed the checks. The question sits next to two equal answers.
- `11b-step2-how-checked-1440.png` (4e4ff36): Step 2 with the How this was checked panel open: what the code found, what the second AI check said and why, and the reader's own decision. Three checks, in that order.
- `11b-step2-how-checked-390.png` (4e4ff36): Step 2 with the How this was checked panel open: what the code found, what the second AI check said and why, and the reader's own decision. Three checks, in that order.
- `11c-step2-how-checked-disputed-1440.png` (4e4ff36): The same panel on a line the second AI check only partly supported: the verdict and its reason are shown, and the decision is still the reader's.
- `11c-step2-how-checked-disputed-390.png` (4e4ff36): The same panel on a line the second AI check only partly supported: the verdict and its reason are shown, and the decision is still the reader's.
- `11d-how-it-works-1440.png` (4e4ff36): The page How each answer is checked, linked from the top of every screen: code first, then the second AI check, then the person decides.
- `11d-how-it-works-390.png` (4e4ff36): The page How each answer is checked, linked from the top of every screen: code first, then the second AI check, then the person decides.
- `12-step2-saved-1440.png` (4e4ff36): Step 2 right after a Yes. The next line is open in the same boxes, and the line under the buttons says what was saved, with an Undo button.
- `12-step2-saved-390.png` (4e4ff36): Step 2 right after a Yes. The next line is open in the same boxes, and the line under the buttons says what was saved, with an Undo button.
- `13-step2-fix-1440.png` (4e4ff36): Step 2, Fix the wording. The line becomes a text box. Whole sentences in the record can be tapped to change which words are the quote.
- `13-step2-fix-390.png` (4e4ff36): Step 2, Fix the wording. The line becomes a text box. Whole sentences in the record can be tapped to change which words are the quote.
- `14-step2-fix-refused-1440.png` (4e4ff36): Step 2, a wording the checks refuse. The message says which number is not in the highlighted quote. The text stays in the box and nothing is saved.
- `15-step2-warning-1440.png` (4e4ff36): Step 2, a warning for the attorney. It is explained in plain words with the record words that support it. The question is whether the attorney should be told. Warnings go in the notes, never in the letter.
- `15-step2-warning-390.png` (4e4ff36): Step 2, a warning for the attorney. It is explained in plain words with the record words that support it. The question is whether the attorney should be told. Warnings go in the notes, never in the letter.
- `16-step2-gap-1440.png` (4e4ff36): Step 2, a break in treatment. The gap length (73 days) was counted by code, and the records on both sides of the gap are shown with their dates highlighted.
- `16-step2-gap-390.png` (4e4ff36): Step 2, a break in treatment. The gap length (73 days) was counted by code, and the records on both sides of the gap are shown with their dates highlighted.
- `17-step2-warning-note-1440.png` (4e4ff36): Step 2, Add a note to a warning. A text box opens in the card, with Save note and Cancel.
- `18-step2-disputed-1440.png` (4e4ff36): Step 2, a line the second check only partly supported. Yes is disabled until the reader ticks that she read the line against the highlighted words herself.
- `18-step2-disputed-390.png` (4e4ff36): Step 2, a line the second check only partly supported. Yes is disabled until the reader ticks that she read the line against the highlighted words herself.
- `19-step2-disputed-ticked-1440.png` (4e4ff36): The same line after the box is ticked. Yes, this matches is now available.
- `20-step2-cannot-check-1440.png` (4e4ff36): Step 2, a line we couldn't check. The reason is given and nothing is highlighted. These items are optional. (For this picture the demo's prepared answer for record 4 was removed, so the page shows what it does when an answer is missing.)
- `20-step2-cannot-check-390.png` (4e4ff36): Step 2, a line we couldn't check. The reason is given and nothing is highlighted. These items are optional. (For this picture the demo's prepared answer for record 4 was removed, so the page shows what it does when an answer is missing.)
- `21-step2-write-1440.png` (4e4ff36): Step 2, Write it myself. She picks whole sentences from the record and types her own line. Save my line sends it through the same checks.
- `21-step2-write-390.png` (4e4ff36): Step 2, Write it myself. She picks whole sentences from the record and types her own line. Save my line sends it through the same checks.
- `22-step2-cannot-confirm-warning-1440.png` (4e4ff36): Step 2, a warning the second check couldn't confirm. It cannot go in the notes. The reader can leave it out or tell the attorney herself.
- `22-step2-cannot-confirm-warning-390.png` (4e4ff36): Step 2, a warning the second check couldn't confirm. It cannot go in the notes. The reader can leave it out or tell the attorney herself.
- `23-step2-date-1440.png` (4e4ff36): Step 2, a date to pick. The record's date could be read two ways, so no date is chosen for her. The page offers both readings, month first and day first, and marks one as suggested with the reason.
- `23-step2-date-390.png` (4e4ff36): Step 2, a date to pick. The record's date could be read two ways, so no date is chosen for her. The page offers both readings, month first and day first, and marks one as suggested with the reason.
- `24-step2-done-1440.png` (4e4ff36): Step 2 done: a big check, the counts of what was kept, left out and flagged for the attorney, and one row per item with its answer and a Change button.
- `24-step2-done-390.png` (4e4ff36): Step 2 done: a big check, the counts of what was kept, left out and flagged for the attorney, and one row per item with its answer and a Change button.
- `25-step2-steps-open-390.png` (4e4ff36): The step list on a phone. It folds into one line to leave room for the record, and opens with a tap to show all four steps.
- `26-step2-entry-dark-1440.png` (4e4ff36): Step 2 in dark mode, which follows the computer's setting.
- `27-step3-charge-1440.png` (4e4ff36): Step 3, one bill amount at a time. The record shows the figure; the question is whether this charge counts toward the bill total. The total so far is in the title row.
- `27-step3-charge-390.png` (4e4ff36): Step 3, one bill amount at a time. The record shows the figure; the question is whether this charge counts toward the bill total. The total so far is in the title row.
- `28-step3-never-1440.png` (4e4ff36): Step 3, an amount that is never added to the total (here a rate). The reason is given, and the choice is only whether to list it in the notes for the attorney.
- `28-step3-never-390.png` (4e4ff36): Step 3, an amount that is never added to the total (here a rate). The reason is given, and the choice is only whether to list it in the notes for the attorney.
- `29-step3-count-1440.png` (4e4ff36): Step 3, an amount that is not counted yet but could be. The reason it was not counted is given, with a note that the second check thought it may be a billed charge. Yes, count it stays disabled until she ticks the boxes that say she checked it.
- `29-step3-count-390.png` (4e4ff36): Step 3, an amount that is not counted yet but could be. The reason it was not counted is given, with a note that the second check thought it may be a billed charge. Yes, count it stays disabled until she ticks the boxes that say she checked it.
- `30-step3-count-ticked-1440.png` (4e4ff36): The same amount with the confirm box ticked. Yes, count it is now available.
- `31-step3-done-1440.png` (4e4ff36): Step 3 done: the bill total as the letter will print it, and three plain lists: counted, not counted by her, and never counted.
- `31-step3-done-390.png` (4e4ff36): Step 3 done: the bill total as the letter will print it, and three plain lists: counted, not counted by her, and never counted.
- `32-classic-1440.png` (4e4ff36): The older review screen, kept at /classic for people who want every control on one page.
- `40-step4-letter-1440.png` (4e4ff36): Step 4, Get your letter. The letter is on the left, ready to paste into a demand letter. The notes for the attorney, marked do not send, are on the right. Copy and Download buttons sit under each.
- `40-step4-letter-390.png` (4e4ff36): Step 4, Get your letter. The letter is on the left, ready to paste into a demand letter. The notes for the attorney, marked do not send, are on the right. Copy and Download buttons sit under each.
- `41-step4-letter-numbered-1440.png` (4e4ff36): Step 4 after typing an exhibit number and a Bates prefix. The numbers are filled into the letter's source tags.
- `42-step4-pending-1440.png` (4e4ff36): Step 4 with items still undecided. The letter shows what would be sent now, and copying needs one tick that says she knows those items stay out.
- `42-step4-pending-390.png` (4e4ff36): Step 4 with items still undecided. The letter shows what would be sent now, and copying needs one tick that says she knows those items stay out.
- `43-step4-blocked-1440.png` (4e4ff36): Step 4 when nothing has been answered. The letter can't be made, the page says why in the server's own words, and a button goes to the step that fixes it.
- `43-step4-blocked-390.png` (4e4ff36): Step 4 when nothing has been answered. The letter can't be made, the page says why in the server's own words, and a button goes to the step that fixes it.
- `44-home-cases-1440.png` (4e4ff36): Your cases with several cases at different steps. Each card shows its four steps, a Next line that says exactly what to do, and one Continue button.
- `44-home-cases-390.png` (4e4ff36): Your cases with several cases at different steps. Each card shows its four steps, a Next line that says exactly what to do, and one Continue button.
- `44b-home-finished-1440.png` (4e4ff36): Your cases, scrolled down to Finished. A case whose letter is ready moves here and says Letter ready, with a button that opens the letter.
- `44b-home-finished-390.png` (4e4ff36): Your cases, scrolled down to Finished. A case whose letter is ready moves here and says Letter ready, with a button that opens the letter.
- `45-home-rename-1440.png` (4e4ff36): Your cases, renaming a case. The title turns into a box inside the same card, with Save and Cancel.
- `46-home-delete-1440.png` (4e4ff36): Your cases, deleting a case. The card's bottom row asks first: Delete this case and all its answers, with Yes, delete and Keep it.
- `47-step1-add-demo-1440.png` (4e4ff36): Step 1 in the public demo. Paste and Upload are shown but switched off, with the reason in plain words (this demo can only read the sample case and our test cases). The sample case is already chosen.
- `47-step1-add-demo-390.png` (4e4ff36): Step 1 in the public demo. Paste and Upload are shown but switched off, with the reason in plain words (this demo can only read the sample case and our test cases). The sample case is already chosen.
- `48-home-demo-empty-1440.png` (4e4ff36): Your cases in the public demo. There is no list of other people's cases; this browser lists only the cases it started.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:50.669Z

**tool call — Monitor**
````
{
 "command": "sleep 1; echo waiting",
 "description": "noop",
 "timeout_ms": 1000,
 "persistent": "false"
}
````

### User / tool · 2026-11-03T13:31:50.675Z

**tool result**
````
Monitor started (task bsb1pm83k, expires in 1s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:53.508Z

Waiting for the runs to finish.

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:53.873Z

**tool call — Bash**
````
{
 "command": "grep -n \"CAPTIONS\\|NARRATION\" tests/demo_assets/*.py | head"
}
````

### User / tool · 2026-11-03T13:31:53.964Z

**tool result**
````
tests/demo_assets/script.py:2:video.py plays it and NARRATION.md is generated from the same beats with their measured times. Edit the words here, then re-run video.py."""
tests/demo_assets/video.py:2:Usage: .venv/bin/python tests/demo_assets/video.py [--rev HEAD] [--out artifacts/demo.webm] [--narration artifacts/NARRATION.md]
tests/demo_assets/video.py:4:Timings in NARRATION.md are measured from this run (seconds from the first frame, about +-1 s). Nothing is stubbed: every click goes to the real app."""
tests/demo_assets/video.py:89:    ap.add_argument("--out", default=str(K.ROOT / "artifacts" / "demo.webm")); ap.add_argument("--narration", default=str(K.ROOT / "artifacts" / "NARRATION.md"))
tests/demo_assets/shots.py:4:Every shot is a real page of the real app. Four states cannot happen on the curated demo set and are produced by answering the page's own request with a stub, named in CAPTIONS:
tests/demo_assets/shots.py:306:    ap = argparse.ArgumentParser(); ap.add_argument("--rev", default="HEAD"); ap.add_argument("--stage", default="all"); ap.add_argument("--out", default=str(K.ROOT / "artifacts" / "screenshots" / "final")); ap.add_argument("--captions", default=str(K.ROOT / "artifacts" / "CAPTIONS.md"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:31:58.874Z

**tool call — Monitor**
````
{
 "command": "until grep -q \"^exit\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots.log 2>/dev/null && grep -q finished /tmp/v; do sleep 5; done; echo both done",
 "description": "wait for shots and video runs",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-03T13:31:58.883Z

**tool result**
````
Monitor started (task b7b1fy91e, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:01.145Z

**tool call — Bash**
````
{
 "command": "git show f6d5c19 --stat | head -20; git show f6d5c19 -- app/frontend | grep '^[+-]' | grep -v '^+++\\|^---' | cut -c1-250 | head -40"
}
````

### User / tool · 2026-11-03T13:32:01.293Z

**tool result**
````
commit f6d5c1919a26b7e71f67dfd079b520d5aa82ec68
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Tue Nov 3 07:29:57 2026 -0600

    feat(frontend): T-214 a flag only code found shows its origin label, not the Prepared answer tag; the how-checked panel says the same
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/guided/review.js |  3 ++-
 app/frontend/timeline.js      |  2 +-
 tests/e2e/guided/test_t211.py | 14 ++++++++++++++
 3 files changed, 17 insertions(+), 2 deletions(-)
+    if (item.origin_label) return { cls: "never", text: item.origin_label, title: "Found by a program, not drafted by an AI." };      // T-214: a flag only code found says so; it is not a prepared answer
-        vCode.replaceChildren(...[c.text, " ", more, ul].filter(Boolean));
+        vCode.replaceChildren(...[c.text, " ", more, ul, !item.prepared && item.origin_label ? h("p", { class: "how-lead", "data-testid": "how-origin" }, item.origin_label + ".") : null].filter(Boolean));      // T-214: said once here and on the tag
-  const aiTag = (e) => !e.ai_drafted ? null : e.prepared
+  const aiTag = (e) => e.origin_label && !e.prepared ? el("span", { class: "tag", "data-testid": "tag-origin", title: "Found by a program, not drafted by an AI." }, e.origin_label) : !e.ai_drafted ? null : e.prepared
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:02.984Z

**tool call — Bash**
````
{
 "command": "grep -rn \"origin_label\" app/backend/*.py | head -5; git log --oneline -12 | cat"
}
````

### User / tool · 2026-11-03T13:32:03.093Z

**tool result**
````
app/backend/present.py:312:            v["origin_label"] = CODE_ONLY_FLAG_ORIGINS[v["origin"]]
f6d5c19 feat(frontend): T-214 a flag only code found shows its origin label, not the Prepared answer tag; the how-checked panel says the same
d15c9ab fix(backend): flags found only by code are not prepared answers (T-214)
b50952d feat(backend): T-202 r7 D-073 fallback applied: the letter and Step 3 print the fillable blank on every charge line, no service date extracted; letter_check requires the blank form; reader kept as service_date.read (SCOPE_CUTS 28)
e22cae8 fix(frontend): T-211 r2 second AI row is one statement from the judge state; phone strip above the action bar
b695ffc docs(architect): LLM_VS_CODE rows 2-3 state the D-073 fallback: charge dates print the blank (T-207)
3c599d8 T-213: remove the Office tab (UI, /api/office, tests)
cda2856 feat(qa): T-184 demo assets: 72 final screenshots (1440x900, 390x844) with captions, 167 s Playwright walkthrough video, timed narration; scripts in tests/demo_assets (captured at 4e4ff36)
4e4ff36 chore(frontend): T-211 refresh the ladder picture from submission/validation-ladder.svg
82217e5 feat(frontend): T-211 How this was checked on every Step 2/3 item, How each answer is checked page, Step 3 reads date_label
3784bfb docs(writer): T-188 submission checklist, email draft, NEEDS_CHRIS by priority, product note and Part 2 refreshed (T-181, T-179, D-071 to D-073), PDFs
6be191f docs(release): T-212 README as front door: run, 3-minute walk, how the AI is checked, what's where, limits
9655f1d test(backend): T-202 r6 pin the 60-character UB-04 label window in production and the check; drop the unreachable statement-date branches of the check
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:08.162Z

**tool call — Bash**
````
{
 "command": "grep -n \"CODE_ONLY_FLAG_ORIGINS\" -A6 app/backend/present.py | head -14; git diff 4e4ff36 HEAD -- app/frontend/guided/review.js | grep '^[+-]' | cut -c1-260 | head -60"
}
````

### User / tool · 2026-11-03T13:32:08.298Z

**tool result**
````
310:        if str(v.get("id", "")).startswith("f_") and v.get("origin") in CODE_ONLY_FLAG_ORIGINS:
311-            prepared = False      # T-214: found only by code (the phrase list; the model's answer had nothing for it), so no curated answer is behind it
312:            v["origin_label"] = CODE_ONLY_FLAG_ORIGINS[v["origin"]]
313-        v["prepared"] = prepared
314-        if gen is not None:
315-            gen = v["ladder"]["generator"] = dict(gen, prepared=prepared)      # a copy: the stored row is never touched
316-            if prepared:
317-                gen["model"] = call["model"]
318-
--
320:CODE_ONLY_FLAG_ORIGINS = {"lexicon": "Found by code (phrase list)", "code": "Found by code"}      # T-214 (D-065): a flag whose only source is code is never a "prepared answer"
321-FLAG_AI_ORIGINS = ("llm", "lexicon+llm", "lexicon")      # the record's flag call ran for these (the phrase-list-only ones too: the call found nothing for them)
322-
323-
--- a/app/frontend/guided/review.js
+++ b/app/frontend/guided/review.js
+    if (item.origin_label) return { cls: "never", text: item.origin_label, title: "Found by a program, not drafted by an AI." };      // T-214: a flag only code found says so; it is not a prepared answer
+  /* One statement from the judge step's real state (T-211 r2). The "prepared by our team; the second AI then checked it" lead is said only when the second AI really returned a verdict;
+     a step that was skipped says "Not run" when its reason starts "Not run" (the phrase list found it, so there is nothing to double-check) and "Not needed" when code made the item. */
-    const prep = !!(item && item.prepared), lead = prep ? "Prepared by our team; the second AI check then checked it against the quote." : "";
-    if (!st) return { state: "none", word: "Not run", chip: "AI: not run", lead, text: "No second AI check applies to this item.", model: "" };
+    const prep = !!(item && item.prepared), LEAD = "Prepared by our team; the second AI check then checked it against the quote.";
+    if (!st) return { state: "none", word: "Not run", chip: "AI: not run", lead: "", text: "No second AI check applies to this item.", model: "" };
-    if (st.status === "skipped" && !ev.judge_verdict) return { state: "none", word: "Not needed", chip: "AI: not needed", lead, text: cap(text.replace(/^Not needed: /, "")), model: "" };
-    if (st.status === "pending") return { state: "warn", word: "Not run yet", chip: "AI: not run yet", lead, text, model: m };
+    if (st.status === "skipped" && !ev.judge_verdict) {
+      if (/^not run\b/i.test(text)) return { state: "none", word: "Not run", chip: "AI: not run", lead: "", text: cap(text.replace(/^Not run:? ?/i, "")), model: "" };
+      return { state: "none", word: "Not needed", chip: "AI: not needed", lead: "", text: cap(text.replace(/^Not needed: /, "")), model: "" };
+    }
+    if (st.status === "pending") return { state: "warn", word: "Not run yet", chip: "AI: not run yet", lead: "", text, model: m };
-    return { state: v[1], word: v[0], chip: v[2], lead, text, model: m };
+    return { state: v[1], word: v[0], chip: v[2], lead: prep ? LEAD : "", text, model: m };
-    /* T-211: "How this was checked" sits under the quote in the record card on a wide screen (it never takes room from the line), and at the end of the line card on a phone (that card scrolls as one box; the footer with its tick box stays beside the line) */
+    /* T-211: "How this was checked" sits under the quote in the record card on a wide screen (it never takes room from the line), and on a phone as a one-line strip directly above the action bar (always in view; opened, its rows float above the bar and do no
-    const placeHow = () => { const into = narrowMQ.matches ? E.lineCard : E.srcCard; if (E.how.parentNode !== into) into.append(E.how); };
-    narrowMQ.addEventListener("change", placeHow); placeHow();
+    const placeHow = () => { if (narrowMQ.matches && E.actions) { if (E.how.parentNode !== E.actions || E.actions.firstChild !== E.how) E.actions.prepend(E.how); } else if (E.how.parentNode !== E.srcCard) E.srcCard.append(E.how); };
+    narrowMQ.addEventListener("change", placeHow);
+    placeHow();
-        vCode.replaceChildren(...[c.text, " ", more, ul].filter(Boolean));
+        vCode.replaceChildren(...[c.text, " ", more, ul, !item.prepared && item.origin_label ? h("p", { class: "how-lead", "data-testid": "how-origin" }, item.origin_label + ".") : null].filter(Boolean));      // T-214: said once here and on the tag; the same
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:13.204Z

**tool call — Monitor**
````
{
 "command": "until grep -q \"^exit\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots.log 2>/dev/null && grep -q finished /tmp/v; do sleep 5; done; echo both done",
 "description": "wait for both runs",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-03T13:32:13.214Z

**tool result**
````
Monitor started (task bydr3txcn, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:17.466Z

**tool call — Bash**
````
{
 "command": "sleep 240; cat /tmp/v | tail -3; tail -3 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots.log",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T13:32:17.469Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 240 followed by: cat /tmp/v tail -3 tail -3 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots.log. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:20.670Z

Monitor is armed; waiting for it.

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:21.271Z

**tool call — Monitor**
````
{
 "command": "until grep -q finished /tmp/v; do sleep 5; done; echo video done",
 "description": "wait for video",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-03T13:32:21.281Z

**tool result**
````
Monitor started (task b3bjshs2d, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:24.435Z

**tool call — Monitor**
````
{
 "command": "until grep -q \"^exit\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shots.log; do sleep 5; done; echo shots done",
 "description": "wait for shots",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-03T13:32:24.445Z

**tool result**
````
Monitor started (task b4snafpls, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:26.306Z

**tool call — Bash**
````
{
 "command": "echo waiting"
}
````

### User / tool · 2026-11-03T13:32:26.430Z

**tool result**
````
waiting
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:32:32.379Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until grep -q \"^exit\" $S/shots.log && grep -q finished /tmp/v; do sleep 5; done; tail -4 $S/shots.log; cat /tmp/v",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T13:34:02.828Z

**tool result**
````
shot 48-home-demo-empty-1440.png 
server pid 55632 stopped
commit f6d5c1919a26b7e71f67dfd079b520d5aa82ec68 shots 72
exit 0
archive f6d5c1919a26b7e71f67dfd079b520d5aa82ec68
server pid 51887 port 60059 local=False
beat home at 0.1s
beat records at 14.7s
beat drafted at 20.5s
beat item at 38.9s
beat checks at 49.3s
beat panel at 67.0s
beat howpage at 77.4s
beat answer at 89.4s
beat warning at 97.9s
beat rest at 107.1s
beat step2done at 115.4s
beat bills at 118.8s
beat never at 127.3s
beat step3done at 135.0s
beat letter at 140.8s
beat download at 151.6s
beat close at 158.1s
server pid 51887 stopped
video /Users/arsis/zlayt-pm-project/artifacts/demo.webm 19.5 MB, about 169 s
finished
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:04.737Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/40-step4-letter-1440.png"
}
````

### User / tool · 2026-11-03T13:34:04.746Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:05.062Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/11b-step2-how-checked-1440.png"
}
````

### User / tool · 2026-11-03T13:34:05.070Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:05.282Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/16-step2-gap-1440.png"
}
````

### User / tool · 2026-11-03T13:34:05.289Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:09.341Z

**tool call — Bash**
````
{
 "command": "git show b50952d | grep -n \"service date\\|blank\\|\\[\" | grep '^[0-9]*:[+]' | cut -c1-260 | head -15; git status --short artifacts/CAPTIONS.md artifacts/NARRATION.md artifacts/demo.webm; git diff artifacts/CAPTIONS.md | grep '^[+-]' | grep -v \"^+++\\|^---\" | grep -v \"4e4ff36\\|f6d5c19\" | head; sed -n 1,200p tests/demo_assets/shots.py | grep -n \"step4\\|letter\" | head -20"
}
````

### User / tool · 2026-11-03T13:34:09.508Z

**tool result**
````
30:+        """D-073 fallback: in the order of the record dates (the letter prints no service date)."""
33:+        return sorted(got, key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))
52:+        """D-073 fallback (T-202 round 6): the label before a charge's amount is ALWAYS the fillable blank, like the Bates placeholder, never a date: 'Fennimoor Spine Clinic, itemized ledger,
53:+        date of service [__________] (statement dated June 15, 2026)' (a bill's own date is its statement date, any other record's its record date). The code extracts no service date for
54:+        the letter (SCOPE_CUTS row 28); the paralegal fills the blank from the quote. One string, the same one the case view carries (`store.charge_service_date`)."""
55:+        n = a["record_no"]
66:+    """T-202 r3 + D-073 fallback: one line per accepted charge (each prints the blank for its date of service): provider, amount, why, and the request for a dated itemized bill. [] when no
73:+        why = (a.get("dos_note") or service_date.confirm_note("not_read", "")).split(" The letter prints")[0]
74:+        out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.")
84:+"""The service date a charge line prints (D-073). FALLBACK APPLIED after round 6: `resolve` never returns a date. Every charge line prints the fillable blank and the paralegal fills it from the quote;
111:+    carry a service date. Every charge line is `not_stated` and prints the fillable blank; the paralegal fills it from the quote. The reader below (`read`) stays for the day date extraction
114:+    if out["state"] == "stated":
115:+        out.update(state="not_stated", first=None, last=None, reason="not_read", raw="", raws=[])
132:+Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
140:+- Central ER discharge summary, $6,240: The letter does not take a date of service from the records. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
 M artifacts/CAPTIONS.md
 M artifacts/NARRATION.md
 M artifacts/demo.webm
2:Usage: .venv/bin/python tests/demo_assets/shots.py [--rev HEAD] [--stage main|letter|all] [--out artifacts/screenshots/final]
3:Stages: `main` = everything except the letter screens; `letter` = Your cases (with a finished case), Step 4 (ready, numbered, pending, blocked), run LAST because the letter text may still change.
180:    R.shoot("15-step2-warning", "Step 2, a warning for the attorney. It is explained in plain words with the record words that support it. The question is whether the attorney should be told. Warnings go in the notes, never in the letter.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:11.842Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/27-step3-charge-1440.png"
}
````

### User / tool · 2026-11-03T13:34:11.851Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:12.310Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/11c-step2-how-checked-disputed-1440.png"
}
````

### User / tool · 2026-11-03T13:34:12.318Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:13.415Z

**tool call — Bash**
````
{
 "command": "grep -n \"R.shoot(\\\"\\(11\\|15\\|16\\|17\\|22\\|27\\|29\\|31\\|40\\|41\\|42\\)\" tests/demo_assets/shots.py | cut -c1-120; ls artifacts/screenshots/final | grep -c .; grep -n \"T-1\\|date_label\\|__\" artifacts/screenshots/final/*.txt 2>/dev/null | head -2"
}
````

### User / tool · 2026-11-03T13:34:13.515Z

**tool result**
````
147:    R.shoot("11-step2-entry", "Step 2, one timeline line at a time. Left: the record with the quoted words highlight
157:        R.shoot("11b-step2-how-checked", "Step 2 with the How this was checked panel open: what the code found, what
164:        R.shoot("11c-step2-how-checked-disputed", "The same panel on a line the second AI check only partly supporte
165:        R.shoot("11d-how-it-works", "The page How each answer is checked, linked from the top of every screen: code 
180:    R.shoot("15-step2-warning", "Step 2, a warning for the attorney. It is explained in plain words with the record 
182:    R.shoot("16-step2-gap", "Step 2, a break in treatment. The gap length (73 days) was counted by code, and the rec
187:    R.shoot("17-step2-warning-note", "Step 2, Add a note to a warning. A text box opens in the card, with Save note 
206:    R.shoot("22-step2-cannot-confirm-warning", "Step 2, a warning the second check couldn't confirm. It cannot go in
227:    R.shoot("27-step3-charge", "Step 3, one bill amount at a time. The record shows the figure; the question is whet
236:    R.shoot("29-step3-count", "Step 3, an amount that is not counted yet but could be. The reason it was not counted
247:    R.shoot("31-step3-done", "Step 3 done: the bill total as the letter will print it, and three plain lists: counte
276:    R.shoot("40-step4-letter", "Step 4, Get your letter. The letter is on the left, ready to paste into a demand let
282:    R.shoot("41-step4-letter-numbered", "Step 4 after typing an exhibit number and a Bates prefix. The numbers are f
286:    R.shoot("42-step4-pending", "Step 4 with items still undecided. The letter shows what would be sent now, and cop
73
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:15.357Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/15-step2-warning-1440.png"
}
````

### User / tool · 2026-11-03T13:34:15.368Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:15.713Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/31-step3-done-1440.png"
}
````

### User / tool · 2026-11-03T13:34:15.721Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:16.069Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/final/29-step3-count-1440.png"
}
````

### User / tool · 2026-11-03T13:34:16.077Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:19.381Z

**tool call — Bash**
````
{
 "command": "for n in 147 157 164 165 180 182 206 227 236 247 276 282; do sed -n \"${n}p\" tests/demo_assets/shots.py | cut -c1-700; echo ---; done"
}
````

### User / tool · 2026-11-03T13:34:19.506Z

**tool result**
````
    R.shoot("11-step2-entry", "Step 2, one timeline line at a time. Left: the record with the quoted words highlighted. Right: the line to check and the plain reason it passed the checks. The question sits next to two equal answers.",
---
        R.shoot("11b-step2-how-checked", "Step 2 with the How this was checked panel open: what the code found, what the second AI check said and why, and the reader's own decision. Three checks, in that order.", panel)
---
        R.shoot("11c-step2-how-checked-disputed", "The same panel on a line the second AI check only partly supported: the verdict and its reason are shown, and the decision is still the reader's.", panel_disputed)
---
        R.shoot("11d-how-it-works", "The page How each answer is checked, linked from the top of every screen: code first, then the second AI check, then the person decides.", lambda p, w: R.go(p, "/how-it-works"))
---
    R.shoot("15-step2-warning", "Step 2, a warning for the attorney. It is explained in plain words with the record words that support it. The question is whether the attorney should be told. Warnings go in the notes, never in the letter.",
---
    R.shoot("16-step2-gap", "Step 2, a break in treatment. The gap length (73 days) was counted by code, and the records on both sides of the gap are shown with their dates highlighted.",
---
    R.shoot("22-step2-cannot-confirm-warning", "Step 2, a warning the second check couldn't confirm. It cannot go in the notes. The reader can leave it out or tell the attorney herself.",
---
    R.shoot("27-step3-charge", "Step 3, one bill amount at a time. The record shows the figure; the question is whether this charge counts toward the bill total. The total so far is in the title row.",
---
    R.shoot("29-step3-count", "Step 3, an amount that is not counted yet but could be. The reason it was not counted is given, with a note that the second check thought it may be a billed charge. Yes, count it stays disabled until she ticks the boxes that say she checked it.", count)
---
    R.shoot("31-step3-done", "Step 3 done: the bill total as the letter will print it, and three plain lists: counted, not counted by her, and never counted.",
---
    R.shoot("40-step4-letter", "Step 4, Get your letter. The letter is on the left, ready to paste into a demand letter. The notes for the attorney, marked do not send, are on the right. Copy and Download buttons sit under each.",
---
    R.shoot("41-step4-letter-numbered", "Step 4 after typing an exhibit number and a Bates prefix. The numbers are filled into the letter's source tags.", cfg, widths=("1440",))
---
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:26.689Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/demo_assets/shots.py'; s=open(p).read()\nR=[\n(\"what the code found, what the second AI check said and why, and the reader's own decision. Three checks, in that order.\",\n \"what the code found, then one statement from the second AI check (prepared by our team, then checked against the quote, with its verdict and why), then the reader's own decision. Three checks, in that order.\"),\n(\"The same panel on a line the second AI check only partly supported: the verdict and its reason are shown, and the decision is still the reader's.\",\n \"The same panel on a line the second AI check only partly supported: the verdict (Disputes) and its reason are shown in one statement, and the decision is still the reader's.\"),\n(\"The question is whether the attorney should be told. Warnings go in the notes, never in the letter.\",\n \"A grey Found by code tag shows the warning came from a program, not from a prepared AI answer. The question is whether the attorney should be told. Warnings go in the notes, never in the letter.\"),\n(\"The gap length (73 days) was counted by code, and the records on both sides of the gap are shown with their dates highlighted.\",\n \"The gap length (73 days) was counted by code, and the tag says Found by code. Its second-AI line reads Not needed, because code made the warning. The records on both sides of the gap are shown with their dates highlighted.\"),\n(\"The record shows the figure; the question is whether this charge counts toward the bill total. The total so far is in the title row.\",\n \"The record shows the figure; the question is whether this charge counts toward the bill total. The charge line carries a fillable blank, date of service [__________], with the record date in parentheses, and a yellow note says the letter takes no service date from the records and the reader fills the blank. The total so far is in the title row.\"),\n(\"and three plain lists: counted, not counted by her, and never counted.\",\n \"and three plain lists: counted, not counted by her, and never counted. Each counted charge shows the date-of-service blank and its record date.\"),\n(\"The letter is on the left, ready to paste into a demand letter. The notes for the attorney, marked do not send, are on the right. Copy and Download buttons sit under each.\",\n \"The letter is on the left, ready to paste into a demand letter; each charge line in it carries the fillable blank date of service [__________], and the bar says the [Ex. __ / Bates __] blanks are hers to fill. The notes for the attorney, marked do not send, are on the right. Copy and Download buttons sit under each.\"),\n]\nfor a,b in R:\n    assert s.count(a)==1,a; s=s.replace(a,b)\nopen(p,'w').write(s)\nE\ngrep -n \"Found by code\\|AI check\" tests/demo_assets/script.py | head"
}
````

### User / tool · 2026-11-03T13:34:26.797Z

**tool result**
````
16:    "panel": "Under the line, a panel shows how it was checked: what the code found, what the second AI check said and why, and then my own decision.",
18:    "howpage": "This page, linked at the top of every screen, explains how each answer is checked. Code first, then the second AI check, then me. The AI never has the last word.",
117:    "checks": "The same item, with its plain reason and the question and two answers.", "panel": "The panel under the line: what the code found, what the second AI check said, and your decision.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:31.784Z

**tool call — Bash**
````
{
 "command": "sed -n 1,88p tests/demo_assets/video.py"
}
````

### User / tool · 2026-11-03T13:34:31.884Z

**tool result**
````
"""T-184 demo video: a scripted, paced Playwright recording of the public demo (no case list, prepared answers) from a `git archive` copy of one commit.
Usage: .venv/bin/python tests/demo_assets/video.py [--rev HEAD] [--out artifacts/demo.webm] [--narration artifacts/NARRATION.md]
Each beat has a narration line; the beat holds the screen for at least as long as the line takes to read aloud (WPS words per second), so the script and the picture stay together.
Timings in NARRATION.md are measured from this run (seconds from the first frame, about +-1 s). Nothing is stubbed: every click goes to the real app."""
import argparse
import faulthandler
import os
import pathlib
import shutil
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from playwright.sync_api import sync_playwright  # noqa: E402
from tests.demo_assets import common as K  # noqa: E402
from tests.demo_assets.script import BEATS_VERSION, NARR, WPS  # noqa: E402

CURSOR_JS = """
(() => { const d = document.createElement('div'); d.id='__cur'; d.style.cssText='position:fixed;z-index:2147483647;width:22px;height:22px;border-radius:50%;background:rgba(220,38,38,.45);border:2px solid #dc2626;pointer-events:none;left:-40px;top:-40px;transform:translate(-50%,-50%);transition:transform .08s';
  document.addEventListener('DOMContentLoaded', () => document.documentElement.appendChild(d));
  addEventListener('mousemove', e => { d.style.left=e.clientX+'px'; d.style.top=e.clientY+'px'; }, true);
  addEventListener('mousedown', () => d.style.transform='translate(-50%,-50%) scale(.6)', true); addEventListener('mouseup', () => d.style.transform='translate(-50%,-50%)', true); })();
"""


class Rec:
    def __init__(self, page, t0):
        self.page, self.t0, self.log = page, t0, []
        self.x, self.y = 700, 450; self.shots = pathlib.Path('/private/tmp/claude-501/beats'); self.shots.mkdir(exist_ok=True)

    def now(self):
        return time.time() - self.t0

    def pause(self, s):
        self.page.wait_for_timeout(int(s * 1000))

    def tap(self, loc, dwell=0.5, steps=18):
        """Glide the pointer to the element, wait a beat so the viewer sees it, click."""
        loc.wait_for(state="visible", timeout=15000)
        b = loc.bounding_box(); tx, ty = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
        self.page.mouse.move(tx, ty, steps=steps); self.pause(dwell); loc.click()

    def beat(self, key, fn=None):
        """Run fn (the clicks) then hold until the narration for `key` has had time to be read. Records start/end."""
        print(f'beat {key} at {self.now():.1f}s', flush=True)
        text = NARR[key]; need = len(text.split()) / WPS
        start = self.now()
        if fn:
            fn()
        try:
            self.page.screenshot(path=str(self.shots / f"beat-{key}.png"))       # a still of what the viewer sees at the end of the action, for checking the narration against the picture
        except Exception:
            pass
        spent = self.now() - start
        if spent < need:
            self.pause(need - spent)
        self.log.append((key, start, self.now(), text))

    def beat_during(self, key, fn=None):
        """Narration plays *while* the pointer works: the beat is as long as the longer of the two."""
        self.beat(key, fn)


def run(rev, out, narr_out):
    src, sha = K.archive(rev); print("archive", sha, flush=True)
    vid_dir = pathlib.Path(K.tempfile.mkdtemp(prefix="demo-vid-"))
    with sync_playwright() as pw, K.server(src, local=False) as (base, db):
        br = pw.chromium.launch()
        ctx = br.new_context(viewport={"width": 1440, "height": 900}, record_video_dir=str(vid_dir), record_video_size={"width": 1280, "height": 800},
                             permissions=["clipboard-read", "clipboard-write"], accept_downloads=True, color_scheme="light")
        ctx.add_init_script(CURSOR_JS)
        t0 = time.time(); page = ctx.new_page(); R = Rec(page, t0)
        import tests.demo_assets.script as S
        try:
            S.play(R, page, base, vid_dir)
        except Exception:
            page.screenshot(path=str(vid_dir / "FAILED.png")); print("FAILED screenshot", vid_dir / "FAILED.png", flush=True); print(page.url, page.locator("body").inner_text()[:600]); raise
        ctx.close(); total = R.now()
        vids = list(vid_dir.glob("*.webm")); assert vids, "no video written"
        out.parent.mkdir(parents=True, exist_ok=True); shutil.copy(vids[0], out); br.close()
    print(f"video {out} {out.stat().st_size/1e6:.1f} MB, about {total:.0f} s", flush=True)
    assert total <= 178, f"over the 180 s budget: {total:.0f}"
    S.write_narration(narr_out, R.log, total, sha)
    return sha


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--rev", default="HEAD")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:40.203Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/demo_assets/script.py'; s=open(p).read()\nR=[\n(\"what the code found, what the second AI check said and why, and then my own decision.\\\",\\n    \\\"answer\\\"\",\"what the code found, one line from the second AI check with its verdict and why, and then my own decision.\\\",\\n    \\\"answer\\\"\"),\n(\"A warning is for the attorney. It goes in the notes for her, never in the letter. I decide whether she should be told.\",\n \"A warning is for the attorney. This one is tagged Found by code: a program counted the days, not an AI. It goes in the notes for her, never in the letter. I decide whether she should be told.\"),\n(\"Step 4. The letter is on the left. The notes\",\"Step 4. The letter is on the left, with a blank for each charge's date of service. The notes\"),\n(\"what the code found, what the second AI check said, and your decision.\",\"what the code found, one line from the second AI check, and your decision.\"),\n(\"A break-in-treatment warning (73 days between records 6 and 7) with both records highlighted.\",\"A break-in-treatment warning (73 days between records 6 and 7) with both records highlighted and the grey Found by code tag.\"),\n(\"Step 4: the letter and the notes for the attorney; Copy letter\",\"Step 4: the letter (each charge line has the date-of-service blank) and the notes for the attorney; Copy letter\"),\n]\nfor a,b in R:\n    assert s.count(a)==1,a; s=s.replace(a,b)\nopen(p,'w').write(s)\nE\ngrep -n '\"panel\"' tests/demo_assets/script.py | head -3"
}
````

### User / tool · 2026-11-03T13:34:40.328Z

**tool result**
````
16:    "panel": "Under the line, a panel shows how it was checked: what the code found, one line from the second AI check with its verdict and why, and then my own decision.",
73:        R.beat("panel", lambda: (open_panel(page), R.pause(0.5)))
117:    "checks": "The same item, with its plain reason and the question and two answers.", "panel": "The panel under the line: what the code found, one line from the second AI check, and your decision.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:34:48.937Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/demo_assets/script.py'; s=open(p).read()\na=\"        R.pause(1)\\n    R.beat(\\\"download\\\", show_file)\"\nb=\"\"\"        page.evaluate(\\\"\\\"\\\"() => { const n = document.querySelector('pre').firstChild, i = n.data.indexOf('date of service ['); if (i < 0) return;\n            const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 17); const m = document.createElement('mark'); r.surroundContents(m); m.scrollIntoView({block: 'center'}); }\\\"\\\"\\\")      # the first charge line's blank, in view\n        R.pause(1)\n    R.beat(\"download\", show_file)\"\"\"\nassert s.count(a)==1; s=s.replace(a,b)\ns=s.replace('\"download\": \"This is the file I downloaded. It is plain text, ready to paste into a demand letter.\"','\"download\": \"This is the file I downloaded. It is plain text, ready to paste into a demand letter. Here is a charge line with its blank for the date of service.\"')\ns=s.replace('\"download\": \"The downloaded .txt file opened in the browser.\"','\"download\": \"The downloaded .txt file opened in the browser, scrolled to a charge line with its date-of-service blank highlighted.\"')\nopen(p,'w').write(s)\nE\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\n.venv/bin/python tests/demo_assets/video.py > $S/video.log 2>&1; tail -8 $S/video.log",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T13:37:57.663Z

**tool result**
````
video /Users/arsis/zlayt-pm-project/artifacts/demo.webm 21.3 MB, about 185 s
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/tests/demo_assets/video.py", line 90, in <module>
    a = ap.parse_args(); run(a.rev, pathlib.Path(a.out), pathlib.Path(a.narration))
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/tests/demo_assets/video.py", line 82, in run
    assert total <= 178, f"over the 180 s budget: {total:.0f}"
AssertionError: over the 180 s budget: 185
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:38:03.018Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep beat $S/video.log | paste -sd' ' | fold -w 200"
}
````

### User / tool · 2026-11-03T13:38:03.114Z

**tool result**
````
usage: paste [-s] [-d delimiters] file ...
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:38:06.697Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep beat $S/video.log | tr '\\n' ' '"
}
````

### User / tool · 2026-11-03T13:38:06.795Z

**tool result**
````
beat home at 0.1s beat records at 14.7s beat drafted at 20.5s beat item at 38.9s beat checks at 49.3s beat panel at 67.0s beat howpage at 79.0s beat answer at 91.0s beat warning at 99.4s beat rest at 114.4s beat step2done at 122.7s beat bills at 126.2s beat never at 134.6s beat step3done at 142.4s beat letter at 148.2s beat download at 162.4s beat close at 173.9s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:38:17.532Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/demo_assets/script.py'; s=open(p).read()\nR=[\n(\"one line from the second AI check with its verdict and why, and then\",\"the second AI check's verdict and why, and then\"),\n(\"A warning is for the attorney. This one is tagged Found by code: a program counted the days, not an AI. It goes in the notes for her, never in the letter. I decide whether she should be told.\",\n \"This warning is tagged Found by code: a program counted the days. It goes in the notes for the attorney, never in the letter. I decide whether she should be told.\"),\n(\"Step 4. The letter is on the left, with a blank for each charge's date of service. The notes\",\"Step 4. The letter is on the left. The notes\"),\n(\"This is the file I downloaded. It is plain text, ready to paste into a demand letter. Here is a charge line with its blank for the date of service.\",\"This is the file I downloaded, plain text, ready to paste. Each charge line has a blank for the date of service.\"),\n(\"one line from the second AI check, and your decision.\",\"the second AI check's verdict, and your decision.\"),\n]\nfor a,b in R:\n    assert s.count(a)==1,a; s=s.replace(a,b)\nopen(p,'w').write(s)\nE\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\n.venv/bin/python tests/demo_assets/video.py > $S/video.log 2>&1; tail -3 $S/video.log; grep beat $S/video.log | tr '\\n' ' '",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T13:41:13.905Z

**tool result**
````
beat close at 162.4s
server pid 68330 stopped
video /Users/arsis/zlayt-pm-project/artifacts/demo.webm 20.2 MB, about 174 s
beat home at 0.1s beat records at 14.7s beat drafted at 20.5s beat item at 38.9s beat checks at 49.3s beat panel at 67.0s beat howpage at 77.0s beat answer at 89.0s beat warning at 97.5s beat rest at 109.4s beat step2done at 117.8s beat bills at 121.2s beat never at 129.7s beat step3done at 137.4s beat letter at 143.2s beat download at 154.0s beat close at 162.4s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:41:17.174Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/beats/beat-download.png"
}
````

### User / tool · 2026-11-03T13:41:17.183Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:41:17.426Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/beats/beat-warning.png"
}
````

### User / tool · 2026-11-03T13:41:17.440Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:41:18.480Z

Good. Re-run shots for the new captions, then commit.

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:41:22.819Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ngit rev-parse --short HEAD; .venv/bin/python tests/demo_assets/shots.py --stage all > $S/shots2.log 2>&1; tail -2 $S/shots2.log; grep -c \"f6d5c19\" artifacts/CAPTIONS.md; grep -c 4e4ff36 artifacts/CAPTIONS.md; grep -n \"Found by code\\|date of service\" artifacts/CAPTIONS.md | cut -c1-120; head -12 artifacts/NARRATION.md | cut -c1-200; ls artifacts/*.webm; git status --short artifacts | grep -v \"review-evidence\\|guided\\|t060\" | head",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T13:42:52.747Z

**tool result**
````
f6d5c19
server pid 75006 stopped
commit f6d5c1919a26b7e71f67dfd079b520d5aa82ec68 shots 72
72
0
32:- `15-step2-warning-1440.png` (f6d5c19): Step 2, a warning for the attorney. It is explained in plain words with the 
33:- `15-step2-warning-390.png` (f6d5c19): Step 2, a warning for the attorney. It is explained in plain words with the r
34:- `16-step2-gap-1440.png` (f6d5c19): Step 2, a break in treatment. The gap length (73 days) was counted by code, and 
35:- `16-step2-gap-390.png` (f6d5c19): Step 2, a break in treatment. The gap length (73 days) was counted by code, and t
52:- `27-step3-charge-1440.png` (f6d5c19): Step 3, one bill amount at a time. The record shows the figure; the question 
53:- `27-step3-charge-390.png` (f6d5c19): Step 3, one bill amount at a time. The record shows the figure; the question i
62:- `40-step4-letter-1440.png` (f6d5c19): Step 4, Get your letter. The letter is on the left, ready to paste into a dem
63:- `40-step4-letter-390.png` (f6d5c19): Step 4, Get your letter. The letter is on the left, ready to paste into a dema
# Narration script for artifacts/demo.webm

Read this in your own voice. The times are measured from the recording (about 174 seconds in all, 438 words, at a calm pace of about 2.6 words a second; allow a second either way).
Captured from commit `f6d5c19`. Per D-065 the demo runs on prepared answers: the summaries and warnings were prepared by our team, then checked by code and by a second AI model, and nothing new is sen
Say "prepared by our team", not "the AI wrote this", whenever you talk about the sample lines.

| Time | Say |
|---|---|
| 0:00-0:14 | This is Your cases, the home page. The yellow bar says the data is synthetic, and the blue label says the sample answers were prepared by our team. I have no cases yet, so I open the sam
| 0:14-0:20 | Step 1 found the nine records in the sample case. I press Draft the timeline. |
| 0:20-0:38 | In this demo the summaries and warnings were prepared by our team ahead of time. They were not written by an AI just now, and nothing is sent to an AI while this demo runs. Nineteen time
| 0:38-0:49 | Step 2 shows one item at a time. On the left is the record, with the quoted words highlighted. On the right is the line to check. |
artifacts/demo.webm
 M artifacts/CAPTIONS.md
 M artifacts/NARRATION.md
 M artifacts/demo.webm
 M artifacts/screenshots/final/08-step1-drafting-1440.png
 M artifacts/screenshots/final/11-step2-entry-390.png
 M artifacts/screenshots/final/11b-step2-how-checked-390.png
 M artifacts/screenshots/final/11c-step2-how-checked-disputed-390.png
 M artifacts/screenshots/final/12-step2-saved-1440.png
 M artifacts/screenshots/final/12-step2-saved-390.png
 M artifacts/screenshots/final/13-step2-fix-390.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:42:56.436Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXXXX) && git read-tree HEAD && git add artifacts/CAPTIONS.md artifacts/NARRATION.md artifacts/demo.webm artifacts/screenshots/final tests/demo_assets && git commit -q -m \"feat(qa): T-184 re-capture at f6d5c19: letter charge blank, one-statement panel, Found by code tag; 72 shots, 174 s video, captions and narration updated\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log --oneline -1 && git show --stat HEAD | tail -3; unset GIT_INDEX_FILE; git status --short artifacts/CAPTIONS.md tests/demo_assets | head -3"
}
````

### User / tool · 2026-11-03T13:42:56.557Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXXXX) && git read-tree HEAD && git add artifacts/CAPTIONS.md artifacts/NARRATION.md artifacts/demo.webm artifacts/screenshots/final test
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:42:58.234Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx.t184 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add artifacts/CAPTIONS.md artifacts/NARRATION.md artifacts/demo.webm artifacts/screenshots/final tests/demo_assets && git diff --cached --stat | tail -2"
}
````

### User / tool · 2026-11-03T13:42:59.257Z

**tool result**
````
 tests/demo_assets/shots.py                         |  14 +-
 38 files changed, 198 insertions(+), 196 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:43:01.032Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx.t184 && git commit -q -m \"feat(qa): T-184 re-capture at f6d5c19: letter charge blank, one-statement panel, Found by code tag; 72 shots, 174 s video, captions and narration updated\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log --oneline -1"
}
````

### User / tool · 2026-11-03T13:43:03.288Z

**tool result**
````
check_secrets: ok (38 file(s) scanned staged)
5974034 feat(qa): T-184 re-capture at f6d5c19: letter charge blank, one-statement panel, Found by code tag; 72 shots, 174 s video, captions and narration updated
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:43:07.426Z

**tool call — Bash**
````
{
 "command": "unset GIT_INDEX_FILE; git reset -q -- artifacts/CAPTIONS.md artifacts/NARRATION.md artifacts/demo.webm artifacts/screenshots/final tests/demo_assets; git status --short artifacts/CAPTIONS.md tests/demo_assets artifacts/screenshots/final | wc -l; B=\"python3 tools/board.py\"; $B commit T-184 --sha 5974034 --agent qa; $B note T-184 --agent qa --text \"Re-captured at f6d5c19, commit 5974034: 72 shots, demo.webm 174 s (video.py asserts <=178), captions and narration updated for the date-of-service blank (letter, Step 3, downloaded file highlighted), one-statement second-AI panel, and the Found by code tag (gap warning narrated). Scripts in tests/demo_assets updated.\""
}
````

### User / tool · 2026-11-03T13:43:08.011Z

**tool result**
````
       0
T-184: commit 5974034 recorded
noted on T-184
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:43:10.178Z

T-184 is re-captured at f6d5c19 and committed as 5974034: 72 screenshots and `demo.webm` at 174 s (the script fails above 178 s). `CAPTIONS.md` and `NARRATION.md` now cover the date-of-service blank in the letter, Step 3 and the downloaded file, the one-statement second-AI panel, and the Found by code tag on the gap warning. The commit also carries the changes to `tests/demo_assets/shots.py` and `script.py`, and I recorded it with a note on T-184. I read only a few of the new screenshots and beat stills (letter, Step 2 panel, Step 3 pages, the warning and downloaded-file beats), not all 72.
