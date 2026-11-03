/* Vertical steppers (T-081, D-042): every check and gate rendered as a rail of steps with pass / fail / skipped / pending, the plain-words why,
   the evidence, and what the human must do next (HITL hand-off). Pattern: <outside project> flow rail (marker, label, detail, note, "x/y done", verdict).
   Data comes from GET /cases/{token}/items/{id}/trace and GET /cases/{token}/trace (memory/contracts/api.md, "Check traces"); nothing is computed here
   except "x of y steps passed" counts of what the server returned. Full-mode-only keys (response_raw, edited_text, events[].before/after) may be absent.
   Exposes ZL.stepper = { item, itemSection, openTrace, traceButton, mountCase, onExport, exportNotice, showExportBlocked, clearExportNotice, rejudge, rerunButton, goto, gotoPanel, label, cue, setLabel, verdictWord, progressLabel }. Server text only goes through ZL.el (text nodes). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const { el, clear } = ZL;
  const S = (ZL.stepper = {});

  // Status is a glyph AND a word, never colour alone. A step that is waiting on the human's decision says so ("Needs your decision") instead of "Failed":
  // "Failed" is kept for a check that went wrong. The export gate that cannot open yet says "Blocked".
  const GLYPH = { pass: "✓", fail: "✕", skipped: "–", pending: "○" };
  const DECISION = ["DECIDE", "COMPARE_BY_HAND", "CONFIRM_DATE", "DISMISS_OR_ENTER_BY_HAND", "EDIT_SUMMARY", "EDIT_QUOTE", "READ_RECORD"];
  const needsRerun = (st) => !!(st && st.next_action && st.next_action.code === "RERUN_JUDGE");
  function statusInfo(st) {
    const decide = st.next_action && DECISION.includes(st.next_action.code);
    if (st.status === "pass") return { glyph: GLYPH.pass, word: "Passed", cat: "pass" };
    if (st._notNeeded) return { glyph: GLYPH.skipped, word: "Not needed", cat: "skipped" };   // the export gate does not list this item: the wording is the paralegal's own (D-045 b)
    if (st.status === "skipped" && needsRerun(st)) return { glyph: GLYPH.fail, word: "Did not run", cat: "need" };   // D-044: the second check never ran, so this item cannot go in the letter yet
    if (st.status === "skipped") return { glyph: GLYPH.skipped, word: "Skipped", cat: "skipped" };
    if (st.id === "export_gate" && st.status === "fail") return { glyph: GLYPH.fail, word: "Blocked", cat: "need" };
    if (st.status === "fail") return decide ? { glyph: GLYPH.pending, word: "Needs your decision", cat: "need" } : { glyph: GLYPH.fail, word: "Failed", cat: "fail" };
    if (st.status === "pending") return decide || st.kind === "human" ? { glyph: GLYPH.pending, word: "Needs your decision", cat: "need" } : { glyph: GLYPH.pending, word: "Not done yet", cat: "wait" };
    return { glyph: "?", word: String(st.status), cat: "wait" };
  }
  // One progress formula for item and case: "9 passed, 1 failed, 1 needs you".
  function progressLabel(steps) {
    const n = { pass: 0, fail: 0, need: 0, wait: 0, skipped: 0 };
    steps.forEach((st) => { n[statusInfo(st).cat] += 1; });
    const bits = [[n.pass, "passed"], [n.fail, "failed"], [n.need, n.need === 1 ? "needs you" : "need you"], [n.wait, "not done yet"], [n.skipped, "skipped"]].filter(([k]) => k).map(([k, w]) => k + " " + w);
    return bits.join(", ");
  }
  S.progressLabel = progressLabel;
  const VERDICT_WORD = { supported: "Supported", partially: "Partly supported", unsupported: "Not supported", disagrees: "Disagrees", unsure: "Could not decide", unavailable: "Unavailable" };
  S.verdictWord = (v) => VERDICT_WORD[v] || v || "";
  const kindOf = (st) => {
    if (st.kind === "human") return "You";
    if (st.kind === "code") return "Code";
    const m = st.evidence && st.evidence.model;
    if (m && m.prepared) return "Prepared answer";         // D-065: a hand-checked demo answer is not an AI draft
    return (m && m.role === "generator") || st.id === "extracted" || st.id === "extract" ? "AI draft" : "AI check";
  };
  const humanize = (k) => String(k).replace(/_/g, " ");
  const rv = () => ZL.rv;
  const caseNow = () => ZL.state.get().case;
  const recSeq = (id) => { const r = ((caseNow() || {}).records || []).find((x) => x.id === id); return r ? r.seq : String(id).replace(/^r/, ""); };

  // ---- labels for items (entry: date and provider; amount: the figure; flag: its title)
  const extraLabels = {};   // narrative sentences register their own label ("ns1" -> first words of the sentence)
  S.setLabel = (id, text) => { const t = String(text || "").trim(); extraLabels[id] = t.length > 60 ? t.slice(0, 57).replace(/\s+\S*$/, "") + "…" : t; };
  // T-117: a could-not-verify tray item (case.tray, D-053 flags included) is not in entries / amounts / flags; it is named by what the AI tried (its summary), else by the flag's category in words.
  const trayItem = (c, id) => ((c && c.tray) || []).find((x) => x.id === id) || null;
  const trayName = (t) => {
    const a = (t.attempt && t.attempt.summary) || "", f = t.flag || {};
    if (a) return a;
    const words = String(f.category || f.type || "").replace(/_/g, " ").trim();
    return words ? words.charAt(0).toUpperCase() + words.slice(1) : t.kind === "flag" ? "Flag" : "Entry";
  };
  S.label = function (id) {
    const c = caseNow(), f = c && rv() && rv().find(c, id);
    if (!f) { const t = trayItem(c, id); return t ? trayName(t) : extraLabels[id] || id; }
    const it = f.item;
    if (f.kind === "entry") return (it.date || "undated") + " · " + (it.provider || "entry");
    if (f.kind === "amount") return (it.text || it.id) + (it.kind ? " (" + it.kind + ")" : "");
    return it.title || it.id;
  };

  // Where an item sits in the records: "Record 3", "Records 3 and 5" (entries and amounts: record_ids; flags: the records of their evidence). Empty when unknown.
  S.cue = function (id) {
    const c = caseNow(), f = c && rv() && rv().find(c, id);
    const t = !f && trayItem(c, id);
    if (!f && !t) return "";
    const it = f ? f.item : t, ids = [];
    const add = (r) => { if (r && !ids.includes(r)) ids.push(r); };
    (it.record_ids || []).forEach(add); ((it.computed || {}).record_ids || []).forEach(add); (it.evidence || []).forEach((e) => add(e && e.record_id));
    const seqs = ids.map(recSeq);
    return !seqs.length ? "" : seqs.length === 1 ? "Record " + seqs[0] : "Records " + seqs.slice(0, -1).join(", ") + " and " + seqs[seqs.length - 1];
  };

  // ---- navigation helpers
  function closeDialogs() { document.querySelectorAll("dialog[open]").forEach((d) => { try { d.close(); } catch (_) { /* ignore */ } }); }
  function flash(node) {
    node.classList.add("zs-flash");
    setTimeout(() => node.classList.remove("zs-flash"), 2200);
  }
  function reveal(node) {
    if (!node.hasAttribute("tabindex")) node.setAttribute("tabindex", "-1");
    // a target taller than 60% of the screen lands with its heading at the top (the sticky banner is cleared by scroll-margin-top); short rows are centred
    const tall = node.getBoundingClientRect().height > window.innerHeight * 0.6;
    node.scrollIntoView({ block: tall ? "start" : "center" }); node.focus({ preventScroll: true }); flash(node);
  }
  S.goto = function (itemId) {
    closeDialogs();
    const node = document.querySelector('[data-testid="queue"] [data-item-id="' + itemId + '"]') || document.querySelector('[data-item-id="' + itemId + '"]');
    if (!node) return false;
    reveal(node); return true;
  };
  function gotoDates(recordId) {
    closeDialogs();
    const node = (recordId && document.querySelector('[data-testid="date-to-confirm-item"][data-record-id="' + recordId + '"]')) ||
      (recordId && document.querySelector('[data-record-id="' + recordId + '"]')) || document.querySelector('[data-testid="dates-to-confirm"]');
    if (node) reveal(node);
  }
  function gotoPanel(name) {
    closeDialogs();
    const node = document.querySelector('[data-panel="' + name + '"]:not([hidden])') || document.querySelector('[data-testid="queue"]');
    if (!node) return false;
    node.querySelectorAll("details[data-open-on-jump]").forEach((d) => { d.open = true; });
    reveal(node); return true;
  }
  S.gotoPanel = gotoPanel;
  function gotoFirstPending() {
    closeDialogs();
    const node = document.querySelector('[data-testid="queue"] [data-item-id][data-review="pending"]') || document.querySelector('[data-item-id][data-review="pending"]') || document.querySelector('[data-testid="queue"]');
    if (!node) return false;
    reveal(node); return true;
  }
  // T-136: the first entry whose edit still waits for her comparison with the quote (the row carries data-edit-check).
  function gotoFirstEdit() {
    closeDialogs();
    const node = document.querySelector('[data-testid="queue"] [data-item-id][data-edit-check]') || document.querySelector('[data-item-id][data-edit-check]');
    if (!node) return gotoFirstPending();
    reveal(node); return true;
  }
  function gotoTray() {
    closeDialogs();
    const node = document.querySelector('[data-testid="rejected-tray"]') || document.querySelector('[data-testid="queue"]');
    if (!node) return false;
    reveal(node); return true;
  }
  async function rerun(confirm, msgNode) {
    const s = ZL.state.get();
    try { msgNode.textContent = ""; await ZL.api.run(s.token, confirm); ZL.pollRun(); } catch (e) { msgNode.textContent = (S.preparedFor(null) ? "The checks could not be started: " : "The AI steps could not be started: ") + e.message; }
  }
  function openRecord(itemId, recordId) {
    const c = caseNow(), f = itemId && c && rv() && rv().find(c, itemId);
    if (f) { rv().openSource(f.item, f.kind); return; }
    if (recordId && typeof ZL.openSource === "function") ZL.openSource([{ record_id: recordId, start: null, end: null }], "Record " + recSeq(recordId));
  }

  // ---- "Run the second check again" (D-044): POST /rejudge for the accepted items whose second AI check never ran. One handler for every place that offers it
  // (case rail, export gate, blocker rows, the export message, the item stepper, the AI-check panel). Busy state and the result in plain words live in module
  // state, so a repaint of the page does not lose the sentence.
  const RERUN = "Run the second check again";
  // D-045(b)/T-098: a code-check blocker on wording the paralegal wrote or edited (the gate's blocker carries step_id; the text is the server's).
  const WORDING = "Your wording doesn't match the quote:";
  const isCodeBlocker = (b) => !!(b && b.item_id && b.step_id);
  const WORDING_AI = "This summary doesn't match the quote:";
  // D-051: a blocker on an accepted AI draft says "This summary", not "Your wording" (the paralegal did not write it); an edited or hand-written one says "Your wording".
  const mine = (id) => { const f = id && caseNow() && rv() && rv().find(caseNow(), id); return !f || f.kind !== "entry" || f.item.ai_drafted === false || f.item.review_status === "edited"; };
  // T-104: where the item's own trace is open, the lead follows the backend verdict string as sent ("... a check on this summary fails" for an AI draft, "... a check on your wording fails"
  // only for wording the paralegal wrote or edited); no verdict (rail and panel rows) falls back to who wrote the item.
  S.wordingLead = (id, verdictLabel) => (/your wording/i.test(verdictLabel || "") ? WORDING : /this summary/i.test(verdictLabel || "") ? WORDING_AI : mine(id) ? WORDING : WORDING_AI);
  const quoteFix = (na) => !!na && String(na.code).toUpperCase() === "EDIT_QUOTE";   // the first failing check is on the quote, not the summary (T-104)
  S.wordingEditText = (id, na, verdictLabel) => (quoteFix(na) ? "Change the quote" : (/your wording/i.test(verdictLabel || "") || (!/this summary/i.test(verdictLabel || "") && mine(id))) ? "Edit your wording" : "Edit the summary");
  S.wordingFix = (id, na) => (quoteFix(na) ? S.changeQuote(id) : S.editItem(id));
  S.WORDING = WORDING; S.isCodeBlocker = isCodeBlocker;
  let rerunBusy = false, rerunNote = null;   // rerunNote: {token, text}
  const rerunSay = (text) => {
    rerunNote = text ? { token: (ZL.state.get() || {}).token, text } : null;
    document.querySelectorAll('[data-testid="rerun-status"]').forEach((n) => { n.textContent = text || ""; });
  };
  const setRerunBusy = (b) => { rerunBusy = b; document.querySelectorAll('[data-testid="btn-rerun-judge"]').forEach((x) => { x.disabled = b; x.setAttribute("aria-busy", b ? "true" : "false"); }); };
  const gateOf = (tr) => ((tr || {}).steps || []).find((x) => x.id === "export_gate");
  const jnrBlockers = (g) => ((g && g.blockers) || []).filter((b) => b.reason_code === "JUDGE_NOT_RUN");
  // ONE button per list: its words say how many items the one POST covers ("these 3"), so the label never promises a single item.
  const groupLabel = (n) => RERUN + (n === 1 ? " for this item" : " for these " + n);
  // T-157 / T-136 debt: "Run the second check again" is offered only when the server says it can get an answer (item.rerun_available, on every item of GET case and of each review response).
  // False in demo mode and with the fixture backend, and after a rerun that got no answer. A field that is missing counts as false: no button that cannot work.
  S.rerunAvailable = function () {
    const c = (ZL.state.get() || {}).case; if (!c) return false;
    return [].concat(c.entries || [], c.undated_entries || [], c.flags || [], c.amounts || []).some((i) => i.rerun_available === true);
  };
  S.rerunButton = function (label, aria) {
    if (!S.rerunAvailable()) return el("p", { class: "zs-ev", "data-testid": "rerun-unavailable" }, "The second check cannot be run again here: no AI model can answer it right now. The items stay out of the letter until it has run.");
    const b = el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-rerun-judge", "aria-label": aria || null, onclick: (ev) => S.rejudge(ev.currentTarget) }, label || RERUN);
    if (rerunBusy) { b.disabled = true; b.setAttribute("aria-busy", "true"); }
    return b;
  };
  // A status line that shows the last rerun sentence (role=status, so a screen reader hears it).
  S.rerunStatus = () => rerunStatus();
  const rerunStatus = () => el("p", { class: "zs-ev zs-rerun-status", role: "status", "data-testid": "rerun-status" }, rerunNote && rerunNote.token === (ZL.state.get() || {}).token ? rerunNote.text : "");
  const OBJECT = ["partially", "unsupported", "disagrees", "unsure"];
  function rerunWords(res) {
    const asked = res.asked || 0, still = (res.still_unavailable || []).length, got = (res.rejudged || []);
    if (!asked) return "There was nothing to run the second check on.";
    const obj = got.filter((r) => OBJECT.includes(r.verdict)).length;
    const stillIds = (res.still_unavailable || []).map((x) => (x && typeof x === "object" ? x.item_id || x.id : x));
    if (stillIds.length && stillIds.every((x) => S.isHeld(x)))   // T-136 r3: every item left is a held re-picked quote: another rerun cannot clear it, her own summary wording does
      return "The second check ran again and still gave no answer on the new quote for " + plural(stillIds.length, "item", "items") + " of " + asked + ". Write the summary in your own words" + (stillIds.length === 1 ? "." : " for each.");
    let t = still ? "The second check still did not answer for " + plural(still, "item", "items") + " of " + asked + ". Try again, or dismiss " + (still === 1 ? "it" : "them") + "."
      : "The second check ran on " + plural(asked, "item", "items") + " and answered for " + (asked === 1 ? "it" : "all of them") + ".";
    if (obj) t += " It questioned " + plural(obj, "item", "items") + "; see How the AI was checked.";
    if (!still && res.export_gate && res.export_gate.ready) t += " Nothing about the second check blocks the export now.";
    return t;
  }
  function rerunError(e) {
    if (e.code === "run_in_progress") return S.preparedFor(null) ? "The run is still going. Try again when it finishes." : "The AI run is still going. Try again when it finishes.";
    if (e.code === "llm_unavailable") return "The second check could not be reached. Try again in a moment.";
    if (e.code === "demo_mode_unsupported_input") return "The demo can only run the second check on its recorded cases.";
    return "The second check could not be run: " + e.message;
  }
  // The answer must be where the pressed button is: after Running… and after the result, scroll the status line of the region the button sat in just into view
  // (a button near the bottom of the screen has its status line below the fold). The region is found again by name because the repaint rebuilds its nodes.
  const REGIONS = '[data-testid="export-blocked"],[data-testid="judge-panel"],[data-testid="case-stepper"],[data-testid="item-stepper"]';
  function showStatusIn(sel) {
    const root = sel && document.querySelector(sel), st = root && Array.from(root.querySelectorAll('[data-testid="rerun-status"]')).find((n) => n.textContent);
    if (st) st.scrollIntoView({ block: "nearest" });
  }
  S.rejudge = async function (origin) {
    if (rerunBusy) return;
    const s = ZL.state.get(); if (!s.token) return;
    const reg = origin && origin.closest ? origin.closest(REGIONS) : null, sel = reg ? '[data-testid="' + reg.getAttribute("data-testid") + '"]' : null;
    setRerunBusy(true);
    // T-158: the count in "Running the second check on N items" comes from the gate; when the trace is not cached yet (pressed right after a load, or under load) ask for it first, so the sentence never loses its count
    if (!(cache && cache.token === s.token)) { try { setCache(s.token, await ZL.api.caseTrace(s.token)); } catch (_) { /* the sentence falls back to no count */ } }
    const n = jnrBlockers(gateOf(cache && cache.token === s.token ? cache.data : null)).length; rerunSay(n ? "Running the second check on " + plural(n, "item", "items") + "…" : "Running the second check…");
    showStatusIn(sel);
    let res = null;
    try { res = await ZL.api.rejudge(s.token); rerunSay(rerunWords(res)); } catch (e) { rerunSay(rerunError(e)); }
    // refresh every view that shows the gate: case trace, AI-check panel, the case itself (item state can change), then tell open dialogs
    try {
      const tr = await ZL.api.caseTrace(s.token);
      setCache(s.token, tr);
      if (ZL.judges) await ZL.judges.reload(tr);
      noticeAfterRerun(gateOf(tr));
      ZL.state.set({ case: await ZL.api.getCase(s.token) });
    } catch (_) { /* the sentence above already told the human what happened */ }
    setRerunBusy(false); showStatusIn(sel);
    document.dispatchEvent(new CustomEvent("zl:rejudged", { detail: res }));
  };

  // ---- "What you need to do": one fixed sentence from the server plus a button where something on the page can do it.
  // Rule: a button is only drawn when its handler can land somewhere (every handler falls back to the queue), never a dead button.
  const plural = (n, one, many) => n + " " + (n === 1 ? one : many);
  function gotoItem(id) {
    if (S.goto(id)) return true;
    return /^ns\d/.test(String(id)) ? gotoPanel("narrative") : gotoFirstPending();
  }
  // Opens the edit box of an item (the same path as pressing e on its row). Used by every "Edit your wording" action.
  S.editItem = function (id) {
    if (!gotoItem(id)) return false;
    const n = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]') || document.querySelector('[data-item-id="' + id + '"]');
    if (n) n.dispatchEvent(new KeyboardEvent("keydown", { key: "e", bubbles: true }));
    return true;
  };
  // T-104: the first failing check is on the quote (next_action EDIT_QUOTE): the action is the quote picker (Change quote on the row), or the record itself when the row has no picker.
  S.changeQuote = function (id) {
    if (!gotoItem(id)) return false;
    if (ZL.openQuoteEditor && ZL.openQuoteEditor(id)) return true;
    openRecord(id, null); return true;
  };
  const VIEW = {   // target.view -> [button text, handler]
    judges: ["Open the AI checks", () => gotoPanel("judges")],
    amounts: ["Go to the charges", () => gotoPanel("charges")],
    queue: ["Go to the first pending item", () => gotoFirstPending()],
    tray: ["Go to the could-not-verify items", () => gotoTray()],
    narrative: ["Go to the draft paragraph", () => gotoPanel("narrative")],
  };
  // Case-level steps say what to do with counts ("Review the 3 items the AI objected to"), not the item-level sentence.
  function caseCopy(st) {
    const c = st.counts || {};
    switch (st.id) {
      case "judges": {
        const obj = c.unsupported || 0, unsure = c.unsure || 0, un = c.unavailable || 0, cant = unsure + un;
        if (!obj && !cant) return null;
        const bits = [];
        if (obj) bits.push("Review the " + plural(obj, "item", "items") + " the AI objected to. Compare each one with its quote, then accept, edit or dismiss it.");
        if (unsure) bits.push("The AI could not decide " + plural(unsure, "item", "items") + "; read " + (unsure === 1 ? "it" : "them") + " yourself.");
        const held = heldNow(), unRerun = Math.max(0, un - held.filter(noAnswer).length);
        if (unRerun) bits.push("The second AI check did not run on " + plural(unRerun, "item", "items") + ". Run it again; accepted items it never checked cannot go in the letter.");
        if (held.length) bits.push(heldWords(held));
        return { text: bits.join(" "), label: obj ? "Review the " + plural(obj, "item", "items") + " the AI objected to" : "Show the " + plural(cant, "item", "items") + " the AI could not check", go: () => gotoPanel("judges"), rerun: unRerun > 0, rerunN: unRerun, write: held.length ? held[0].item_id : null };
      }
      case "totals": {
        const n = c.pending_charges || 0;
        return { text: "Decide the " + plural(n, "detected charge", "detected charges") + ": accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.", label: "Go to the totals", go: () => gotoPanel("charges") };
      }
      case "review": {
        const n = c.pending || 0, ed = c.edit_to_check || 0;
        if (!n && ed) return { text: "Compare " + plural(ed, "edit", "edits") + " with the quote, then click \u201cI compared it with the quote\u201d on " + (ed === 1 ? "it" : "each") + ". Until you do, " + (ed === 1 ? "it stays" : "they stay") + " out of the letter.", label: "Go to the first edit to check", go: () => gotoFirstEdit() };
        return { text: "Decide the " + plural(n, "pending item", "pending items") + ": accept, edit or dismiss each one.", label: "Go to the first pending item", go: () => gotoFirstPending() };
      }
      case "export_gate": {
        const bl = st.blockers || [], n = c.blocking || bl.length, jnr = plainBlockers(st), held = heldBlockers(st), canRerun = rerunBlockers(st);
        if (!bl.length) return null;
        const b = firstBlocker(bl);
        if (!b && !jnr.length && !held.length) return null;     // only whole-case blockers (nothing accepted, run state): the step's own action (go to the queue) says it
        const parts = [];
        if (jnr.length) parts.push(plural(jnr.length, "accepted item", "accepted items") + " never got the second AI check, so the export is blocked. Run the second check again; if it still cannot answer, dismiss " + (jnr.length === 1 ? "that item" : "those items") + ".");
        if (held.length) parts.push(heldWords(held));
        const text = parts.length ? parts.join(" ") : "Settle the " + plural(n, "blocker", "blockers") + " listed here and the export opens.";
        return { text, label: "Go to the first blocking item", go: b ? () => gotoItem(b.item_id) : null, rerun: canRerun.length > 0, rerunN: canRerun.length, write: held.length ? held[0].item_id : null };
      }
      default: return null;
    }
  }
  // The first blocker in QUEUE order, so "Go to the first blocking item" lands where "Go to the first pending item" would.
  const queueIds = () => Array.from(document.querySelectorAll('[data-testid="queue"] [data-item-id]')).map((n) => n.getAttribute("data-item-id"));
  function firstBlocker(bl) {
    const ids = queueIds(), withItem = (bl || []).filter((b) => b.item_id);
    const idx = (b) => { const i = ids.indexOf(b.item_id); return i < 0 ? 1e6 : i; };
    return withItem.slice().sort((a, b) => idx(a) - idx(b))[0] || null;
  }
  // List order: whole-case blockers, then entries that need review, other entries, then charges and flags. Stable.
  function orderBlockers(bl) {
    const rank = (b) => {
      if (!b.item_id) return 0;
      const f = rv() && caseNow() && rv().find(caseNow(), b.item_id);
      return f && f.kind === "entry" ? (f.item.state === "needs_review" ? 1 : 2) : 3;
    };
    return (bl || []).map((b, i) => [b, i]).sort((x, y) => rank(x[0]) - rank(y[0]) || x[1] - y[1]).map((x) => x[0]);
  }
  function actionNode(na, ctx, st) {
    if (!na) return null;
    const t = na.target || {}, buttons = [], msg = el("p", { class: "zs-ev zs-err", role: "alert" });
    const itemId = t.item_id || ctx.itemId, recId = t.record_id || (ctx.recordId || null);
    const btn = (text, fn, extra) => buttons.push(el("button", Object.assign({ type: "button", class: "btn", "data-testid": "btn-step-action", "data-action-code": na.code, onclick: fn }, extra || {}), text));
    const view = t.view && VIEW[t.view];
    let text = na.text || "";
    const cc = ctx.level === "case" && st ? caseCopy(st) : null;
    let rerunToo = false;
    if (cc) {
      text = cc.text;
      if (cc.rerun) { const n = cc.rerunN != null ? cc.rerunN : (st.counts || {}).unavailable || 0; buttons.push(n ? S.rerunButton(groupLabel(n)) : S.rerunButton()); rerunToo = true; }
      if (cc.write) buttons.push(el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-write-summary-case", "aria-label": "Write the summary for " + S.label(cc.write), onclick: () => S.editItem(cc.write) }, "Write the summary"));
      if (cc.go) btn(cc.label, cc.go);
    }
    else switch (na.code) {
      case "CONFIRM_DATE": btn("Go to Dates to confirm", () => gotoDates(recId)); break;
      case "EDIT_SUMMARY": if (itemId) btn("Go to the item and edit the summary", () => S.editItem(itemId)); break;
      case "EDIT_QUOTE": case "READ_RECORD": case "COMPARE_BY_HAND":
        if (view && !itemId) btn(view[0], view[1]); else if (itemId || recId) btn("Open the record", () => openRecord(itemId, recId), { "aria-label": "Open " + ((itemId && S.cue(itemId)) || "the record").toLowerCase() }); break;
      case "DISMISS_OR_ENTER_BY_HAND":
        if (view) btn(view[0], view[1]); else if (t.item_id) btn("Go to the item", () => gotoItem(t.item_id)); else if (recId) btn("Go to the record", () => gotoDates(recId)); break;
      case "RERUN": case "CONFIRM_RERUN":
        btn(S.preparedFor(null) ? "Run the checks again" : "Run the AI steps again", () => rerun(na.code === "CONFIRM_RERUN", msg)); break;
      case "RERUN_JUDGE":
        buttons.push(S.rerunButton()); rerunToo = true;
        if (t.view === "judges" && !(st && st.id === "judges")) btn("Open the AI checks", () => gotoPanel("judges"));
        break;
      case "SENTENCE_REMOVED": btn("Go to the draft paragraph", () => gotoPanel("narrative")); break;
      case "DECIDE":
        if (view) btn(view[0], view[1]); else if (t.view === "dates_to_confirm") btn("Go to Dates to confirm", () => gotoDates(recId));
        else if (itemId) btn("Go to the decision buttons", () => gotoItem(itemId)); break;
      default:
        if (t.view === "dates_to_confirm") btn("Go to Dates to confirm", () => gotoDates(recId));
        else if (view) btn(view[0], view[1]);
        else if (t.item_id) btn("Go to the item", () => gotoItem(t.item_id));
    }
    return el("div", { class: "zs-todo", "data-testid": "step-action" },
      el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), text), buttons.length ? el("div", { class: "zs-todo-btns" }, buttons) : null, rerunToo ? rerunStatus() : null, msg);
  }

  // ---- evidence
  function quote(rec, text) {
    return el("figure", { class: "zs-quote" }, rec ? el("figcaption", {}, "Record " + recSeq(rec)) : null, el("blockquote", {}, text));
  }
  const fmtVal = (k, v) => (/_cents$/.test(k) && typeof v === "number" && rv() ? [humanize(k.replace(/_cents$/, "")), rv().money(v)] : [humanize(k), v && typeof v === "object" ? JSON.stringify(v) : String(v)]);
  function evidenceNode(st) {
    const ev = Object.assign({}, st.evidence || {}), out = [];
    if (st._notNeeded) { delete ev.judge_verdict; delete ev.rationale; delete ev.judge_reason_code; }   // "Not needed" must not also print "The second AI check said: Unavailable"
    if (ev.excerpt && ev.excerpt.text) out.push(quote(ev.excerpt.record_id, ev.excerpt.text));
    (ev.spans || []).forEach((sp) => { if (sp && sp.text) out.push(quote(sp.record_id, sp.text)); });
    if (ev.tokens && ev.tokens.length) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Not found in the quote: "), ev.tokens.map((t) => el("code", { class: "zs-tok" }, t))));
    if (ev.values) {
      const bits = Object.entries(ev.values).filter(([, v]) => v != null && v !== "").map(([k, v]) => fmtVal(k, v));
      if (bits.length) out.push(el("p", { class: "zs-ev", "data-testid": "step-values" }, bits.map(([k, v]) => el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), v))));
    }
    if (ev.date) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Date: "), (ev.date.date_raw ? "written “" + ev.date.date_raw + "”" : "no date written"),
      ev.date.date_iso ? ", read as " + ev.date.date_iso : "", ev.date.date_status ? " (" + humanize(ev.date.date_status) + ")" : "", (ev.date.candidates || []).length ? "; possible readings: " + ev.date.candidates.join(" or ") : ""));
    if (ev.judge_verdict) {
      out.push(el("p", { class: "zs-ev zs-judge", "data-testid": "step-judge-reason" }, el("strong", {}, "The second AI check said: "), S.verdictWord(ev.judge_verdict),
        ev.rationale ? ". " + ev.rationale : ""));
    } else if (ev.rationale) out.push(el("p", { class: "zs-ev" }, ev.rationale));
    if (ev.events && ev.events.length) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your decisions: "), ev.events.map((e) => (e.action || "") + (e.at ? " at " + e.at : "")).join("; ")));
    else if (ev.action) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your decision: "), ev.action + (ev.at ? " at " + ev.at : "")));
    if (ev.edited_text) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your wording: "), ev.edited_text));
    // technical detail for the audit-minded reader, collapsed
    const m = ev.model, tech = [];
    const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), String(v)));
    tech.push(kv("reason code", st.reason_code), kv("rule", st.rule), kv("judge reason code", ev.judge_reason_code && ev.judge_reason_code !== "NONE" ? ev.judge_reason_code : null));
    if (m) tech.push(kv("model", m.id), kv("role", m.role), kv("independent of the drafting model", m.independent_of_generator == null ? null : m.independent_of_generator ? "yes" : "no"));
    const prep = !!(m && m.prepared);      // D-065: no prompt made a prepared answer, so none is shown
    tech.push(prep ? null : kv("prompt", ev.prompt_version), prep ? null : kv("prompt hash", ev.prompt_sha256 && String(ev.prompt_sha256).slice(0, 12)), kv("call", ev.call_id), kv("backend", ev.backend),
      kv("recorded from", ev.recorded_from && ev.recorded_from.backend), kv("latency", ev.latency_ms != null ? ev.latency_ms + " ms" : null), kv("parsed", ev.parsed_ok == null ? null : ev.parsed_ok ? "yes" : "no"));
    const techNodes = tech.filter(Boolean);
    if (techNodes.length || ev.response_raw)
      out.push(el("details", { class: "zs-more", "data-testid": "step-tech" }, el("summary", {}, "Technical details"), techNodes.length ? el("p", { class: "zs-ev" }, techNodes) : null,
        ev.response_raw ? el("pre", { class: "zs-pre" }, typeof ev.response_raw === "string" ? ev.response_raw : JSON.stringify(ev.response_raw, null, 2)) : null));
    return out;
  }

  // Count chips in the paralegal's words: no "llm", "lexicon" or reason codes in the primary view (those are in Technical details).
  const WORD = { code: "code", llm: "AI", lexicon: "phrase list", "lexicon+llm": "phrase list and AI" }, PREP_WORD = { llm: "prepared answers", "lexicon+llm": "phrase list and prepared answers" };   // T-204 r2: a prepared case has no AI finder
  const KEY = { by_origin: "found by", by_type: "kinds", method: "records split by", unsupported: "AI objected", supported: "AI agreed", unsure: "undecided", items_judged: "items checked", pending_items: "not reviewed", judge_not_run: "second check did not run", date_unconfirmed: "dates to confirm" };
  function fmtCounts(counts) {
    const out = [];
    Object.entries(counts || {}).forEach(([k, v]) => {
      if (k === "llm_split" || k === "reasons") return;
      if (v && typeof v === "object") {
        const inner = Object.entries(v).map(([a, b]) => ((S.preparedFor(null) && PREP_WORD[a]) || WORD[a] || humanize(a)) + " " + b).join(", ");
        if (inner) out.push((KEY[k] || humanize(k)) + ": " + inner);
      } else if (/_cents$/.test(k) && typeof v === "number" && rv()) out.push(humanize(k.replace(/_cents$/, "")) + " " + rv().money(v));
      else if (v != null && v !== "") out.push((KEY[k] || humanize(k)) + " " + (k === "method" ? ((S.preparedFor(null) && PREP_WORD[v]) || WORD[v] || v) + (v === "code" ? " (not AI)" : "") : v));
    });
    return out;
  }

  // ---- one step
  function stepNode(st, active, ctx) {
    const { glyph, word } = statusInfo(st);
    const li = el("li", { class: "zs-step", "data-testid": ctx.testid || "step", "data-step-id": st.id, "data-status": st.status, "data-kind": st.kind, "aria-current": active ? "step" : null, tabindex: active ? "-1" : null },
      el("span", { class: "zs-marker", "aria-hidden": "true", "data-testid": "step-marker" }, glyph),
      el("div", { class: "zs-body" },
        el("div", { class: "zs-head" },
          el("span", { class: "zs-label" }, st.label), el("span", { class: "zs-kind zs-kind-" + st.kind, "data-testid": "step-kind" }, kindOf(st)),
          el("span", { class: "zs-status", "data-testid": "step-status" }, word), st.blocks_export ? el("span", { class: "zs-blocks" }, "Blocks export") : null),
        st.why ? el("p", { class: "zs-why", "data-testid": "step-why" }, st.why) : null));
    const body = li.lastChild;
    const ev = evidenceNode(st); if (ev.length) body.append(el("div", { class: "zs-evidence", "data-testid": "step-evidence" }, ev));
    if (ctx.extra) { const x = ctx.extra(st); if (x) body.append(x); }
    if (st.status === "fail" || st.status === "pending" || (st.status === "skipped" && needsRerun(st))) { const a = actionNode(st.next_action, ctx, st); if (a) body.append(a); }
    return li;
  }
  // The active step is the one the human has to deal with now: the first fail or pending step that carries a next action.
  function activeIndex(steps) {
    let i = steps.findIndex((s) => (s.status === "fail" || s.status === "pending" || (s.status === "skipped" && needsRerun(s))) && s.next_action);
    if (i < 0) i = steps.findIndex((s) => s.status === "fail" || s.status === "pending");
    return i;
  }

  // ---- item level
  const firstSentence = (t) => { const m = /^[\s\S]*?[.!?](?=\s|$)/.exec(t || ""); return m ? m[0] : t || ""; };
  // gate: the export_gate step of GET /trace (null when it could not be loaded). The gate decides what blocks the export; this view reads it and the item's own trace
  // and decides nothing: a judge step that never ran is "second check missing" only when the gate lists JUDGE_NOT_RUN for this item, otherwise the wording is the
  // paralegal's own (D-045 b) and the step is "Not needed". A code step the trace marks blocks_export is "Your wording doesn't match the quote".
  const HUMAN_NOTE = "Not needed: this is your own wording, so the second AI check does not apply. The code checks on it still run.";
  S.item = function (tr, gate) {
    let steps = (tr.steps || []).slice();
    const v = Object.assign({}, tr.verdict || {});
    const decided = tr.review_status === "accepted" || tr.review_status === "edited";
    const gated = !!gate && ((gate.blockers || []).some((b) => b.reason_code === "JUDGE_NOT_RUN" && b.item_id === tr.item_id));
    const skippedJudge = steps.some((x) => x.status === "skipped" && needsRerun(x));
    let notAIChecked = false;
    if (decided && gate && !gated && skippedJudge) {   // the gate does not hold this item for a missing second check
      notAIChecked = true;
      steps = steps.map((x) => (x.status === "skipped" && needsRerun(x) ? Object.assign({}, x, { _notNeeded: true, next_action: null, reason_code: null, why: HUMAN_NOTE }) : x));
    }
    const wf = steps.find((x) => x.kind === "code" && x.status === "fail" && x.blocks_export) || null;   // a failing code check on the paralegal's wording (T-098)
    const act = activeIndex(steps);
    if (v.code === "accepted" && !wf) {
      if (notAIChecked) v.label = (tr.review_status === "edited" ? "Edited" : "Accepted") + " by you, not AI-checked";
      else if (skippedJudge) { v.code = "needs_attention"; v.label = "Accepted, second check missing"; }   // the gate (or an unloaded gate) holds it: not a green "Accepted by you"
    }
    if (v.code === "accepted" && tr.review_status === "edited" && /^Accepted by you/.test(v.label || "")) v.label = v.label.replace(/^Accepted by you/, "Edited by you");   // an item the paralegal wrote reads "Edited", not "Accepted"
    const ctx = { itemId: tr.item_id };
    // a record id for date steps
    const dstep = steps.find((s) => s.evidence && s.evidence.date); if (dstep) ctx.recordId = dstep.evidence.date.record_id;
    const rail = el("ol", { class: "zs-rail", "aria-label": "Checks for " + S.label(tr.item_id) }, steps.map((s, i) => stepNode(s, i === act, ctx)));
    const showActive = () => { const a = rail.querySelector('[aria-current="step"]'); if (a) { a.scrollIntoView({ block: "nearest" }); a.focus({ preventScroll: true }); } };
    const now = act >= 0 ? steps[act] : null;
    const root = el("div", { class: "zs zs-item", "data-testid": "item-stepper", "data-verdict": v.code || "" },
      el("div", { class: "zs-top" },
        el("span", { class: "zs-verdict zs-v-" + (v.code || "none"), "data-testid": "item-verdict" }, v.label || ""),
        el("span", { class: "zs-progress", role: "status", "data-testid": "item-progress" }, progressLabel(steps))),
      wf ? el("div", { class: "zs-wording", role: "alert", "data-testid": "item-wording-fail" },
        el("p", { class: "zs-todo-text" }, el("strong", {}, S.wordingLead(tr.item_id, (tr.verdict || {}).label) + " "), wf.why || ""),
        el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-wording-edit", "aria-label": S.wordingEditText(tr.item_id, wf.next_action, (tr.verdict || {}).label) + " for " + S.label(tr.item_id), onclick: () => S.wordingFix(tr.item_id, wf.next_action) }, S.wordingEditText(tr.item_id, wf.next_action, (tr.verdict || {}).label)))) : null,
      now ? el("div", { class: "zs-now", "data-testid": "item-active" },
        el("p", { class: "zs-now-text" }, el("strong", {}, statusInfo(now).word + ": "), now.label, " ", el("span", { class: "zs-ev" }, firstSentence(now.why))),
        el("button", { type: "button", class: "btn", "data-testid": "btn-jump-active", onclick: showActive }, "Show this step")) : null,
      (tr.state_reasons || []).length ? el("ul", { class: "zs-reasons" }, tr.state_reasons.map((r) => el("li", {}, r.why))) : null,
      rail);
    root._showActive = showActive;
    return root;
  };
  // A section that fetches its own trace; used inside the Why dialog. On open it scrolls to the step that needs the human and focuses it.
  S.itemSection = function (token, id) {
    const box = el("section", { class: "zs-section", "aria-labelledby": "zs-h-" + id }, el("h3", { id: "zs-h-" + id }, "Step by step: how this was checked"));
    const msg = el("p", { class: "muted", role: "status" }, "Loading the checks…"); box.append(msg);
    const load = () => Promise.all([ZL.api.trace(token, id), ZL.api.caseTrace(token).then(gateOf, () => null)]).then(([tr, gate]) => { msg.remove(); const old = box.querySelector(".zs-item"); const n = S.item(tr, gate); const fn = (tr.steps || []).some((x) => x.id === "charge_flag") || !ZL.chargeFlagNote ? null : ZL.chargeFlagNote(id, "trace-charge-flag"); if (fn) n.firstChild.after(fn); const rn = rv() && rv().rerunNoteFor ? rv().rerunNoteFor(id) : null; if (rn) n.firstChild.after(rn); if (old) old.replaceWith(n); else box.append(n); requestAnimationFrame(() => n._showActive()); },
      (e) => { msg.textContent = ZL.API_MODE === "mock" ? "Step-by-step checks need the live server." : "The checks could not be loaded: " + e.message; });
    load();
    const again = () => { if (!box.isConnected) { document.removeEventListener("zl:rejudged", again); return; } load(); };
    document.addEventListener("zl:rejudged", again);
    return box;
  };
  S.openTrace = async function (id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    ZL.$("#why-title").textContent = "How this was checked: " + S.label(id);
    body.append(S.itemSection(s.token, id));
    if (!dlg.open) dlg.showModal();
  };
  // Small button for cards that have no Why? button of their own (flags, charges, could-not-verify items).
  S.traceButton = (id, cls, text) => el("button", { type: "button", class: cls || "btn btn--link", "data-testid": "btn-trace", "data-trace-for": id, "aria-label": (text || "Why this status") + ": " + S.label(id), onclick: () => S.openTrace(id) }, text || "Why this status");

  // ---- case level
  // Collapsed by default at every width to ONE line ("7/10 checks passed · 3 need you · Export blocked by 2") so the review queue stays on the first screen.
  // It expands by the human's click, or when the export gate is blocked and the human clicks Export. Passed steps stay in pipeline order inside.
  let cache = null, openPref = false, seq = 0, curDet = null;
  // T-149: the case overview block (overview.js) reads the same trace. It paints from the cached one at once and again on `zl:trace` (sent whenever a fresh trace has been stored).
  const setCache = (token, data) => { cache = { token, data }; document.dispatchEvent(new CustomEvent("zl:trace", { detail: { token, data } })); };
  S.cachedTrace = (token) => (cache && cache.token === token ? cache.data : null);
  S.statusInfo = (st) => statusInfo(st);

  // One blocker row, shared by the case rail and the message beside the Export button.
  // D-058 (T-136 F-2): a compared quote-only edit under the AI's own summary is held by the second check; writing the summary herself is the way out that always works.
  function writeSummary(b) {
    const c = ZL.state.get().case, e = c && b.reason_code === "JUDGE_NOT_RUN" && b.item_id ? [].concat(c.entries || [], c.undated_entries || []).find((x) => x.id === b.item_id) : null;
    return !!e && ZL.comparedEdit(e) && ZL.secondCheckPending(e);
  }
  // T-136 r3 (paralegal r2 F-1, D-058, T-134 r4). A compared re-picked quote under the AI's own summary is "held": its second check has no answer on the new quote. Until a rerun has tried
  // the new quote, a rerun CAN clear it, so it is offered beside "Write the summary" (the server's own sentence says both). After a rerun that gave no answer the server sets
  // `rerun_no_answer` on the blocker: a rerun can no longer clear it, so none is offered and nothing says "run it again" or "dismiss it"; only "Write the summary" remains.
  const noAnswer = (b) => !!b && b.rerun_no_answer === true;
  S.isHeld = (id) => { const c = ZL.state.get().case, e = c && id ? [].concat(c.entries || [], c.undated_entries || []).find((x) => x.id === id) : null; return !!e && ZL.comparedEdit(e) && ZL.secondCheckPending(e); };
  const heldBlockers = (g) => jnrBlockers(g).filter(writeSummary);
  const rerunBlockers = (g) => jnrBlockers(g).filter((b) => !(writeSummary(b) && noAnswer(b)));        // what a rerun can still clear
  const plainBlockers = (g) => jnrBlockers(g).filter((b) => !writeSummary(b));
  const heldNow = () => heldBlockers(gateOf(cache && cache.token === (ZL.state.get() || {}).token ? cache.data : null));
  // T-204 r2 / D-065 / D-069: a prepared answer is never "the AI's summary". `prep` (true when every held item is a prepared answer) picks the prepared twin: same facts, the item's own words. The real second check stays "second AI check".
  S.preparedFor = (id) => { const c = caseNow(), e = c && id ? [].concat(c.entries || [], c.undated_entries || []).find((x) => x.id === id) : null; return !!(e && e.prepared) || !!(c && c.models && c.models.generator_prepared); };
  S.allPrepared = (ids) => !!ids.length && ids.every((id) => S.preparedFor(id));
  const keepsWords = (n, prep) => (prep ? "the prepared wording" : "the AI's summary");
  S.HELD_NO_RERUN = (n, prep) => (n === 1 ? "You changed the quote on an accepted entry and kept " + keepsWords(n, prep) + ". The second AI check ran again and gave no answer on the new quote."
    : plural(n, "accepted entry keeps", "accepted entries keep") + " " + keepsWords(n, prep) + " under a quote you changed. The second AI check ran again and gave no answer on the new quotes.") + " Write the summary in your own words" + (n === 1 ? "." : " for each.");
  S.HELD_CAN_RERUN = (n, prep) => (n === 1 ? "You changed the quote on an accepted entry and kept " + keepsWords(n, prep) + ", and the second AI check has no answer on the new quote."
    : plural(n, "accepted entry keeps", "accepted entries keep") + " " + keepsWords(n, prep) + " under a quote you changed, and the second AI check has no answer on the new quotes.") + " Run the second check again, or write the summary in your own words.";
  // the one sentence for the held items of a gate: says what is left that can clear them
  const heldWords = (held) => { const prep = S.allPrepared(held.map((b) => b.item_id)); return held.some((b) => !noAnswer(b)) ? S.HELD_CAN_RERUN(held.length, prep) : S.HELD_NO_RERUN(held.length, prep); };
  function blockerRow(b, hideWhy) {
    const name = b.item_id ? S.label(b.item_id) : "Whole case";
    const wording = isCodeBlocker(b);
    return el("li", { class: "zs-blocker", "data-testid": "gate-blocker", "data-blocker-code": b.reason_code, "data-jump-item": b.item_id || null },
      el("span", { class: "zs-blocker-name" }, name), " ", hideWhy ? null : el("span", { class: "zs-ev" }, wording ? [el("strong", {}, S.wordingLead(b.item_id) + " "), b.why || ""] : b.why || ""),
      b.item_id ? el("button", { type: "button", class: "btn", "data-testid": "btn-gate-jump", "aria-label": "Go to item " + name, onclick: () => gotoItem(b.item_id) }, "Go to item") : null,
      writeSummary(b) ? el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-gate-write-summary", "aria-label": "Write the summary for " + name, onclick: () => S.editItem(b.item_id) }, "Write the summary") : null,
      wording ? el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-gate-edit", "aria-label": S.wordingEditText(b.item_id, b.next_action) + " for " + name, onclick: () => S.wordingFix(b.item_id, b.next_action) }, S.wordingEditText(b.item_id, b.next_action)) : null,
      null);
  }
  // Rows only offer Go to item (and Edit for a wording blocker): the one rerun button lives with the list (the gate step, the refused-export message), because one POST reruns them all.
  function blockerList(bl, title, hideWhy) {
    const sorted = orderBlockers(bl), first = sorted.slice(0, 6), rest = sorted.slice(6);
    return el("div", { class: "zs-gate", "data-testid": "gate-blockers" },
      el("p", { class: "zs-ev" }, el("strong", {}, (title || "Blocking the export") + " (" + sorted.length + "):")),
      el("ul", { class: "zs-blockers" }, first.map((b) => blockerRow(b, hideWhy))),
      rest.length ? el("details", { class: "zs-more" }, el("summary", {}, "Show the other " + rest.length), el("ul", { class: "zs-blockers" }, rest.map((b) => blockerRow(b, hideWhy)))) : null);
  }
  // D-045(a): items nobody has decided yet are a WARNING on the gate, not a blocker: they stay out of the letter and the AI disclosure line counts them.
  function warningNode(st) {
    const ws = st.warnings || [];
    if (!ws.length) return null;
    return el("div", { class: "zs-gate-warns", "data-testid": "gate-warnings" }, ws.map((w) => {
      const edit = w.reason_code === "EDIT_NOT_CONFIRMED";   // T-136 (T-134): her reworded entry is still marked Needs review; the server's own sentence says why it is not in the letter
      return el("div", { class: "zs-warnbox", "data-testid": "gate-warning", "data-warning-code": w.reason_code },
        el("p", { class: "zs-todo-text" }, el("strong", {}, (edit ? "Edit to check (" : "Not reviewed (") + (w.count != null ? w.count : "") + "): "), w.why || ""),
        el("p", { class: "zs-ev" }, "This does not block the export." + ""),
        el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "btn", "data-testid": "btn-gate-warning-jump", onclick: () => (edit ? gotoFirstEdit() : gotoFirstPending()) }, edit ? "Go to the first edit to check" : "Go to the first pending item")));
    }));
  }
  function gateNode(st) {
    const bl = st.blockers || [];
    const a = bl.length ? blockerList(bl) : null, w = warningNode(st), said = rerunNote && rerunNote.token === (ZL.state.get() || {}).token;
    return a || w || said ? el("div", {}, a, w, said && !bl.length ? rerunStatus() : null) : null;   // the last rerun sentence stays visible after the blockers are gone
  }
  function caseExtra(st) {
    if (st.id === "export_gate") return gateNode(st);
    if (st.id === "judges" && st.status === "pass") return el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "btn", "data-testid": "btn-to-judges", onclick: () => gotoPanel("judges") }, "See how the AI was checked"));
    return null;
  }
  function caseCounts(st) {
    const bits = fmtCounts(st.counts);
    return bits.length ? el("p", { class: "zs-counts", "data-testid": "step-counts" }, bits.map((b) => el("span", { class: "zs-chip" }, b))) : null;
  }
  function caseRail(tr) {
    const steps = tr.steps || [], act = activeIndex(steps), v = tr.verdict || {};
    const ctx = { testid: "case-step", level: "case", extra: (st) => { const a = caseCounts(st), b = caseExtra(st); return a || b ? el("div", {}, a, b) : null; } };
    const nr = notReviewed(steps), vc = v.code === "ready" && nr ? "ready_for_decision" : v.code || "none";   // never a green "Ready to export" while items are undecided (T-149 r3): amber, the same words as the chip
    return el("div", { class: "zs zs-case-inner" },
      el("p", { class: "zs-top" }, el("span", { class: "zs-verdict zs-v-" + vc, "data-testid": "case-verdict" }, v.code === "ready" && nr ? CAN_EXPORT(nr) : v.label || ""),
        el("span", { class: "zs-progress", role: "status", "data-testid": "case-progress" }, progressLabel(steps))),
      el("ol", { class: "zs-rail", "aria-label": "Case checks, from reading the paste to the export gate" }, steps.map((s, i) => stepNode(s, i === act, ctx))),
      el("p", { class: "zs-legend" }, "✓ passed · ✕ failed or blocked · – skipped · ○ not done yet, or waiting for you. “Needs your decision” means the next move is yours. “Code” steps are done by a program, “You” steps are your decisions, and " + (S.preparedFor(null) ? "“Prepared answer” steps are our team\u2019s wording for this demo, checked by a second AI model." : "“AI” steps are done by a model.")));
  }
  // Items the export gate would leave out of the letter because nobody decided them (the server's ITEMS_NOT_REVIEWED warning count).
  // T-174 F9: the number is the case's own open total (the header's), not the gate's warning count, which leaves out an edit she still has to compare.
  const warnedOf = (g) => { const n = ZL.openLeft ? ZL.openLeft() : null; return n != null ? n : ((g && g.warnings) || []).reduce((t, w) => t + (w.count || 0), 0); };
  const notReviewed = (steps) => { const g = steps.find((x) => x.id === "export_gate"); return g && g.status === "pass" ? warnedOf(g) : 0; };
  const CAN_EXPORT = (n) => "Can export \u2014 " + n + " not reviewed (they stay out of the letter)";
  // The one-line summary: how many checks passed, how many need the human, and what the export is waiting for.
  function summaryBits(steps) {
    const passed = steps.filter((s) => s.status === "pass").length, need = steps.filter((s) => s.status === "fail" || s.status === "pending").length;
    const gate = steps.find((s) => s.id === "export_gate"), bl = (gate && gate.blockers) || [];
    const n = gate ? (gate.counts && gate.counts.blocking) || bl.length : 0;
    let gateText = "";
    const warned = gate && gate.status === "pass" ? warnedOf(gate) : 0;
    if (gate && gate.status === "pass") gateText = warned ? "Can export \u2014 " + warned + " not reviewed" : "Ready to export";
    else if (bl.length && bl.every((b) => b.reason_code === "RUN_IN_PROGRESS")) gateText = "Export waits for the run to finish";
    else if (gate) gateText = "Export blocked by " + (n || 1);
    return { passed, need, gateText, total: steps.length };
  }
  function paintCase(host, tr) {
    clear(host);
    const steps = tr ? tr.steps || [] : [], sb = summaryBits(steps);
    const toggle = el("span", { class: "zs-toggle", "aria-hidden": "true" }, "Show");
    const sum = el("summary", { "data-testid": "case-summary" }, el("span", { class: "zs-case-title" }, "Case checks"),
      tr ? [el("span", { class: "zs-progress", "data-testid": "case-summary-progress" }, sb.passed + "/" + sb.total + " checks passed"),
        sb.gateText === "Ready to export" ? (sb.total - sb.passed ? el("span", { class: "zs-sumv", "data-testid": "case-summary-need" }, (sb.total - sb.passed) + (sb.total - sb.passed === 1 ? " check was not run" : " checks were not run")) : null)
          : sb.need ? el("span", { class: "zs-sumv", "data-testid": "case-summary-need" }, sb.need + " need you") : null,
        sb.gateText ? el("span", { class: "zs-sumv zs-sumgate", "data-testid": "case-summary-gate" }, sb.gateText) : null] : el("span", { class: "zs-progress", "data-testid": "case-summary-progress" }, "loading…"), toggle);
    const det = el("details", { class: "zs-case-det" }, sum, tr ? caseRail(tr) : el("p", { class: "muted", role: "status" }, "Loading the case checks…"));
    det.open = !!openPref;
    toggle.textContent = det.open ? "Hide" : "Show";
    det.addEventListener("toggle", () => { openPref = det.open; toggle.textContent = det.open ? "Hide" : "Show"; });
    host.append(det); curDet = det;
    // "What you need to do", visible without opening the checks: the next step that waits on the human, in the words the rail uses (T-060, paralegal F2).
    const i = tr ? activeIndex(steps) : -1, st = i >= 0 ? steps[i] : null, na = st && st.next_action;
    if (st && na) {
      const cc = caseCopy(st), text = (cc && cc.text) || na.text || "";
      if (text) host.append(el("div", { class: "zs-nextline", "data-testid": "case-next-action" },
        el("p", {}, el("strong", {}, "What you need to do: "), text),
        el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-show-next-step", onclick: () => { det.open = true; const n = det.querySelector('[data-step-id="' + st.id + '"]') || det; n.scrollIntoView({ block: "center" }); flash(n); } }, "Show this step")));
    }
  }
  // ---- the message beside the Export button. A refused export (422 judge_not_run / export_blocked) is shown right under the toolbar, scrolled into view and
  // focused, with the same Go to item list as the gate and the rerun button; never in the Export view 12,000 px further down.
  let blocked = null, curNotice = null;   // blocked: {token, message, blockers[], cleared}
  function paintNotice(host) {
    clear(host);
    const s = ZL.state.get();
    if (!blocked || blocked.token !== s.token) { host.hidden = true; return; }
    host.hidden = false;
    const bl = blocked.blockers || [], rerun = bl.some((b) => b.reason_code === "JUDGE_NOT_RUN");
    host.className = "zs-exnote" + (blocked.cleared ? " zs-exnote-ok" : "");
    host.append(el("p", { class: "zs-exnote-msg", role: blocked.cleared ? "status" : "alert", "data-testid": "export-blocked-msg" }, el("strong", {}, blocked.cleared ? "Nothing blocks the export now. " : "The export is blocked. "), (blocked.message || "").replace(/\s*The export is blocked\.?\s*$/i, "")));
    // The rerun button and its Running… / result sentence sit together right under the lead sentence, above the (possibly long) blocker list, so the answer is
    // where the pressed button is. The same status node serves the cleared message.
    if (!blocked.cleared && rerun) host.append(el("div", { class: "zs-todo-btns" }, S.rerunButton(groupLabel(bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").length))));
    host.append(rerunStatus());
    // the lead sentence already says it when it carries the blockers' own wording: say it once (T-060 r3, paralegal F8)
    const said = (blocked.message || "").replace(/\s+/g, " ");
    const dup = bl.length > 0 && bl.every((b) => b.why && said.includes(String(b.why).replace(/\s+/g, " ").trim()) && !isCodeBlocker(b));
    if (!blocked.cleared && bl.length) host.append(blockerList(bl, null, dup));
    host.append(el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "btn", "data-testid": "btn-export-blocked-close", onclick: () => { blocked = null; paintNotice(host); const b = ZL.$('[data-testid="btn-export"]'); if (b) b.focus(); } }, "Close this message")));
  }
  S.exportNotice = function () {
    const host = el("section", { "data-testid": "export-blocked", tabindex: "-1", "aria-label": "Why the export is blocked" });
    curNotice = host; paintNotice(host); return host;
  };
  S.showExportBlocked = function (err, reveal_) {
    const s = ZL.state.get();
    const d = (err && err.detail) || {};
    blocked = { token: s.token, message: (err && err.message) || "The export could not be built.", blockers: d.blockers || [] };
    if (!curNotice || !curNotice.isConnected) return false;
    paintNotice(curNotice);
    if (reveal_ !== false) {
      reveal(curNotice);
      const b = ZL.$('[data-testid="btn-export"]'), r = b && b.getBoundingClientRect();   // the button this message explains stays in view with it, so Export can be pressed again
      if (r && (r.top < 0 || r.bottom > window.innerHeight)) b.scrollIntoView({ block: "start" });
    }
    return true;
  };
  // The message must not outlive its cause: after any decision, ask the server again (GET /export has no side effects). Blockers gone -> "Nothing blocks the export now";
  // still blocked -> the current list.
  let reTimer = null;
  ZL.state.subscribe((st) => {
    if (!blocked || blocked.cleared || !st.case) return;
    clearTimeout(reTimer);
    reTimer = setTimeout(async () => {
      if (!blocked || blocked.cleared) return;
      const tok = blocked.token;
      try { await ZL.api.exportCase(tok); if (blocked && blocked.token === tok) { blocked = { token: tok, cleared: true, message: "Click Export again to open it.", blockers: [] }; if (curNotice && curNotice.isConnected) paintNotice(curNotice); } }
      catch (e) { if (blocked && blocked.token === tok && e && e.detail && Array.isArray(e.detail.blockers)) { blocked.blockers = e.detail.blockers; blocked.message = e.message || blocked.message; if (curNotice && curNotice.isConnected) paintNotice(curNotice); } }
    }, 400);
  });
  S.clearExportNotice = function () { if (blocked) { blocked = null; if (curNotice && curNotice.isConnected) paintNotice(curNotice); } };
  // After a rerun: refresh the blocker list in the message; when nothing blocks any more say so.
  function noticeAfterRerun(gate) {
    if (!blocked || !gate) return;
    if (gate.ready || !(gate.blockers || []).length) blocked = { token: blocked.token, cleared: true, message: "Every accepted item now has its second check. Click Export again.", blockers: [] };
    else { blocked.blockers = gate.blockers; blocked.message = gate.why || blocked.message; }
    if (curNotice && curNotice.isConnected) paintNotice(curNotice);
  }
  S.onExport = function () { /* the refused export shows its own message beside the button (showExportBlocked); the rail is left as the human set it */ };
  S.mountCase = function (parent, before) {
    const s = ZL.state.get(); if (!s.token || !s.case) return;
    const host = el("section", { class: "zs-case", "data-testid": "case-stepper", "aria-label": "Case checks" });
    parent.insertBefore(host, before || null);
    if (ZL.judges) ZL.judges.mount(parent, before);
    const mine = ++seq;
    if (cache && cache.token !== s.token) { cache = null; openPref = false; }
    paintCase(host, cache && cache.token === s.token ? cache.data : null);
    ZL.api.caseTrace(s.token).then((tr) => {
      const same = cache && cache.token === s.token && JSON.stringify(cache.data) === JSON.stringify(tr);
      setCache(s.token, tr);
      if (!same && host.isConnected && mine === seq) paintCase(host, tr);
    }, () => { document.dispatchEvent(new CustomEvent("zl:trace", { detail: { token: s.token, data: null, error: true } })); if (host.isConnected && !cache) host.hidden = true; });
  };
})();
