# Case library sources (T-052)

Seven synthetic packets in `evals/library/` (`case_lib01_*` to `case_lib07_*`, golden/1 schema), each mirroring one real-world PI scenario.
Rebuild: `python3 research/library_build.py`. Validate: `python3 research/validate_library.py` (runs `evals/golden/check_golden.py` over golden + library,
then a denylist scan for real identifiers).

**Rules followed.** No real name, provider, place, date, amount or case facts were copied. Each packet takes a *pattern* (what the treatment record looks like
and what the other side attacks) and re-expresses it with invented people, providers, towns and numbers. The sources are mostly plaintiff-side blogs and one
news report, so what they say about adjusters is advocacy; I use them for scenario shape, not as legal authority. Where a source was not opened I say so.

| # | Source (URL) | Opened? | Takeaway (one line) | What the packet mirrors | Packet |
|---|---|---|---|---|---|
| S1 | https://www.rmdlaw.com/blog/the-gap-in-treatment-insurance-trap-how-a-delay-can-lower-your-claim-value/ | yes (fetched) | Claims software reads treatment dates without context and treats a gap as a stand-in for severity; an ER-only visit followed by a long pause is scored as a gap, and the reason helps only if the provider charted it. | ER visit, negative x-ray, first follow-up 44 days later; the reason for the delay appears only as the patient's own statement, attributed; new symptom after the gap. | `case_lib01_er_only_then_gap` |
| S2 | https://www.studicata.com/summaries/superior-court-appellate-division-of-new-jersey/nichols-v-duke-linden-llc-2023-ox7g9x (a 2023 New Jersey appellate summary) | **no** (HTTP 403; takeaway from the search-result summary only) | A plaintiff who says a fall aggravated an earlier knee or back condition needs a comparative medical analysis; the defense leans on prior-symptom entries in treating records. Corroborated by S5 (defense expert attributes a future replacement to prior knee surgeries). | Store slip-and-fall, same knee previously operated, imaging that names both acute and prior surgical change, hedged "aggravation ... possible" wording; the tool shows the language and apportions nothing. | `case_lib02_slip_fall_prior_knee` |
| S3 | https://oklahomalawyer.com/soft-tissue-cases-and-chiropractic-care/ | yes (fetched) | Soft-tissue injuries are often treated by chiropractors several times a week for months; adjusters raise "excessive treatment" late, argue "if you're not treating, you're not hurt", and discount subjective pain when imaging is negative. | Tractor-trailer rear-end, plan of 36 visits, "unchanged" pain note, discharge after 31 visits, 28-day near-miss interval, then an MRI with "likely chronic" and desiccation. | `case_lib03_truck_rear_end_chiro` |
| S4 | https://plasticsurgerypractice.com/treatment-solutions/innovations/research/revision-surgery-often-needed-for-facial-dog-bite-injuries-in-children/ | yes (fetched) | In a study of facial dog bites in children, most wounds were closed at first repair, more than three quarters later had scar revision, and about a quarter needed a second or third revision. | Adult facial dog bite: ED repair, plastic-surgery follow-ups with photographs, a planned 8-week return that code still flags as a gap, a revision estimate, a later revision with a surgeon fee. The source is about children; the adult record shape is my assumption. | `case_lib04_dog_bite_scar_revision` |
| S5 | https://valawyersweekly.com/2013/04/01/pedestrian-struck-in-old-town-alexandria-crosswalk-550000-verdict/ | yes (fetched) | A pedestrian with a displaced tibial plateau fracture had ORIF within days, a second surgery about seven months later to remove screws, lasting atrophy and pain, and a defense expert who tied any future knee replacement to prior knee conditions. | Pedestrian in a crosswalk, ORIF, PT, hardware removal about seven months later, hedged future knee replacement, a prior arthroscopy in the history; two flagged gaps. | `case_lib05_pedestrian_orif_hardware` |
| S6 | https://www.thompsoncoe.com/resources/publications/texas-supreme-court-limits-evidence-on-medical-expenses/ | yes (fetched) | The Texas rule limiting medical-expense damages to amounts paid or incurred makes billed-but-not-owed amounts a litigation issue; letters of protection are the contested workaround. | Attorney-referred clinic treating under a letter of protection; billing statement with a balance; imaging bill with charge, adjustment and amount due. Only stated charges are counted (D-019); the rest is unclear and goes to internal notes. The tool decides no legal question. | `case_lib06_lop_billed_vs_adjusted` |
| S7 | https://www.rissman.com/?p=2203 | yes (fetched) | In a slip-and-fall defense result the plaintiff did not obtain earlier records from another jurisdiction, the treating surgeon did not use reasonable-probability language on aggravation, and treatment under letters of protection was questioned. | Fall in an employer's parking lot (patient says not on duty), prior back surgery in another state, outside records requested and not received, MRI hedge, surgeon who declines a causation opinion; all intervals 28 days (no gap flags). | `case_lib07_parking_lot_fall_outside_records` |

## What each packet stresses (coverage map)

| Packet | Gap flags | Pre-existing | Causation / hedge | Amounts | Special |
|---|---|---|---|---|---|
| lib01 | 44 d | none (must_not) | new onset after gap (should) | charge, rate | patient-stated reason is attributed, never the tool's |
| lib02 | 49 d (partial PT records) | prior arthroscopy, degenerative wording | "may reflect both", "possible" | 2 charges, rate | no apportionment |
| lib03 | 35 d, 28-d near-miss | desiccation | "likely chronic" | 2 charges, rate | plan vs actual visits; never "excessive" |
| lib04 | 56 d (planned), 273 d | none | none | charge, estimate, charge | estimate not counted; no permanence |
| lib05 | 49 d, 119 d | prior arthroscopy | "may be needed" | 2 charges, rate | second surgery |
| lib06 | 35 d (statement inside), 56 d | tendinosis (tolerated) | attorney referral | 4 charges, 3 unclear | billed vs adjusted |
| lib07 | none (all 28 d) | degenerative, prior surgery, post-op | "cannot be excluded", no causation opinion | 2 charges | work-adjacent, missing records |

## Assumptions and limits

- Dates, amounts and clinical wording are invented to exercise the tool; none is taken from a source. Dates run into late 2026 and one packet to 2026-09; the golden README says future-dated records are intentional.
- Every `must` flag in a packet is a record-language flag the tool should show, not a finding of fact. `should` and `tolerated` follow the golden README levels.
- S2 was not opened; if it matters for the submission, open the opinion itself before quoting it.
- Search results also surfaced a Manitoba auto-insurance tribunal decision on chiropractic visit counts and Texas cases on letters of protection (e.g. discovery of provider rates); I did not open them and did not use them for any packet.
- Packet names (e.g. Marrowgate, Dr. Pennywhistle) are invented; any resemblance to a real person or provider is unintended.
