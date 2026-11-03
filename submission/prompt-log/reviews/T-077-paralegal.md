# T-077 review: paralegal-reviewer (research/case-library-sources-v2.md, commit bb26bf0)

**Verdict: changes.** The 17 patterns are mostly what a Texas PI paralegal sees (second accident, priors, EOBs vs bills, cloned notes, scanned chiro notes, ER-missed concussion, conclusory causation letters), and the read-depth labelling is honest. I fetched 11 source URLs. Nine opened and matched the doc's claims. Two (the NJ Rodriguez PDF and the studicata Hampton page) returned 403 to me, as the doc says for Hampton. The blocking issue is synthetic safety. The doc says the real names must go on the denylist before any packet is built, and nothing has done that. The list the doc gives is also incomplete.

## What I opened and found
| Source | Result |
|---|---|
| P1 JLG v. Garza, txcourts PDF | Confirmed: ortho visit 5 days after crash 1, about 11 weeks PT, second crash with ambulance and hard collar, first MRI after crash 2, fusion in 2012. The treating doctor's July note had no other history (cross-exam). The record features follow from the opinion. |
| P5 In re Central Oregon, txcourts PDF | Confirmed: two prior accidents, memory complaints, tailbone surgery. The court's six billing-discovery items are confirmed, but they are not the "six ledger columns" the doc claims (finding 5). |
| P10 Steinkamp, PubMed | Confirmed: 104,456,653 notes, 50.1%, 33.0% to 54.2%, 45.9% from a different author. |
| P11 ElGhrably, nature.com | Confirmed: 44 errors in 32 sets, 19 later corrected, 3 consent forms. |
| P12 Rodriguez-Vera, PMC | Confirmed: 18 of 117 (15%) unclear, worse in surgical departments. |
| P16 Lewis Brisbois write-up | Confirmed, including the ortho-vs-PCP contradiction and the photos. The doc correctly leaves out the drug-use facts. |
| P4 Chiv v. Figueroa, hallapproved | The Spanish-translation and counteraffidavit holdings are confirmed. The case says nothing about record content (finding 2). |
| P6 Gunn v. McCoy, dallas-appellate blog | Date June 15, 2018 and the subrogation-agent holding confirmed. The blog calls it a "medical malpractice case". |
| P3 Hills v. Donis, mdjwlaw.com | Holding confirmed. The "withdrawn and substituted 2021-02-11" claim is not on the page (finding 3). |

## Judgement on the four asks
1. **Realistic for PI practice, features follow from the source.** Mostly yes. Gaps are in findings 2, 4 and 5.
2. **Summary-level claims marked.** Source read depth is marked on every pattern. The "Record features" lines are not marked as source-derived or inferred (finding 2).
3. **Synthetic-safety notes.** The six rules are sound. The enforcement is missing (finding 1).
4. **lib08 to lib15 cover D-042.** On paper, yes (coverage map). Three features rest on premises the table doesn't state (finding 6).

```json
{"card": "T-077", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "research/case-library-sources-v2.md at commit bb26bf0; cross-read with research/validate_library.py, board cards T-077/T-079, memory/ORCHESTRATOR_DECISIONS.md D-042/D-043; no app run (research card)",
 "exercised": [
  "Read personas/paralegal.md, the whole v2 doc, validate_library.py, board.py show T-077/T-078/T-079, D-042 and D-043",
  "Fetched with curl and pdftotext: txcourts Garza (130978.pdf) and Central Oregon (200945pc.pdf), PubMed 36156143, mdjwlaw.com Hills v. Donis page, hallapproved.com Chiv v. Figueroa, legal500.com Lewis Brisbois write-up, nature.com 6702590, PMC1279250, dallas-appellate.blogspot.com Gunn v. McCoy",
  "403 on njcourts.gov Rodriguez PDF and studicata.com Hampton page (matches the doc's own note for Hampton)",
  "Grepped the fetched text for each numeric and holding claim the doc makes",
  "Checked evals/library/case_lib03 format and the validate_library.py DENYLIST"],
 "verdict": "changes",
 "scores": {"realism_for_PI_practice": 4, "source_fidelity": 4, "summary_level_claims_marked": 3, "synthetic_safety_enforcement": 2, "d042_coverage": 4},
 "findings": [
  {"severity": "major", "title": "Denylist for v2 real names is not in place, and the doc's list is incomplete and unsafe as written",
   "evidence": "Doc rule 2 (case-library-sources-v2.md lines 24-26): 'the real case names in this file (e.g. Garza, Broussard, Rodriguez) must be added to that denylist before any v2 packet is built.' research/validate_library.py:13-15 DENYLIST still holds only v1 terms ('Nichols', 'Duke Linden', 'Haygood', ... 'Cutch'); none of Garza, JLG, Guevara, Ferrer, Hills, Donis, Chiv, Figueroa, Broussard, Gunn, McCoy, Hampton, Miskell, Wal-Mart, Brisbois is present. The match is a case-sensitive word-boundary regex (validate_library.py:33), so 'GARZA' or 'garza' would pass. T-079 (the packet builder) is status ready with a note telling someone to do this.",
   "why_it_matters": "A real captioned party, doctor or county in a synthetic packet is exactly the leak the data rule forbids. The only guard is the denylist, and the doc hands the builder three example names. Garza, Rodriguez, Figueroa and Hills are also very common Texas surnames, so a blanket ban will collide with the invented Spanish-language names lib09 needs unless the builder knows to avoid them.",
   "fix": "Researcher adds an explicit 'Denylist additions' block to the v2 doc and updates validate_library.py (case-insensitive) before T-079 starts. Include distinctive tokens: JLG, Pechero, Zapata, Guevara, Ferrer, Donis, Chiv, Figueroa, Broussard, 'Central Oregon', McCoy, Miskell, Wal-Mart, Brisbois, 'Harris County'. For common surnames (Garza, Rodriguez, Hills, Gunn, Hampton) ban them as invented-name choices and state that in the doc.",
   "acceptance_test": "A unit test builds a temp packet containing each listed token in mixed case and asserts validate_library.py exits non-zero for each; the test also greps the v2 doc for capitalised case-caption names and fails if any is missing from DENYLIST."},
  {"severity": "minor", "title": "'Record features' mix source-derived and inferred content, and two sources do not support the record shape at all",
   "evidence": "P4 (hallapproved page): the holdings are about a deposition lacking a certified translation and a stricken counteraffidavit; the page has nothing on 'history via interpreter' charting. P17 Hampton v. Miskell: the opinion is about a reconstructionist's testimony, and the cite has no court district or docket number; studicata page returns 403 to me (curl http 403, 1398 bytes). P5 'intake forms answering prior accidents: none' is not in In re Central Oregon (grep of the pdftotext output finds only the discovery list, the two priors and the memory testimony). The doc's read-depth note says only that the PI framing of the medical studies is 'ours'.",
   "why_it_matters": "A builder reading 'Record features' will treat them as documented real-world shapes. The adjuster-style ones are plausible, but for a paralegal reviewing the library 'real-world pattern' should mean the source says it. Inferred ones need a label.",
   "fix": "Tag each Record-features line 'from source' or 'our inference'. Give Hampton a full citation (court, district, docket or WL cite) or replace it with a retrievable source. Say plainly that P4 and P17 support only the scenario theme.",
   "acceptance_test": "Every 'Record features:' bullet carries one of two tags, and every case citation includes court, district and docket or reporter cite; a grep-based check passes."},
  {"severity": "minor", "title": "Hills v. Donis 'withdrawn and substituted 2021-02-11' is not supported by the cited page",
   "evidence": "Doc P3: 'memorandum op. 2020-01-14, withdrawn and substituted 2021-02-11'. The cited mdjwlaw.com page is a newsbrief dated '11 Feb 2020' that cites 'Hills v. Donis, No. 14-18-00566-CV, 2020 WL 206187 ... Jan. 14, 2020, no pet. h.' and never says 'withdrawn' or 'substituted' (searched the fetched HTML). Looks like a 2020/2021 slip, or an unsourced claim.",
   "why_it_matters": "If the memorandum opinion was withdrawn, the write-up may describe a superseded holding. If it was not, the doc misstates the record. A paralegal would not cite either without checking.",
   "fix": "Either cite the substituted opinion with its own date and URL, or delete the sentence. Re-read the opinion itself, since the doc admits it was not opened.",
   "acceptance_test": "The P3 entry names the opinion date and the URL of the opinion that carries that date, and no claim in it lacks a retrievable page."},
  {"severity": "minor", "title": "P7/lib12 (defense IME) and P16 assume documents a demand-stage packet usually does not contain",
   "evidence": "P7 source is a New Jersey trial-evidence ruling, and lib12 is 'Defense IME with symptom-magnification wording'. P16's contradiction ('denying back and neck pain to her primary care doctor') was found by defense subpoena per the Lewis Brisbois text ('Lewis Brisbois subpoenaed post-accident records from the hospital, which showed...').",
   "why_it_matters": "The tool prepares a pre-suit demand chronology. A defense medical exam is a post-suit event in Texas, and the PCP record that contradicts the ortho note is often not in the paralegal's file at all. The tool can still process both, but the packet should say which stage it simulates so a reviewer does not mistake it for a typical demand file.",
   "fix": "Label lib12 as litigation-stage, or recast it as a carrier records-review/peer-review letter or a treating-provider FCE note. Say in lib13 that the PCP note arrived from a records request.",
   "acceptance_test": "Each proposed packet row states the case stage (pre-suit demand or post-suit) and how each cross-provider record entered the file."},
  {"severity": "minor", "title": "P5 claim that provider ledgers 'match the six categories exactly' overstates the opinion",
   "evidence": "In re Central Oregon (pdftotext lines 54-59): '(1) total billed charges; (2) adjustments or write-offs; (3) the amount paid to the provider and by whom; (4) outstanding balances; (5) copies of any contracts for services with ... health-insurance carrier; and (6) any letters of protection, contracts, liens, or other guarantees'. The doc's ledger columns are 'billed, adjusted, paid, payer, balance, LOP/lien'; item 5 is copies of contracts, not a column.",
   "why_it_matters": "lib11 and the billing-analysis card (T-083) will build six columns and call them the court's list. Item 5 is a document request, so the ledger packet would imply the contracts are on the page.",
   "fix": "Reword to 'ledger columns derived from items 1-4 and 6; item 5 (carrier contracts) is a separate document the packet may reference but not reproduce'.",
   "acceptance_test": "The P5 text distinguishes the four ledger-derivable categories from the contract-copy request."},
  {"severity": "minor", "title": "Three D-042 features are credited to packets whose premises do not carry them",
   "evidence": "Coverage map: date-convention suggestion -> 'P9 (assumption), P12'; but the lib09 and lib14 premises in the packet table mention no DD/MM date with day <= 12. Dismissal-pattern learning -> P8/lib12, but lib12's premise does not say it supplies enough credibility flags to dismiss. P16 notes 'estimate is not a charge, D-019', yet lib13's premise ('Copied ROS denies the complaint the ortho charts the same week') omits the surgical cost estimate.",
   "why_it_matters": "T-079 AC1 lists specific fixtures. If the premise lines are all the builder reads, these features get no test packet.",
   "fix": "Add a 'must contain' column to the packet table, e.g. lib09: one form dated 03/06/2026 day-first plus 14/05/2026; lib12: at least 4 credibility sentences (2 clean, 2 mixed) across 3 dates; lib13: a surgical estimate line.",
   "acceptance_test": "Each lib08-lib15 row lists its D-042 features, and T-079's expected.json for each packet asserts them."},
  {"severity": "nit", "title": "P6 source is a medical-malpractice case, and statute currency is not stated",
   "evidence": "dallas-appellate blog: 'The central issue in this medical malpractice case was...' for Gunn v. McCoy. The doc's Texas authorities (2007-2022) do not say whether CPRC 18.001 text was checked for later amendments.",
   "why_it_matters": "Low risk, since the doc says the opinions are only for scenario shape. A paralegal would still want to know before quoting.",
   "fix": "Add 'health care liability claim' to P6 and one line saying current statute text was not checked.",
   "acceptance_test": "The P6 entry names the case type and the assumptions section has the currency line."}
 ],
 "whats_right": [
  "Read depth is stated per source ('full text' vs 'summary'), the 403 pages are admitted, and the P16 drug-use facts are deliberately left out.",
  "Verified numbers match the sources: Garza interval facts, Central Oregon discovery list, Steinkamp 50.1%, ElGhrably 44 errors in 32 sets, Rodriguez-Vera 15% of 117.",
  "Synthetic-safety rules 1-6 (pattern not facts, dates shifted, features recombined across two patterns, SYNTHETIC banner) are the right design."],
 "questions_for_chris": []}
```
