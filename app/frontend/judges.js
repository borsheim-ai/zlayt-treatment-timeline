/* "How the AI was checked" panel (T-082, D-042). Reads GET /cases/{token}/judges: items the second AI check judged, agreed / objected / unavailable counts,
   each objection with its fixed-sentence reason, and where the code checks and the AI read an item differently. Every row links to the item's stepper.
   This is a report on the AI's drafts, never a verdict on the case: the label says so. Counts are the server's; nothing is added here.
   Placement (round 2): mounted by ZL.stepper.mountCase right under the case checks, collapsed by default to ONE summary row that carries the signal
   ("16 checked, 13 agreed with the draft, 3 questioned"). One row per item: an item the AI objected to AND that appears under "disagreements" is merged
   into one row with chips. Model, prompt and reason-code internals sit in closed "Technical details".
   Rows carry data-target-item (not data-item-id) so the review keyboard flow and the panels' j/k walk do not treat them as review items. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let cache = null, wasOpen = false, gate = null;   // gate: what the export gate lists, {jnr: [item ids with a JUDGE_NOT_RUN blocker], code: [code-check blockers on the paralegal's wording]}; null until the case trace has loaded

  const DIS = {
    judge_objects: "Code checks passed, the AI objected",
    judge_agrees_code_flags: "Code raised a doubt, the AI found it supported",
    sources_disagree: "The phrase list and the AI disagree",
  };
  // Who actually answered (T-204 r3): on a prepared item a flag disagreement is between the phrase list and the prepared answers; a judge disagreement is the second AI check. A live item keeps "the AI".
  const DIS_PREP = {
    judge_objects: "Code checks passed, the second AI check objected",
    judge_agrees_code_flags: "Code raised a doubt, the second AI check found it supported",
    sources_disagree: "The phrase list and the prepared answers disagree",
  };
  const prepDis = (x) => ZL.stepper.preparedFor(x.item_id);
  const disLabel = (x) => (prepDis(x) ? DIS_PREP : DIS)[x.type] || x.type;
  const whoSaid = (x) => (!prepDis(x) ? "the AI" : x.type === "sources_disagree" ? "the prepared answers" : "the second AI check");
  const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1);
  const RS = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const KIND = { entry: "Entry", amount: "Amount", flag: "Flag" };
  const READING = {   // the verdict in words that name who disagrees with whom
    partially: "The AI found the draft only partly supported by the quote.",
    unsupported: "The AI found the draft not supported by the quote.",
    disagrees: "The AI reads this differently from the draft.",
  };
  const TODO_COMPARE = "Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.";   // same fixed sentence as the item stepper (COMPARE_BY_HAND)
  const TODO_AMOUNT = "Compare the amount with the quote yourself. Accept it as a charge, leave it unclear, or dismiss it.";
  const TODO_UNCHECKED = "Read it yourself, then accept, edit or dismiss it. The AI did not give an answer you can rely on.";   // item not decided yet
  const TODO_PENDING = "Run the second check again first. If you accept it before the second check has run, the export is blocked until it does.";   // undecided item with no AI answer
  const TODO_BLOCKED = "The second AI check did not run on this item, so it can't go in the letter yet. Run the second check again; if it still cannot answer, dismiss the item.";   // accepted/edited: same sentence as the export gate
  const plural = (n, one, many) => n + " " + (n === 1 ? one : many);

  function title(id) { const cue = ZL.stepper.cue(id); return ZL.stepper.label(id) + (cue ? " · " + cue : ""); }
  // Which items block the export is the GATE's answer (the blockers of GET /trace), never a guess from the item's review status: D-045(b) exempts summaries the paralegal
  // wrote or edited from the judge, but not from the code checks, so an edited item can lack a judge answer and be ready, or fail a code check and block. gate is null while the trace is loading.
  function reviewOf(it) { const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return (f && f.item.review_status) || (it.unres || {}).review_status; }
  const gateSet = (tr) => {
    const g = ((tr || {}).steps || []).find((x) => x.id === "export_gate"); if (!g) return null;
    const bl = g.blockers || [];
    return { jnr: bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").map((b) => b.item_id), noAnswer: bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN" && b.rerun_no_answer === true).map((b) => b.item_id), code: bl.filter((b) => ZL.stepper.isCodeBlocker(b)), verdict: (tr && tr.verdict) || null };
  };
  const codeIds = () => new Set(((gate && gate.code) || []).map((b) => b.item_id));
  const unchecked = (it) => !!(it.unres && !it.rej && it.unres.verdict === "unavailable");
  const blocking = (it) => unchecked(it) && !!gate && gate.jnr.includes(it.id);
  // T-136 r3: an accepted re-picked quote under the AI's own summary is blocking too, but a rerun cannot clear it: only her own summary wording does (D-058).
  const held = (it) => blocking(it) && !!ZL.stepper.isHeld && ZL.stepper.isHeld(it.id);
  const heldFinal = (it) => held(it) && gate.noAnswer.includes(it.id);     // a rerun already gave no answer on this quote: only her own summary clears it
  // The paralegal wrote or edited this wording: no second check applies (D-045 b), and the gate does not list it.
  const humanWording = (it) => { if (!unchecked(it) || blocking(it)) return false; const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return reviewOf(it) === "edited" || !!(f && f.item.ai_drafted === false); };
  const waiting = (it) => unchecked(it) && !blocking(it) && !humanWording(it) && reviewOf(it) === "pending";   // undecided and unchecked: a rerun covers it
  // A flag the AI suggested and the checks did not confirm sits in the Could-not-verify tray: nothing can be accepted there, so the row neither shows a decision nor says "accept".
  const trayFlag = (id) => { const c = ZL.state.get().case; return !!(c && (c.tray || []).some((t) => t.id === id && t.kind === "flag")); };
  const TODO_TRAY = "Nothing to accept here. It is left out of the letter. If it matters, open the record and check it yourself.";
  function links(id) {
    const t = title(id);
    return el("div", { class: "zs-todo-btns" },
      el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-judge-goto", "aria-label": "Go to item " + t, onclick: () => ZL.stepper.goto(id) }, "Go to item"),
      el("button", { type: "button", class: "btn", "data-testid": "btn-judge-steps", "aria-label": "Why this status: " + t, onclick: () => ZL.stepper.openTrace(id) }, "Why this status"));
  }
  const noCode = (t) => String(t || "").replace(/\s*\([A-Z]{3,}(?:_[A-Z]+)*\)\s*$/, "");   // the closed reason code lives in Technical details
  const chip = (text, cls) => el("span", { class: "zs-chip " + (cls || "") }, text);

  // One item, once: group the three server lists by item id.
  function byItem(d) {
    const m = new Map();
    const get = (id, kind) => { if (!m.has(id)) m.set(id, { id, kind, rej: null, unres: null, dis: [] }); return m.get(id); };
    (d.rejections || []).forEach((r) => { get(r.item_id, r.kind).rej = r; });
    (d.unresolved || []).forEach((r) => { get(r.item_id, r.kind).unres = r; });
    (d.disagreements || []).forEach((x) => { get(x.item_id, x.kind).dis.push(x); });
    return Array.from(m.values());
  }

  function techDetails(it) {
    const r = it.rej || it.unres, bits = [];
    const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), String(v)));
    if (r) bits.push(kv("reason code", r.reason_code), kv("model", r.model), kv("prompt", r.prompt_version), kv("your decision", RS[r.review_status] || r.review_status));
    it.dis.forEach((x) => bits.push(kv("kind of disagreement", x.type), kv("resolution", x.resolution), kv("the code check said", x.code_says), kv(whoSaid(x) + " said", noCode(x.judge_says))));
    const nodes = bits.filter(Boolean);
    if (!nodes.length && !(r && r.response_raw)) return null;
    return el("details", { class: "zs-more", "data-testid": "judge-row-tech" }, el("summary", { "aria-label": "Technical details: " + title(it.id) }, "Technical details"), nodes.length ? el("p", { class: "zs-ev" }, nodes) : null,
      r && r.response_raw ? el("pre", { class: "zs-pre" }, r.response_raw) : null);
  }

  function row(it, testid) {
    const r = it.rej, u = it.unres, chips = [], mine = humanWording(it), tray = trayFlag(it.id);
    if (tray) chips.push(chip("Left out of the letter"));
    else if (r) chips.push(chip("AI objected", "zj-chip-bad"));
    else if (mine) chips.push(chip("Edited by you, not AI-checked"));
    else if (u) chips.push(chip(u.verdict === "unavailable" ? "AI did not check" : "AI could not decide", "zj-chip-bad"));
    it.dis.forEach((x) => { if (!(r && x.type === "judge_objects")) chips.push(chip(disLabel(x))); });   // "the AI objected" is already the first chip
    const decision = tray ? null : (r || u || it.dis[0] || {}).review_status;
    let why = null;
    if (r) why = el("p", { class: "zs-why" }, el("strong", {}, (READING[r.verdict] || ZL.stepper.verdictWord(r.verdict) + ".") + " "), r.rationale || "");
    else if (mine) why = el("p", { class: "zs-why" }, "You edited this item, so it is your wording and does not need the second check.");
    else if (u) why = el("p", { class: "zs-why" }, u.verdict === "unavailable" ? "The second check did not answer, so no AI judge looked at this item." : "The second check could not decide.");
    const blk = blocking(it);
    if (blk) { chips.push(chip("Blocks the export", "zj-chip-bad")); why = null; }
    const todo = tray ? TODO_TRAY : heldFinal(it) ? ZL.stepper.HELD_NO_RERUN(1, ZL.stepper.preparedFor(it.id)) : held(it) ? ZL.stepper.HELD_CAN_RERUN(1, ZL.stepper.preparedFor(it.id)) : blk ? TODO_BLOCKED : mine ? null : waiting(it) ? TODO_PENDING : r || u ? (u && !r ? TODO_UNCHECKED : it.kind === "amount" ? TODO_AMOUNT : TODO_COMPARE) : null;
    return el("li", { class: "zj-row", "data-testid": testid, "data-target-item": it.id },
      el("div", { class: "zs-head" }, el("span", { class: "zs-label", "data-testid": "judge-row-title" }, title(it.id)), el("span", { class: "zs-kind" }, KIND[it.kind] || it.kind)),
      el("p", { class: "zj-chips" }, chips, decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
      why,
      tray ? null : it.dis.map((x) => el("p", { class: "zs-ev" }, el("span", { class: "zs-k" }, "The code check said: "), x.code_says || "", el("br"), el("span", { class: "zs-k" }, cap(whoSaid(x)) + " said: "), noCode(x.judge_says))),
      todo ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), todo) : null,
      held(it) ? el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-write-summary-case", "aria-label": "Write the summary for " + title(it.id), onclick: () => ZL.stepper.editItem(it.id) }, "Write the summary")) : null,
      links(it.id), techDetails(it));
  }
  // An edited or hand-written item whose wording fails a code check: the row is the gate's blocker as the server wrote it (reason, fix sentence), with an Edit action.
  function wordingRow(b) {
    const id = b.item_id, t = title(id), decision = reviewOf({ id });
    return el("li", { class: "zj-row", "data-testid": "judge-wording", "data-target-item": id },
      el("div", { class: "zs-head" }, el("span", { class: "zs-label", "data-testid": "judge-row-title" }, t), el("span", { class: "zs-kind" }, KIND.entry)),
      el("p", { class: "zj-chips" }, chip("Blocks the export", "zj-chip-bad"), decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
      el("p", { class: "zs-why" }, el("strong", {}, ZL.stepper.wordingLead(id) + " "), b.why || ""),
      b.next_action && b.next_action.text ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), b.next_action.text) : null,
      el("div", { class: "zs-todo-btns" },
        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-judge-edit", "aria-label": ZL.stepper.wordingEditText(id, b.next_action) + " for " + t, onclick: () => ZL.stepper.wordingFix(id, b.next_action) }, ZL.stepper.wordingEditText(id, b.next_action)),
        el("button", { type: "button", class: "btn", "data-testid": "btn-judge-goto", "aria-label": "Go to item " + t, onclick: () => ZL.stepper.goto(id) }, "Go to item"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-judge-steps", "aria-label": "Why this status: " + t, onclick: () => ZL.stepper.openTrace(id) }, "Why this status")));
  }
  const CAP = 5;   // rows shown per group before "Show the other N"; the full list is one click away
  const list = (testid, label, rows, mk, empty, extra) => el("section", { class: "zj-group", "data-testid": testid, "aria-label": label },
    el("h3", {}, label + " (" + plural(rows.length, "item", "items") + ")"), extra || null,
    rows.length ? el("ul", { class: "zj-list" }, rows.slice(0, CAP).map(mk)) : el("p", { class: "rv-empty" }, empty),
    rows.length > CAP ? el("details", { class: "zs-more", "data-testid": "judge-more" }, el("summary", {}, "Show the other " + (rows.length - CAP)), el("ul", { class: "zj-list" }, rows.slice(CAP).map(mk))) : null);

  function tile(n, label) { return el("li", { class: "zj-tile" }, el("strong", { class: "zj-n" }, String(n)), el("span", { class: "zj-l" }, label)); }

  // Built from the server's totals and from the gate; each kind of item is named once, and only items the gate lists carry the blocking words ("blocks export"). An edited item the
  // gate does not hold is counted as "edited by you, not AI-checked" and never as blocking, so the panel and the rail ("Export blocked by N") agree.
  function summaryText(d) {
    const t = d.totals || {}, bits = [], n = t.items_judged || 0;
    const nb = ((gate && gate.jnr) || []).length, nc = ((gate && gate.code) || []).length, cids = codeIds();
    const rest = byItem(d).filter((i) => unchecked(i) && !blocking(i) && !cids.has(i.id));
    const nEdit = gate ? rest.filter(humanWording).length : 0, nWait = gate ? rest.length - nEdit : t.unavailable || 0;
    // T-166 F10: "all agreed" is said only when nothing is left that the second check did not answer (a check that did not run, or an edit it never read: the edit has no judge row of its own, so it is read
    // from the case); otherwise agreed and not-available are counted apart
    const cs = ZL.state && ZL.state.get().case, nUnread = cs ? [].concat(cs.entries || [], cs.undated_entries || []).filter((i) => i.edited && (i.reasons || []).includes("JUDGE_UNAVAILABLE")).length : 0;
    if (!t.unsupported && !t.unsure && !t.unavailable && !nb && !nc && !nWait && !nEdit && !nUnread) bits.push("checked " + n + ", all agreed with the draft");
    else {
      bits.push(n + " checked", (t.supported || 0) + " agreed with the draft");
      if (t.unsupported) bits.push(t.unsupported + " questioned");
      if (t.unsure) bits.push(t.unsure + " undecided");
      if (nb) bits.push(nb + " not checked, blocks export: " + nb);
      if (nWait) bits.push(nWait + " not checked");
      if (nEdit) bits.push(nEdit + " edited by you, not AI-checked");
      if (!nEdit && nUnread) bits.push(nUnread + " edited by you, second check not available");
      if (!nb && !nWait && !nEdit && t.unavailable && !nc) bits.push(t.unavailable + " not checked");
    }
    if (nc) bits.push(nc + (nc === 1 ? " summary fails a check" : " summaries fail a check") + ", blocks export: " + nc);
    return bits.join(", ");
  }

  function paint(root, d, note) {
    const prev = root.querySelector("details.zj-det"); if (prev) wasOpen = prev.open;
    clear(root); root.hidden = false;
    root.setAttribute("data-testid", "judge-panel"); root.setAttribute("aria-labelledby", "zj-h");
    const toggle = el("span", { class: "zs-toggle", "aria-hidden": "true" }, "Show");
    const det = el("details", { class: "zs-case-det zj-det", "data-open-on-jump": "1" },
      el("summary", { "data-testid": "judge-summary" }, el("h3", { class: "zs-case-title", id: "zj-h" }, "How the AI was checked"),
        el("span", { class: d && ((d.totals || {}).unsupported || (d.totals || {}).unavailable || (d.totals || {}).unsure || (gate && gate.code.length)) ? "zs-sumv zj-sum-bad" : "zs-sumv", "data-testid": "judge-summary-counts" }, d ? summaryText(d) : note || "loading…"), toggle));
    det.open = wasOpen; toggle.textContent = det.open ? "Hide" : "Show";
    det.addEventListener("toggle", () => { wasOpen = det.open; toggle.textContent = det.open ? "Hide" : "Show"; });
    root.append(det);
    const prepared = d && d.models ? !!d.models.generator_prepared : ZL.stepper.preparedFor(null);   // before the data arrives the case says whose answers they are      // D-065: a prepared (hand-checked) demo answer was not drafted by a model; nothing here may say it was
    det.append(el("p", { class: "rv-help", "data-testid": "judge-label" }, el("strong", {}, "AI quality checks. "),
      (prepared ? "This shows how a second AI model checked the answers our team prepared for this demo. " : "This shows how a second AI model checked the first AI's drafts. ") + "It is not a verdict on the case, the care or the claim, and it does not replace your review."));
    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
    const t = d.totals || {}, m = d.models || {}, items = byItem(d);
    det.append(prepared
      ? el("p", { class: "zj-models", "data-testid": "judge-model-line" }, "Prepared by our team (not by an AI model), checked by ", el("strong", {}, m.judge || "unknown"), ".")
      : el("p", { class: "zj-models", "data-testid": "judge-model-line" },
        "Drafted by ", el("strong", {}, m.generator || "unknown"), ", checked by ", el("strong", {}, m.judge || "unknown"),
        d.independent_models ? " (a different model, so it does not grade its own work)." : " (the same model: this check is weaker, read more closely)."));
    det.append(el("ul", { class: "zj-tiles", "data-testid": "judge-totals", "aria-label": "AI check totals" },
      tile(t.items_judged || 0, "items checked by AI"), tile(t.supported || 0, "agreed with the draft"), tile(t.unsupported || 0, "AI objected"),
      tile(t.unsure || 0, "could not decide"), tile(t.unavailable || 0, "unavailable"), tile(t.human_overrides || 0, "you accepted despite an objection")));
    const cids = codeIds(), cblk = (gate && gate.code) || [];
    const asked = items.filter((i) => i.rej), open = items.filter((i) => !i.rej && i.unres && !cids.has(i.id)), differ = items.filter((i) => !i.rej && !i.unres && i.dis.length);
    const verdictLine = cblk.length && gate.verdict && gate.verdict.label   // the case verdict exactly as the server words it (the same text as the case checks)
      ? el("p", { class: "zj-case-verdict" }, el("span", { class: "zs-verdict zs-v-" + (gate.verdict.code || "none"), "data-testid": "judge-case-verdict" }, gate.verdict.label), " ", el("span", { class: "zs-ev" }, "Case verdict from the export gate.")) : null;
    if (cblk.length) det.append(list("judge-wording-list", "Where a summary does not match its quote", cblk, wordingRow, "", verdictLine));
    det.append(list("judge-rejections", "Where the AI objected", asked, (i) => row(i, "judge-rejection"), "No objections. The second check agreed with every item it checked."));
    const nHeld = open.filter(heldFinal).length, nBlock = open.filter(blocking).length - nHeld, nWait = open.filter(waiting).length, nRun = nBlock + nWait;
    // One rerun button for the whole list, its Running… / result sentence right under it (the sentence is read from the stored note, so a repaint keeps it). It covers only what a rerun can clear.
    const group = nRun || nHeld ? el("div", { class: "zs-todo", "data-testid": "judge-rerun-group" },
      nRun ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "),
        nBlock ? plural(nBlock, "accepted item", "accepted items") + " cannot go in the letter until the second AI check has run on " + (nBlock === 1 ? "it" : "them") + "."
          : "The second check has not run on " + plural(nWait, "item", "items") + " you have not decided yet. Run it before you accept " + (nWait === 1 ? "it" : "them") + ".") : null,
      nRun ? el("div", { class: "zs-todo-btns" }, ZL.stepper.rerunButton(nRun === 1 ? "Run the second check again for this item" : "Run the second check again for these " + nRun)) : null,
      nHeld ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), ZL.stepper.HELD_NO_RERUN(nHeld, ZL.stepper.allPrepared(open.filter(heldFinal).map((i) => i.id)))) : null,
      ZL.stepper.rerunStatus()) : null;
    if (open.length) det.append(list("judge-unresolved-list", "Where the AI could not check or decide", open, (i) => row(i, "judge-unresolved"), "", group));
    const dWho = !differ.length || !differ.every((i) => i.dis.every(prepDis)) ? "the AI" : differ.every((i) => i.dis.every((x) => x.type === "sources_disagree")) ? "the prepared answers" : differ.every((i) => i.dis.every((x) => x.type !== "sources_disagree")) ? "the second AI check" : "the answers";
    if (differ.length) det.append(list("judge-disagreements", "Where code and " + dWho + " read an item differently", differ, (i) => row(i, "judge-disagreement"), ""));
    const jr = (d.judges || []).filter((j) => j.label && j.items + (j.unavailable || 0) > 0);
    det.append(el("details", { class: "zs-more zj-tech", "data-testid": "judge-tech" }, el("summary", {}, "Technical details"),
      el("p", { class: "zs-ev", "data-testid": "judge-prompts" }, el("span", { class: "zs-k" }, "Prompt versions: "), (d.prompt_versions || []).join(", ") || "none"),
      jr.length ? el("details", { class: "zs-more zj-by", "data-testid": "judge-by-check" }, el("summary", {}, "By kind of check (" + jr.length + ")"),
        el("ul", { class: "zj-list" }, jr.map((j) => el("li", { class: "zj-row" }, el("div", { class: "zs-head" }, el("span", { class: "zs-label" }, j.label)),
          el("p", { class: "zs-ev" }, j.items + " checked: " + j.supported + " agreed, " + (j.partially || 0) + " partly, " + (j.unsupported || 0) + " not supported, " + (j.disagrees || 0) + " read differently, " + (j.unsure || 0) + " undecided, " + (j.unavailable || 0) + " unavailable. ",
            el("span", { class: "zs-k" }, "Prompt "), j.prompt_version || "", el("span", { class: "zs-k" }, " · model "), (j.models || []).join(", ")))))) : null));
  }

  // Mounted right under the case checks by ZL.stepper.mountCase, so the AI-check signal sits at the top of the results.
  ZL.judges = {
    // Fetch the report again and repaint the mounted panel (used after "Run the second check again").
    async reload(tr) {
      const s = ZL.state.get(); if (!s.token) return;
      const [d, t] = await Promise.all([ZL.api.judges(s.token), tr || ZL.api.caseTrace(s.token).catch(() => null)]);
      cache = { token: s.token, data: d, gate: gateSet(t) }; gate = cache.gate;
      document.querySelectorAll('[data-panel="judges"]').forEach((r) => { if (r.isConnected) paint(r, d); });
    },
    mount(parent, before) {
      const s = ZL.state.get(); if (!s.token || !s.case) return null;
      const root = el("section", { class: "rv-panel zj-panel", "data-panel": "judges" });
      parent.insertBefore(root, before || null);
      if (cache && cache.token !== s.token) { cache = null; gate = null; wasOpen = false; }
      if (cache) gate = cache.gate;
      paint(root, cache && cache.token === s.token ? cache.data : null);
      Promise.all([ZL.api.judges(s.token), ZL.api.caseTrace(s.token).then(gateSet, () => null)]).then(([d, g]) => {
        const same = cache && cache.token === s.token && JSON.stringify(cache.data) === JSON.stringify(d) && JSON.stringify(cache.gate) === JSON.stringify(g);
        cache = { token: s.token, data: d, gate: g }; gate = g;
        if (!same && root.isConnected) paint(root, d);
      }, () => { if (cache) return; if (ZL.API_MODE === "mock" && root.isConnected) paint(root, null, "AI check details need the live server."); else root.hidden = true; });
      return root;
    },
  };
})();
