# Proposed PI-practice assumptions for memory/ASSUMPTIONS.md

Card: T-008 · Author: researcher (instance A). The orchestrator owns memory/ASSUMPTIONS.md; these are proposals.
Each has evidence (research file + source #) and a confidence. CP / AA / TX = chronology-practice / adjuster-attacks / texas-pi-notes.

| ID | Proposed assumption | Evidence | Confidence | Refines |
|---|---|---|---|---|
| P-01 | The paralegal assembles the chronology; an LNC may interpret clinical meaning on larger cases; the attorney decides what goes in the demand and signs it. | CP src 1, 8, 9 | Medium (vendor + bar blog) | A-101 |
| P-02 | A treatment gap is measured between consecutive dates of service across **all** providers (case-level), and the 30-day threshold comes from the Zlayt spec, not an industry rule — make it configurable. | AA src 1, 4, 5 (no source sets a number); spec | High for "case-level"; threshold is spec-given | A-102 |
| P-03 | The chronology feeds the medical-treatment section of a **pre-suit** demand to the at-fault driver's liability carrier (Texas is an at-fault state). | CP src 5; TX §7 | Medium | A-103 |
| P-04 | Demands are usually sent after MMI/completion; the Rivera records end mid-treatment (rec 9: "Recommend cervical epidural steroid injection", recommended, not performed), so the export must not imply treatment is complete. | CP src 2; record 9 | Medium | new |
| P-05 | Dollar amounts in clinical notes are **billed** charges; the tool must never label the total "damages" or "recoverable" because Texas limits recovery to paid/incurred amounts (Haygood). | TX src 1 | High (primary law) | new |
| P-06 | Surfacing a gap, prior condition or conflict is the tool's job; deciding whether and how to explain it in the letter is the attorney's. Hiding a known weakness costs credibility with adjusters. | CP src 1; AA src 5, 15 | Medium-high | new |
| P-07 | A patient's statement that symptoms began after the collision is history, not a causation opinion; Texas generally requires expert testimony for causation. The tool attributes it ("patient states") and never restates it as fact. | AA src 9, 11 | High (primary law) | new |
| P-08 | Hedged imaging language ("may represent degenerative change; correlate clinically") is equivocal by design; adjusters read it as pre-existing, plaintiffs as aggravation. The tool preserves the hedge verbatim and flags it. | AA src 6, 7, 8 | High | new |
| P-09 | Missed appointments/early discharge are review flags (mitigation is the defendant's burden and outcomes vary), not conclusions. | AA src 13, 14 | Medium | new |
| P-10 | A second, different accident date in any record is material — defense uses it to suggest a different incident (JLG Trucking). Both dates must be surfaced; neither is "corrected". | AA src 10, 17 | High | new |
| P-11 | A prior condition in a **different body region** (rec 3 "Patient reports low back pain in 2023, resolved" vs rec 3 "Persistent neck pain 6/10") is still surfaced; relevance is the paralegal's call. | AA src 2, 15; Appendix C | Medium | new |
| P-12 | Firms cite records by Bates/page; the prototype's record # + verbatim excerpt stands in for that. | TX src 8; CP src 1 | Low-medium (assumption) | new |
| P-13 | Paralegals at PI firms are not covered by a single chronology standard; conventions vary by firm, so the export format should be plain, editable text, not a fixed template. | CP src 9 (no standard found) | Medium | new |
| P-14 | Adjusters check delay from accident to first treatment before anything else. Because records can carry conflicting accident dates (Rivera: rec 7 "Date of accident per intake form: 2026-01-19" vs treatment records dated 2026-01-09 that state no accident date), the tool shows only "first recorded treatment: <earliest date of service>" and never computes a delay from an accident date (D-017). The attorney does that arithmetic. | adjuster-attacks.md A12 (src 1, 16); D-017 | High that adjusters check it; design per D-017 | new |
| P-15 | Scene and mechanism facts (speed, transport, ambulatory, vehicle damage) usually appear only in EMS/police records, and they cut both ways. Surface them as internal-notes flags (D-018/D-001), never as letter text chosen by the tool. | adjuster-attacks.md A13 (src 1) | Medium | new |

Not proposed (insufficient evidence): any number for time spent per chronology or for settlement-value impact of
gaps (only a vendor's "up to 20%" claim, AA/CP src 7).
