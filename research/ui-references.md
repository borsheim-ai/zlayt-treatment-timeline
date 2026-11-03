# UI references for a legal / claims review tool (T-060 pass 1)

Purpose: ground the review UI in how real products and design systems handle verification, evidence citation, status, density and errors, so the design
brief (`docs/UI_DESIGN_BRIEF.md`) borrows from named, checked sources instead of taste.

**Method and honesty note.** Every URL under "Opened" was fetched in this session and summarized by the fetch tool's small model; I did not see screenshots.
The legal-tech products below publish marketing pages with almost no interface detail, so for them I record only what the page states and mark what I
borrow as an inference. The design systems publish specific rules (sizes, roles, wording), which is where most concrete values come from. Nothing here is
copied product text beyond a few short phrases in quotation marks.

## A. Legal and claims products

| Product | Opened URL | What the page evidences | What it does well (for a review UI) | Borrow |
|---|---|---|---|---|
| EvenUp | https://www.evenuplaw.com/ | Says users can "verify every fact, citation, and exhibit in one click with line-level citations", has an "interactive care timeline", exhibit reordering/redaction, and an AI-draft vs legal-reviewed demand choice. No interface shown. | The promise is one click from a claim to its source line, at line level. It also offers a reviewed tier, which concedes that AI output needs a human gate. | Citation granularity target: the quote, not just the page, one action from the entry. Our quote-in-record highlight (R-RV-9) is the same bar. Do not copy the "AI draft vs reviewed" split: here review is mandatory and per item. (inference) |
| Supio | https://supio.com/ | Medical chronologies "from weeks into days and hours"; AI "finds connections ... treatment gaps". Page says nothing on citations, source linking or review workflow. | Treats treatment gaps as a headline output. It also shows the market gap: no stated verification path. | Our differentiator is the missing piece: visible per-item review state and code-checked citations. Keep gap display factual (days, dates, both records) with no AI "connections". (inference) |
| Filevine | https://www.filevine.com/ | "MedChron" named as a chronology tool (no detail); an AI platform whose actions are described as "traceable to its source"; tasks and deadlines as AI actions. No UI described. | Positions traceability of each AI action as a feature. | A visible "where this came from" affordance on every AI-made item (our `AI-made` badge plus quote). (inference) |
| Litify | https://www.litify.com/ | "Citation-backed questionnaire pre-fills" at intake; dashboards and reporting praised in a testimonial. No layout described. | Applies citation-backing to prefilled fields, i.e. to data a human then confirms. | Pre-filled value + its citation + a confirm action as one unit (our entry row: summary, quote, accept). (inference) |
| CaseMark (page now branded "Para") | https://casemark.com/ | AI colleague that "checks with you before anything leaves the firm"; sign-off requested before a letter goes out; output goes under an attorney's name; record locations quoted (a page number). Review interface not shown. | Puts the human sign-off at the exit point and says so. | Export gate: nothing leaves without accepted items and an explicit confirmation; show the count of unreviewed items at the export button. (inference) |
| Guidewire ClaimCenter (adjuster workbench) | not opened; search results only: https://docs.guidewire.com/cloud/cc/202302/cloudapibf/cloudAPI/topics/141-Framework/03_notes/c_notes.html and https://docs.guidewire.com/cloud/cc/202402/cloudapibf/cloudAPI/topics/111-CCFNOL/05-exposures/c_additional-exposure-endpoints.html | Docs describe a claim Summary, Activities, Notes, Exposures and a work plan; notes attach to a claim, an exposure, a contact or an activity; closing an exposure with open activities is blocked with a message. | The adjuster who reads our output works in a record-first workbench: summary on top, notes attached to the object they concern, open items block closure. | Reviewer notes attach to the item they concern (our flag note, R-RV-2); the export button states what is still open instead of failing silently. Not verified in the UI. |
| Clio | https://www.clio.com/ and /features/... returned HTTP 403 | not opened | | none claimed |
| DocuSign agreement AI | https://www.docusign.com/products/intelligent-agreement-management returned HTTP 404 | not opened | | none claimed |

Gap in the evidence: I found no public screenshots or help-center pages for any PI chronology product in this pass. The next pass could try product demo
videos or help-center articles (EvenUp, Supio, MedChron) to see how they render a citation.

## B. Design systems (rules with concrete values)

| System | Opened URL | Concrete rules found | Borrow |
|---|---|---|---|
| IBM Carbon, data table | https://carbondesignsystem.com/components/data-table/usage/ | Five row sizes: extra small 24, small 32, medium 40 (default), large 48, extra large 64 px; header row matches body row size; 64 px only for two-line rows. Batch-action bar appears on selection and disables row actions. Sorted column shows an arrow, unsorted only on hover. Skeletons instead of spinners for long loads. Row hover always on. | Density scale (32 / 40 / 64 for two-line timeline rows). Skeleton loading. Charges table sort and hover rules. We do NOT adopt batch actions (D-011 withdrew batch accept). |
| IBM Carbon, status indicators | https://carbondesignsystem.com/patterns/status-indicator-pattern/ | Three attention levels (high = act now, medium = progress or acknowledgement, low = ready or changed). Combine icon, shape, color and label; at least three of the four; icon 16 px with 14 px type or 20 px with 16 px; 3:1 contrast for indicators; must survive grayscale; same shape must not carry different meanings. | Review-state chips: `verified`, `needs_review`, `rejected` each get a distinct shape and a text label, so state never depends on color. |
| IBM Carbon, notification | https://carbondesignsystem.com/components/notification/usage/ | Inline (near the item or top of content), toast (about 5 s, non-modal), actionable (one action). Kinds: info, success, warning, error. Inline stays until resolved or dismissed. Keep titles short with no period, one or two short sentences, two lines max, "View more" for longer. Notifications are disruptive, use sparingly. | Banner types and copy limits. Run-level problems are inline and persistent, not toasts. |
| Microsoft Fluent 2, typography | https://fluent2.microsoft.design/typography | Web ramp (Segoe UI): caption 12/16, body 14/20 (regular, strong 600, stronger 700), subtitle 16/22 and 20/26, titles 24/32, 28/36, 32/40. | The type scale in the brief: 12/16, 14/20 body, 16/22, 20/26, 24/32. |
| Microsoft Fluent 2, MessageBar | https://fluent2.microsoft.design/components/web/react/core/messagebar/usage | Intents info/success/warning/error; warnings and errors must carry a link or button; errors listed first when stacked; dismissed but unresolved warnings and errors return next session; errors and warnings use an assertive live region, info and success polite; use a dialog, not a bar, to stop a destructive action. | Banner behaviour: severity order, mandatory action on warnings and errors, assertive vs polite announcement. |
| GOV.UK Design System, error summary | https://design-system.service.gov.uk/components/error-summary/ | Summary at top of main, below breadcrumbs, above h1; focus moves to it automatically; each message links to its field; summary text matches the inline message; heading "There is a problem"; page title prefixed "Error:"; inline message has a visually hidden "Error:" prefix and `aria-describedby`. | Export-blocked and save-failed pattern: a summary that takes focus and links to each offending item (for example "3 items still need review"). |
| GOV.UK Design System, summary list | https://design-system.service.gov.uk/components/summary-list/ | Key / value / action rows; "check answers" use; change link with visually hidden context text; borders kept because they help zoom users; missing info shown as a link to supply it. | Charges table and entry metadata: label / value / action rows with accessible action names ("Dismiss charge $6,240 from Central ER discharge summary"). Pre-export "check your answers" screen. |
| WCAG 2.2 SC 1.4.3 | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | Text 4.5:1; large text (18 pt, or 14 pt bold, about 24 px or 18.5 px bold) 3:1; ratio formula (L1+0.05)/(L2+0.05); thresholds are not rounded. | All contrast figures in the brief are computed with this formula (script in the brief's appendix). |

## C. Cross-cutting findings used in the brief

1. **A claim and its source are one unit.** The only product page that states a citation promise (EvenUp) promises line-level and one click; Litify applies citations to
   prefilled fields. The brief makes the verbatim quote part of the row, with the full record one key away.
2. **Status must not depend on color.** Carbon requires at least three of symbol, shape, color and text; Fluent pairs intent with an announcement level. The brief
   gives each state an icon shape and a word.
3. **Errors summarize and take you there.** GOV.UK and Fluent both put the problem at the top, focus it, and link to the cause.
4. **Density is a setting, not a style.** Carbon ships five row heights and recommends 64 px only for two-line rows; the timeline row is two lines.
5. **Persistent over transient.** Carbon toasts last about five seconds; review states and run warnings must survive, so they are inline.
6. **Human gate at the exit.** CaseMark's page puts sign-off at the point where work leaves the firm; the export step here lists what is unreviewed.

## D. Not verified / open questions

- None of the legal-tech pages show an interface; every "borrow" from them is an inference from marketing text.
- Clio and DocuSign pages could not be opened (403, 404); no claims made.
- Guidewire links came from search results, not opened pages.
- Contrast and type values in the brief are design choices; only the thresholds (WCAG) and the scales (Carbon, Fluent) come from the opened sources.
