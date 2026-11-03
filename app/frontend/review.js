/* Review controls shared by entries, flags and charges (T-043, frontend-2).
   Exposes ZL.rv = { controls, act, money, chips, find, openSource, say, legend, nextId }.
   - ZL.rv.controls(item, kind) -> element with Accept / Edit / Dismiss / Reset (kind: "entry" | "flag" | "amount").
   - Registered as a row action so every timeline entry row gets the same controls (ZL.registerRowActions).
   - One document-level key handler works on ANY element that carries data-item-id (queue items, entry rows, flag and charge cards).
   Untrusted text only ever goes through ZL.el (text nodes) / textContent. No amounts are added or compared here. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const el = (...a) => ZL.el(...a);
  const RV = (ZL.rv = {});
  const drafts = {};        // id -> {open, text, reasonOpen, reason}  (survives re-renders)
  const ui = {};            // id -> {openEdit}  latest controls instance per item
  const busy = new Set();

  RV.caseNow = () => (ZL.state && ZL.state.get().case) || null;
  RV.find = function (c, id) {
    for (const [k, kind] of [["entries", "entry"], ["undated_entries", "entry"], ["amounts", "amount"], ["flags", "flag"]]) {
      const it = ((c && c[k]) || []).find((x) => x.id === id);
      if (it) return { item: it, kind };
    }
    return null;
  };
  // Display formatting of an integer-cents value by string slicing only (no arithmetic).
  RV.money = function (cents) {
    if (cents == null) return "";
    const neg = String(cents)[0] === "-";
    const s = String(cents).replace("-", "").padStart(3, "0");
    const d = s.slice(0, -2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    const c = s.slice(-2);
    return (neg ? "-" : "") + "$" + d + "." + c;   // always cents, so a column of amounts lines up and matches the letter
  };
  // Stable sort: needs_review before everything else (R-TL-5 order, applied inside each group / table).
  RV.needsReviewFirst = (list) => list.map((x, i) => [x, i]).sort((a, b) => ZL.firstRank(a[0].id, a[0].state) - ZL.firstRank(b[0].id, b[0].state) || a[1] - b[1]).map((p) => p[0]);
  // Plain JSON request for endpoints ZL.api does not wrap (mock or real). Returns {status, body}; never throws on HTTP errors.
  RV.http = async function (method, path, body) {
    if (ZL.API_MODE === "mock") return ZL.mock.handle(method, path, body);
    const res = await fetch("/api" + path, { method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined });
    let b = null; try { b = await res.json(); } catch (_) { /* empty body */ }
    return { status: res.status, body: b };
  };
  RV.errMsg = (r, fallback) => (r && r.body && r.body.error && r.body.error.message) || fallback || "That did not work.";
  RV.label = (item) => item.title || (item.provider ? item.provider + (item.date ? ", " + item.date : "") : null) || item.text || item.id;

  const REVIEW_LABEL = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const STATE_LABEL = { verified: "Quote matches", needs_review: "Needs review", rejected: "Could not verify" };
  const STATE_TONE = { verified: ["info", "match"], needs_review: ["warn", "alert"], rejected: ["bad", "x"] };
  const DECISION = { accepted: ["ok", "check"], edited: ["ok", "pencil"], dismissed: ["muted", "dash"] };
  RV.chips = function (item) {   // machine state, then (only once decided) the human decision: two chips, two icons
    const t = STATE_TONE[item.state] || ["muted", "info"], d = DECISION[item.review_status];
    // T-114 r3: a decided rate / estimate / unclear amount reads one chip, "Accepted" (kept in the internal notes): its "Needs review" doubt is what she just resolved
    if (item.review_status === "dismissed") return el("span", { class: "rv-chips" }, el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-chip": "review" }, REVIEW_LABEL.dismissed));   // T-060 r5 (paralegal M1): a dismissed item is decided; it no longer reads "Needs review"
    const noted = item.accept_effect && item.accept_effect !== "letter_total" && (item.review_status === "accepted" || item.review_status === "edited");
    if (noted) return el("span", { class: "rv-chips" }, el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-chip": "review" }, REVIEW_LABEL[item.review_status]));
    return el("span", { class: "rv-chips" },
      el("span", { class: "chip chip--" + t[0], "data-icon": t[1], "data-chip": "state" }, STATE_LABEL[item.state] || item.state),
      d ? el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-chip": "review" }, REVIEW_LABEL[item.review_status]) : null);
  };

  // ---- live region: created once at load (a region that appears with its first message is often not announced)
  let live;
  function liveRegion() { if (!live) { live = document.getElementById("rv-live") || el("div", { id: "rv-live", class: "rv-sr", "aria-live": "polite", role: "status" }); if (!live.isConnected) document.body.append(live); } return live; }
  if (document.body) liveRegion(); else document.addEventListener("DOMContentLoaded", liveRegion);
  RV.say = function (msg, isError) {
    const l = liveRegion();
    l.textContent = "";
    setTimeout(() => { l.textContent = msg; }, 20);
    l.setAttribute("role", isError ? "alert" : "status");
  };

  // ---- open the source record(s) of an item (R-RV-9); entries/amounts: one record, flags: every record in the evidence
  RV.sourceTargets = function (item, kind) {
    if (kind === "flag") {   // one span per record, so a two-record flag opens both records once each
      const seen = {}, spans = [];
      (item.evidence || []).forEach((e) => { if (!seen[e.record_id]) { seen[e.record_id] = 1; spans.push({ record_id: e.record_id, start: e.start, end: e.end }); } });
      return { ids: spans.map((s) => s.record_id), spans };
    }
    if (kind === "entry" && typeof ZL.entrySpans === "function") { const spans = ZL.entrySpans(item); return { ids: spans.map((s) => s.record_id), spans }; }
    const ids = item.record_ids || [];
    return { ids, spans: ids.length ? [{ record_id: ids[0], start: item.excerpt_start, end: item.excerpt_end }] : [] };
  };
  RV.openSource = function (item, kind, title) {   // T-042's modal: ZL.openSource(spans, title)
    const t = RV.sourceTargets(item, kind);
    if (!t.spans.length || typeof ZL.openSource !== "function") return;
    const c = RV.caseNow(), seqs = t.ids.map((id) => { const r = ((c && c.records) || []).find((x) => x.id === id); return r ? r.seq : id; });
    ZL.openSource(t.spans, title || (seqs.length > 1 ? "Records " + seqs.join(" and ") : "Record " + seqs[0]));
  };

  // ---- one linear queue in page order (T-060, paralegal F1). Items are every [data-item-id] row that is on screen, in document order: dates to confirm,
  // the timeline rows (needs review first), the could-not-verify tray, flags, charges. j / k walk that list; a / d / Enter-on-a-button advance to the next
  // item that still needs a decision, needs-review ones before verified ones.
  const NOT_QUEUE = "dialog, .sbs-pane";
  RV.itemRowOf = function (t) {   // the item row that holds focus, or null (focus on Export, the header, a dialog or the page body is not "in" the queue)
    const r = t && t.closest && t.closest("[data-item-id]");
    return r && !r.closest(NOT_QUEUE) ? r : null;
  };
  // T-136 (paralegal pass 5 F2): dismissed flags and amounts wait in a collapsed "Dismissed (n)" group inside their own panel, like dismissed entries do under the timeline. Not in the letter; each keeps Undo.
  // The group opens for the item she just dismissed (so she sees where it went) and stays as she leaves it.
  ZL.dismissedOpenBy = ZL.dismissedOpenBy || {};
  // T-162 r2: a collapsed Dismissed group says how many of its items carry a re-run note, so a note on a dismissed item is not hidden behind a closed fold.
  RV.rerunMarker = (body) => {
    const n = body.querySelectorAll('[data-testid="rerun-note"]').length;
    return n ? el("span", { class: "rv-rerun-marker", "data-testid": "rerun-marker" }, " " + n + (n === 1 ? " has a re-run note." : " have re-run notes.")) : null;
  };
  RV.dismissedBox = function (kind, count, body) {
    const d = el("details", { class: "dismissed-group", "data-testid": "dismissed-group-" + kind, open: ZL.dismissedOpenBy[kind] || null },
      el("summary", { "data-testid": "dismissed-summary-" + kind }, "Dismissed (" + count + ")", el("span", { class: "muted small" }, " Not in the letter. Open to read them or press Undo."), RV.rerunMarker(body)), body);
    d.addEventListener("toggle", () => { ZL.dismissedOpenBy[kind] = d.open; });
    return d;
  };
  RV.domItems = () => Array.from(document.querySelectorAll("[data-item-id]")).filter((n) => !n.closest(NOT_QUEUE) && n.offsetParent !== null);
  const decidable = (n) => { const rs = n.getAttribute("data-review"); return (rs === "pending" || (rs === "edited" && n.hasAttribute("data-edit-check"))) && n.getAttribute("data-state") !== "rejected" && !n.hasAttribute("data-tray-kind"); };
  RV.nextPendingAfter = function (items, at) {   // items after `at` first, then wrapping. Order of preference: a needs-review entry in the timeline, then any needs-review item, then any item that still needs a decision
    const order = items.slice(at + 1).concat(items.slice(0, Math.max(at, 0) + (at < 0 ? 0 : 1)));
    const open = order.filter(decidable), needs = (n) => n.getAttribute("data-state") === "needs_review";
    return open.find((n) => needs(n) && n.closest('[data-testid="queue"]')) || open.find(needs) || open[0] || null;
  };
  // T-060 r5 (ux F3): after a / d the next row is the next row of the SAME list (the timeline, one flag kind, the charges table, the unclear table). It is never a row of another
  // kind: a run of `a a a` down the timeline can not accept a conflict flag. "The next item that needs a decision anywhere" is Start review's job only.
  const GROUP = '[data-group], [data-testid="queue"], [data-testid="dates-to-confirm"]';
  const groupKey = (g) => (g.hasAttribute("data-group") ? '[data-group="' + g.getAttribute("data-group") + '"]' : g.getAttribute("data-testid") ? '[data-testid="' + g.getAttribute("data-testid") + '"]' : null);
  const groupName = (g) => g.hasAttribute("data-group") ? (g.querySelector(":scope > h3") ? g.querySelector(":scope > h3").textContent.replace(/\s*\(\d+\)\s*$/, "") : g.getAttribute("data-group") === "charges" ? "Charges" : g.getAttribute("data-group") === "unclear-amounts" ? "Unclear amounts" : g.getAttribute("data-group"))
    : g.getAttribute("data-testid") === "queue" ? "Timeline" : g.getAttribute("data-testid") === "dates-to-confirm" ? "Dates to confirm" : "this list";
  const rowsIn = (g) => Array.from(g.querySelectorAll("[data-item-id]")).filter((n) => !n.closest(NOT_QUEUE) && n.offsetParent !== null);
  RV.planAdvance = function (id) {
    const ae = document.activeElement, mine = ae && ae.closest && ae.closest("[data-item-id]");
    const row = mine && mine.getAttribute("data-item-id") === id ? mine : document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]') || document.querySelector('[data-item-id="' + id + '"]');
    const g = row && row.closest(GROUP), key = g && groupKey(g);
    return key ? { key, ids: rowsIn(g).map((n) => n.getAttribute("data-item-id")), id } : { key: null, ids: [], id };
  };
  function focusNode(t) {
    if (!t) return false;
    if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "0");
    t.focus({ preventScroll: true }); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" });
    return true;
  }
  function focusItem(id) {
    const q = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]');
    return focusNode(q || document.querySelector('[data-item-id="' + id + '"]'));
  }
  // T-174 F8: "the first item" is ONE item. The case overview names it (case.next_action, the line "Do this first", data-do-first-item); the skip link, Start review and the n key all go there. Only when
  // the server names none (or the item is not on screen) does it fall back to the first row that needs a decision, needs-review ones first.
  RV.firstItemId = function () { const box = document.querySelector('[data-testid="case-overview"]'); return box ? box.getAttribute("data-do-first-item") : null; };
  RV.focusFirstPending = function () {
    const named = RV.firstItemId(); if (named && ZL.stepper && ZL.stepper.goto && ZL.stepper.goto(named)) return true;
    const items = RV.domItems(); const t = items.filter(decidable).find((n) => n.getAttribute("data-state") === "needs_review") || items.find(decidable) || items[0];
    return focusNode(t);
  };
  function focusExport(msg) { const b = document.querySelector('[data-testid="btn-export"]'); if (b) { b.focus(); if (msg) RV.say(msg); } }
  function restoreFocus(pf) {
    if (!pf) return;
    requestAnimationFrame(() => {
      if (pf.nextFrom) {
        const plan = pf.plan || { key: null, ids: [], id: pf.nextFrom }, g = plan.key && document.querySelector(plan.key);
        const now = new Map((g ? rowsIn(g) : []).map((n) => [n.getAttribute("data-item-id"), n]));
        const at = plan.ids.indexOf(plan.id), order = plan.ids.slice(at + 1).concat(plan.ids.slice(0, Math.max(at, 0)));
        const t = order.map((i) => now.get(i)).filter(Boolean).find(decidable);
        if (t) { focusNode(t); return; }
        const c = RV.caseNow(), left = c ? ZL.progressOf(c).left : 0;
        if (!left) { focusExport("Nothing left to decide. Export is next."); return; }   // the last decision: the next control is the one that finishes the job, not the top of the page
        // this list is finished but others are not: T-166 F6 moves focus on to the first open item of the NEXT list (page order, wrapping at the end) and says so. It never decides that item:
        // a or d on it is a new press. "The next item anywhere" (Start review, n) is the same move from any row.
        const g0 = plan.key && document.querySelector(plan.key), all = RV.domItems().filter((n) => decidable(n) && !(g0 && g0.contains(n)));
        const after = g0 ? all.filter((n) => g0.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_FOLLOWING) : all, nx = after[0] || all[0];
        if (nx) {
          focusNode(nx);
          const f = RV.find(RV.caseNow(), nx.getAttribute("data-item-id")), ng = nx.closest(GROUP);
          RV.say((g0 ? groupName(g0) + " done. " : "") + "Next: " + (ng ? groupName(ng) + ", " : "") + (f ? RV.ghostLabel(f.item) : "the next item") + ". " + left + (left === 1 ? " item is" : " items are") + " still open.");
          return;
        }
        const stay = now.get(plan.id) || order.map((i) => now.get(i)).filter(Boolean)[0];
        if (stay) focusNode(stay); else { const s = document.querySelector('[data-testid="btn-start-review"]'); if (s) s.focus(); }
        RV.say("Nothing more to decide here. " + left + (left === 1 ? " item is" : " items are") + " still open, but each needs something other than a plain decision (a date, a check of your wording).");
        return;
      }
      if (pf.action === "dismiss") {   // T-166 F5: the dismissed row is now a placeholder in its slot; focus its Undo (never the row's old buttons, which moved to the Dismissed group, often off screen)
        const u = document.querySelector('[data-ghost-for="' + pf.id + '"] button');
        if (u) { u.focus({ preventScroll: true }); u.scrollIntoView({ block: "nearest" }); return; }
      }
      const root = document.querySelector('[data-controls-for="' + pf.id + '"]');
      const t = root && (root.querySelector('[data-action="' + pf.action + '"]') || root.querySelector("button"));
      if (t) { t.focus({ preventScroll: true }); t.scrollIntoView({ block: "nearest" }); } else focusItem(pf.id);
    });
  }

  // T-166 F11/F7: a row keeps the four things she does most (Accept, Edit, Dismiss, Open record); the rest (Why this status, Change quote, Audit, Dismiss with a reason) wait behind one "More" button.
  // Returns {btn, panel}: put btn where the link row ends and panel right after it (the panel's buttons then follow it in Tab order and flow in the same line when it is open).
  RV.moreActions = function (items, name, o) {
    const opt = o || {}, panel = el("div", { class: "rv-more-panel", hidden: !opt.open, "data-testid": opt.panelTestid || "more-panel" }, items.filter(Boolean));
    const btn = el("button", { type: "button", class: "btn btn--link rv-more-btn", "data-testid": opt.testid || "btn-more", "aria-expanded": String(!!opt.open), "aria-label": "More actions: " + name,
      onclick: () => { const on = panel.hidden; panel.hidden = !on; btn.setAttribute("aria-expanded", String(on)); btn.textContent = on ? "Less" : "More"; btn.setAttribute("aria-label", (on ? "Less actions: " : "More actions: ") + name); if (opt.onToggle) opt.onToggle(on); } }, opt.open ? "Less" : "More");
    return { btn, panel };
  };

  // T-166 F5: a dismissed row leaves a placeholder in its own slot for six seconds ("Dismissed: Capital PT, visit 8. Undo"), so the click has a visible result where she clicked and the way back is right there.
  // Then it collapses into the Dismissed (n) group. The page repaints on every change, so each placeholder is re-inserted after every paint (zl:panels) at the position it was captured at:
  // before the row that followed it (or after the row that preceded it, or first in its list).
  const GHOST_MS = 6000, ghosts = new Map();   // id -> {id, label, key, nextId, prevId, tr, timer}
  RV.ghostLabel = (item) => (item.provider ? item.provider + (item.date ? ", " + ZL.fmtDate(item.date) : "") : RV.label(item));
  function slotOf(id) {
    const ae = document.activeElement, mine = ae && ae.closest && ae.closest("[data-item-id]");
    const row = mine && mine.getAttribute("data-item-id") === id ? mine : document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]') || document.querySelector('[data-item-id="' + id + '"]');
    const g = row && row.closest(GROUP), key = g && groupKey(g); if (!row || !key) return null;
    const near = (n, dir) => { let x = row; while ((x = dir > 0 ? x.nextElementSibling : x.previousElementSibling)) { if (x.hasAttribute("data-item-id")) return x.getAttribute("data-item-id"); } return null; };
    return { key, nextId: near(row, 1), prevId: near(row, -1), tr: row.tagName === "TR" };
  }
  function ghostNode(g) {
    const undo = el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-undo-dismiss", "aria-label": "Undo dismissing " + g.label, onclick: () => RV.act(g.id, { action: "reset" }, { focus: "reset" }) }, "Undo");
    const msg = el("span", { class: "rv-ghost-msg" }, el("strong", {}, "Dismissed: "), g.label, " ");
    return g.tr ? el("tr", { class: "rv-ghost", "data-testid": "dismiss-ghost", "data-ghost-for": g.id }, el("td", { colspan: "4" }, msg, undo))
      : el("div", { class: "rv-ghost", "data-testid": "dismiss-ghost", "data-ghost-for": g.id }, msg, undo);
  }
  let ghostFocus = null;   // the id whose placeholder button holds (or just held) focus
  document.addEventListener("focusin", (ev) => { const g = ev.target && ev.target.closest ? ev.target.closest('[data-testid="dismiss-ghost"]') : null; ghostFocus = g ? g.getAttribute("data-ghost-for") : null; });
  function placeGhosts() {
    // T-174 N3: every repaint rebuilds the placeholders; focus that sat on one's Undo must move to the new Undo, not fall to the page (the 1-in-2 failure of the charge-dismiss spec).
    const ae = document.activeElement, held = ae && ae.closest ? ae.closest('[data-testid="dismiss-ghost"]') : null;
    const heldId = held ? held.getAttribute("data-ghost-for") : (!ae || ae === document.body) && ghostFocus && ghosts.has(ghostFocus) ? ghostFocus : null;   // the repaint may already have removed the focused node: focus is then on the page and the last focusin tells where it was
    document.querySelectorAll('[data-testid="dismiss-ghost"]').forEach((n) => n.remove());
    const c = RV.caseNow();
    ghosts.forEach((g) => {
      const f = c && RV.find(c, g.id);
      if (!f || f.item.review_status !== "dismissed") { dropGhost(g.id, false); return; }
      const box = document.querySelector(g.key); if (!box) return;
      const rowOf = (id) => id && box.querySelector('[data-item-id="' + id + '"]'), node = ghostNode(g);
      const nxt = rowOf(g.nextId), prv = rowOf(g.prevId);
      if (nxt) nxt.before(node);
      else if (prv) prv.after(node);
      else { const tb = box.querySelector("tbody"), h = box.querySelector(":scope > h3"); if (tb) tb.prepend(node); else if (h) h.after(node); else box.prepend(node); }
    });
    if (heldId) { const u = document.querySelector('[data-ghost-for="' + heldId + '"] button'); if (u) u.focus({ preventScroll: true }); }
  }
  function dropGhost(id, refocus) {
    const g = ghosts.get(id); if (!g) return;
    clearTimeout(g.timer); ghosts.delete(id);
    const n = document.querySelector('[data-ghost-for="' + id + '"]');
    if (n) {
      const held = n.contains(document.activeElement), nb = n.nextElementSibling && n.nextElementSibling.hasAttribute("data-item-id") ? n.nextElementSibling : (n.previousElementSibling && n.previousElementSibling.hasAttribute("data-item-id") ? n.previousElementSibling : null);
      n.remove();
      if (held && refocus !== false) { if (nb) focusNode(nb); else { const s = document.querySelector('[data-testid="btn-start-review"]'); if (s) s.focus(); } }
    }
  }
  function addGhost(id, item, slot) {
    if (!slot) return;
    dropGhost(id, false);
    const g = Object.assign({ id, label: RV.ghostLabel(item) }, slot);
    g.timer = setTimeout(() => dropGhost(id, true), GHOST_MS); ghosts.set(id, g);
  }
  document.addEventListener("zl:panels", placeGhosts);
  RV.ghostCount = () => ghosts.size;

  // The server names a refused number the way it compares it ("9000"). Show it the way the paralegal typed it ("$9,000"): swap the first matching figure in the message for the
  // same figure as it appears in her own text. Display only; nothing is added or compared.
  RV.asTyped = function (msg, tokens, text) {
    let out = String(msg || "");
    (tokens || []).forEach((tok) => {
      if (!/^\d[\d.]*$/.test(String(tok))) return;
      const re = /\$?\s?\d[\d,]*(?:\.\d+)?/g; let m, typed = null;
      while ((m = re.exec(text || "")) && !typed) { const bare = m[0].replace(/[$,\s]/g, ""); if (bare === tok || bare.replace(/\.0+$/, "") === tok) typed = m[0].trim(); }
      if (!typed || typed === tok) return;
      out = out.replace(new RegExp("(^|[^\\d$,.])" + String(tok).replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![\\d,]|\\.\\d)"), (_, pre) => pre + typed);
    });
    return out;
  };
  // What happened to an edit, in plain words, kept on the row until the next decision: the code re-checks the wording against the quote on every save, then a second AI check reads it.
  const rechecks = {};   // id -> sentence
  // T-136 (paralegal pass 5 F1): the confirmation "I compared it with the quote" is a statement by the paralegal. The a key (and Start review, which lands on this row) must not make it for her:
  // a asks, in a visible line, and puts focus on the button; she records it by clicking the button or pressing Enter on it.
  const comparePrompt = new Set();
  const COMPARE_PROMPT = "Not recorded yet. Read the quote against your edit. Then click \u201cI compared it with the quote\u201d, or press Enter on it, to say you did.";
  // T-179 / D-066: the same statement for an item the second AI check disputed. Nothing is sent by the a key; the button says it, and the server refuses an accept without it.
  const DISPUTE_PROMPT = "Not recorded yet. Read the quote against the summary. Then click \u201cI compared it with the quote\u201d, or press Enter on it, to say you did.";
  const disputeHint = (item) => (ZL.DISPUTE_SENTENCE[ZL.judgeDispute(item)] || "The second AI check did not agree.") + " Read it against the quote, then press \u201cI compared it with the quote\u201d to say you did. Until then it stays open.";
  // T-136 r2 / D-058 (paralegal F-2): a re-picked quote keeps the AI's summary, and its second check has no answer on the new quote. Accepting alone does not put it in the letter. The words are the
  // server's (item trace "human" step, case trace blocker); the sentences below are only what shows until they arrive or when they cannot be loaded, and say the same thing.
  // Conditional on purpose (T-134 r4b, staff review): before she accepts the gate PASSES and nothing is blocked; D-044 blocks only after she accepts. The server's sentence replaces this one as soon as it arrives.
  const AI_HELD = "You changed the quote, but the summary is still the AI's wording and its second AI check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers or you edit the summary in your own words.";
  const ACCEPTED_HELD = "Compared by you. The second AI check still has no answer on the new quote, so the export stays blocked until it answers or you write the summary in your own words.";
  // T-204 / D-065 / D-069: for a prepared answer (item.prepared, or the case's models.generator_prepared) the fallback is the prepared twin of the sentence (the same words as the server's TRACE_WHY_PREPARED),
  // never the AI-worded one, so the first paint and the swap both say "prepared wording". Keyed by the item, not by rewriting the AI text.
  const PREPARED_HELD = "You changed the quote, but the summary is still the prepared wording and its second check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers or you edit the summary in your own words.";
  const PREPARED_ACCEPTED_HELD = "Compared by you. The second check still has no answer on the new quote, so the export stays blocked until it answers or you write the summary in your own words.";
  const isPrepared = (item) => { const c = ZL.state.get().case; return !!(item && item.prepared) || !!(c && c.models && c.models.generator_prepared); };
  const heldText = (item) => (isPrepared(item) ? PREPARED_HELD : AI_HELD);
  const serverText = new Map();   // "item:<id>" | "blocker:<id>" -> the server's sentence for this page load
  function withServerText(node, key, load, prefix) {   // paint the fallback now; swap in the server's sentence when it arrives
    const set = (t) => { node.textContent = (prefix || "") + t; };
    if (serverText.has(key) && !key.startsWith("blocker:")) { set(serverText.get(key)); return node; }   // a blocker sentence changes with each rerun: ask again
    load().then((t) => { if (t) { serverText.set(key, t); if (node.isConnected) set(t); } }).catch(() => {});
    return node;
  }
  const loadItemWhy = (id) => () => ZL.api.trace(ZL.state.get().token, id).then((tr) => { const h = ((tr && tr.steps) || []).find((x) => x.id === "human"); return h && h.why ? h.why : null; });   // as given: whatever the server says about this item (no pattern test on its words)
  const loadBlockerWhy = (id) => () => ZL.api.caseTrace(ZL.state.get().token).then((tr) => { const g = ((tr && tr.steps) || []).find((x) => x.id === "export_gate"), b = ((g && g.blockers) || []).find((x) => x.item_id === id && x.reason_code === "JUDGE_NOT_RUN"); return b && b.why ? "Compared by you. " + b.why : null; });
  const comparePromptNode = (item) => {
    const base = ZL.editToCheck(item) ? COMPARE_PROMPT : DISPUTE_PROMPT;
    const p = el("p", { class: "rv-help rv-compare-prompt", "data-testid": "edit-compare-prompt" }, base + (ZL.editToCheck(item) && ZL.secondCheckPending(item) ? " " + heldText(item) : ""));
    if (ZL.editToCheck(item) && ZL.secondCheckPending(item)) withServerText(p, "item:" + item.id, loadItemWhy(item.id), base + " ");
    return p;
  };
  function askCompare(id) {
    comparePrompt.add(id);
    const root = document.querySelector('[data-controls-for="' + id + '"]'); if (!root) return;
    const f = RV.find(RV.caseNow(), id);
    let p = root.querySelector('[data-testid="edit-compare-prompt"]');
    if (!p) { p = comparePromptNode(f.item); const h = root.querySelector('[data-testid="edit-check-hint"], [data-testid="dispute-compare-hint"]'); if (h) h.after(p); else root.append(p); }
    const b = root.querySelector('[data-testid="btn-accept"]'); if (b) b.focus();
    RV.say(p.textContent);
  }
  function recheckSentence(resp) {
    const w = (resp && resp.warnings) || [], st = resp && resp.item && resp.item.state;
    const lead = "Saved and re-checked. The code compared every number, date and negation in your wording with the quote and found no difference.";
    if (w.length) return lead + " " + w.map((x) => x.message).filter(Boolean).join(" ") + " Compare it with the quote yourself.";
    return lead + (st === "needs_review" ? " The entry still needs your review." : " The second AI check agreed.");
  }

  // ---- errors (R-RV-3, D-034, D-047). A refused edit is a hard 422 whose plain-words reason is shown right under the edit box, which stays open with the typed text.
  // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
  // m2: a refused edit is tied to its field (aria-invalid + aria-describedby) as well as announced
  function markInvalid(id, s) { const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (!ta || !s) return; s.id = s.id || "rv-err-" + id; ta.setAttribute("aria-invalid", "true"); ta.setAttribute("aria-describedby", s.id); }
  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) { s.textContent = msg; markInvalid(id, s); } RV.say(msg, true); }
  const nextCode = (e) => { const n = e && e.detail && e.detail.next_action; return n && n.code ? String(n.code).toUpperCase() : null; };   // T-104: EDIT_SUMMARY | EDIT_QUOTE
  const QUOTE = "Change the quote";
  const changeQuote = (id) => () => { if (ZL.stepper && ZL.stepper.changeQuote) ZL.stepper.changeQuote(id); };
  // T-104: CODE_CHECK_FAILED returned by an EDIT: the server's sentence sits under the edit box (the box stays open with the typed text); EDIT_QUOTE adds a Change the quote action.
  function showEditRefusal(id, e) {
    const ta0 = document.querySelector('[data-controls-for="' + id + '"] textarea');
    const s = slot(id, "rv-error"), msg = RV.asTyped(e.message || "That wording fails a check. Edit it to match the quote.", e.detail && e.detail.tokens, ta0 ? ta0.value : "");
    if (s) {
      ZL.clear(s);
      s.append(el("span", { "data-testid": "edit-refused-msg" }, msg));
      if (nextCode(e) === "EDIT_QUOTE") s.append(" ", el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-edit-refused-quote", "aria-label": QUOTE + " for " + (ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id), onclick: changeQuote(id) }, QUOTE));
    }
    markInvalid(id, s);
    RV.say("Not saved: " + msg, true);
    const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
  }

  // ---- D-051 (T-098 r2): Accept is refused with 422 CODE_CHECK_FAILED when the summary fails a code check. The server's plain reason (it ends "Edit the summary to match the
  // quote.") shows right under the item's buttons with an Edit action; nothing was changed. It stays until the item changes (any successful decision) or the paralegal edits.
  const refusals = {};       // id -> {message}
  function paintRefusal(root, id, edit) {
    const r = refusals[id], box = root.querySelector(".rv-refused");
    if (!box) return;
    ZL.clear(box); box.hidden = !r;
    if (!r) return;
    box.append(el("p", { class: "rv-refused-msg", "data-testid": "accept-refused-msg" }, el("strong", {}, "Not accepted. "), r.message),
      r.code === "EDIT_QUOTE"   // T-104: the first failing check is on the quote, so the fix is the quote, not the summary
        ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-accept-refused-quote", "aria-label": QUOTE + " for " + r.label, onclick: changeQuote(r.id) }, QUOTE)
        : edit ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-accept-refused-edit", "aria-label": "Edit the summary for " + r.label, onclick: edit }, "Edit the summary") : null);
  }
  // T-158: the refused-Accept box must end up fully on screen, clear of the sticky header. The layout is still moving right after the click (the case trace and the panels repaint, the sticky
  // header can change height, the list re-renders and the box node is rebuilt), so one scroll at click time is not enough: scroll now, again on the next two frames, and once more after the
  // repaints have settled. Each pass looks the box up again by item id and does nothing when it is already inside the viewport.
  function showRefusalInView(id) {
    const pass = () => {
      const row = document.querySelector('[data-controls-for="' + id + '"]'), box = row && row.querySelector(".rv-refused:not([hidden])");
      if (!box) return;
      const hdr = document.querySelector('[data-testid="app-header"]'), top = hdr ? Math.max(hdr.getBoundingClientRect().bottom, 0) + 8 : 60, r = box.getBoundingClientRect();
      if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16);
      else if (r.top < top) window.scrollBy(0, r.top - top);
    };
    pass(); requestAnimationFrame(() => { pass(); requestAnimationFrame(pass); }); setTimeout(pass, 250); setTimeout(pass, 700);
  }
  RV.clearRefusal = (id) => { if (refusals[id]) { delete refusals[id]; repaintRefusal(id); } };   // T-108: a saved quote change ends the refused-Accept box at once
  function repaintRefusal(id) { document.querySelectorAll('[data-controls-for="' + id + '"]').forEach((root) => paintRefusal(root, id, root._openEdit)); }
  RV.isCodeCheckRefusal = (e) => !!e && String(e.code).toUpperCase() === "CODE_CHECK_FAILED";

  // ---- D-041: an entry with no confirmed date cannot be accepted into the letter
  const DATE_FIRST = "Confirm the date first.", DATE_WHY = "This entry has no confirmed date, so it cannot go into the letter yet. Pick the right date in Dates to confirm.";
  RV.needsDate = (item, kind) => kind === "entry" && !item.date;
  function goToDateRow(id) {   // the entry's own row sits in Dates to confirm: move focus to its date choices
    const row = document.querySelector('[data-testid="dates-to-confirm"] [data-entry-id="' + id + '"]');
    const t = row && (row.querySelector('[data-testid="confirm-date"]:checked') || row.querySelector('[data-testid="confirm-date"]') || row);
    const box = document.querySelector('[data-testid="dates-to-confirm"]');
    const f = t || box; if (!f) return;
    if (!f.hasAttribute("tabindex") && !/^(BUTTON|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1");
    f.focus(); if (f.scrollIntoView) f.scrollIntoView({ block: "center" });
  }

  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
  RV.act = async function (id, body, opts) {
    const o = opts || {}; const c = RV.caseNow();
    if (!c || busy.has(id)) return false;
    const found = RV.find(c, id);
    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
    if (body.action === "accept" && !body.confirm && found && found.kind === "amount" && found.item.confirm_required && found.item.flag && ZL.confirmCharge) {   // D-059 (T-154): a flagged charge is counted only after she names the flag
      busy.add(id); const ok = await ZL.confirmCharge(found.item.flag, found.item); busy.delete(id);
      if (!ok) return false;
      body = Object.assign({}, body, { confirm: found.item.flag.confirm_with });
    }
    busy.add(id);
    const plan = o.advance ? RV.planAdvance(id) : null;   // the list she is working in, read before the repaint
    const slot = body.action === "dismiss" ? slotOf(id) : null;   // T-166 F5: where the row sits now, for its placeholder
    try {
      const resp = await ZL.api.review(c.token, id, body);
      comparePrompt.delete(id);
      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }
      if (drafts[id] && body.action === "edit") drafts[id].open = false;
      if (drafts[id] && body.action === "dismiss") { drafts[id].reasonOpen = false; drafts[id].reason = ""; }
      if (body.action === "edit" && found && found.kind === "entry") rechecks[id] = recheckSentence(resp); else delete rechecks[id];
      if (body.action === "dismiss" && found && found.kind === "entry") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo
      else if (body.action === "dismiss" && found) ZL.dismissedOpenBy[found.kind === "amount" ? "amounts" : "flags"] = true;   // a flag or amount does the same in its own panel
      if (body.action === "dismiss" && found) addGhost(id, found.item, slot); else if (body.action === "reset") dropGhost(id, false);
      ZL.state.applyReview(resp);
      if (rechecks[id]) RV.say(rechecks[id]);
      const left = ZL.progressOf(RV.caseNow() || c).left;   // T-166 F9: the one open count (the same number as the header: undecided items, including an edit still to check)
      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
      restoreFocus(o.advance ? { nextFrom: id, plan } : o.focus ? { id, action: o.focus } : null);
      return true;
    } catch (e) {
      if (RV.isCodeCheckRefusal(e) && body.action === "edit") showEditRefusal(id, e);   // T-104: inline under the edit box, typed text kept, not the generic path
      else if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
        const d = e.detail || {}, ta0 = document.querySelector('[data-controls-for="' + id + '"] textarea'), typed = ta0 ? ta0.value : "";
        const toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || "").includes(d.tokens[0]) ? " Not in the quote: " + d.tokens.join(", ") + "." : "";
        showError(id, RV.asTyped((e.message || "That edit is not allowed.") + toks, d.tokens, typed));
        const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
      } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
        refusals[id] = { id, code: nextCode(e), message: RV.asTyped(e.message || "The summary fails a check. Edit the summary to match the quote.", e.detail && e.detail.tokens, (found && found.item && ((found.item.edited && found.item.edited.summary) || found.item.summary)) || ""), label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
        repaintRefusal(id); RV.say("Not accepted: " + refusals[id].message, true);
        showRefusalInView(id);
      } else if (e && String(e.code).toUpperCase() === "CONFIRM_REQUIRED" && body.action === "accept" && !body.confirm && ZL.confirmCharge) {   // D-059: the page did not know the charge was flagged; the server's flag opens the same confirm
        const d = e.detail || {}; busy.delete(id);
        const ok = await ZL.confirmCharge({ flag: d.flag, name: d.name, message: d.message || e.message, confirm_with: d.confirm_with }, found && found.item);
        if (ok) return RV.act(id, Object.assign({}, body, { confirm: d.confirm_with }), o);
        return false;
      } else if (e && String(e.code).toUpperCase() === "COMPARE_REQUIRED" && body.action === "accept" && !body.compared) {   // D-066: the page did not know the second check disputed it; ask for the compare, record nothing
        comparePrompt.add(id); showError(id, e.message || "Compare it with the quote first."); const b = document.querySelector('[data-controls-for="' + id + '"] [data-testid="btn-accept"]'); if (b) b.focus();
      } else if (e && String(e.code).toUpperCase() === "DATE_UNCONFIRMED") showError(id, DATE_FIRST + " " + DATE_WHY);
      else showError(id, (e && e.message) || "That did not work. Try again.");
      return false;
    } finally { busy.delete(id); }
  };

  // T-162 (T-146): a re-run that disagreed with or failed on a decided item kept it as it was and left a note; the server's sentence is shown beside the item and in its trace.
  RV.rerunNote = (item) => el("p", { class: "rv-reason-line rv-rerun-note", role: "note", "data-testid": "rerun-note" }, el("strong", {}, "Re-run: "), item.rerun_note);
  RV.rerunNoteFor = (id) => { const c = RV.caseNow(), f = c && RV.find(c, id); return f && f.item.rerun_note ? RV.rerunNote(f.item) : null; };

  // T-166 F12: Undo (or r) on an item she edited would throw her wording away with no way back. It asks first, inline, with Keep as the focused answer; nothing is sent until she says Discard.
  const discardOpen = new Set();
  const wordsOf = (item) => (item.edited && item.edited.original_excerpt != null && item.edited.original_summary == null ? "your change to the quote" : "your wording");
  function discardBox(id, item) {
    const keep = () => { discardOpen.delete(id); const root = document.querySelector('[data-controls-for="' + id + '"]'), b = root && root.querySelector('[data-testid="discard-confirm"]'); if (b) b.remove(); const r = root && root.querySelector('[data-action="reset"]'); if (r) r.focus(); RV.say("Kept " + wordsOf(item) + "."); };
    const w = wordsOf(item), box = el("div", { class: "rv-help rv-discard", role: "group", "aria-label": "Confirm undo", "data-testid": "discard-confirm" },
      el("p", {}, "Undo will throw away " + w + " and bring back the original. Discard " + w + "?"),
      el("div", { class: "rv-actions" },
        el("button", { type: "button", class: "btn", "data-testid": "btn-discard-edit", onclick: () => { discardOpen.delete(id); RV.act(id, { action: "reset" }, { focus: "reset" }); } }, "Discard " + w),
        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-keep-edit", onclick: keep }, "Keep " + w)));
    box.addEventListener("keydown", (ev) => { if (ev.key === "Escape") { ev.stopPropagation(); keep(); } });
    return box;
  }
  RV.reset = function (id) {   // the one way back for a decided item (the Undo button and the r key)
    const c = RV.caseNow(), f = c && RV.find(c, id);
    if (f && f.item.edited && !discardOpen.has(id)) {
      discardOpen.add(id);
      const root = document.querySelector('[data-controls-for="' + id + '"]'); if (!root) return RV.act(id, { action: "reset" }, { focus: "reset" });
      const b = discardBox(id, f.item); root.append(b); const k = b.querySelector('[data-testid="btn-keep-edit"]'); k.focus({ preventScroll: true }); k.scrollIntoView({ block: "nearest" });
      RV.say("Undo will throw away " + wordsOf(f.item) + ". Press Keep to cancel, or Discard to go on.");
      return Promise.resolve(false);
    }
    if (f && f.item.edited && discardOpen.has(id)) { const k = document.querySelector('[data-controls-for="' + id + '"] [data-testid="btn-keep-edit"]'); if (k) k.focus(); return Promise.resolve(false); }
    return RV.act(id, { action: "reset" }, { focus: "reset" });
  };

  // ---- controls
  RV.controls = function (item, kind) {
    const id = item.id, st = item.review_status || "pending";
    const isFlag = kind === "flag", canEdit = kind === "entry" || isFlag;
    const noted = kind === "amount" && item.kind !== "charge";
    const initial = isFlag ? (item.reviewer_note || (item.edited && item.edited.note) || "") : ((item.edited && item.edited.summary) || item.summary || "");
    const d = drafts[id] || (drafts[id] = { open: false, text: initial, reasonOpen: false, reason: "" });
    if (!d.open) d.text = initial;
    const lbl = RV.label(item);
    const root = el("div", { class: "rv-controls", "data-controls-for": id });
    const dismissed = st === "dismissed";
    // T-060 r5 (paralegal M2): a reworded entry that is still marked Needs review is not settled. Its one next step is to compare it with the quote and say so (an Accept on her own wording).
    const toCheck = ZL.editToCheck(item);
    const mustCompare = !toCheck && ZL.needsCompare(item);      // T-179 / D-066: the second check disputed it, so Accept is her statement that she compared it with the quote
    const compare = toCheck || mustCompare;
    const accepted = (st === "accepted" || st === "edited") && !toCheck;

    // T-060 r3: a decided row shows its state, not the action it already took. Primary (filled) is for an undecided item only; Accepted / Dismissed read as quiet state words, Undo is the way back.
    const VARIANT = { accept: st === "pending" || toCheck ? (noted && !mustCompare ? "" : "btn--primary") : st === "dismissed" ? "" : "rv-decided", edit: "", dismiss: st === "dismissed" ? "rv-decided rv-decided--muted" : "btn--ghost", reset: "btn--link", audit: "btn--link", "dismiss-reason": "btn--link" };
    const btn = (action, text, tid, extra, name) => el("button", Object.assign({ type: "button", class: ("btn " + (VARIANT[action] || "") + " rv-" + action).replace("  ", " "), "data-testid": tid, "data-action": action, "aria-label": (name || text).replace("…", "") + ": " + lbl }, extra || {}), text);
    const bar = el("div", { class: "rv-actions", role: "group", "aria-label": "Review actions" });
    const blocked = RV.needsDate(item, kind) && st !== "accepted";
    const acceptText = compare ? "I compared it with the quote" : accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
    // a dismissed item keeps only its state word, Undo and Audit: no Accept, Keep in notes or Edit (the paralegal's M1: one key must not reverse a dismissal)
    if (!dismissed) bar.append(btn("accept", acceptText, "btn-accept", { "data-icon": accepted ? "check" : null, "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked ? "why-blocked-" + id : null,
      onclick: (ev) => { if (accepted) { RV.say(acceptText + " already. Use Undo to change it."); return; } RV.act(id, compare ? { action: "accept", compared: true } : { action: "accept" }, ev.detail === 0 ? { advance: true } : { focus: "accept" }); } }));
    let form;
    if (canEdit && !dismissed) bar.append(btn("edit", isFlag ? "Edit note" : "Edit", "btn-edit", { onclick: () => toggleEdit(true), disabled: blocked }));
    bar.append(btn("dismiss", st === "dismissed" ? "Dismissed" : "Dismiss", "btn-dismiss", { "data-icon": st === "dismissed" ? "dash" : null, "aria-pressed": String(st === "dismissed"),
      onclick: (ev) => { if (st === "dismissed") { RV.say("Already dismissed. Use Undo to change it."); return; } RV.act(id, { action: "dismiss" }, ev.detail === 0 ? { advance: true } : { focus: "dismiss" }); } }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { "aria-expanded": String(!!d.reasonOpen), "aria-controls": "dr-" + id, onclick: (ev) => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; ev.currentTarget.setAttribute("aria-expanded", String(d.reasonOpen)); if (d.reasonOpen) reasonIn.focus(); } }));
    if (st !== "pending") bar.append(btn("reset", "Undo", "btn-reset", { onclick: () => RV.reset(id) }));
    bar.append(btn("audit", "Audit", "btn-audit", { onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);
    if (item.rerun_note) root.append(RV.rerunNote(item));
    root.append(el("div", { class: "rv-refused", role: "alert", hidden: true, "data-testid": "accept-refused" }));
    if (toCheck && !rechecks[id]) {
      const held = ZL.secondCheckPending(item), base = "Still marked Needs review. " + (ZL.wordingEdited(item) ? "Compare your wording with the quote" : "Compare the new quote with the record") + ", then press the button to say you did. Until then it is not in the letter and counts as open.";
      const h = el("p", { class: "rv-help rv-recheck", "data-testid": "edit-check-hint" }, base + (held ? " " + heldText(item) : ""));
      root.append(held ? withServerText(h, "item:" + id, loadItemWhy(id), base + " ") : h);
    }
    if (mustCompare) root.append(el("p", { class: "rv-help rv-recheck rv-dispute", "data-testid": "dispute-compare-hint" }, disputeHint(item)));
    if (compare && comparePrompt.has(id)) root.append(comparePromptNode(item));
    if (ZL.comparedEdit(item) && ZL.secondCheckPending(item)) {   // D-058: the action that matches the gate is writing the summary, not a rerun that cannot clear it
      const t = el("p", {}, isPrepared(item) ? PREPARED_ACCEPTED_HELD : ACCEPTED_HELD);
      root.append(el("div", { class: "rv-help rv-export-note", "data-testid": "compare-export-note" }, withServerText(t, "blocker:" + id, loadBlockerWhy(id)),
        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-write-summary", "aria-label": "Write the summary: " + lbl, onclick: () => { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); } }, "Write the summary")));
    }
    if (rechecks[id] && st === "edited") root.append(el("p", { class: "rv-recheck", "data-testid": "edit-recheck-note" }, rechecks[id]));
    if (blocked) root.append(el("p", { class: "rv-help rv-blocked", id: "why-blocked-" + id, "data-testid": "accept-blocked-reason" }, DATE_FIRST + " ",
      el("button", { type: "button", class: "btn btn--link", "data-testid": "link-confirm-date", onclick: () => goToDateRow(id) }, "Go to its date choices")));

    // dismiss reason (flags only; optional - R-RV-5)
    const reasonIn = el("input", { type: "text", id: "dr-" + id, class: "rv-input", maxlength: "300", "aria-label": "Reason for dismissing (optional)", "data-testid": "dismiss-reason", value: d.reason || "" });
    reasonIn.addEventListener("input", () => { d.reason = reasonIn.value; });
    const reasonRow = el("form", { class: "rv-reason", hidden: !(isFlag && d.reasonOpen), onsubmit: (ev) => { ev.preventDefault(); const r = reasonIn.value.trim(); RV.act(id, r ? { action: "dismiss", note: r } : { action: "dismiss" }, { focus: "dismiss" }); } },
      reasonIn, el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-dismiss-confirm" }, "Dismiss"));
    if (isFlag) root.append(reasonRow);

    if (canEdit && !dismissed) {
      const hint = isFlag ? "Your note (internal notes only, never in the letter)" : "Summary wording (the quoted excerpt, date and provider cannot be changed)";
      const ta = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: isFlag ? "note" : "summary", "data-testid": isFlag ? "flag-note" : "edit-summary" });   // named by its visible label (WCAG 2.5.3)
      ta.value = d.text;
      ta.addEventListener("input", () => { d.text = ta.value; ta.removeAttribute("aria-invalid"); });
      form = el("form", { class: "rv-edit", hidden: !d.open, onsubmit: (ev) => {
        ev.preventDefault(); const v = ta.value.trim();
        if (!v) { showError(id, isFlag ? "Write a note first, or cancel." : "The summary can't be empty."); return; }
        const h = form.querySelector(".rv-recheck-hint"), was = h ? h.textContent : "";
        if (h) h.textContent = "Checking your wording against the quote…";
        // T-166 F4: "Save and accept" is her statement that the wording matches the quote beside it, made by clicking that button; the code's check of every number, date and negation still runs on save, and a refusal stops it.
        const both = !isFlag && !!(ev.submitter && ev.submitter.getAttribute("data-testid") === "btn-save-accept");
        RV.act(id, { action: "edit", edits: isFlag ? { note: v } : { summary: v } }, { focus: both ? null : "edit" })
          .then((ok) => (ok && both ? RV.act(id, { action: "accept", compared: true }, { focus: "accept" }) : null))      // Save and accept is her statement that the wording matches the quote beside it (D-066)
          .finally(() => { if (h && h.isConnected) h.textContent = was; });
      } },
        !isFlag && item.edited && item.edited.original_summary ? el("p", { class: "rv-original muted small", "data-testid": "edit-original" }, el("strong", {}, "Original wording: "), item.edited.original_summary) : null,
        el("label", { class: "rv-label" }, hint, ta),
        isFlag ? null : el("p", { class: "rv-help rv-recheck-hint", "data-testid": "edit-recheck-hint" }, "When you save, the code checks every number, date and negation in your wording against the quote, then a second AI check reads it. Nothing is added to the letter until it passes."),
        el("div", { class: "rv-actions" },
          isFlag ? null : el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-save-accept", title: "Saves your wording and accepts it, saying it matches the quote beside it" }, "Save and accept"),
          el("button", { type: "submit", class: "btn" + (isFlag ? " btn--primary" : ""), "data-testid": "btn-save-edit" }, "Save"),
          el("button", { type: "button", class: "btn", "data-testid": "btn-cancel-edit", onclick: () => toggleEdit(false) }, "Cancel")));
      ta.addEventListener("keydown", (ev) => {
        if (ev.key === "Escape") { ev.stopPropagation(); toggleEdit(false); }
        else if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); form.requestSubmit(); }
      });
      root.append(form);
      var toggleEdit = function (open) {
        d.open = open; form.hidden = !open;
        if (open) ta.focus(); else { const b = bar.querySelector('[data-action="edit"]'); if (b) b.focus(); }
      };
      ui[id] = { openEdit: () => toggleEdit(true) };
      root._openEdit = () => toggleEdit(true);
    } else ui[id] = {};
    root.append(el("div", { class: "rv-error", role: "alert" }));
    if (discardOpen.has(id) && st !== "pending" && item.edited) root.append(discardBox(id, item)); else discardOpen.delete(id);
    paintRefusal(root, id, root._openEdit);
    return root;
  };

  // ---- legend (one line; the full list is the Shortcuts dialog)
  RV.legend = () => el("p", { class: "rv-keys", "data-testid": "keys-hint" }, el("strong", {}, "Keyboard: "),
    "with an item selected, j and k move between items, a accepts, d dismisses, e edits, n jumps to the next open item, x to Export. Press ? for the full list.");

  // ---- the shortcut sheet: opened by the header "Shortcuts" button, or by ? while an item is selected
  const KEYS = [["j / k", "Next / previous item (dates to confirm, then entries, flags, charges)"], ["a", "Accept the selected item, then move to the next one that needs a decision; at the end of a list, to the first item of the next list without deciding it (a flagged charge asks first)"], ["d", "Dismiss the selected item, then move on the same way"],
    ["e", "Edit the wording of the selected item"], ["r", "Reset a decided item"], ["o", "Open the source record in a dialog"], ["p", "Move focus to the source record beside the list (Esc returns)"],
    ["n", "Jump to the first item that still needs a decision, from any item"], ["x", "Jump to Export, from any item"],
    ["Shift+A", "Accept all verified entries (asks first, with the count)"], ["?", "This list"]];
  RV.openShortcuts = function () {
    let d = document.querySelector('[data-testid="shortcuts-modal"]');
    if (!d) {
      d = el("dialog", { class: "dlg dlg--md", "data-testid": "shortcuts-modal", "aria-labelledby": "kb-title" },
        el("div", { class: "dlg-head" }, el("h2", { id: "kb-title" }, "Keyboard shortcuts"), el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-close-shortcuts", onclick: () => d.close() }, "Close")),
        el("div", { class: "dlg-body" },
          el("p", { class: "muted" }, "Letter keys work only while an item is selected: use Start review, or press Tab and then Enter on the first skip link. They never act from Export, the header or a text box."),
          el("dl", { class: "kv kv--keys", "data-testid": "shortcuts-list" }, KEYS.flatMap(([k, v]) => [el("dt", {}, el("kbd", {}, k)), el("dd", {}, v)]))));
      document.body.append(d);
    }
    const back = document.activeElement;
    d.addEventListener("close", () => { if (back && back.isConnected) back.focus(); }, { once: true });
    if (!d.open) d.showModal();
  };

  // ---- keyboard flow (R-RV-4, WCAG 2.1.4 / T-060 blocker). Single-key shortcuts act ONLY while focus is on an item row or on something inside one.
  // From Export, the header, a dialog, a text field or the page body they do nothing, so a stray key can never change a decision.
  const typing = (t) => !!t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable);
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (typing(t)) return;
    if (document.querySelector("dialog[open]")) {   // a dialog swallows the letter keys; say so instead of doing nothing (T-060 r3, paralegal F11)
      if (ev.key.length === 1 && "jkadernox".includes(ev.key.toLowerCase()) && !ev.shiftKey && ZL.state.get().case) RV.say("A window is open. Press Escape to close it first, then use the key again.");
      return;
    }
    const row = RV.itemRowOf(t);
    if (!row) return;
    const c = RV.caseNow(); if (!c) return;
    const key = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key, id = row.getAttribute("data-item-id");
    if (ev.key === "?") { ev.preventDefault(); if (RV.openShortcuts) RV.openShortcuts(); return; }
    if (ev.shiftKey) return;   // Shift+A is the batch key (batch.js); a capital letter never means the single-item key
    if (key === "j" || key === "k") {
      const items = RV.domItems(), at = items.indexOf(row), n = items[at + (key === "j" ? 1 : -1)];
      ev.preventDefault();
      if (n) focusNode(n); else RV.say(key === "j" ? "That is the last item." : "That is the first item.");
      return;
    }
    if (key === "n" || key === "x") {   // T-166 F6: n = the first item that still needs a decision, from any row; x = Export. Both only while an item row has focus (WCAG 2.1.4), like every letter key
      ev.preventDefault();
      if (key === "x") { focusExport("Export. Press Enter to open it."); return; }
      const left = ZL.progressOf(c).left;
      if (!left) { focusExport("Nothing left to decide. Export is next."); return; }
      if (RV.focusFirstPending()) { const at = document.activeElement, f = at && at.getAttribute && RV.find(c, at.getAttribute("data-item-id")), g = at && at.closest && at.closest(GROUP);
        RV.say("First open item: " + (g ? groupName(g) + ", " : "") + (f ? RV.ghostLabel(f.item) : "") + ". " + left + (left === 1 ? " item is" : " items are") + " open."); }
      return;
    }
    if (ev.key.length !== 1 || !"aedro".includes(key)) return;
    const f = RV.find(c, id); if (!f || f.item.state === "rejected") return;
    ev.preventDefault();
    if ((key === "a" || key === "d" || key === "e") && f.item.review_status === "dismissed") {   // T-060 r5 (paralegal M1): one key never undoes a dismissal; only Undo (or r) does
      RV.say("This item is dismissed. Press r or Undo to bring it back first.");
      return;
    }
    if (key === "a" && /^(accepted|edited)$/.test(f.item.review_status) && !ZL.editToCheck(f.item)) {   // as the Accept button: a decided item is not decided twice (T-154: a confirmed flagged charge must not reopen "not counted" or write a second accept)
      RV.say((f.kind === "amount" && f.item.kind !== "charge" ? "Kept in notes" : f.item.review_status === "edited" ? "Edited" : "Accepted") + " already. Use Undo to change it.");
      return;
    }
    if (key === "a" && (ZL.editToCheck(f.item) || ZL.needsCompare(f.item))) { askCompare(id); return; }      // D-066 too: an item the second check disputed   // T-136 (paralegal F1): one key press never records "I compared it with the quote"; the button (click, or Enter on it) does
    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true });
    else if (key === "r") { if (f.item.review_status !== "pending") RV.reset(id); }
    else if (key === "o") RV.openSource(f.item, f.kind);
    else if (key === "e") { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); }
  });

  // ---- registration (T-042 extension points), tolerant of load order
  function mountSection(mountEl, name) {
    let s = mountEl.querySelector(':scope > [data-panel="' + name + '"]');
    if (!s) { s = el("section", { class: "rv-panel", "data-panel": name }); mountEl.append(s); }
    return s;
  }
  RV.registerPanel = function (name, render) {
    const reg = () => ZL.registerPanel((c, mountEl) => { if (!c || !mountEl) return; const sec = mountSection(mountEl, name); try { render(sec, c); } catch (err) { ZL.panelFailed(sec, name, err); } });
    if (typeof ZL.registerPanel === "function") reg(); else (ZL._pendingPanels = ZL._pendingPanels || []).push(reg);
  };
  const drain = () => { (ZL._pendingPanels || []).splice(0).forEach((f) => f()); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", drain); else drain();
  if (typeof ZL.registerRowActions === "function") {
    ZL.registerRowActions((entry, rowEl) => {
      if (!rowEl || entry.state === "rejected" || rowEl.querySelector(":scope > .rv-controls")) return;
      rowEl.setAttribute("data-item-id", entry.id); rowEl.setAttribute("data-review", entry.review_status || "pending");
      if (ZL.editToCheck(entry)) rowEl.setAttribute("data-edit-check", ""); else rowEl.removeAttribute("data-edit-check");
      if (!rowEl.hasAttribute("tabindex")) rowEl.setAttribute("tabindex", "0");
      const ctrl = RV.controls(entry, "entry"); rowEl.append(ctrl);
      const au = ctrl.querySelector(".rv-audit"), links = rowEl.querySelector(".row-actions");
      if (au && links) links.append(au);   // Why? / Open record / Change quote / Audit are one group of links on the right of the row
      if (entry.entered_by_reviewer || /reviewer/i.test(entry.entered_by || "")) {   // typed by the paralegal, not drafted by the model
        const head = rowEl.querySelector(".entry-head") || rowEl;
        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
      }
    });
  }
})();
