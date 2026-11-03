/* "How each answer is checked" (/how-it-works). T-211, D-074. Reachable from the header on every screen (app.js draws the link).
   A plain explanation of the validation ladder for a first-time reader: draft (AI, or prepared answers in the demo) -> code checks -> an independent second AI check -> you decide. What is code and what is AI, with the repo's doc names in text.
   The wording about who drafted follows the same provenance rule as the rest of the app (G.provenance, D-065): a prepared demo never says an AI wrote the answers.
   In demo mode a how-demo-note paragraph says the second-check results are recorded, not run live (T-216). Page contract: G.pages.how = async (ctx) => cleanup. Text only (textContent); no inline style attributes. Test ids: how-page, how-steps, how-step-1..4, how-ladder-img, how-ladder-open, how-code-vs-ai, how-repo, how-back. */
(function () {
  const G = window.G, { h } = G;

  const code = (t) => h("code", {}, t);

  G.pages.how = async function (ctx) {
    await G.healthNow(ctx.signal);
    const p = G.provenance();
    const draft = p.kind === "prepared"
      ? ["Prepared by our team. ", "In this demo the sample answers were written ahead of time, not by an AI model. A real run has an AI model draft a one-line summary of each record and pick the exact words it came from."]
      : p.kind === "recorded"
        ? ["Drafted by an AI model. ", "An AI model drafted a one-line summary of each record and picked the exact words it came from. In this demo those answers were recorded earlier."]
        : ["Drafted by an AI model. ", "An AI model reads each record, drafts a one-line summary and picks the exact words it came from."];
    const back = h("button", { type: "button", class: "btn", "data-testid": "how-back", onclick: () => { if (G.navigated) history.back(); else ctx.go("/"); } }, "‹ Back");      // by a link inside the app: back to where she was; opened directly (history.length also counts the blank tab): to the cases
    const step = (n, head, body) => h("li", { "data-testid": "how-step-" + n }, h("span", { class: "how-n", "aria-hidden": "true" }, String(n)), h("div", {}, h("b", {}, head), " ", body));

    ctx.view.append(h("main", { class: "wrap how-page", id: "main", "data-testid": "how-page" },
      h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("h1", { "data-testid": "page-title" }, "How each answer is checked"),
        h("p", {}, "Nothing reaches your letter until code has checked it, a second AI has checked it, and you have said yes.")), back),
      h("div", { class: "panel" },
        h("ol", { class: "how-steps", "data-testid": "how-steps" },
          step(1, draft[0], draft[1]),
          step(2, "Code checks it.", "Plain code, not AI, confirms the quote is in the record word for word and that every date, amount and number in the line is in the quote. Dates, gaps and totals are worked out by code alone."),
          step(3, "A second AI checks it.", "A different model, with a different prompt, reads the record and the answer. It says it agrees, disputes it or could not check, with a one-line reason. If it disputes, you must confirm you compared the line with the quote."),
          step(4, "You decide.", "You accept, edit or dismiss every item. Code builds the letter from what you accepted, and nothing else.")),
        p.kind !== "live" ? h("p", { class: "how-demo-note", "data-testid": "how-demo-note" }, h("b", {}, "In this demo: "), "the second AI check's results were recorded when the demo was built, not run live. A real model did check each of these answers, and its results are replayed here. Nothing is sent to an AI while you use the demo.") : null,
        h("p", { class: "muted how-note" }, "Each item in steps 2 and 3 shows these three checks under “How this was checked”. The second AI can be wrong too, which is why the last word is yours.")),
      h("div", { class: "panel" }, h("h2", {}, "The checks, as a picture"),
        h("div", { class: "how-fig", tabindex: "0", role: "group", "aria-label": "The validation ladder picture. It scrolls sideways on a narrow screen." },
          h("img", { src: "/validation-ladder.svg", width: "820", height: "600", alt: "Validation ladder. A record goes to a draft. Rung 1, code, checks the quote word for word and every number. Rung 2, a second AI with a different prompt, agrees, disputes or could not check. Rung 3, you accept, edit or dismiss. Code builds the export from accepted items only. Items that fail a check go to a could-not-verify list and never reach the letter.", "data-testid": "how-ladder-img" })),
        h("p", { class: "muted how-note" }, h("a", { href: "/validation-ladder.svg", target: "_blank", rel: "noopener", "data-testid": "how-ladder-open" }, "Open the picture full size"), " (it opens in a new tab).")),
      h("div", { class: "panel", "data-testid": "how-code-vs-ai" }, h("h2", {}, "What is code and what is AI"),
        h("div", { class: "how-cols" },
          h("div", {}, h("h3", {}, "Code only, never AI"),
            h("ul", {}, h("li", {}, "Splitting the pasted text into records"), h("li", {}, "Reading dates, and the days between visits"), h("li", {}, "Finding every dollar amount, saying what kind it is, and adding up the total"),
              h("li", {}, "Checking that a quote is in the record word for word, and that its numbers are in the quote"), h("li", {}, "The wording of each warning, sorting, and building the letter"))),
          h("div", {}, h("h3", {}, "AI, always checked"),
            h("ul", {}, h("li", {}, "Drafting a one-line summary and picking the quote" + (p.kind === "prepared" ? " (prepared by our team in this demo)" : "")), h("li", {}, "The second check that reads each answer against the record"),
              h("li", {}, "Spotting wording the other side could use, which code then checks and you decide"))))),
      h("div", { class: "panel", "data-testid": "how-repo" }, h("h2", {}, "Where to read more in the repo"),
        h("ul", { class: "how-repo" },
          h("li", {}, code("docs/LLM_VS_CODE.md"), ": every step, whether it is code or AI, and how it is checked."),
          h("li", {}, code("app/llm/prompts/"), ": the second check's prompts, for example ", code("judge_faithfulness_v1.md"), " and ", code("judge_amount_class_v1.md"), "."),
          h("li", {}, code("app/backend/grounding.py"), ": the word-for-word and number checks. ", code("app/backend/judges.py"), ": how the second AI's answer becomes a verdict."),
          h("li", {}, code("evals/"), ": the golden cases and reports that measure both checks."),
          h("li", {}, code("memory/ORCHESTRATOR_DECISIONS.md"), ": D-065 (prepared answers are never called AI output) and D-066 (a disputed line needs your comparison).")),
        h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: "/", "data-testid": "how-home" }, "Back to your cases")))));
    ctx.setTitle("How each answer is checked");
    return undefined;
  };
})();
