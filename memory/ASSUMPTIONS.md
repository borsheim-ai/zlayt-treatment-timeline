# ASSUMPTIONS (orchestrator writes; workers propose via card notes)

The spec asks us to state what we assume about PI practice. Each entry: the assumption · basis · confidence · what changes if wrong · how we'd check.
Researcher-proposed assumptions (research/ASSUMPTIONS-proposed.md) are merged here after review.

## Run / environment
| ID | Assumption | Basis | Conf. | If wrong | How to check |
|---|---|---|---|---|---|
| A-001 | No usable API key exists during the build; dev runs on `LLM_BACKEND=claude-cli`. | `.env` value is 10 chars (real keys are ~100). | High | We'd add an anthropic-api cross-check eval run (§5.2). | Chris drops a real key in `.env`; STATE notes it. |
| A-002 | Zlayt reviewers have neither Claude Code nor a key; the <5-minute path is Docker/README in cached demo mode. | Spec: "run it from a link, or from your repo in under 5 minutes". | High | Live mode becomes the primary demo; rate limits matter more. | Installer-reviewer runs the README cold (M4). |

## PI practice (seeded by orchestrator; researcher refines with sources in M1)
| ID | Assumption | Basis | Conf. | If wrong | How to check |
|---|---|---|---|---|---|
| A-101 | The paralegal assembles the chronology; the attorney reviews and signs the demand. | Scenario wording ("a paralegal spends hours"). | Med-high | The user and the review UI's audience shift to attorneys. | Discovery Q to the litigation lead (Part 2, area 1). |
| A-102 | A treatment gap is measured between consecutive dates of service across all providers, not per provider. | Appendix C computes gaps across the merged timeline (73 days PT→pain mgmt). | High for this spec | Per-provider gaps would add flags (e.g., PCP never revisited). | Paralegal persona review; T-008 research. |
| A-103 | The chronology feeds the "medical treatment" section of a pre-suit demand letter to a liability carrier. | Scenario ("before every demand letter"). | High | Export format would change (e.g., litigation exhibit). | Litigation-lead persona review. |
| A-104 | "Longer than 30 days" is strict: 30 days is not a gap, 31 is. | Spec wording "longer than 30 days". | High | Boundary flips by one day; unit test pins it. | 29/30/31 unit test; paralegal review. |
| A-105 | Each pasted record carries its date and source on its first line or table row, as the sample does; undated records go to `date_ambiguous`, never silently into the timeline. | Sample format; spec "date arithmetic is a decision". | Med | Ingest heuristics need an LLM split fallback (flagged). | Chaos test with pasted PDF text. |
| A-106 | The export cites each line by provider (as written in the record header) + date of service, with an `[Ex. __ / Bates __]` placeholder the paralegal fills; the tool assigns no numbers. Internal notes cite `record N (provider, date)` per REQUIREMENTS R-EX-4. | No Bates numbers in synthetic records; D-002. | High | Citation format becomes a config field. | Paralegal + litigation-lead review of export; Part 2 discovery Q. |
| A-107 | A per-visit rate is not a billable total until visits attended/billed are itemized. | Appendix C ("PT total is unclear and must not be totaled"). | High | Would allow an estimate line, clearly labeled. | Claims-adjuster review. |
| A-108 | Same-day records from different providers stay separate entries (no merging). | ER + EMS on 2026-01-09 are distinct sources. | High | Timeline would lose per-provider citation. | Golden duplicate-record case. |
| A-109 | Library packet case_lib01 record 3 keeps its recorded extract failure (LLM_FAILED_AFTER_RETRIES: the live model answered with two JSON objects on every attempt); we do not harden the extract prompt to hide it. | A real model failure is the honest demo of "no silent loss"; the UI lists the record under "Records without an entry" with manual entry, and a rerun retries it. | High | Harder extract prompt would need a full re-record and curated rebuild. | Replay of case_lib01 on the fixture backend (errors: record 3). |
- 2026-11-02 (T-133): A history sentence whose source is the patient ('per patient', 'patient reports history of') still raises the prior-condition flag; the paralegal decides. Assumed because a missed prior is costlier than a dismiss; pinned by tests/unit/test_t133_lexicon.py.
