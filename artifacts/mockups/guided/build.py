"""Builds the static guided-UI mockup pages (T-180, D-068). Run: python3 artifacts/mockups/guided/build.py
Content is the Appendix A sample case (SYNTHETIC) and two synthetic library cases, taken from a fixture-backend run of the real API
(answers: prepared). Pages marked "state variant" in screens.html show a state the sample does not produce, on sample content.
No backend, no network. Spec: docs/GUIDED_UI_SPEC.md."""
from html import escape as e
from pathlib import Path

OUT = Path(__file__).resolve().parent
BANNER = "Synthetic data only — never paste real records"
DEMO = "Demo: sample answers prepared by our team"
DEMO_NOTE = "The AI's own answers on these cases are in the evaluation report."
AI_BANNER = "In this demo the sample summaries and flags were prepared by our team and checked by code; you decide every item."

# ---------------------------------------------------------------- record texts (verbatim from the synthetic inputs)
RIVERA = {
    1: ("2026-01-09", "Austin EMS run report", "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."),
    2: ("2026-01-09", "Central ER discharge summary", "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."),
    3: ("2026-01-16", "Dr. Alvarez, primary care", "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."),
    4: ("2026-01-23", "Capital PT, initial evaluation", "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."),
    5: ("2026-02-20", "Capital PT, visit 8", "Pain 4/10, improving. Patient reports missing 3 days of work."),
    6: ("2026-03-06", "Capital PT, visit 9", "Discharged from PT after two missed appointments. Pain 3/10."),
    7: ("2026-05-18", "Hill Country Pain Management, new patient", "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19."),
    8: ("2026-05-29", "Austin Imaging, cervical MRI", "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150."),
    9: ("2026-06-12", "Hill Country Pain Management, follow-up", "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."),
}
LIB11_R9 = ("2026-06-15", "Fennimoor Spine Clinic, itemized ledger",
            "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")
C01_R8 = ("04/05/2026", "Dr. Orla Pennywhistle, phone note", "Patient reports no new symptoms.")

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def long_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"


# ---------------------------------------------------------------- the four cases' step states (state, status)
LABELS = [("Add records", "Records"), ("Check the timeline", "Timeline"), ("Check the bills", "Bills"), ("Get your letter", "Letter")]
STEP_PAGES = {
    "rivera": ["step1-found.html", "step2-entry.html", "step3-charge.html", "step4-letter.html"],
    "lib11": ["#", "#", "step3-count.html", "#"],
    "c01": ["#", "step2-date.html", "#", "#"],
    "lib01": ["step1-drafting-lib01.html", "#", "#", "#"],
    "lib08": ["step1-failed.html", "#", "#", "#"],
    "new": ["step1-add.html", "#", "#", "#"],
    "practice": ["#", "#", "#", "step4-letter-practice.html"],
}


def head(title, body_class):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Treatment Timeline (mockup)</title>
<link rel="stylesheet" href="guided.css">
<script src="guided.js" defer></script>
</head>
<body class="{body_class}">
<div class="banner" role="note"><span>{e(BANNER)}</span><span class="b-demo">{e(DEMO)}</span></div>
"""


def header(case_title=None, sub=None):
    right = f'<span class="demo-pill" title="{e(DEMO_NOTE)}">{e(DEMO)}</span><button type="button" class="theme-btn" data-theme-btn>Dark mode</button>'
    if case_title is None:
        left = '<a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">TT</span><span>Treatment Timeline</span></a>'
    else:
        left = (f'<a class="back-cases" href="index.html"><span aria-hidden="true">&#8249;</span><span class="long">Your cases</span><span class="short">Cases</span></a>'
                f'<div style="min-width:0;display:flex;align-items:baseline;gap:12px"><span class="case-title">{e(case_title)}</span>'
                + (f'<span class="case-sub">{e(sub)}</span>' if sub else "") + "</div>")
    return f'<header class="header">{left}<span class="spacer"></span>{right}</header>\n'


def stepbar(case, states, here):
    lis = []
    for i, ((state, status), (long, short)) in enumerate(zip(states, LABELS)):
        n = i + 1
        cls = state + (" current" if n == here else "")
        mark = "&#10003;" if state == "done" else ("!" if state == "attn" and n != here else str(n))
        href = STEP_PAGES[case][i]
        attrs = 'aria-current="step"' if n == here else ""
        tag = "span" if state == "locked" else "a"
        link = "" if tag == "span" else f' href="{href}"'
        dis = ' aria-disabled="true"' if state == "locked" else ""
        lis.append(f'<li><{tag} class="step {cls}"{link} {attrs}{dis}><span class="dot" aria-hidden="true">{mark}</span><span class="st-text">'
                   f'<span class="st-label"><span class="long">{n} {long}</span><span class="short">{short}</span></span>'
                   f'<span class="st-status">{e(status)}</span></span><span class="sr"> (step {n} of 4)</span></{tag}></li>')
    return f'<nav class="steps" aria-label="Steps"><ol>{"".join(lis)}</ol></nav>\n'


def footer(extra=""):
    return (f'<footer class="footer"><span>{e(DEMO)}. {e(DEMO_NOTE)}</span>{extra}'
            '<a href="screens.html">Mockup: all screens</a></footer>\n')


def rec_html(seq, rec, marks=(), sentences=None, show_head=True):
    """Record text as pasted (Date/Source/Excerpt lines), with marks on verbatim substrings or tappable sentences."""
    date, src, body = rec
    lines = f'<span class="meta">=== Record {seq} ===\nDate: {e(date)}\nSource: {e(src)}\nExcerpt: </span>'
    txt = e(f'"{body}"')
    if sentences is not None:
        out = '"'
        for s, on in sentences:
            out += f'<span class="sent{" on" if on else ""}">{e(s)}</span> '
        txt = out.rstrip() + '"'
    else:
        for m in marks:
            txt = txt.replace(e(m), f"<mark>{e(m)}</mark>", 1)
    for m in marks:     # header-line marks (gap evidence)
        if m.startswith("Date:") or m.startswith("Source:"):
            lines = lines.replace(e(m), f"<mark>{e(m)}</mark>", 1)
    dl = long_date(date) if "-" in date else date
    h = f'<div class="rec-h">Record {seq} · {e(src)} · {e(dl)}</div>' if show_head else ""
    return f'{h}<div class="rec">{lines}{txt}</div>'


def frame(*, fname, title, case, case_title, sub, states, here, eyebrow, h1, count, answered, total, pct, source_head, source_body,
          card_head, card_body, card_foot, foot_cls="", question, yes, no, small, status="", chip=None, extra_status=""):
    count_box = (f'<div class="count-box"><div class="count-line"><span class="num">{e(count)}</span><span class="of num">{answered} answered · {total} to go</span></div>'
                 f'<div class="bar" role="progressbar" aria-label="Progress in this step" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}"><i style="width:{pct}%"></i></div></div>')
    chip_html = (f'<div class="total-chip" aria-live="polite"><div class="tc-l">Bill total so far</div><div class="tc-v num">{e(chip)}</div></div>' if chip else "")
    html = head(title, "frame") + header(case_title, sub) + stepbar(case, states, here)
    html += (f'<div class="titlebar"><div class="t-main"><div class="eyebrow">{e(eyebrow)}</div><h1>{e(h1)}</h1>'
             f'<div class="t-ai">{e(AI_BANNER)}</div></div>{chip_html}{count_box}</div>\n')
    html += (f'<main class="work" id="main">'
             f'<section class="card card-src" aria-label="From the record"><div class="card-h"><span class="ch-title">From the record</span><span class="ch-sub">{source_head}</span></div>'
             f'<div class="card-b" data-scroll-mark tabindex="0">{source_body}</div></section>'
             f'<section class="card" aria-label="To check"><div class="card-h">{card_head}</div><div class="card-b">{card_body}</div>'
             f'<div class="card-f {foot_cls or "plain"}">{card_foot}</div></section></main>\n')
    html += (f'<div class="actions"><div class="actions-in"><p class="question" id="q">{e(question)}</p>'
             f'<div class="big" role="group" aria-labelledby="q">{yes}{no}</div><div class="small">{small}</div>'
             f'<p class="status" role="status" aria-live="polite">{status}{extra_status}</p></div></div>\n')
    html += "</body>\n</html>\n"
    (OUT / fname).write_text(html)


def A(label, href, cls="answer", id_=None, disabled=False, sub=None):
    i = f' id="{id_}"' if id_ else ""
    d = ' aria-disabled="true" tabindex="-1"' if disabled else ""
    inner = e(label) + (f'<span class="sub">{sub}</span>' if sub else "")
    extra = " two" if sub else ""
    return f'<a class="btn {cls}{extra}" href="{href}"{i}{d}>{inner}</a>'


def smalls(back="#", third=None, later="#"):
    parts = [A("‹ Back", back, "quiet")]
    if third:
        parts.append(A(third[0], third[1], "quiet", disabled=third[1] is None))
    else:       # keep the slot so Back and Decide later never move between items
        parts.append('<span class="btn quiet" aria-hidden="true" style="visibility:hidden">Fix the wording</span>')
    parts.append(A("Decide later", later, "quiet"))
    return "".join(parts)


def page(fname, title, body, *, case=None, case_title=None, sub=None, states=None, here=None, wide=False):
    html = head(title, "page") + '<div class="stick">' + header(case_title, sub)
    if states:
        html += stepbar(case, states, here)
    html += f'</div><main class="wrap{" wide" if wide else ""}" id="main">{body}</main>' + footer() + "</body>\n</html>\n"
    (OUT / fname).write_text(html)


# ---------------------------------------------------------------- case step states
RIV_S2 = [("done", "Done"), ("current", "16 of 19 left"), ("todo", "4 amounts"), ("todo", "Not yet")]
RIV_S2_LATE = lambda left: [("done", "Done"), ("current", f"{left} of 19 left"), ("todo", "4 amounts"), ("todo", "Not yet")]
RIV_S3 = lambda left: [("done", "Done"), ("done", "Done"), ("current", f"{left} of 4 left" if left else "Done"), ("todo", "Not yet")]
RIV_DONE = [("done", "Done"), ("done", "Done"), ("done", "Done"), ("done", "Ready")]
RIV_PENDING = [("done", "Done"), ("attn", "2 left"), ("attn", "1 left"), ("todo", "3 open")]
LIB11 = [("done", "Done"), ("done", "Done"), ("current", "7 of 8 left"), ("todo", "Not yet")]
C01 = [("done", "Done"), ("current", "1 of 10 left"), ("todo", "1 amount"), ("todo", "Not yet")]
NEW = [("current", "Now"), ("locked", "After step 1"), ("locked", "After step 1"), ("locked", "After step 1")]
FOUND = [("current", "9 records"), ("locked", "After step 1"), ("locked", "After step 1"), ("locked", "After step 1")]
DRAFT = [("current", "Drafting"), ("locked", "After step 1"), ("locked", "After step 1"), ("locked", "After step 1")]
FAILED = [("attn", "Run again"), ("todo", "Some ready"), ("todo", "Some ready"), ("locked", "After step 1")]

PREP = '<span class="tag prep">Prepared answer</span>'
WHY_OK = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def entry_head(tag, iso, src):
    return f'{tag}<span class="ch-sub">{e(long_date(iso))} · {e(src)}</span>'


def rhead(seq):
    d, s, _ = RIVERA[seq]
    return f"Record {seq} · {e(s)} · {e(long_date(d))}"


# ================================================================ HOME
def card(title, meta, track, nxt, nxt_cls, btn, href, btn_label="Continue"):
    tr = "".join(f'<li class="{s}"><i></i>{e(l)}</li>' for s, l in zip(track, ["Add records", "Timeline", "Bills", "Letter"]))
    return (f'<article class="ccard" data-title="{e(title)}"><div class="cc-top"><h3>{e(title)}</h3><button type="button" class="btn quiet">Rename</button></div>'
            f'<div class="cc-meta">{e(meta)}</div><ol class="track" aria-label="Steps">{tr}</ol>'
            f'<p class="next {nxt_cls}">{nxt}</p>'
            f'<div class="cc-bottom"><a class="btn lg {btn}" href="{href}">{e(btn_label)}</a><button type="button" class="btn quiet danger" data-delete>Delete</button></div>'
            f'<div class="cc-bottom" hidden><span style="flex:1;font-weight:600">Delete this case and all its answers?</span><button type="button" class="btn danger">Yes, delete</button><button type="button" class="btn" data-keep>Keep it</button></div></article>')


def home():
    cards_prog = [
        card("Jordan Rivera (sample)", "Started Nov 2 · 9 records", ["done", "current", "", ""], "<b>Next:</b> Check the timeline. 16 of 19 items left.", "", "primary", "step2-entry.html"),
        card("Priors and ledger", "Started Nov 2 · 9 records", ["done", "done", "current", ""], "<b>Next:</b> Check the bills. 7 of 8 amounts left.", "", "primary", "step3-count.html"),
        card("Date formats", "Started Nov 2 · 8 records", ["done", "current", "", ""], "<b>Next:</b> Check the timeline. 1 item left: pick a date.", "", "primary", "step2-date.html"),
        card("Er only then gap", "Started Nov 2 · 6 records", ["current", "", "", ""], "<b>Next:</b> Wait while the timeline is drafted (stage 3 of 8).", "", "primary", "step1-drafting-lib01.html"),
        card("Second crash, MRI after", "Started Nov 2 · 7 records", ["attn", "", "", ""], "<b>Next:</b> Drafting stopped. Run it again.", "warn", "primary", "step1-failed.html"),
    ]
    cards_done = [card("Sample case (practice run)", "Started Nov 1 · 9 records · finished Nov 1", ["done", "done", "done", "done"],
                       "<b>Finished.</b> Your letter is ready.", "ok", "go", "step4-letter-practice.html", "Open letter")]
    body = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'
            '<a class="btn primary lg" href="step1-add.html">+ Start a new case</a></div>'
            '<div class="find"><label class="sr" for="find-case">Find a case</label><input id="find-case" type="search" placeholder="Find a case by name"></div>'
            f'<h2 class="sec-h">In progress <span class="c">{len(cards_prog)}</span></h2><div class="cases">{"".join(cards_prog)}</div>'
            f'<h2 class="sec-h">Finished <span class="c">{len(cards_done)}</span></h2><div class="cases">{"".join(cards_done)}</div>')
    page("index.html", "Your cases", body, wide=True)

    empty = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div></div>'
             '<div class="panel empty"><div class="em-ic" aria-hidden="true">+</div><h2>You don\'t have any cases yet.</h2>'
             '<p>A case is one client\'s medical records. We\'ll guide you through 4 steps: add the records, check the timeline, check the bills, and get your letter.</p>'
             '<div class="row-actions"><a class="btn primary lg" href="step1-add.html">+ Start a new case</a><a class="btn lg" href="step1-found.html">Try the sample case</a></div></div>')
    page("home-empty.html", "Your cases (empty)", empty, wide=True)

    sk = "".join('<article class="ccard" aria-hidden="true"><div class="skel" style="height:28px;width:60%"></div><div class="skel" style="height:18px;width:40%"></div>'
                 '<div class="skel" style="height:24px"></div><div class="skel" style="height:44px"></div><div class="skel" style="height:56px"></div></article>' for _ in range(3))
    loading = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'
               '<a class="btn primary lg" href="step1-add.html">+ Start a new case</a></div>'
               f'<p class="sr" role="status">Loading your cases</p><h2 class="sec-h">Loading your cases…</h2><div class="cases">{sk}</div>')
    page("home-loading.html", "Your cases (loading)", loading, wide=True)

    err = ('<div class="home-h"><div style="flex:1"><h1>Your cases</h1><p>Each case goes through 4 steps. Pick up where you left off.</p></div>'
           '<a class="btn primary lg" href="step1-add.html">+ Start a new case</a></div>'
           '<div class="panel empty"><div class="em-ic" aria-hidden="true" style="background:var(--bad-bg);color:var(--bad)">!</div><h2>We couldn\'t load your cases.</h2>'
           '<p>The server didn\'t answer. Your cases are safe; nothing was changed.</p><div class="row-actions"><a class="btn primary lg" href="index.html">Try again</a></div></div>')
    page("home-error.html", "Your cases (error)", err, wide=True)


# ================================================================ STEP 1
def step1():
    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>Add records</h1>'
            '<p>Add the medical records for this case. We\'ll read them and draft a timeline for you to check.</p></div></div>'
            '<div class="panel"><div class="field"><label for="case-name">Name this case (optional)</label>'
            '<input id="case-name" value="Jordan Rivera (sample)" maxlength="120"><span class="hint">For example the client\'s name. You can change it later.</span></div>'
            '<fieldset style="border:0;padding:0;margin:0"><legend class="sr">How do you want to add the records?</legend><div class="tiles">'
            '<label class="tile"><input type="radio" name="how" value="paste"><span class="tl-h">Paste text</span><p>Copy the records and paste them here.</p></label>'
            '<label class="tile"><input type="radio" name="how" value="file"><span class="tl-h">Upload a file</span><p>A .txt or .pdf file, up to 5 MB.</p></label>'
            '<label class="tile"><input type="radio" name="how" value="sample" checked><span class="tl-h">Use the sample case</span><p>A short synthetic case to try it out.</p></label>'
            '</div></fieldset>'
            '<div class="input-box solid"><div style="display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;height:100%"><b style="font-size:1.25rem">The sample case</b>'
            '<span class="muted">9 short records from a fictional car-accident case (Jordan Rivera, 41, Austin). Every name and date in it is made up.</span></div></div>'
            '<p class="err-slot" role="alert"></p>'
            '<div class="row-actions" style="margin-top:8px;align-items:center"><a class="btn primary lg" href="step1-found.html">Read the records</a>'
            '<span class="muted">This demo can only read the sample and our test cases.</span></div></div>')
    page("step1-add.html", "Add records", body, case="new", case_title="New case", states=NEW, here=1)

    rows = "".join(f'<li><span class="n">{n}</span><span class="num">{e(long_date(d))}</span><span class="src">{e(s)}</span></li>' for n, (d, s, _) in RIVERA.items())
    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>We found 9 records</h1>'
            '<p>Check that these are the records you meant to add. Next, we\'ll draft a one-line timeline entry for each one.</p></div></div>'
            '<div class="panel fixed-box"><div class="note-box ok" style="margin-bottom:16px"><span class="nb-text">Every record has a date we could read.</span></div>'
            f'<ol class="list" style="max-height:440px">{rows}</ol>'
            '<div class="row-actions"><a class="btn primary lg" href="step1-drafting.html">Draft the timeline</a><a class="btn lg" href="step1-add.html">Start over with other records</a></div></div>')
    page("step1-found.html", "Records found", body, case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=FOUND, here=1)

    def drafting(fname, case, title, prepared, start, slow, sub, nxt, counts):
        stg = [("Reading the records", ""), ("Loading the prepared line for each record" if prepared else "Writing one line for each record", ""),
               ("Checking every quote word for word", ""), ("Double-checking each line a second way", ""), ("Finding the bill amounts", ""),
               ("Comparing the records with each other", ""), ("Looking for things the attorney should know", ""), ("Putting it all together", "")]
        lis = "".join(f'<li class="{"done" if i < start else ("now" if i == start else "")}"><span class="ic" aria-hidden="true">{"&#10003;" if i < start else ""}</span>{e(s)}</li>' for i, (s, _) in enumerate(stg))
        body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>Drafting the timeline</h1>'
                '<p>This usually takes under a minute. You can leave this page; we\'ll keep going.</p></div></div>'
                f'<div class="panel fixed-box"><div id="draft-running"><div class="count-line"><span>Working on it</span><span class="num" id="draft-count">{start + 1} of 8</span></div>'
                f'<div class="bar" role="progressbar" aria-label="Drafting progress"><i id="draft-bar" style="width:{round(start / 8 * 100)}%"></i></div>'
                f'<ol class="stages" id="stages" data-start="{start}"{" data-slow" if slow else ""} aria-live="polite">{lis}</ol></div>'
                f'<div id="draft-done" hidden><div class="done-hero"><div class="big-check" aria-hidden="true">&#10003;</div><div><h2>All set.</h2>'
                f'<p>{e(counts)}</p></div></div><p class="muted" style="margin-top:16px">{e(AI_BANNER)}</p>'
                f'<div class="row-actions"><a class="btn primary lg" href="{nxt}">Go to step 2: Check the timeline</a></div></div></div>')
        page(fname, "Drafting", body, case=case, case_title=title, sub=sub, states=DRAFT, here=1)

    drafting("step1-drafting.html", "rivera", "Jordan Rivera (sample)", True, 0, False, "9 records", "step2-entry.html",
             "19 timeline items and 4 bill amounts are ready for you to check.")
    drafting("step1-drafting-lib01.html", "lib01", "Er only then gap", False, 2, True, "6 records", "index.html",
             "The timeline items and bill amounts are ready for you to check.")

    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 1 of 4</div><h1>Drafting stopped</h1>'
            '<p>Some of the work finished. You can run it again; nothing you decided is lost.</p></div></div>'
            '<div class="panel fixed-box"><div class="done-hero"><div class="big-warn" aria-hidden="true">!</div><div><h2>Drafting stopped before it finished.</h2>'
            '<p>The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.</p></div></div>'
            '<div class="row-actions"><a class="btn primary lg" href="step1-drafting-lib01.html">Run it again</a><a class="btn lg" href="index.html">Back to your cases</a></div>'
            '<p class="muted" style="margin-top:20px">The items that did finish can be checked now in steps 2 and 3.</p></div>')
    page("step1-failed.html", "Drafting stopped", body, case="lib08", case_title="Second crash, MRI after", sub="7 records", states=FAILED, here=1)


# ================================================================ STEP 2
def step2():
    small_entry = lambda back="#", nxt="#", fix="step2-fix.html": smalls(back, ("Fix the wording", fix), nxt)
    # --- entry, item 4 of 19
    frame(fname="step2-entry.html", title="Check the timeline", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S2, here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Item 4 of 19", answered=3, total=16, pct=16,
          source_head=rhead(3), source_body=rec_html(3, RIVERA[3], ["Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."], show_head=False)
          + '<div class="also"><b>Also in this record, not in any line:</b><br><q>Patient reports low back pain in 2023, resolved.</q></div>',
          card_head=entry_head(PREP, "2026-01-16", "Dr. Alvarez, primary care"),
          card_body='<p class="line-text">Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.</p>',
          card_foot=f'<span class="label-cap">How it was checked</span><br>{e(WHY_OK)}',
          question="Does this line say the same thing as the highlighted words?",
          yes=A("Yes, this matches", "step2-flag.html", "answer primary"), no=A("No, leave it out", "step2-flag.html"),
          small=small_entry(nxt="step2-flag.html"),
          status='<b>Saved:</b> item 3 (Central ER discharge summary) kept in the letter. <a href="#">Undo</a>')

    # --- fix the wording (with a refused edit shown)
    sents = [("Persistent neck pain 6/10, daily headaches.", True), ("Refer to physical therapy 2x/week for 6 weeks.", True), ("Patient reports low back pain in 2023, resolved.", False)]
    frame(fname="step2-fix.html", title="Fix the wording", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S2, here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Item 4 of 19", answered=3, total=16, pct=16,
          source_head=rhead(3), source_body='<p class="muted" style="margin-bottom:12px;font-size:1rem">To change which words are highlighted, tap whole sentences below.</p>'
          + rec_html(3, RIVERA[3], sentences=sents, show_head=False),
          card_head='<span class="tag you">Your wording</span><span class="ch-sub">January 16, 2026 · Dr. Alvarez, primary care</span>',
          card_body='<label class="sr" for="fix">Your wording for this line</label><textarea class="edit" id="fix">Persistent neck pain 7/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.</textarea>',
          card_foot='<strong>Not saved.</strong> The summary says “7/10”, which the quote does not say. Remove it or change the quote.', foot_cls="bad",
          question="Change the line so it says only what the highlighted words say, then save it.",
          yes=A("Save my wording", "step2-entry.html", "answer primary"), no=A("Cancel", "step2-entry.html"),
          small=smalls("#", ("Fix the wording", None), "#"),
          status="Numbers, left or right, and words like “no” or “possible” must match the highlighted words.")

    # --- prior-condition warning, item 5 of 19
    frame(fname="step2-flag.html", title="Warning for the attorney", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S2_LATE(15), here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Item 5 of 19", answered=4, total=15, pct=21,
          source_head=rhead(3), source_body=rec_html(3, RIVERA[3], ["Patient reports low back pain in 2023, resolved."], show_head=False),
          card_head='<span class="tag warn">Warning for the attorney</span>',
          card_body='<p class="warn-title">An earlier health problem is mentioned</p><p class="explain"><b>Mention of a prior or pre-existing condition.</b> '
                    'Dr. Alvarez, primary care (January 16, 2026) mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.”</p>',
          card_foot="Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.",
          question="Should the attorney be told about this?",
          yes=A("Yes, tell the attorney", "step2-gap.html", "answer primary"), no=A("No, not needed", "step2-gap.html"),
          small=smalls("step2-entry.html", ("Add a note", "#"), "step2-gap.html"),
          status='<b>Saved:</b> item 4 (Dr. Alvarez, primary care) kept in the letter. <a href="#">Undo</a>')

    # --- gap warning, item 10 of 19 (two records)
    src = (rec_html(6, RIVERA[6], ["Date: 2026-03-06", "Source: Capital PT, visit 9"]) +
           rec_html(7, RIVERA[7], ["Date: 2026-05-18", "Source: Hill Country Pain Management, new patient"]).replace('<div class="rec-h">', '<div class="rec-h" style="margin-top:24px;padding-top:20px;border-top:1px dashed var(--border)">', 1))
    frame(fname="step2-gap.html", title="A break in treatment", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S2_LATE(10), here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Item 10 of 19", answered=9, total=10, pct=47,
          source_head="Records 6 and 7", source_body=src,
          card_head='<span class="tag warn">Warning for the attorney</span>',
          card_body='<p class="warn-title">A break in treatment</p><p class="explain"><b>Gap of 73 days.</b> Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).</p>',
          card_foot="Calculated by code from two dates read from the record headers. Warnings only go in the notes for the attorney, never in the letter.",
          question="Should the attorney be told about this?",
          yes=A("Yes, tell the attorney", "step2-disputed.html", "answer primary"), no=A("No, not needed", "step2-disputed.html"),
          small=smalls("step2-flag.html", ("Add a note", "#"), "step2-disputed.html"),
          status='<b>Saved:</b> item 9 (Capital PT, visit 9) kept in the letter. <a href="#">Undo</a>')

    # --- disputed (D-066), item 15 of 19
    frame(fname="step2-disputed.html", title="Compare before you say yes", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S2_LATE(5), here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Item 15 of 19", answered=14, total=5, pct=74,
          source_head=rhead(8), source_body=rec_html(8, RIVERA[8], ["C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."], show_head=False),
          card_head=entry_head(PREP, "2026-05-29", "Austin Imaging, cervical MRI"),
          card_body='<p class="line-text">C5-C6 disc herniation with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.</p>',
          card_foot='<strong>The second check found this only partly supported by the quote.</strong> Read it against the highlighted words before you say yes.'
                    '<label class="check"><input type="checkbox" data-unlocks="yes-disputed"> I read this line against the highlighted words myself.</label>', foot_cls="attn",
          question="Does this line say the same thing as the highlighted words?",
          yes=A("Yes, this matches", "step2-done.html", "answer primary", id_="yes-disputed", disabled=True), no=A("No, leave it out", "step2-done.html"),
          small=small_entry("step2-gap.html", "step2-done.html"),
          status='<b>Saved:</b> item 14 (New-onset wording) — the attorney will be told. <a href="#">Undo</a>')

    # --- could not check (tray entry), optional
    frame(fname="step2-cannot-check.html", title="We couldn't check this one", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S2_LATE(12), here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Optional item", answered=7, total=12, pct=37,
          source_head=rhead(5), source_body=rec_html(5, RIVERA[5], show_head=False),
          card_head='<span class="tag warn">We couldn\'t check this one</span><span class="ch-sub">February 20, 2026 · Capital PT, visit 8</span>',
          card_body='<p class="explain">The model\'s quote does not appear word for word in the record, so it cannot be used.</p>'
                    '<p class="explain muted" style="margin-top:14px">What was suggested (not used): “Visit 8: pain 4/10, improving.”<br>Its quote: “Pain is 4/10 and improving.”</p>',
          card_foot="Nothing from this suggestion goes in the letter unless you write the line yourself. Skipping it leaves this record out of the timeline.", foot_cls="attn",
          question="Read the record. Do you want to write this line yourself?",
          yes=A("Write it myself", "step2-write.html", "answer primary"), no=A("Skip it", "step2-gap.html"),
          small=smalls("step2-flag.html", None, "step2-gap.html"),
          status='<b>Saved:</b> item 7 (The plan and what happened differ) — the attorney will be told. <a href="#">Undo</a>')

    # --- write it myself
    frame(fname="step2-write.html", title="Write the line yourself", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S2_LATE(12), here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Optional item", answered=7, total=12, pct=37,
          source_head=rhead(5), source_body='<p class="muted" style="margin-bottom:12px;font-size:1rem">Tap the sentences your line is based on. They become the highlighted words.</p>'
          + rec_html(5, RIVERA[5], sentences=[("Pain 4/10, improving.", True), ("Patient reports missing 3 days of work.", False)], show_head=False),
          card_head='<span class="tag you">Written by you</span><span class="ch-sub">February 20, 2026 · Capital PT, visit 8</span>',
          card_body='<label class="sr" for="mine">Your line for the timeline</label><textarea class="edit" id="mine">Pain 4/10, improving.</textarea>',
          card_foot="Use only what the chosen sentences say. Numbers, left or right, and words like “no” or “possible” must match.",
          question="Write the line for the timeline, then save it.",
          yes=A("Save my line", "step2-gap.html", "answer primary"), no=A("Cancel", "step2-cannot-check.html"),
          small=smalls("step2-cannot-check.html", None, "step2-gap.html"))

    # --- date to pick (Date formats case), item 10 of 10
    frame(fname="step2-date.html", title="Which date is right?", case="c01", case_title="Date formats", sub="8 records", states=C01, here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Item 10 of 10", answered=9, total=1, pct=90,
          source_head="Record 8 · Dr. Orla Pennywhistle, phone note · 04/05/2026", source_body=rec_html(8, C01_R8, ["Date: 04/05/2026"], show_head=False),
          card_head='<span class="tag warn">Pick the date</span><span class="ch-sub">Dr. Orla Pennywhistle, phone note</span>',
          card_body='<p class="warn-title">Which date is right?</p><p class="explain">The record says <b>04/05/2026</b>. That could be two different dates.</p>'
                    '<p class="explain muted" style="margin-top:12px">The line waiting for this date: “Patient reports no new symptoms.”</p>',
          card_foot='<span class="label-cap">Suggested: April 5, 2026</span><br>4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)',
          question="Which date is right for this record?",
          yes=A("April 5, 2026", "step2-date-confirmed.html", "answer", sub='month first <span class="chip-sug">Suggested</span>'),
          no=A("May 4, 2026", "step2-date-confirmed.html", "answer", sub="day first"),
          small=smalls("#", None, "index.html"))

    frame(fname="step2-date-confirmed.html", title="Check the line", case="c01", case_title="Date formats", sub="8 records", states=C01, here=2,
          eyebrow="Step 2 of 4", h1="Check the timeline", count="Item 10 of 10", answered=9, total=1, pct=90,
          source_head="Record 8 · Dr. Orla Pennywhistle, phone note · April 5, 2026", source_body=rec_html(8, C01_R8, ["Patient reports no new symptoms."], show_head=False),
          card_head='<span class="tag ai">AI draft</span><span class="ch-sub">April 5, 2026 · Dr. Orla Pennywhistle, phone note</span>',
          card_body='<p class="line-text">Patient reports no new symptoms.</p>',
          card_foot='<span class="label-cap">Part 2 of 2</span><br>The date is set. Now check the line itself.',
          question="Does this line say the same thing as the highlighted words?",
          yes=A("Yes, this matches", "index.html", "answer primary"), no=A("No, leave it out", "index.html"),
          small=smalls("step2-date.html", ("Fix the wording", "#"), "index.html"),
          status="<b>Saved:</b> record 8 is dated April 5, 2026 and now sits in the timeline.")

    # --- step 2 done
    rows = [
        ("Jan 9, 2026", "Austin EMS run report", "Kept"), ("Jan 9, 2026", "The records disagree about the accident date", "Tell the attorney"),
        ("Jan 9, 2026", "Central ER discharge summary", "Kept"), ("Jan 16, 2026", "Dr. Alvarez, primary care", "Kept"),
        ("Jan 16, 2026", "An earlier health problem is mentioned", "Tell the attorney"), ("Jan 23, 2026", "Capital PT, initial evaluation", "Kept"),
        ("Jan 23, 2026", "The plan and what happened differ", "Tell the attorney"), ("Feb 20, 2026", "Capital PT, visit 8", "Kept"),
        ("Mar 6, 2026", "Capital PT, visit 9", "Kept"), ("Mar 6, 2026", "A break in treatment (73 days)", "Tell the attorney"),
        ("Mar 6, 2026", "Missed or ended treatment", "Tell the attorney"), ("May 18, 2026", "Hill Country Pain Management, new patient", "Kept"),
        ("May 18, 2026", "Where the accident date comes from", "Not needed"), ("May 18, 2026", "Wording about a new problem", "Tell the attorney"),
        ("May 29, 2026", "Austin Imaging, cervical MRI", "Kept"), ("May 29, 2026", "Wording about wear and tear", "Tell the attorney"),
        ("May 29, 2026", "Hedged wording (“may”, “possible”)", "Tell the attorney"), ("Jun 12, 2026", "Hill Country Pain Management, follow-up", "Kept"),
        ("Jun 12, 2026", "The patient, not a doctor, says what caused it", "Tell the attorney"),
    ]
    tagc = {"Kept": "ok", "Tell the attorney": "warn", "Not needed": "never"}
    lis = "".join(f'<li><span class="n">{i + 1}</span><span class="d">{e(d)}</span><span class="lbl">{e(l)}</span><span class="ans"><span class="tag {tagc[a]}">{e(a)}</span></span>'
                  f'<a class="btn" href="step2-entry.html">Change</a></li>' for i, (d, l, a) in enumerate(rows))
    body = ('<div class="panel"><div class="done-hero"><div class="big-check" aria-hidden="true">&#10003;</div><div><h2>You checked every item on the timeline.</h2>'
            '<p>9 kept in the letter · 0 left out · 9 warnings for the attorney · 1 not needed</p></div></div>'
            '<div class="row-actions"><a class="btn primary lg" href="step3-charge.html">Go to step 3: Check the bills</a></div></div>'
            f'<div class="panel"><h2>Your answers</h2><p class="muted">Every item in the order you saw it. Change any answer here.</p><ol class="answers">{lis}</ol></div>'
            '<div class="panel"><h2>What we compared between records</h2><p><b>We checked for:</b> a stated plan of care against a course that ended early; a denial of prior problems against a prior condition; '
            'a stated accident date against the record dates; the same clinician under two practice names.</p>'
            '<p style="margin-top:8px"><b>Not checked:</b> medication doses, left versus right across records, a diagnosis that differs between records, pain scores on the same day, plans measured in months, history reported by a relative.</p></div>')
    page("step2-done.html", "Timeline checked", '<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 2 of 4</div><h1>Check the timeline</h1></div></div>' + body,
         case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S3(4), here=2)


# ================================================================ STEP 3
def step3():
    frame(fname="step3-charge.html", title="Check the bills", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S3(4), here=3,
          eyebrow="Step 3 of 4", h1="Check the bills", count="Amount 1 of 4", answered=0, total=4, pct=0, chip="$0.00",
          source_head=rhead(2), source_body=rec_html(2, RIVERA[2], ["ER charges: $6,240."], show_head=False),
          card_head='<span class="tag ok">Charge</span><span class="ch-sub">Central ER discharge summary · January 9, 2026</span>',
          card_body='<p class="money">$6,240.00</p><p class="explain muted" style="margin-top:6px">Billed by Central ER on January 9, 2026.</p>',
          card_foot="If you count it, it's added to the bill total in the letter, with the highlighted words as its source.",
          question="Should this charge count toward the bill total?",
          yes=A("Yes, count it", "step3-never.html", "answer primary"), no=A("No, don't count it", "step3-never.html"),
          small=smalls("step2-done.html", None, "step3-never.html"))

    frame(fname="step3-never.html", title="An amount that is never counted", case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_S3(2), here=3,
          eyebrow="Step 3 of 4", h1="Check the bills", count="Amount 3 of 4", answered=2, total=2, pct=50, chip="$8,390.00",
          source_head=rhead(4), source_body=rec_html(4, RIVERA[4], ["Charge per visit $185."], show_head=False),
          card_head='<span class="tag never">Never counted</span><span class="ch-sub">Capital PT, initial evaluation · January 23, 2026</span>',
          card_body='<p class="money">$185</p><p class="explain" style="margin-top:6px">This figure is a rate, not a charge, so it is not added to the total.</p>',
          card_foot="Either way, it is never added to the bill total. If you list it, the notes tell the attorney to request the itemized PT ledger.",
          question="This amount is never added to the total. List it in the notes for the attorney?",
          yes=A("Yes, list it", "step3-done.html", "answer primary"), no=A("No, leave it out", "step3-done.html"),
          small=smalls("step3-charge.html", None, "step3-done.html"),
          status='<b>Saved:</b> $2,150.00 (Austin Imaging, cervical MRI) counted. <a href="#">Undo</a>')

    ledger_marks = ["New patient exam charge $250.00"]
    frame(fname="step3-count.html", title="Count this amount?", case="lib11", case_title="Priors and ledger", sub="9 records", states=LIB11, here=3,
          eyebrow="Step 3 of 4", h1="Check the bills", count="Amount 2 of 8", answered=1, total=7, pct=13, chip="$3,260.00",
          source_head="Record 9 · Fennimoor Spine Clinic, itemized ledger · June 15, 2026", source_body=rec_html(9, LIB11_R9, ledger_marks, show_head=False),
          card_head='<span class="tag warn">Not counted yet</span><span class="ch-sub">Fennimoor Spine Clinic, itemized ledger</span>',
          card_body='<p class="money">$250.00</p><p class="explain" style="margin-top:6px">The line states no date of service, so it is not an itemized service line and is not totaled.</p>',
          card_foot='You can still count it if you checked the ledger yourself.<label class="check"><input type="checkbox" data-unlocks="yes-count"> I checked this is a separate charge for a service.</label>',
          foot_cls="attn",
          question="Should this amount count toward the bill total?",
          yes=A("Yes, count it", "index.html", "answer primary", id_="yes-count", disabled=True), no=A("No, don't count it", "index.html"),
          small=smalls("#", None, "index.html"),
          status='<b>Saved:</b> $3,260.00 (Wexcombe Memorial ED) counted. <a href="#">Undo</a>')

    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 3 of 4</div><h1>Check the bills</h1></div></div>'
            '<div class="panel"><div class="done-hero"><div class="big-check" aria-hidden="true">&#10003;</div><div><h2>You checked every bill amount.</h2>'
            '<p>This is the total line your letter will carry:</p></div></div>'
            '<p class="total-line num">Billed charges accepted from these records: $8,390.00</p>'
            '<div class="row-actions"><a class="btn primary lg" href="step4-letter.html">Go to step 4: Get your letter</a></div></div>'
            '<div class="panel"><h2>Counted (2)</h2><table class="mini"><thead><tr><th>Amount</th><th>From</th><th>Date</th><th></th></tr></thead><tbody>'
            '<tr><td class="amt">$6,240.00</td><td>Central ER discharge summary</td><td>January 9, 2026</td><td><a class="btn" href="step3-charge.html">Change</a></td></tr>'
            '<tr><td class="amt">$2,150.00</td><td>Austin Imaging, cervical MRI</td><td>May 29, 2026</td><td><a class="btn" href="step3-charge.html">Change</a></td></tr></tbody></table></div>'
            '<div class="panel"><h2>Not counted by you (0)</h2><p class="muted">You didn\'t leave out any charge.</p></div>'
            '<div class="panel"><h2>Never counted (2)</h2><p class="muted">These are never added to the total. The ones you listed go in the notes for the attorney.</p>'
            '<table class="mini" style="margin-top:8px"><thead><tr><th>Amount</th><th>From</th><th>Why it\'s never counted</th></tr></thead><tbody>'
            '<tr><td class="amt">$185</td><td>Capital PT, initial evaluation</td><td>This figure is a rate, not a charge, so it is not added to the total.</td></tr>'
            '<tr><td class="amt">missing 3 days of work</td><td>Capital PT, visit 8</td><td>This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.</td></tr></tbody></table></div>')
    page("step3-done.html", "Bills checked", body, case="rivera", case_title="Jordan Rivera (sample)", sub="9 records", states=RIV_DONE[:3] + [("todo", "Ready")], here=3)


# ================================================================ STEP 4
def golden():
    txt = (OUT.parents[2] / "evals/golden/sample.export.expected.txt").read_text()
    letter = txt.split("=== LETTER_TEXT (block 1: paste into letter) ===\n")[1].split("=== INTERNAL_NOTES_TEXT")[0].rstrip("\n")
    notes = txt.split("=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\n")[1].rstrip("\n")
    return letter, notes


def step4():
    letter, notes = golden()

    def letter_page(fname, case, title, states, top, copy_lock, notes_txt):
        lock = ' aria-disabled="true" tabindex="-1"' if copy_lock else ""
        body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 4 of 4</div><h1>Get your letter</h1>'
                '<p>Copy the treatment section into your demand letter, or download it. The notes on the right are for the attorney only.</p></div></div>'
                f'{top}<div class="letter-grid" style="margin-top:20px"><section><div class="doc-h"><h2>Your letter section</h2><span class="muted">Paste into the demand letter</span></div>'
                f'<pre class="doc" id="letter" tabindex="0">{e(letter)}</pre>'
                f'<div class="doc-actions"><button type="button" class="btn primary lg" data-copy="letter" id="copy-letter"{lock}>Copy letter</button>'
                f'<button type="button" class="btn lg" data-download="letter" data-name="jordan-rivera-letter.txt" id="dl-letter"{lock}>Download letter (.txt)</button></div></section>'
                '<section><div class="doc-h"><h2>Notes for the attorney</h2><span class="muted" style="color:var(--bad);font-weight:700">Do not send</span></div>'
                f'<pre class="doc notes" id="notes" tabindex="0">{e(notes_txt)}</pre>'
                f'<div class="doc-actions"><button type="button" class="btn lg" data-copy="notes"{lock}>Copy notes</button>'
                f'<button type="button" class="btn lg" data-download="notes" data-name="jordan-rivera-notes.txt"{lock}>Download notes</button></div></section></div>'
                '<div class="panel" style="margin-top:24px"><h2>Exhibit and page numbers (optional)</h2><p class="muted">Fill these in to replace “[Ex. __ / Bates __]” in every source line.</p>'
                '<div class="cfg"><div class="field"><label for="ex">Exhibit</label><input id="ex" placeholder="e.g. 4"></div>'
                '<div class="field"><label for="bp">Bates prefix</label><input id="bp" placeholder="e.g. RIV"></div>'
                '<div class="field"><label for="bs">First number</label><input id="bs" inputmode="numeric" placeholder="e.g. 1"></div>'
                '<button type="button" class="btn lg">Save numbers</button></div></div>')
        page(fname, "Get your letter", body, case=case, case_title=title, sub="9 records", states=states, here=4, wide=True)

    ready = ('<div class="note-box ok"><span class="nb-text">Your letter is ready. Every item has an answer.'
             '<span>9 timeline lines and 2 charges are in it. Nothing is left undecided.</span></span></div>')
    letter_page("step4-letter.html", "rivera", "Jordan Rivera (sample)", RIV_DONE, ready, False, notes)
    letter_page("step4-letter-practice.html", "practice", "Sample case (practice run)", RIV_DONE, ready, False, notes)

    pending_notes = notes.replace("Items not reviewed: 0.", "Items not reviewed: 3.")
    pend = ('<div class="note-box"><span class="nb-text">3 items still need a decision.<span>If you don\'t decide them, they stay out of the letter. The letter below is what would be sent now.</span></span>'
            '<a class="btn primary lg" href="step2-flag.html">Go to the first one</a></div>'
            '<label class="check" style="margin-top:14px"><input type="checkbox" data-unlocks="copy-letter dl-letter"> Copy it anyway, without those 3 items.</label>')
    letter_page("step4-pending.html", "rivera", "Jordan Rivera (sample)", RIV_PENDING, pend, True, pending_notes)

    body = ('<div class="page-h"><div class="ph-main"><div class="eyebrow">Step 4 of 4</div><h1>Get your letter</h1>'
            '<p>Copy the treatment section into your demand letter, or download it.</p></div></div>'
            '<div class="note-box bad"><span class="nb-text">The letter can\'t be made yet.<span>Fix the problem below, then come back here.</span></span></div>'
            '<ul class="blockers"><li><span>Nothing is accepted or edited yet, so the letter would be empty.</span><a class="btn primary" href="step2-entry.html">Go to step 2</a></li></ul>'
            '<div class="letter-grid" style="margin-top:20px"><section><div class="doc-h"><h2>Your letter section</h2></div>'
            '<div class="doc placeholder">Your letter will appear here once the problem above is fixed.</div>'
            '<div class="doc-actions"><button type="button" class="btn primary lg" aria-disabled="true" tabindex="-1">Copy letter</button><button type="button" class="btn lg" aria-disabled="true" tabindex="-1">Download letter (.txt)</button></div></section>'
            '<section><div class="doc-h"><h2>Notes for the attorney</h2></div><div class="doc notes placeholder">The notes appear with the letter.</div></section></div>')
    page("step4-blocked.html", "Letter blocked", body, case="rivera", case_title="Jordan Rivera (sample)", sub="9 records",
         states=[("done", "Done"), ("attn", "19 of 19 left"), ("attn", "4 of 4 left"), ("attn", "1 problem")], here=4, wide=True)


# ================================================================ SCREENS INDEX
def screens():
    groups = [
        ("Your cases", [("index.html", "Your cases", "Six synthetic cases at different steps, each with one Continue button."),
                        ("home-empty.html", "No cases yet", "Empty state with Start a new case and Try the sample case."),
                        ("home-loading.html", "Loading", "Skeleton cards of the final size."),
                        ("home-error.html", "Couldn't load", "Error state with Try again.")]),
        ("Step 1 · Add records", [("step1-add.html", "Add records", "Name, three ways in (paste, upload, sample), Read the records."),
                                  ("step1-found.html", "Records found", "The 9 sample records; Draft the timeline."),
                                  ("step1-drafting.html", "Drafting", "Plain-words stage list (prepared answers); turns into All set."),
                                  ("step1-drafting-lib01.html", "Drafting, another case", "Live/recorded wording, mid-run."),
                                  ("step1-failed.html", "Drafting stopped", "Interrupted run, Run it again.")]),
        ("Step 2 · Check the timeline", [("step2-entry.html", "A timeline line", "Item 4 of 19: quote beside the line, Yes / No."),
                                         ("step2-fix.html", "Fix the wording", "Same boxes; a refused edit shows the server's reason."),
                                         ("step2-flag.html", "A warning", "Item 5: an earlier health problem; tell the attorney?"),
                                         ("step2-gap.html", "A break in treatment", "Item 10: evidence in two records."),
                                         ("step2-disputed.html", "Compare first (D-066)", "State variant: Yes unlocks only after the compare box."),
                                         ("step2-cannot-check.html", "We couldn't check this one", "State variant (api.md tray example): write it or skip."),
                                         ("step2-write.html", "Write it myself", "Tap sentences, type the line."),
                                         ("step2-date.html", "Pick a date", "Date formats case: two big date answers, suggestion shown."),
                                         ("step2-date-confirmed.html", "Date set, now the line", "Part 2 of the same item."),
                                         ("step2-done.html", "Timeline done", "Counts, every answer with Change, what was compared.")]),
        ("Step 3 · Check the bills", [("step3-charge.html", "A charge", "$6,240.00: count it?"),
                                      ("step3-count.html", "Count with a check (D-064)", "Priors and ledger: $250.00, named confirm."),
                                      ("step3-never.html", "Never counted", "$185 rate: list it for the attorney?"),
                                      ("step3-done.html", "Bills done", "The letter's total line and three plain lists.")]),
        ("Step 4 · Get your letter", [("step4-letter.html", "Letter ready", "Golden letter and notes; Copy and Download."),
                                      ("step4-pending.html", "3 items undecided", "State variant: go to the first one, or copy anyway."),
                                      ("step4-blocked.html", "Blocked", "Nothing accepted yet: the real server reason, Go to step 2.")]),
    ]
    body = ('<div class="page-h"><div class="ph-main"><h1>Guided UI mockup: all screens</h1>'
            '<p>Static mockup for T-180 (D-068). No backend: buttons move between these pages. Content is the synthetic Appendix A sample and two synthetic library cases, '
            'taken from a fixture run of the real API. Spec: docs/GUIDED_UI_SPEC.md.</p></div></div>')
    for g, items in groups:
        body += f'<h2 class="sec-h">{e(g)}</h2><div class="screens">' + "".join(
            f'<a href="{h}"><b>{e(t)}</b><span>{e(d)}</span>{"<div class=variant>State variant</div>" if "variant" in d else ""}</a>' for h, t, d in items) + "</div>"
    page("screens.html", "All screens", body, wide=True)


if __name__ == "__main__":
    home(); step1(); step2(); step3(); step4(); screens()
    print("wrote", len(list(OUT.glob("*.html"))), "pages to", OUT)
