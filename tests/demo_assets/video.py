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


# Burned-in captions (the narration, in short lines): a dark band at the bottom of every page, white text. The page polls the exposed
# binding __cap (answered from the recorder's clock), so the band survives navigations and every page of the context shows it.
# The band sits BELOW the app, not over it: the viewport is BAND_PX taller than the 900 px the app was designed for, and the guided frame (body.frame, which is 100vh
# tall by design) is made that much shorter, so its bottom bar (the Saved line and Undo) sits just above the band instead of behind it; other pages get bottom padding.
BAND_PX = 96
CAPTION_JS = """
(() => { if (window.__capInstalled) return; window.__capInstalled = true; const BAND = __BAND__;
  const mk = () => { const sh = new CSSStyleSheet();      // a constructed sheet: the app's Content-Security-Policy blocks an inline <style>
    sh.replaceSync('body.frame{height:calc(100vh - ' + BAND + 'px)!important;height:calc(100dvh - ' + BAND + 'px)!important}body:not(.frame){padding-bottom:' + BAND + 'px!important}');
    document.adoptedStyleSheets = [...document.adoptedStyleSheets, sh];
    const d = document.createElement('div'); d.id='__caption';
    d.style.cssText='position:fixed;left:0;width:100vw;bottom:0;height:' + BAND + 'px;box-sizing:border-box;z-index:2147483646;pointer-events:none;background:#0f172a;color:#fff;font:600 26px/1.3 system-ui,-apple-system,Segoe UI,sans-serif;text-align:center;padding:0 56px;display:flex;align-items:center;justify-content:center;letter-spacing:.1px';
    document.documentElement.appendChild(d);
    const tick = async () => { try { const t = await window.__cap(); d.textContent = t || ''; } catch (e) {} };
    setInterval(tick, 150); tick(); };
  if (document.documentElement) mk(); else document.addEventListener('DOMContentLoaded', mk); })();
""".replace('__BAND__', str(BAND_PX))
CAP_WORDS = 11    # at most this many words on screen at once (two short lines at most)


def vtt_time(t):
    ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}.{ms % 1000:03d}"


def chunks(text):
    """Split a narration line into caption pieces of <= CAP_WORDS words, breaking after a sentence end or comma when one is near."""
    w = text.split(); n = -(-len(w) // CAP_WORDS); size = -(-len(w) // n); out = []; i = 0
    while i < len(w):
        j = min(i + size, len(w))
        for k in range(j, max(i + 4, j - 3), -1):          # prefer a break at punctuation within the last 3 words
            if w[k - 1][-1] in ".,;:?":
                j = k; break
        out.append(" ".join(w[i:j])); i = j
    return out


class Rec:
    def __init__(self, page, t0):
        self.page, self.t0, self.log = page, t0, []
        self.cues = []; self.sched = []          # cues: (start, end, text) in recording seconds; sched: the current beat's pieces [(start, text)]
        self.x, self.y = 700, 450; self.shots = pathlib.Path('/private/tmp/claude-501/beats'); self.shots.mkdir(exist_ok=True)

    def now(self):
        return time.time() - self.t0

    def caption(self):
        """Answer the page's poll: the piece of the current beat that is due now ('' between beats)."""
        t = self.now(); cur = ""
        for st, tx in self.sched:
            if t >= st:
                cur = tx
        return cur

    def set_sched(self, text, start, need):
        pcs = chunks(text); total = max(len(text.split()), 1); done = 0; self.sched = []
        for pc in pcs:
            self.sched.append((start + need * done / total, pc)); done += len(pc.split())

    def close_cues(self, end):
        for i, (st, tx) in enumerate(self.sched):
            e = self.sched[i + 1][0] if i + 1 < len(self.sched) else end
            self.cues.append((st, e, tx))
        self.sched = []

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
        start = self.now(); self.set_sched(text, start, need)
        if fn:
            fn()
        try:
            self.page.screenshot(path=str(self.shots / f"beat-{key}.png"))       # a still of what the viewer sees at the end of the action, for checking the narration against the picture
        except Exception:
            pass
        spent = self.now() - start
        if spent < need:
            self.pause(need - spent)
        self.log.append((key, start, self.now(), text)); self.close_cues(self.now())

    def beat_during(self, key, fn=None):
        """Narration plays *while* the pointer works: the beat is as long as the longer of the two."""
        self.beat(key, fn)


def run(rev, out, narr_out):
    src, sha = K.archive(rev); print("archive", sha, flush=True)
    vid_dir = pathlib.Path(K.tempfile.mkdtemp(prefix="demo-vid-"))
    with sync_playwright() as pw, K.server(src, local=False) as (base, db):
        br = pw.chromium.launch()
        ctx = br.new_context(viewport={"width": 1440, "height": 900 + BAND_PX}, record_video_dir=str(vid_dir), record_video_size={"width": 1280, "height": round((900 + BAND_PX) * 1280 / 1440 / 2) * 2},
                             permissions=["clipboard-read", "clipboard-write"], accept_downloads=True, color_scheme="light")
        ctx.add_init_script(CURSOR_JS)
        t0 = time.time(); R = Rec(None, t0)
        ctx.expose_function("__cap", R.caption); ctx.add_init_script(CAPTION_JS)
        page = ctx.new_page(); R.page = page
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
    vtt = out.with_suffix(".vtt")
    vtt.write_text("WEBVTT\n\n" + "".join(f"{i}\n{vtt_time(a)} --> {vtt_time(b)}\n{tx}\n\n" for i, (a, b, tx) in enumerate(R.cues, 1)))
    print("captions", vtt, len(R.cues), "cues", flush=True)
    return sha


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--out", default=str(K.ROOT / "artifacts" / "demo.webm")); ap.add_argument("--narration", default=str(K.ROOT / "artifacts" / "NARRATION.md"))
    a = ap.parse_args(); run(a.rev, pathlib.Path(a.out), pathlib.Path(a.narration))
