#!/usr/bin/env python3
"""Helper for deploy/make_public_snapshot.sh (T-194). Subcommands (Python 3 stdlib only):

  init-patterns REPO   write the LOCAL, git-ignored patterns file (deploy/.private_patterns) from REPO's own history and files
                       (non-publish commit authors, tailnet host names, device names). Values are never printed.
  prune DIR            delete every image/media file that is not on the allow-list (see ALLOW below).
  redact DIR           replace secrets, tailnet hosts/IPs and every private literal in every text file under DIR; also the
                       outside project name (shared switch in evals/finalize_prompt_log.py) -> <outside project>.
  drop-chris DIR       remove board/inbox/ (Chris's own notes) and replace the text of his inbox events in board/activity.jsonl
                       (his instruction: only MASTER_PROMPT.md of his own words may be published).
  scan DIR             strict independent scan of every file (text, backslash-stripped text, paths, binaries as latin-1) plus
                       the image rules. Exit 1 on any hit. Prints file:line and a category, never the value.

Private literals (work email, employer domain, device names, the tailnet host) are NOT written in this file or anywhere else in the
repo. They are read at run time from a gitignored file (deploy/.private_patterns, or $SNAPSHOT_PATTERNS) that init-patterns derives
from the repo's own data; without that file every command exits 2 with an explanation. Only generic shapes (a `tail`+hex label, the
tailnet suffix, the <redacted-private>/10 range) are spelled here.
"""
from __future__ import annotations

import bisect
import collections
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
# The outside-project-name rule (T-198/T-199) is NOT copied here: it is imported from evals/finalize_prompt_log.py so the prompt log
# and the snapshot share one switch (REDACT_OUTSIDE_PROJECT_NAME), one regex (OUTSIDE_RX), one marker (M_OUTSIDE) and one
# backslash-insensitive substituter (sub_normalized). It does not depend on the local patterns file.
sys.path.insert(0, str(HERE.parent / "tools"))
sys.path.insert(0, str(HERE.parent / "evals"))
import finalize_prompt_log as fpl  # noqa: E402
PATTERNS_FILE = Path(os.environ.get("SNAPSHOT_PATTERNS") or HERE / ".private_patterns")
PUBLISH_EMAIL = "cborsheim@gmail.com"  # the public identity the snapshot commit uses; not private

# ---- image allow-list --------------------------------------------------------------------------------------------------
# Only these locations may carry images/media in the snapshot. Everything else is deleted by `prune` and is a scan failure.
ALLOW = ("artifacts/screenshots/guided/", "artifacts/screenshots/final/", "artifacts/mockups/", "submission/", "artifacts/demo.webm", "app/frontend/")
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".ico", ".icns", ".avif", ".heic", ".heif",
             ".svg", ".mp4", ".mov", ".webm", ".m4v", ".avi", ".pdf"}
MAGIC = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"GIF87a", b"GIF89a", b"BM", b"II*\x00", b"MM\x00*", b"%PDF-")
RASTER_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff"}


def is_media(p: Path, head: bytes) -> bool:
    if p.suffix.lower() in MEDIA_EXT:
        return True
    if head[:12].startswith(MAGIC[:6]) or head[:5] == b"%PDF-":  # renamed picture
        return True
    return head[:4] == b"RIFF" and head[8:12] == b"WEBP" or head[4:8] == b"ftyp"


def allowed(rel: str) -> bool:
    return rel.startswith(ALLOW)


# ---- generic shapes (no private value is spelled here) ----------------------------------------------------------------
DOT = r"(?:\.|\[\.\]|\(\.\)|%2e|\s+dot\s+)"
CG = r"(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])"
SYNTHETIC_IPS = ("<redacted-private>",)  # the one documentation-style peer address the D-036 test uses; exempt in redaction and scan
_EX = "".join(r"(?!" + re.escape(i) + r"\b)" for i in SYNTHETIC_IPS)
GENERIC = [
    ("tailnet host label (tail + hex)", "tailnet host",
     re.compile(r"(?:[A-Za-z0-9-]+" + DOT + r")?tail(?=[0-9a-f]*\d)[0-9a-f]{6,}(?:" + DOT + r"ts" + DOT + r"net)?", re.I)),
    ("tailnet suffix (ts + net)", "tailnet host", re.compile(r"(?:[A-Za-z0-9-]+" + DOT + r")*ts" + DOT + r"net", re.I)),
    ("CGNAT address <redacted-private>/10", "tailnet host",
     re.compile(r"(?<![\d.])" + _EX + r"100" + DOT + CG + DOT + r"\d{1,3}" + DOT + r"\d{1,3}(?![\d/])")),
]
MARK = {"tailnet host": "<redacted-private>", "private": "<redacted-private>", "device": "<device>"}

# A backslash run in front of punctuation is dropped (host\.name -> host.name); backslash+letter (\b, \n) becomes a space so regex
# word boundaries and JSON newlines still separate tokens. Offsets are mapped back by _to_orig.
ESC = re.compile(r"\\+(?=[^A-Za-z0-9\\])|\\[A-Za-z]")


def _strip(text: str):
    if "\\" not in text:
        return text, [], []
    ends, cum, out, last, removed, spos = [], [], [], 0, 0, 0
    for m in ESC.finditer(text):
        a, b = m.span()
        out.append(text[last:a])
        spos += a - last
        rep = " " if text[b - 1].isalpha() else ""
        out.append(rep)
        spos += len(rep)
        removed += (b - a) - len(rep)
        ends.append(spos)
        cum.append(removed)
        last = b
    out.append(text[last:])
    return "".join(out), ends, cum


def _to_orig(p: int, ends, cum, start: bool) -> int:
    i = bisect.bisect_right(ends, p) if start else bisect.bisect_left(ends, p)
    return p + (cum[i - 1] if i else 0)


def _binary(data: bytes) -> bool:
    return data[:2] not in (b"\xff\xfe", b"\xfe\xff") and b"\0" in data[:8000]


def _text(data: bytes) -> str:
    if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return data.decode("utf-16", "replace")
    return data.decode("utf-8", "surrogateescape")


def _files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.relative_to(root).parts[0] == ".git":
            continue
        if p.is_symlink() or not p.is_file():
            continue
        yield p


# ---- private literals --------------------------------------------------------------------------------------------------
def _literal_rx(lit: str) -> re.Pattern:
    out = []
    for ch in lit:
        if ch == ".":
            out.append(DOT)
        elif ch == "@":
            out.append(r"(?:@|%40|\s+at\s+)")
        else:
            out.append(re.escape(ch))
    core = "".join(out)
    # word-ish boundaries so a short token does not match inside a longer word, tolerant of the \b a regex source leaves behind
    return re.compile(r"(?<![A-Za-z0-9])" + core + r"(?![A-Za-z0-9])", re.I)


def _read_patterns():
    """[(kind, value)] from the local patterns file; exits 2 with a clear message if it is missing or empty."""
    if not PATTERNS_FILE.is_file():
        sys.stderr.write(
            "snapshot: the local private-patterns file is missing, so the scan could not look for private values.\n"
            f"  expected: {PATTERNS_FILE}\n"
            "  It is deliberately NOT in git (no private value may be committed). Create it from this repo's own data with:\n"
            "      python3 deploy/snapshot_tool.py init-patterns .\n"
            "  (or point SNAPSHOT_PATTERNS at your own file: one `kind<TAB>value` per line, kind = email|device|term). Nothing was built.\n")
        sys.exit(2)
    out = []
    for n, line in enumerate(PATTERNS_FILE.read_text(encoding="utf-8").splitlines(), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        kind, _, val = line.partition("\t")
        val = val.strip()
        if kind not in ("email", "device", "term") or not val:
            sys.exit(f"snapshot: {PATTERNS_FILE} line {n}: expected `email|device|term<TAB>value`")
        out.append(("device" if kind == "device" else "private", val))
    if not out:
        sys.exit(f"snapshot: {PATTERNS_FILE} has no patterns; refusing to run a scan that looks for nothing")
    return out


def load_private():
    """[(kind, regex, index)] (word-bounded literal matchers, for the plain and backslash-stripped views)."""
    return [(kind, _literal_rx(val), i) for i, (kind, val) in enumerate(_read_patterns(), 1)]


# ---- normalized view (D-070): quotes, '+', whitespace, backslashes dropped; case folded by re.I ---------------
# 'abc' + 'def', "abc" "def", abc\def, a b c and abc[.]com all collapse to a form a plain substring match finds. Only literals of at
# least NORM_MIN characters are matched in this view (without word boundaries a short token would match inside glued words).
NORM_MIN = 8
_NDROP = fpl._VIEW_ALL  # the same view as the prompt log (backslash, quotes, backticks, '+', whitespace); brackets stay, term_rx knows [.]


def _norm(text: str):
    """(view, view_starts, orig_starts): the view plus the segment table that maps a view offset back to the original offset."""
    parts, vs, os_, v, last = [], [], [], 0, 0
    for m in _NDROP.finditer(text):
        if m.start() > last:
            parts.append(text[last:m.start()])
            vs.append(v)
            os_.append(last)
            v += m.start() - last
        last = m.end()
    if last < len(text):
        parts.append(text[last:])
        vs.append(v)
        os_.append(last)
    return "".join(parts), vs, os_


def _to_orig_n(p: int, vs, os_, end: bool) -> int:
    q = p - 1 if end else p
    i = bisect.bisect_right(vs, q) - 1
    return os_[i] + (q - vs[i]) + (1 if end else 0)


def _norm_literal_rx(lit: str):
    """Regex for a private literal against the normalized view, or None when the literal is too short for this view."""
    n = _NDROP.sub("", lit)
    if len(n) < NORM_MIN:
        return None
    out = []
    for ch in n:
        out.append(r"(?:\.|dot|%2e)" if ch == "." else r"(?:@|%40|at)" if ch == "@" else re.escape(ch))
    return re.compile("".join(out), re.I)


def _prefilter(value: str, wildcard: bool):
    """[(alt, ...), ...]: lower-case alnum runs of which, for every group, at least one must occur in any match of the value's regex
    (empty list: cannot pre-filter). With one-character wildcards (8+ characters) the replaced character sits in only one half, so
    the longest run of either half is required."""
    n = _NDROP.sub("", value).lower()

    def longest(t):
        runs = re.findall(r"[a-z0-9]+", t)
        return max(runs, key=len) if runs else ""
    if wildcard and len(n) >= 8:
        a, b = longest(n[:len(n) // 2]), longest(n[len(n) // 2:])
        return [(a, b)] if len(a) >= 3 and len(b) >= 3 else []
    r = longest(n)
    return [(r,)] if len(r) >= 3 else []


def _fpl_term_rules():
    """Private-term rules of the finalize rule set (values come from the patterns file) as [(label, regex)]; shared, never copied."""
    rules = [("work email / tailnet host term (finalize)", fpl.PRIVATE_TERM_RX), ("device name (finalize)", fpl.DEVICE_RX),
             ("third-party name (finalize)", fpl.THIRD_RX), ("personal file name (finalize)", fpl.PERSONAL_BARE_RX)]
    if fpl.REDACT_OUTSIDE_PROJECT_NAME:
        rules.append(("outside project name (shared switch)", fpl.OUTSIDE_RX))
        if fpl.OUTSIDE_WORD_RX is not None:   # the ticker: whole-word on the raw text, not on the stripped view
            rules.append(("outside project name, short value (shared switch)", fpl.OUTSIDE_WORD_RX))
    return rules


def _fpl_shape_rules():
    """Path / shape rules of the finalize rule set (no private value in them), for the plain and backslash-stripped views."""
    return ([("private network shape (finalize)", fpl.PRIVATE_RX)]
            + [("personal file path (finalize)", rx) for rx in fpl.PERSONAL_RXS]
            + [("home-directory path (finalize)", rx) for rx in fpl.HOME_RXS])


def _require_terms():
    """Fail closed: with the outside-name switch on, the patterns file must carry its #@outside line (the value is deliberately not
    in tracked code, and no repo data names it, so init-patterns cannot derive it)."""
    if fpl.REDACT_OUTSIDE_PROJECT_NAME and not fpl.TERMS.get("outside"):
        sys.stderr.write(
            "snapshot: REDACT_OUTSIDE_PROJECT_NAME is on but the patterns file has no `#@outside<TAB>name` line, so the name would not be\n"
            f"  redacted or scanned for.\n  file: {PATTERNS_FILE}\n"
            "  init-patterns keeps existing `#@` lines but cannot derive this one (D-070: no private value in tracked code). Add it once.\n"
            "  Nothing was built.\n")
        sys.exit(2)
    missing = [k for k in ("third", "personal") if not fpl.TERMS.get(k)]
    if missing:
        sys.stderr.write(f"snapshot: WARNING no `#@{'`, `#@'.join(missing)}` term in the patterns file: those finalize rules are inactive.\n")


def init_patterns(repo: Path) -> int:
    """Derive the private literals from the repo's own data, write them (mode 600) to the git-ignored file. Values are not printed."""
    def git(*a):
        return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout
    vals: dict = {}
    for line in git("log", "--format=%ae%n%ce").splitlines():
        line = line.strip().lower()
        if "@" in line and line != PUBLISH_EMAIL and "noreply" not in line:
            vals[("email", line)] = 1
            local, _, dom = line.partition("@")
            vals[("email", local)] = 1
            vals[("email", dom)] = 1
    envf = repo / "memory" / "ENVIRONMENT.md"
    if envf.is_file():
        for rx in (r"node `([^`]{4,})`", r"phone `([^`]{4,})`"):
            for m in re.finditer(rx, envf.read_text(encoding="utf-8")):
                vals[("device", m.group(1))] = 1
    # tailnet host names as they appear in tracked files: host label and the full name (generic shape only)
    try:
        hosts = git("grep", "-hoIE", r"[A-Za-z0-9-]+\.tail[0-9a-f]{6,}\." + "ts" + r"\." + "net", "HEAD", "--").splitlines()
    except subprocess.CalledProcessError:
        hosts = []
    for h in hosts:
        h = h.strip().lower().split(":", 1)[-1] if h.startswith("HEAD:") else h.strip().lower()
        vals[("term", h)] = 1
        vals[("device", h.split(".")[0])] = 1
    if not vals:
        sys.exit("init-patterns: found nothing private to derive; write the file by hand (kind<TAB>value per line)")
    PATTERNS_FILE.parent.mkdir(parents=True, exist_ok=True)
    keep = []  # finalize-only classes (#@third|outside|personal<TAB>value) are entered by hand and survive a re-run
    if PATTERNS_FILE.is_file():
        keep = [ln for ln in PATTERNS_FILE.read_text(encoding="utf-8").splitlines() if ln.startswith("#@") and "\t" in ln]
    PATTERNS_FILE.write_text(
        "# LOCAL ONLY, never commit. kind<TAB>value; read by deploy/snapshot_tool.py. Derived from this repo's history and files.\n"
        "# finalize-only classes (ignored by snapshot_tool.py, read by evals/finalize_prompt_log.py): #@third|outside|personal<TAB>value\n"
        + "".join(f"{k}\t{v}\n" for k, v in sorted(vals)) + "".join(ln + "\n" for ln in keep), encoding="utf-8")
    os.chmod(PATTERNS_FILE, 0o600)
    print(f"init-patterns: wrote {len(vals)} pattern(s) to {PATTERNS_FILE} (values not shown); keep it out of git")
    return 0


# ---- prune ---------------------------------------------------------------------------------------------------------------
def prune(root: Path) -> int:
    gone, kept = [], []
    for p in _files(root):
        rel = p.relative_to(root).as_posix()
        with p.open("rb") as f:
            head = f.read(16)
        if not is_media(p, head):
            continue
        if allowed(rel):
            kept.append(rel)
        else:
            p.unlink()
            gone.append(rel)
    for d in sorted((x for x in root.rglob("*") if x.is_dir() and ".git" not in x.relative_to(root).parts[:1]), reverse=True):
        try:
            d.rmdir()  # drop directories emptied by the prune
        except OSError:
            pass
    by_dir = collections.Counter(str(Path(g).parent) for g in gone)
    print(f"prune: removed {len(gone)} image/media file(s) not on the allow-list ({', '.join(ALLOW)}); kept {len(kept)} allow-listed")
    for d, n in by_dir.most_common():
        print(f"  removed {n} from {d}/")
    return 0


# ---- drop-chris ----------------------------------------------------------------------------------------------------------
def drop_chris(root: Path) -> int:
    d = root / "board" / "inbox"
    nfiles = sum(1 for p in d.rglob("*") if p.is_file()) if d.is_dir() else 0
    if d.exists():
        shutil.rmtree(d)
    a = root / "board" / "activity.jsonl"
    nev = fpl.omit_inbox_file(a) if a.is_file() else 0
    print(f"drop-chris: removed board/inbox/ ({nfiles} file(s)); replaced the text of {nev} inbox event(s) in board/activity.jsonl")
    return 0


# ---- redact --------------------------------------------------------------------------------------------------------------
def redact(root: Path) -> int:
    sys.dont_write_bytecode = True
    _require_terms()
    priv = load_private()
    sys.path.insert(0, str(root / "tools"))
    sys.modules.pop("check_secrets", None)  # finalize_prompt_log (imported above) cached the repo's copy; use the snapshot's own
    import check_secrets as cs  # the snapshot's own secret patterns
    rules = [(rx, kind, label) for label, kind, rx in GENERIC] + [(rx, kind, f"private literal #{i}") for kind, rx, i in priv]
    counts: collections.Counter = collections.Counter()
    fcounts: collections.Counter = collections.Counter()
    touched, skipped = set(), 0
    for p in _files(root):
        data = p.read_bytes()
        if _binary(data) or data[:2] in (b"\xff\xfe", b"\xfe\xff"):
            skipped += 1
            continue
        text = new = data.decode("utf-8", "surrogateescape")
        for rx, name in cs.PATTERNS:
            def sub(m, name=name):
                counts["secret-shaped value"] += 1
                if name == "ANTHROPIC_API_KEY with a value":
                    return re.match(r"^(ANTHROPIC_API_KEY\s*[=:]\s*['\"]?)", m.group(0)).group(1) + "<redacted>"
                return "<redacted>"
            new = rx.sub(sub, new)
        new = fpl.scrub(new, "-", fcounts)  # the full prompt-log rule set (D-070): terms on the normalized view, shapes and paths
        stripped, ends, cum = _strip(new)
        spans = []
        for rx, kind, label in rules:
            for m in rx.finditer(stripped):
                spans.append((_to_orig(m.start(), ends, cum, True), _to_orig(m.end(), ends, cum, False), kind, label))
        if spans:
            spans.sort()
            merged = []
            for a, b, kind, label in spans:
                if merged and a < merged[-1][1]:
                    if b > merged[-1][1]:
                        merged[-1][1] = b
                    continue
                merged.append([a, b, kind, label])
            out, last = [], 0
            for a, b, kind, label in merged:
                out += [new[last:a], MARK[kind]]
                last = b
                counts["device name" if kind == "device" else "tailnet host / IP / private literal"] += 1
            out.append(new[last:])
            new = "".join(out)
        if new != text:
            touched.add(p.relative_to(root).as_posix())
            p.write_bytes(new.encode("utf-8", "surrogateescape"))
    for (_, cat), n in fcounts.items():
        counts["finalize rules: " + cat] += n
    counts += collections.Counter()  # drop zero entries
    print(f"redact: {sum(counts.values())} replacement(s) in {len(touched)} file(s); {skipped} binary/utf-16 file(s) not rewritten")
    for k, v in counts.most_common():
        print(f"  {k}: {v}")
    py = sorted(t for t in touched if t.endswith(".py"))
    if py:
        print(f"  rewritten code/test files ({len(py)}): " + ", ".join(py))
    return 0


# ---- strict scan ---------------------------------------------------------------------------------------------------------
def _ocr(p: Path, rules) -> list:
    """Hits found by tesseract in one raster image (labels only)."""
    r = subprocess.run(["tesseract", str(p), "-", "--psm", "11"], capture_output=True, text=True, timeout=120)
    txt = re.sub(r"\s+", " ", r.stdout)
    return [lab for rx, lab in rules if rx.search(txt)]


def scan(root: Path) -> int:
    _require_terms()
    priv = load_private()
    rules = [(rx, label) for label, _, rx in GENERIC] + [(rx, f"private literal #{i} ({'device' if k == 'device' else 'value'})") for k, rx, i in priv]
    shape = [(rx, lab) for lab, rx in _fpl_shape_rules()]  # plain + backslash-stripped views, text files only
    # Terms are matched on the normalized view only (it only deletes characters, so every plain or backslash-stripped match is also
    # a match there): quotes, '+', whitespace, backslashes dropped, case folded. Each regex gets a cheap
    # pre-filter (an exact alnum run that must occur in any match) so a multi-MB transcript is not scanned by every wildcard branch.
    nrules = []
    for i, (k, v) in enumerate(_read_patterns(), 1):
        if _norm_literal_rx(v):
            nrules.append((_norm_literal_rx(v), _prefilter(v, False), f"split/quoted spelling of private literal #{i}"))
    for kind, label in (("email", None), ("term", None), ("device", "device name (finalize)"), ("third", "third-party name (finalize)"),
                        ("personal", "personal file name (finalize)"), ("outside", "outside project name (shared switch)")):
        if kind == "outside" and not fpl.REDACT_OUTSIDE_PROJECT_NAME:
            continue
        for v in fpl.TERMS.get(kind, []):
            nrules.append((fpl.term_rx([v]), _prefilter(v, True), (label or "work email / tailnet host term (finalize)") + ", normalized"))
    hits: dict = {}
    nfiles = 0
    rasters = []
    for p in _files(root):
        rel = p.relative_to(root).as_posix()
        nfiles += 1
        for rx, label in rules:
            if rx.search(rel):
                hits[(rel, label, "path")] = 1
        if rel.startswith("board/inbox/"):
            hits[(rel, "Chris's own board-inbox note (must not be published)", "file")] = 1
        if rel == "board/activity.jsonl":
            for ln_no, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if fpl.omit_inbox_text(ln)[1]:
                    hits[(rel, "Chris's board-inbox note text", f"line {ln_no}")] = 1
        data = p.read_bytes()
        if is_media(p, data[:16]):
            if not allowed(rel):
                hits[(rel, "image/media file not on the allow-list", "file")] = 1
            elif p.suffix.lower() in RASTER_EXT:
                rasters.append(p)
        binary = _binary(data)
        text = data.decode("latin-1") if binary else _text(data)
        stripped, _, _ = _strip(text)
        for rx, label in rules + ([] if binary else shape):  # path shapes make no sense on image bytes read as latin-1
            for variant, body in (("plain", text), ("escaped", stripped)):
                if variant == "escaped" and stripped == text:
                    continue
                for m in rx.finditer(body):
                    line = body.count("\n", 0, m.start()) + 1
                    hits.setdefault((rel, label, ("binary" if binary else variant) + f" line {line}"), 1)
        if not binary:  # normalized view: quotes, '+', whitespace, backslashes, brackets stripped, case folded
            view, vs, os_ = _norm(text)
            low = view.lower()
            for rx, pre, label in nrules:
                if pre and not all(any(x in low for x in alt) for alt in pre):
                    continue
                for m in rx.finditer(view):
                    line = text.count("\n", 0, _to_orig_n(m.start(), vs, os_, False)) + 1
                    hits.setdefault((rel, label, f"normalized line {line}"), 1)
    ocr_note = ""
    if rasters:
        if shutil.which("tesseract"):
            for p in rasters:
                for lab in _ocr(p, rules):
                    hits[(p.relative_to(root).as_posix(), lab, "pixels (OCR)")] = 1
            nfinal = sum(1 for p in rasters if p.relative_to(root).as_posix().startswith("artifacts/screenshots/final/"))
            ocr_note = f"; {len(rasters)} allow-listed raster image(s) OCR-checked ({nfinal} under artifacts/screenshots/final/; counts only, no values printed)"
        else:
            ocr_note = (f"; WARNING: tesseract not installed, so the pixels of {len(rasters)} allow-listed raster image(s) were NOT checked "
                        "(look at each by eye before publishing)")
    print(f"scan: {nfiles} file(s) checked against {len(rules)} pattern(s) (3 generic + {len(priv)} private + the finalize rule set, plain / backslash-stripped / normalized) + the image allow-list{ocr_note}")
    print("scan: image/media allowed only under " + ", ".join(ALLOW) + "; text scan cannot see pixels, so nothing else may be an image")
    lines = [f"HIT {rel}: {label} ({where})" for (rel, label, where) in sorted(hits)]
    if lines:
        print("\n".join(lines[:200]))
        if len(lines) > 200:
            print(f"... and {len(lines) - 200} more")
        print(f"scan: FAIL ({len(lines)} hit(s))")
        return 1
    print("scan: ok (0 hits)")
    return 0


if __name__ == "__main__":
    cmds = {"init-patterns": init_patterns, "prune": prune, "drop-chris": drop_chris, "redact": redact, "scan": scan}
    if len(sys.argv) != 3 or sys.argv[1] not in cmds:
        sys.exit("usage: snapshot_tool.py init-patterns|prune|drop-chris|redact|scan DIR")
    sys.exit(cmds[sys.argv[1]](Path(sys.argv[2]).resolve()))
