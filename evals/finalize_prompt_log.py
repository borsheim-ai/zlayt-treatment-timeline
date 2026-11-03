#!/usr/bin/env python3
"""Build submission/prompt-log/ (T-187). Re-runnable and idempotent.

  python3 evals/finalize_prompt_log.py

1. Copies docs/CONTRACT.md, board/activity.jsonl, reviews/, memory/{DECISIONS,ORCHESTRATOR_DECISIONS,LESSONS}.md.
2. Runs tools/export_prompt_log.py in-process with the tool-result cap effectively off. Its render_content is wrapped so that
   the tool result of any call (or any result text) that touches a path under the home directory other than this repo,
   ~/.claude, the nvm/playwright caches and the Claude scratch dir is replaced by "<outside-repo file omitted>".
3. Redacts every file (not README/TOOLS/REDACTIONS) in these classes, each counted in REDACTIONS.md (file, class, count; never a value):
   secrets (tools/check_secrets.py patterns), private network details and a work email, device names, a third-party name,
   personal job-application file names, and other home-directory paths.
4. Rewrites the "edit classes" block of README.md from real marker counts so the README matches the output.
5. Self-test: fails (exit 1) if any private term remains in any output file.
6. Chris's own words are not published (his instruction, except MASTER_PROMPT.md which he authorized): (a) a session transcript that carries
   any of his own user turns (origin kind "human", i.e. the orchestrator sessions) is not written at all and is dropped from INDEX.md;
   (b) in every other file, a run of 8+ words copied verbatim from one of his messages is replaced by one marker, except runs that also
   occur in MASTER_PROMPT.md; (c) the text of his board-inbox events in board-activity.jsonl is replaced. His messages are read at run time from
   the local Claude Code JSONL files; no word of them is written in this repo.

NO PRIVATE VALUE IS WRITTEN IN THIS FILE (D-070). Every private term (work email and its parts, device names, tailnet hosts, the
third-party name, personal file-name pieces, the outside project name) is read at run time from the git-ignored
deploy/.private_patterns (or $SNAPSHOT_PATTERNS), in the format deploy/snapshot_tool.py uses: one `kind<TAB>value` per line,
kind = email|device|term. Finalize-only classes are carried on comment lines the snapshot tool ignores: `#@third|outside|personal<TAB>value`.
Only generic shapes (a tail+hex label, the tailnet suffix, the <redacted-private>/10 range) are spelled here. Without the file the build
stops with an explanation.

Terms are matched on a NORMALIZED view of each text: backslashes, quotes (straight and curly), backticks, `+` and all whitespace are
removed and case is folded, so a value split into quoted fragments joined with `+`, escaped, or spread over lines is still found;
spans are mapped back to the original text. Terms of 8+ characters are also matched with any one letter or digit replaced by `.`, `?` or `*`
(regex-wildcard spellings). Terms of 7+ letters and digits are also matched GAPPED: any run of 0-12 punctuation characters may sit between
two of their letters/digits (a separator the value itself has, such as `.`, `-` or `_`, must still be there), so `ab*.cd`, `("ab","cd")` and
`ab\\*cd` forms are found. Terms have no word boundaries on purpose: stripped spellings glue neighbouring letters to the match.

Derived terms (T-187 r4 / D-072; computed from the file, nothing extra is stored): a device name with a trailing `-<digits>` is also matched
without that suffix; the first `/`-separated piece (top folder, 8+ characters) of a personal value is also a personal term. A `term`/`email`/`device`/
`third` line whose normalized value equals an `#@outside` value is dropped, so REDACT_OUTSIDE_PROJECT_NAME is the only thing that decides
whether that name is masked.
"""
from __future__ import annotations

import bisect
import collections
import json
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_secrets as cs  # noqa: E402
import export_prompt_log as ex  # noqa: E402

OUT = ROOT / "submission" / "prompt-log"
HAND_WRITTEN = {"TOOLS.md", "README.md", "REDACTIONS.md"}
ANTHROPIC = "ANTHROPIC_API_KEY with a value"
C_SECRET = "secret-shaped string (check_secrets patterns)"
C_PRIVATE = "private network detail (tailnet host/IP, work email; plain, escaped, split and regex-literal forms)"
C_DEVICE = "device name"
C_THIRD = "third-party name"
C_PERSONAL = "personal job-application file name"
C_HOME = "home-directory path outside this repo"
C_OMIT = "outside-repo tool result omitted"
C_OUTSIDE = "outside project name (bare, any case; switch REDACT_OUTSIDE_PROJECT_NAME)"
C_CHRIS = "run of 8+ words copied verbatim from one of Chris's own messages"
C_INBOX = "Chris's board-inbox note text (board-activity.jsonl)"
SEP = re.compile(r"^(ANTHROPIC_API_KEY\s*[=:]\s*['\"]?)")

M_SECRET, M_PRIVATE, M_DEVICE, M_THIRD, M_PERSONAL, M_HOME, M_OMIT = (
    "<redacted>", "<redacted-private>", "<device>", "<third-party name>", "<personal file>", "<home-path>", "<outside-repo file omitted>")

# --- THE SWITCH (T-198) -----------------------------------------------------------------------------------------------
# Until Chris answers T-193 the name of the outside project (the one his other local project folder is named after) is redacted
# everywhere in the prompt log: any case, any form (path segment, prose, JSON/regex-escaped). Set this to False ONLY when he says
# "show" in T-193; nothing else needs to change (the rule, the README edit text and the self-test all follow it).
REDACT_OUTSIDE_PROJECT_NAME = True
M_OUTSIDE = "<outside project>"
M_CHRIS = "<Chris's message omitted>"
M_INBOX = "<Chris's inbox note omitted>"
MIN_SPAN = 8   # words
MASTER_PROMPT = ROOT / "MASTER_PROMPT.md"   # the one thing Chris authorized: its wording is never treated as "his message"

# --- private terms: read at run time from the git-ignored patterns file (D-070) ----------------------------------------
PATTERNS_FILE = Path(os.environ.get("SNAPSHOT_PATTERNS") or ROOT / "deploy" / ".private_patterns")
_VIEW_ALL = re.compile("[\\\\\"'`+‘’“”\\s]")  # chars removed for the normalized view
_NEVER = re.compile(r"(?!x)x")
KINDS = ("email", "device", "term", "third", "outside", "personal")


def load_terms() -> dict | None:
    """{kind: [value, ...]} from the patterns file, or None if it is missing. Never prints a value."""
    if not PATTERNS_FILE.is_file():
        return None
    out: dict = {k: [] for k in KINDS}
    for n, line in enumerate(PATTERNS_FILE.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        if line.startswith("#@"):
            kind, _, val = line[2:].partition("\t")
        elif line.lstrip().startswith("#"):
            continue
        else:
            kind, _, val = line.partition("\t")
        val = val.strip()
        if kind not in KINDS or not val:
            sys.exit(f"finalize: {PATTERNS_FILE} line {n}: expected `<kind><TAB><value>`, kind one of {', '.join(KINDS)} (value not shown)")
        out[kind].append(val)
    return _derive(out)


def _key(v: str) -> str:
    return re.sub(r"[^a-z0-9]", "", v.lower())


def _derive(t: dict) -> dict:
    """Partial terms and the outside-name precedence (see the module docstring). Longest values first, so a full value wins over its stem."""
    outside = {_key(v) for v in t["outside"]}
    for kind in ("email", "device", "term", "third"):
        t[kind] = [v for v in t[kind] if _key(v) not in outside]   # the switch alone decides about the outside name
    for v in list(t["device"]):
        m = re.match(r"(.+?)-\d+$", v)
        if m and len(_key(m.group(1))) >= 8:
            t["device"].append(m.group(1))
    for v in list(t["personal"]):
        if "/" in v:
            first = v.split("/")[0]   # the top folder only: later pieces are often common words ("Applications") that would redact "Application Support"
            if len(_key(first)) >= 8:
                t["personal"].append(first)
    for kind in t:
        seen, uniq = set(), []
        for v in sorted(t[kind], key=lambda x: -len(x)):
            if v not in seen:
                seen.add(v)
                uniq.append(v)
        t[kind] = uniq
    return t


def require_terms() -> dict:
    t = load_terms()
    if t is None or not any(t.values()):
        sys.stderr.write(
            "finalize: the local private-patterns file is missing or empty, so the prompt log cannot be redacted or checked.\n"
            f"  expected: {PATTERNS_FILE}\n"
            "  It is deliberately NOT in git (no private value may be committed). Create it with:\n"
            "      python3 deploy/snapshot_tool.py init-patterns .\n"
            "  then add the finalize-only lines (#@third / #@outside / #@personal<TAB>value), or set SNAPSHOT_PATTERNS to your own file.\n"
            "  Nothing was built.\n")
        sys.exit(2)
    return t


_DOT = r"(?:\.|\[\.\]|\(\.\)|%2e|u002e|x2e|dot)"
_AT = r"(?:@|%40|at)"


_GAP0 = r"[^A-Za-z0-9]{0,12}"   # inside a word


def _gapped(v: str) -> str | None:
    """Regex for v with 0-12 punctuation characters between any two of its letters/digits. Each separator the value itself has (`.`, `-`,
    `_`, `/`, also a leading or trailing one) must still be present, literally, between up to 6 extra punctuation characters on each side, so
    `name*.tld` and `name\\*.tld` match but a person's `First Last` does not match a `first.last` value and `First Last <mail>` does not match `FirstLast_`.
    None when v has fewer than 7 letters/digits."""
    pieces = re.findall(r"[A-Za-z0-9\u0080-\U0010ffff]+|[^A-Za-z0-9\u0080-\U0010ffff]+", _VIEW_ALL.sub("", v))
    if sum(len(x) for x in pieces if re.match(r"[A-Za-z0-9\u0080-\U0010ffff]", x)) < 7:
        return None
    out = []
    for i, x in enumerate(pieces):
        if re.match(r"[A-Za-z0-9\u0080-\U0010ffff]", x):
            out.append(_GAP0.join(re.escape(ch) for ch in x))
        else:
            inner = 0 < i < len(pieces) - 1   # inside the value `-` and `_` are interchangeable; at its ends the character is literal
            out.append(r"[^A-Za-z0-9]{0,6}" + r"[^A-Za-z0-9]{0,6}".join(r"[-_]" if inner and ch in "-_" else re.escape(ch) for ch in x) + r"[^A-Za-z0-9]{0,6}")
    return "".join(out)


def term_rx(values: list, wildcard: bool = True, boundaries: bool = False) -> re.Pattern:
    """Case-insensitive regex for literal values (for the normalized view: no whitespace, quotes, '+', backslashes).
    '.' also matches a bracketed or spelled-out dot and '@' also 'at'; values of 8+ characters also match with one character replaced by . ? or *;
    values of 7+ letters/digits also match gapped (see _gapped). Values are tried longest first."""
    if not values:
        return _NEVER
    alts = []
    for v in sorted(values, key=lambda x: -len(x)):
        chars = _VIEW_ALL.sub("", v)
        toks = [_DOT if ch == "." else _AT if ch == "@" else re.escape(ch) for ch in chars]
        if not toks:
            continue
        g = _gapped(v)
        if g:
            alts.append(g)
        alts.append("".join(toks))
        if wildcard and len(toks) >= 8:
            for i in range(len(toks)):
                if chars[i].isalnum():   # a separator (`_`, `-`, `.`) is never the wildcarded character: `Name_` must not match `**Name**`
                    alts.append("".join(toks[:i]) + r"[.?*]" + "".join(toks[i + 1:]))
    if not alts:
        return _NEVER
    core = "(?:" + "|".join(alts) + ")"
    return re.compile((r"(?<![A-Za-z0-9])" + core + r"(?![A-Za-z0-9])") if boundaries else core, re.I)


TERMS = load_terms() or {k: [] for k in KINDS}
# A 3-4 character outside value (the company's stock ticker, bare or with a `$`) cannot be matched on the whitespace-stripped view: that view
# glues neighbouring words onto it, so there is no word boundary and a boundary-free match would redact inside ordinary words and identifiers.
# Short values are therefore matched whole-word on the raw text (OUTSIDE_WORD_RX); longer ones (the name, `EXCH:TICKER`) on the stripped view.
OUTSIDE_SHORT = sorted((v for v in TERMS["outside"] if len(re.sub(r"[^a-z0-9]", "", v.lower())) <= 4), key=lambda v: -len(v))
TERMS["outside"] = [v for v in TERMS["outside"] if v not in OUTSIDE_SHORT]
OUTSIDE_WORD_RX = (re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(re.escape(v) for v in OUTSIDE_SHORT) + r")(?![A-Za-z0-9])", re.I)
                   if OUTSIDE_SHORT else None)
PRIVATE_TERM_RX = term_rx(TERMS["email"] + TERMS["term"])   # work email and its parts, tailnet hosts
DEVICE_RX = term_rx(TERMS["device"])
THIRD_RX = term_rx(TERMS["third"])
OUTSIDE_RX = term_rx(TERMS["outside"])                      # bare name, no word boundaries: matches inside paths, slugs, snake/kebab/camel forms
PERSONAL_BARE_RX = term_rx(TERMS["personal"])
# a path that runs through the outside name (dir/name-suffix/sub/file.ext): the whole path is one marker, not just the name (backslash-stripped view)
OUTSIDE_PATH_RX = (re.compile("|".join(r"(?:[\w.~$@-]+/)*[\w.-]*" + re.escape(v) + r"[\w.-]*(?:/[^\s\"'`\\)<>|;,:]*)+" for v in TERMS["outside"]), re.I)
                   if TERMS["outside"] else _NEVER)

# generic shapes (no private value): tailnet label / suffix and the <redacted-private>/10 range, applied to a backslash-stripped copy
_PDOT = r"(?:\.|\[\.\]|\(\.\)|\s+dot\s+)"
_CG = r"(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])"  # <redacted-private>/10 second octet
PRIVATE_RX = re.compile("|".join([
    r"(?:[A-Za-z0-9-]+\.)?tail(?=[0-9a-f]*\d)[0-9a-f]{6,}(?:\.<redacted-private>)?",   # tailnet label / host
    r"(?:[A-Za-z0-9-]+\.)*ts" + _PDOT + r"net",                               # bare suffix and any host under it (no word boundaries: \\b spellings must match)
    r"(?<![\d.])100\." + _CG + r"\.\d{1,3}\.\d{1,3}",                         # CGNAT address
    r"(?<![\d.])100\." + _CG + r"\.",                                       # CGNAT /16 prefix (grep commands)
    r"(?<![\d.])<redacted-private>?[^)\n]{0,80}\)",                            # regex-literal IP pattern: <redacted-private>
]), re.I)

# personal job-application names: path / file-name rules on the backslash-stripped copy, then the bare piece on the normalized view
PERSONAL_RXS = []
for _v in TERMS["personal"]:
    _t = r"".join(re.escape(c) for c in _v)
    PERSONAL_RXS.append(re.compile(r"(?:(?:/Users/arsis/|~/)?)" + _t + r"(?:/[^\s\"'`\\)<>|;]*)?", re.I))
    PERSONAL_RXS.append(re.compile(_t + r"[^\"'`\n\\/]*?\.(?:pdf|docx?|md|txt)", re.I))
_HOME = r"(?:/Users/arsis|(?<![\w$])~)"
_ALLOWED = r"(?:zlayt-pm-|\.claude\b|\.nvm/|Library/(?:Caches/ms-playwright|Application Support/Claude))"
HOME_RXS = [
    re.compile(_HOME + r"/(?:Google Drive|Downloads|Documents)/[^\n\"'`\\<>|;]*"),
    re.compile(_HOME + r"/(?!" + _ALLOWED + r")[^\s\"'`\\)<>|;,:]+"),
    re.compile(r"-Users-arsis-(?!zlayt-pm-project|Library-Application-Support-Claude)[A-Za-z0-9._-]+"),
]
SCRATCH_RX = HOME_RXS[2]


def _outside_paths(text: str) -> bool:
    """True if text names a place under the home directory that is not this repo / ~/.claude / caches / Claude scratch."""
    for m in re.finditer(r"(?:/Users/arsis|(?<![\w$])~|\$HOME|\$\{HOME\})", text):
        tail = text[m.end(): m.end() + 90]
        if tail.startswith("/"):
            if not re.match(r"/" + _ALLOWED, tail[1:]) and not re.match(r"/(?:zlayt-pm-)", tail):
                return True
            if tail.startswith("/.claude/projects/-Users-arsis-") and not tail.startswith("/.claude/projects/-Users-arsis-<home-path>"):
                return True
        elif m.group(0) != "~" or re.match(r"(?:[\s\"'`\\;|&]|$)", tail):
            if not re.match(r"[\w.-]", tail[:1] or " "):
                return True
    return bool(SCRATCH_RX.search(text))


# --- Chris's own words (his instruction: only MASTER_PROMPT.md may be published) ----------------------------------------------
_WORD = re.compile(r"[^\W_]+")
_JSON_ESC = re.compile(r'\\[nrtbf"\\/]')   # JSON escapes inside tool-call inputs; replaced by two spaces (same length) so words on either side stay separate


def _words(text: str) -> list:
    return [w.lower() for w in _WORD.findall(text)]


def human_turns() -> list:
    """Texts of Chris's own user turns (origin kind "human") in the local Claude Code transcripts of this project. Read at run time, never stored."""
    out = []
    for j in sorted(ex.PROJ.glob("**/*.jsonl")) if ex.PROJ.is_dir() else []:
        for raw in j.read_text(errors="replace").splitlines():
            if '"human"' not in raw:
                continue
            try:
                d = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if d.get("type") != "user" or (d.get("origin") or {}).get("kind") != "human":
                continue
            c = (d.get("message") or {}).get("content")
            if isinstance(c, list):
                c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
            if isinstance(c, str) and c.strip():
                out.append(c)
    return out


def _grams(words: list, n: int = MIN_SPAN) -> set:
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def load_chris_grams() -> set:
    """Every MIN_SPAN-word run in Chris's messages, minus the runs that also occur in MASTER_PROMPT.md (authorized)."""
    g: set = set()
    for t in human_turns():
        g |= _grams(_words(t))
    if MASTER_PROMPT.is_file():
        g -= _grams(_words(MASTER_PROMPT.read_text(encoding="utf-8", errors="replace")))
    return g


CHRIS_GRAMS = load_chris_grams()
CHRIS_FIRST = {g[0] for g in CHRIS_GRAMS}


def chris_spans(text: str) -> list:
    """[(start, end)] character spans of text that are runs of MIN_SPAN+ words copied verbatim from one of Chris's messages (merged)."""
    if not CHRIS_GRAMS:
        return []
    view = _JSON_ESC.sub("  ", text)
    toks = [(m.group(0).lower(), m.start(), m.end()) for m in _WORD.finditer(view)]
    words = [t[0] for t in toks]
    spans = []
    for i in range(len(toks) - MIN_SPAN + 1):
        if words[i] in CHRIS_FIRST and tuple(words[i:i + MIN_SPAN]) in CHRIS_GRAMS:
            a, b = toks[i][1], toks[i + MIN_SPAN - 1][2]
            if spans and a <= spans[-1][1]:
                spans[-1][1] = max(spans[-1][1], b)
            else:
                spans.append([a, b])
    return [(a, b) for a, b in spans]


def scrub_chris(text: str) -> tuple:
    sp = chris_spans(text)
    if not sp:
        return text, 0
    out, pos = [], 0
    for a, b in sp:
        out += [text[pos:a], M_CHRIS]
        pos = b
    out.append(text[pos:])
    return "".join(out), len(sp)


def omit_inbox_text(line: str) -> tuple:
    """One board-activity.jsonl line: the text of an event by Chris's inbox (event "inbox") is replaced. Returns (line, changed)."""
    try:
        d = json.loads(line)
    except json.JSONDecodeError:
        return line, False
    if isinstance(d, dict) and d.get("event") == "inbox" and d.get("text") != M_INBOX:
        d["text"] = M_INBOX
        return json.dumps(d, ensure_ascii=False), True
    return line, False


def omit_inbox_file(path: Path) -> int:
    lines, n = [], 0
    for ln in path.read_text(encoding="utf-8").splitlines():
        new, ch = omit_inbox_text(ln)
        lines.append(new)
        n += ch
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return n


def has_human_turn(jsonl: Path) -> bool:
    for raw in jsonl.read_text(errors="replace").splitlines():
        if '"human"' in raw:
            try:
                d = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if d.get("type") == "user" and (d.get("origin") or {}).get("kind") == "human":
                return True
    return False


# --- outside-repo omission, wired into the exporter ------------------------------------------------------------------
OUTSIDE_IDS: set = set()
OMIT_COUNT: collections.Counter = collections.Counter()
_CUR = [""]
_orig_render = ex.render_content
_orig_export = ex.export


def _result_text(c) -> str:
    r = c.get("content")
    if isinstance(r, list):
        return "\n".join(x.get("text", "") for x in r if isinstance(x, dict))
    return str(r or "")


def _render(content, max_result):
    if isinstance(content, list):
        new = []
        for c in content:
            if isinstance(c, dict):
                t = c.get("type")
                if t == "tool_use" and _outside_paths(json.dumps(c.get("input"), ensure_ascii=False)):
                    OUTSIDE_IDS.add(c.get("id"))
                elif t == "tool_result" and (c.get("tool_use_id") in OUTSIDE_IDS or _outside_paths(_result_text(c))):
                    c = {**c, "content": M_OMIT}
                    OMIT_COUNT[_CUR[0]] += 1
            new.append(c)
        content = new
    return _orig_render(content, max_result)


DROPPED: list = []   # transcript files not written because the session carries Chris's own messages


def _export(jsonl, title, dest, max_result):
    if has_human_turn(jsonl):
        DROPPED.append(dest.name)
        return 0
    _CUR[0] = "transcripts/" + dest.name
    return _orig_export(jsonl, title, dest, max_result)


# --- normalized substitution ------------------------------------------------------------------------------------------
_KEEP_ALL = re.compile("[^\\\\\"'`+‘’“”\\s]+")
_KEEP_BS = re.compile(r"[^\\]+")


def sub_normalized(text: str, rx: re.Pattern, repl: str, view: str = "all") -> tuple[str, int]:
    """Replace matches of rx found in a normalized copy of text, mapping each span back to the original (the replaced original span
    includes any removed characters inside it). view='all' removes backslashes, quotes, backticks, '+' and whitespace (D-070);
    view='bs' removes backslashes only (for rules that must see spaces and quotes as delimiters)."""
    keep = _KEEP_ALL if view == "all" else _KEEP_BS
    if not rx.search(_VIEW_ALL.sub("", text) if view == "all" else text.replace("\\", "")):
        return text, 0  # fast path: nothing to replace
    runs = [(m.start(), m.end()) for m in keep.finditer(text)]
    stripped = "".join(text[a:b] for a, b in runs)
    spans = [(m.start(), m.end()) for m in rx.finditer(stripped) if m.end() > m.start()]
    if not spans:
        return text, 0
    cum, tot = [], 0
    for a, b in runs:
        cum.append(tot)
        tot += b - a
    def orig(k: int) -> int:
        i = bisect.bisect_right(cum, k) - 1
        return runs[i][0] + (k - cum[i])
    out, pos = [], 0
    for a, b in spans:
        oa, ob = orig(a), orig(b - 1) + 1
        out.append(text[pos:oa])
        out.append(repl)
        pos = ob
    out.append(text[pos:])
    return "".join(out), len(spans)


def scrub(text: str, rel: str, counts: collections.Counter) -> str:
    text, n = scrub_chris(text)   # first, while the words are intact
    counts[(rel, C_CHRIS)] += n
    for rx, name in cs.PATTERNS:
        def sub(m, name=name):
            counts[(rel, C_SECRET)] += 1
            return SEP.match(m.group(0)).group(1) + M_SECRET if name == ANTHROPIC else M_SECRET
        text = rx.sub(sub, text)
    text, n = sub_normalized(text, PRIVATE_RX, M_PRIVATE, "bs")
    counts[(rel, C_PRIVATE)] += n
    text, n = sub_normalized(text, PRIVATE_TERM_RX, M_PRIVATE)
    counts[(rel, C_PRIVATE)] += n
    text, n = sub_normalized(text, DEVICE_RX, M_DEVICE)
    counts[(rel, C_DEVICE)] += n
    text, n = sub_normalized(text, THIRD_RX, M_THIRD)
    counts[(rel, C_THIRD)] += n
    for rx in PERSONAL_RXS:
        text, n = sub_normalized(text, rx, M_PERSONAL, "bs")
        counts[(rel, C_PERSONAL)] += n
    text, n = sub_normalized(text, PERSONAL_BARE_RX, M_PERSONAL)
    counts[(rel, C_PERSONAL)] += n
    for i, rx in enumerate(HOME_RXS):
        text, n = sub_normalized(text, rx, "-Users-arsis-" + M_HOME if i == 2 else M_HOME, "bs")
        counts[(rel, C_HOME)] += n
    if REDACT_OUTSIDE_PROJECT_NAME:  # last, so the more specific path / file-name rules above keep their own markers
        text, n = sub_normalized(text, OUTSIDE_PATH_RX, M_OUTSIDE, "bs")   # whole path tails first
        counts[(rel, C_OUTSIDE)] += n
        text, n = sub_normalized(text, OUTSIDE_RX, M_OUTSIDE)
        counts[(rel, C_OUTSIDE)] += n
        if OUTSIDE_WORD_RX is not None:
            text, n = OUTSIDE_WORD_RX.subn(M_OUTSIDE, text)
            counts[(rel, C_OUTSIDE)] += n
    return text


INBOX_OMITTED = [0]


def copy_sources() -> None:
    shutil.copyfile(ROOT / "docs" / "CONTRACT.md", OUT / "CONTRACT.md")
    shutil.copyfile(ROOT / "board" / "activity.jsonl", OUT / "board-activity.jsonl")
    INBOX_OMITTED[0] = omit_inbox_file(OUT / "board-activity.jsonl")
    dst = OUT / "reviews"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ROOT / "reviews", dst)
    d = OUT / "decisions-and-lessons"
    d.mkdir(exist_ok=True)
    for n in ("DECISIONS.md", "ORCHESTRATOR_DECISIONS.md", "LESSONS.md"):
        shutil.copyfile(ROOT / "memory" / n, d / n)


def export_transcripts() -> None:
    t = OUT / "transcripts"
    if t.exists():
        shutil.rmtree(t)
    ex.render_content = _render
    ex.export = _export
    sys.argv = ["export_prompt_log.py", "--out", "submission/prompt-log/transcripts", "--max-result", "1000000000"]
    DROPPED.clear()
    ex.main()
    idx = t / "INDEX.md"
    keep = [ln for ln in idx.read_text(encoding="utf-8").splitlines() if not any(f"[{n}]" in ln for n in DROPPED)]
    idx.write_text("\n".join(keep) + "\n", encoding="utf-8")


def redact_all() -> collections.Counter:
    counts: collections.Counter = collections.Counter()
    for p in sorted(OUT.rglob("*")):
        if not p.is_file() or (p.parent == OUT and p.name in HAND_WRITTEN):
            continue
        rel = str(p.relative_to(OUT))
        text = p.read_text(encoding="utf-8", errors="surrogateescape")
        new = scrub(text, rel, counts)
        new = new.replace("Unedited except secret redaction.", "Unedited except redactions and format changes listed in the README.")
        if new != text:
            p.write_text(new, encoding="utf-8", errors="surrogateescape")
    for rel, n in OMIT_COUNT.items():
        counts[(rel, C_OMIT)] += n
    if INBOX_OMITTED[0]:
        counts[("board-activity.jsonl", C_INBOX)] += INBOX_OMITTED[0]
    return +counts


def _marker_stats() -> dict:
    marks = {"secret": M_SECRET, "private": M_PRIVATE, "device": M_DEVICE, "third": M_THIRD, "personal": M_PERSONAL, "home": M_HOME,
             "omit": M_OMIT, "outside": M_OUTSIDE, "chris": M_CHRIS, "inbox": M_INBOX, "image": "[image]", "fence": "` ` ` `"}
    stat = {k: [0, 0] for k in marks}
    for p in OUT.rglob("*"):
        if not p.is_file() or p.name in {"README.md", "REDACTIONS.md", "TOOLS.md"} and p.parent == OUT:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for k, m in marks.items():
            n = text.count(m)
            if n:
                stat[k][0] += n
                stat[k][1] += 1
    return stat


def write_readme_block() -> None:
    st = _marker_stats()
    f = lambda k: f"{st[k][0]:,} occurrences in {st[k][1]} files"  # noqa: E731
    if REDACT_OUTSIDE_PROJECT_NAME:
        item7 = (f"\n7. **Outside project name redacted until Chris decides**, marker `{M_OUTSIDE}` ({f('outside')}). The name of one other project of Chris's "
                 "(the one the omitted excerpts in edit 4 came from) is replaced wherever it appears, in any letter case and in these forms: a path segment, "
                 "a file-name slug, prose, a backslash-escaped spelling, a value cut into quoted pieces joined with `+` or spread over whitespace, a tuple or regex whose pieces are separated by punctuation (up to 12 characters), or one character replaced by a wildcard. "
                 "A path that runs through the name (a folder named after it, its sub-folders and the file) is replaced whole by the one marker. Unicode (`\\u`), percent and HTML-entity escapes are not decoded. This is a default, not a verdict: it stays on until Chris says whether "
                 "the name may be shown, and `REDACT_OUTSIDE_PROJECT_NAME` in `evals/finalize_prompt_log.py` is the single switch for it (no entry in the local patterns file can mask the name when the switch is off). "
                 "Where a path or file-name rule from edit 3 already covers the whole path, that rule's marker is used instead.")
        kinds = "eight"
    else:
        item7, kinds = "", "seven"
    item8 = (f"\n{8 if REDACT_OUTSIDE_PROJECT_NAME else 7}. **Chris's own words omitted at his request**, markers `{M_CHRIS}` ({f('chris')}) and `{M_INBOX}` ({f('inbox')}). "
             "Chris's own conversation with the orchestrator and his inbox notes are omitted: the two orchestrator session files (every session that carries his own user turns) are not in `transcripts/` or `INDEX.md`; "
             "in every other file a run of eight or more words copied verbatim from one of his messages is replaced by the first marker (runs that also occur in `MASTER_PROMPT.md` are kept, because he authorized that document); "
             "and the text of each board-inbox event in `board-activity.jsonl` is replaced by the second marker. Shorter quotations and paraphrases of his steering by the agents are not edited.")
    block = f"""<!-- EDITS:START (written by evals/finalize_prompt_log.py from the files as built; do not edit by hand) -->
Nothing else was changed in the transcripts, `reviews/`, `decisions-and-lessons/` or `board-activity.jsonl` (the copies of `docs/CONTRACT.md` and the three memory files get edits 1 and 2 only). Edits {'1 to 4, 7 and 8' if REDACT_OUTSIDE_PROJECT_NAME else '1 to 4 and 7'} apply to every file in this folder except `README.md`, `TOOLS.md` and `REDACTIONS.md`; the counts below are occurrences of each marker in the built folder, so they include any marker string that was already in a source document.

1. **Secret redaction**, marker `<redacted>` ({f('secret')}). Any string matching a `tools/check_secrets.py` pattern is replaced (for `ANTHROPIC_API_KEY=` only the value). The exporter masks `sk-ant-` keys and `ANTHROPIC_API_KEY=` values as it exports and `evals/finalize_prompt_log.py` replaces anything else the scanner matches. No key-shaped value remains in the folder, and values masked at export time were not inspected. `REDACTIONS.md` itemizes the finalize step's replacements by file and class, never by value.
2. **Private-network redaction**, marker `<redacted-private>` ({f('private')}). Tailnet hostnames and labels, any mention of the tailnet suffix, Tailscale 100.64/10 addresses and the `100.x.` prefix, a work email address and its domain (one former-employer name in the bio in the `CONTRACT.md` copy is among them), and regex, backslash-escaped, quote-and-plus-split, one-character-wildcard and punctuation-gapped spellings of all of these (for example a pattern written with a backslash before each dot, a value cut into quoted pieces joined with `+` or into a tuple of quoted pieces, a regex with `*` or `?` between the name and the dot). A bare work-email domain counts as one of these. Names of Chris's computers and phone are replaced by `<device>` ({f('device')}); the phone name is also replaced when it appears without its trailing number. The final check removes backslashes, quotes, `+` and whitespace from every file, folds case, allows up to 12 punctuation characters between the characters of each term, and confirms none of these terms remains.
3. **Personal and third-party redaction until Chris decides**, markers `<third-party name>` ({f('third')}), `<personal file>` ({f('personal')}) and `<home-path>` ({f('home')}). A third party's name is masked; the names of Chris's job-application folders and files, and of his call-prep files, are `<personal file>` (a folder name on its own too); paths under the home directory other than this repo, `~/.claude`, the nvm and Playwright caches and the Claude scratch folder are `<home-path>` (so other local project names and `-Users-arsis-<project>` temp folder names are masked). The local `/Users/<name>` prefix of this repo's own path is left as it is. Prose that merely mentions another project by name is not edited, except the one outside project covered by edit 7.
4. **Content from outside this repo omitted**, marker `<outside-repo file omitted>` ({f('omit')}). The tool result of any command or file read that touches a place under the home directory other than the paths allowed above, or whose result text itself names such a place, is replaced by this marker; the call itself stays. This removes file excerpts from Chris's other local projects (for example a sibling product repo) and directory listings of his job-search folders. If an agent repeated such content in its own reply or reasoning, that text is not edited.
5. **Images shown as `[image]`** ({f('image')}). The agents and reviewers looked at screenshots; the export has no image data, so each image block is the literal text `[image]`.
6. **Four-backtick fences escaped** ({f('fence')}). Tool output is wrapped in a four-backtick fence; any four-backtick run inside it is rewritten to `` ` ` ` ` `` so the markdown stays valid. Non-text tool-result blocks are likewise shown as `[<type>]`, and the first line of each transcript says "Unedited except redactions and format changes listed in the README".{item7}{item8}

Tool results are otherwise at full length (no result was capped). The transcripts are a snapshot taken when this folder was built (the card that built it, T-187, is the last transcript), so a rebuild grows them slightly and counts can shift by a few.
<!-- EDITS:END -->"""
    rd = OUT / "README.md"
    t = rd.read_text(encoding="utf-8")
    new = re.sub(r"<!-- EDITS:START.*?<!-- EDITS:END -->", lambda m: block, t, flags=re.S)
    new = re.sub(r"\b(?:six|seven|eight) kinds of edit were made", f"{kinds} kinds of edit were made", new, count=1)
    rd.write_text(new, encoding="utf-8")


def write_record(counts: collections.Counter) -> None:
    by_pat: collections.Counter = collections.Counter()
    by_file: dict = collections.defaultdict(collections.Counter)
    for (f, name), n in counts.items():
        by_pat[name] += n
        by_file[f][name] += n
    lines = ["# Redaction record", "",
             f"Generated by `evals/finalize_prompt_log.py`. The edits made to the files in this directory are listed in `README.md` (edit classes 1 to {8 if REDACT_OUTSIDE_PROJECT_NAME else 7}). "
             "This file counts the replacements made after export by class and file, and the tool results omitted during export; values are never listed. "
             "The exporter had already masked `sk-ant-` keys and `ANTHROPIC_API_KEY=` values in the transcripts, and those masked values were not inspected. "
             "Secret-class hits found by the scanner were documentation placeholders, test fixture strings (for example fake keys a security reviewer "
             "wrote into a scanner test), bare `-----BEGIN ... PRIVATE KEY-----` header lines with no key body, or exporter markers.", "",
             f"Total replacements and omissions: **{sum(by_pat.values())}** across **{len(by_file)}** files.", "",
             "| Class | Count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in by_pat.most_common()]
    lines += ["", "| File | Class | Count |", "|---|---|---|"]
    for f in sorted(by_file):
        for k, v in by_file[f].most_common():
            lines.append(f"| `{f}` | {k} | {v} |")
    (OUT / "REDACTIONS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# --- self-test -------------------------------------------------------------------------------------------------------
def self_test() -> int:
    """Normalized-view check (D-070): remove backslashes, quotes, backticks, '+' and whitespace, fold case, and fail on any private term
    (and on any generic private shape or secret-scanner pattern). Prints file and class, never a value."""
    bad = 0
    groups = [("work email / tailnet host", PRIVATE_TERM_RX), ("device name", DEVICE_RX), ("third-party name", THIRD_RX),
              ("personal job-application name", PERSONAL_BARE_RX)]
    if REDACT_OUTSIDE_PROJECT_NAME:
        groups.append(("outside project name", OUTSIDE_RX))
    bs_rules = [("private network detail", PRIVATE_RX), ("home path outside repo", re.compile("|".join(r.pattern for r in HOME_RXS[:2]))),
                ("scratch-folder project name", SCRATCH_RX), ("exporter PRIVATE pattern", ex.PRIVATE)]
    if REDACT_OUTSIDE_PROJECT_NAME and OUTSIDE_WORD_RX is not None:
        bs_rules.append(("outside project name, short value (ticker)", OUTSIDE_WORD_RX))
    for p in sorted(OUT.rglob("*")):
        if not p.is_file():
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        view = _VIEW_ALL.sub("", raw)
        nobs = raw.replace("\\", "")
        for label, rx in groups:
            n = len(rx.findall(view))
            if n:
                bad += n
                print(f"SELF-TEST FAIL {label}: {p.relative_to(OUT)} x{n}")
        for label, rx in bs_rules:
            n = len(rx.findall(nobs))
            if n:
                bad += n
                print(f"SELF-TEST FAIL {label}: {p.relative_to(OUT)} x{n}")
        for rx, name in cs.PATTERNS:
            n = len(rx.findall(raw))
            if n:
                bad += n
                print(f"SELF-TEST FAIL {name}: {p.relative_to(OUT)} x{n}")
        n = len(chris_spans(raw))
        if n:
            bad += n
            print(f"SELF-TEST FAIL {C_CHRIS}: {p.relative_to(OUT)} x{n}")
        if p.name == "board-activity.jsonl":
            n = sum(1 for ln in raw.splitlines() if omit_inbox_text(ln)[1])
            if n:
                bad += n
                print(f"SELF-TEST FAIL {C_INBOX}: {p.relative_to(OUT)} x{n}")
    for n in DROPPED:
        if (OUT / "transcripts" / n).exists():
            bad += 1
            print(f"SELF-TEST FAIL transcript with Chris's own turns present: {n}")
    return bad


if __name__ == "__main__":
    require_terms()
    OUT.mkdir(parents=True, exist_ok=True)
    copy_sources()
    export_transcripts()
    c = redact_all()
    write_record(c)
    write_readme_block()
    left = self_test()
    print(f"redacted/omitted {sum(c.values())} item(s) in {len({f for f, _ in c})} file(s); self-test failures {left}")
    sys.exit(1 if left else 0)
