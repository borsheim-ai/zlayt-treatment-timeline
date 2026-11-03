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
    "panel": "Under the line, a panel shows how it was checked: what the code found, the second AI check's verdict and why, and then my own decision.",
    "answer": "I read the highlighted words, then say Yes, this matches. The next item opens in the same boxes, and I can undo.",
    "howpage": "This page, linked at the top of every screen, explains how each answer is checked. Code first, then the second AI check, then me. The AI never has the last word.",
    "warning": "This warning is tagged Found by code: a program counted the days. It goes in the notes for the attorney, never in the letter. I decide whether she should be told.",
    "rest": "To save time I will say yes to the rest. In real use I would read each one.",
    "step2done": "Step 2 is done. Every item has an answer.",
    "bills": "Step 3 is the bill amounts. Code finds them and adds them up. I decide whether each charge counts toward the total.",
    "never": "Some amounts, like this rate, are never added to the total. The page says so.",
    "step3done": "Step 3 is done. The total is added up by code, not by an AI.",
    "letter": "Step 4. The letter is on the left. The notes for the attorney, marked do not send, are on the right. I copy the letter, then download it.",
    "download": "This is the file I downloaded, plain text, ready to paste. Each charge line has a blank for the date of service.",
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
        page.evaluate("""() => { const n = document.querySelector('pre').firstChild, i = n.data.indexOf('date of service ['); if (i < 0) return;
            const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + 17); const m = document.createElement('mark'); r.surroundContents(m); m.scrollIntoView({block: 'center'}); }""")      # the first charge line's blank, in view
        R.pause(1)
    R.beat("download", show_file)

    def home():
        page.goto(base + "/"); page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=20000)
    R.beat("close", home)


SCREEN = {
    "home": "Your cases with no cases yet, then the sample is opened.", "records": "Step 1: the nine records of the sample case; Draft the timeline is pressed.",
    "drafted": "Step 1 done: 19 timeline items and 4 bill amounts ready.", "item": "Step 2, the first item: the record with the quote highlighted, and the line to check.",
    "checks": "The same item, with its plain reason and the question and two answers.", "panel": "The panel under the line: what the code found, the second AI check's verdict, and your decision.",
    "howpage": "The How each answer is checked page, then back to the item.", "answer": "Yes, this matches is pressed; the next item opens; the Saved line shows an Undo button.",
    "warning": "A break-in-treatment warning (73 days between records 6 and 7) with both records highlighted and the grey Found by code tag.", "rest": "Quick yes-clicks through the remaining timeline items and warnings.",
    "step2done": "Step 2 done: the counts and one row per item with its answer.", "bills": "Step 3: the first charge; Yes, count it is pressed; the bill total so far changes.",
    "never": "Step 3: an amount that is never counted (a rate), with its reason.", "step3done": "Step 3 done: the total line as the letter will print it, and the lists.",
    "letter": "Step 4: the letter (each charge line has the date-of-service blank) and the notes for the attorney; Copy letter and Download letter are pressed.", "download": "The downloaded .txt file opened in the browser, scrolled to a charge line with its date-of-service blank highlighted.",
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
