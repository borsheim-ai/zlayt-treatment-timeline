---
name: source-fetching
description: How to spot-check cited URLs when WebFetch isn't available to this reviewer; known blocked hosts
metadata:
  type: reference
---

WebFetch was not in this reviewer's toolset on 2026-11-02, even though the briefs ask for it. Use `curl -sL -A "<Safari UA>"` into a scratchpad dir, strip the HTML with a local `python3 -I` script, grep for the claimed text, and record the substitution in the evidence file. hhs.gov returns 403 to curl; https://web.archive.org/web/2025/<url> works. ABA PDFs are known to block fetches (researcher notes).
