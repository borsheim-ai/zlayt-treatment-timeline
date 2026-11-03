#!/usr/bin/env python3
"""Secret scanner. `--staged` checks what is staged for commit (used by git-guard and the native pre-commit hook);
default scans tracked files. Exit 1 with a list of hits if a key-shaped string or an env file would enter git.
Never prints the secret itself.

Round 2 (T-006 security review): NUL-separated file names (spaces/unicode safe), renames/copies included,
no file-level allowlist (patterns are written so they don't match themselves; tests build keys by concatenation),
broader key patterns and env-file names, non-empty ANTHROPIC_API_KEY assignments.
Residual risk: a key split across lines or encoded (base64) is not detected.
"""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}"), "Anthropic key"),
    (re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9]{32,}\b"), "OpenAI-style key"),
    (re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"), "Hugging Face token"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), "GitHub token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b"), "GitHub fine-grained token"),
    (re.compile(r"\bxox[abposr]-[A-Za-z0-9\-]{10,}\b"), "Slack token"),
    (re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"), "Google API key"),
    (re.compile(r"\b[rs]k_live_[0-9A-Za-z]{20,}\b"), "Stripe live key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?[A-Za-z0-9/+]{40}"), "AWS secret key"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "JWT"),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9_\-\.=]{30,}"), "Bearer token"),
    (re.compile(r"-----BEGIN ((RSA|EC|DSA|OPENSSH|PGP|ENCRYPTED) )?PRIVATE KEY( BLOCK)?-----"), "private key"),
    # a non-empty, non-placeholder value assigned to ANTHROPIC_API_KEY
    (re.compile(r"ANTHROPIC_API_KEY\s*[=:]\s*['\"]?(?!['\"]?\s*$)(?!<|\$|your|changeme|xxx|\.\.\.|None|null|os\.|getenv|environ)[^\s'\"#]{6,}"),
     "ANTHROPIC_API_KEY with a value"),
]
ENV_NAME = re.compile(r"(^|/)(\.env(\..+)?|\.envrc|[^/]*\.env)$", re.I)


def git(*args) -> bytes:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True)
    if r.returncode != 0 and args[0] != "show":
        print(f"check_secrets: BLOCKED (git {' '.join(args[:2])} failed: {r.stderr.decode(errors='replace').strip()[:200]})")
        sys.exit(1)  # fail closed: never report 'ok' when we could not list files
    return r.stdout


def main(argv):
    staged = "--staged" in argv
    if staged:
        raw = git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT")
    else:
        raw = git("ls-files", "-z")
    files = [f for f in raw.decode("utf-8", "surrogateescape").split("\0") if f]
    hits = []
    for f in files:
        if ENV_NAME.search(f) and not f.lower().endswith(".env.example"):
            hits.append(f"{f}: env file must never be committed")
            continue
        if staged:
            data = git("show", f":{f}")
        else:
            p = ROOT / f
            data = p.read_bytes() if p.is_file() else b""
        if data[:2] in (b"\xff\xfe", b"\xfe\xff"):
            text = data.decode("utf-16", "replace")
        elif b"\0" in data[:8000]:
            continue  # binary
        else:
            text = data.decode("utf-8", "replace")
        for i, line in enumerate(text.splitlines(), 1):
            for pat, label in PATTERNS:
                if pat.search(line):
                    hits.append(f"{f}:{i}: {label} (value redacted)")
    if hits:
        print("check_secrets: BLOCKED\n" + "\n".join(hits))
        return 1
    print(f"check_secrets: ok ({len(files)} file(s) scanned{' staged' if staged else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
