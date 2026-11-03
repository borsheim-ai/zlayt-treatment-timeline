# GATE-M3 round 1 — triage (orchestrator)

Pinned commit d0b04bc. Panel: ux-designer (pass), paralegal (changes, verify_quickly 4), accessibility (pass), staff-engineer (changes), chaos-tester (fail), product-manager (fail).
Result: **fail** (2 blockers). Every finding at major or above is mapped to a card or decision; the gate re-runs on the fix commit.

| Severity | Source | Finding | Card / decision |
|---|---|---|---|
| blocker | product-manager | Curated demo answers labelled as AI output (badge, tags, trace, audit) | D-065, T-177 |
| blocker | chaos-tester | A run interrupted by a server restart stays 'running' forever | T-178 |
| major | product-manager | One click accepts a summary the second check disputed | D-066, T-179 |
| major | product-manager, paralegal | Drafted treatment paragraph: no eval; letter lines lack quotes and Bates placeholder | D-067, T-179; scope cut 22 |
| major | product-manager | Stale cut list and spec | SCOPE_CUTS 22-23 added; spec sync with the gate summary |
| major | product-manager | Library flag recall 0.81 vs 1.000 golden | scope cut 23 (reported, not hidden) |
| major | staff-engineer | 375px scroll check cannot fail; rejected-item guard untested; latest.json stale pointer | T-045 round 2 |
| major | chaos-tester | Stale second tab overrides a dismissal; zero-width paste spends model calls; lone surrogate 500 | T-178 |
| minor | ux-designer, accessibility | h1, Undo row under header, Try again focus, announcements, refused-edit wording, 320px controls | T-179 |
| question | chaos-tester | Is a lone-surrogate 500 a blocker? | Decided: fixed as major in T-178; no paste may return 500 |
