/* Side-by-side source viewer (T-046, R-ST-1). At viewport >= 1024 px the full source record sits beside the review queue and follows the
   selected item (focus or click on anything that carries data-item-id: entries, flags, charges), scrolled to the highlight.
   Below 1024 px this module does nothing and the R-RV-9 modal (source.js) is the only source viewer. The explicit "Open record" buttons and
   the o key always open the modal, at every width. No new endpoint: spans come from ZL.rv.sourceTargets (code offsets, never model-made).
   All record text goes in as text nodes (ZL.el / createTextNode); nothing here uses innerHTML. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  const mq = window.matchMedia("(min-width: 1024px)");
  let pane, body, titleEl, flagsBar, current = null, lastToken = null;   // current = {id}

  // withHeading is false for a single-record item: the pane title already names the record, so no second heading.
  function recordSection(rec, span, withHeading) {
    const box = el("section", { class: "src-rec", "data-testid": "sbs-record", "data-record-id": rec.id });
    if (withHeading) box.append(el("h3", {}, `Record ${rec.seq}: ${rec.source_label}`));
    const pre = el("pre", { class: "src-text" });
    const rs = span.start == null ? null : span.start - rec.char_start, re = span.end == null ? null : span.end - rec.char_start;
    if (rs == null) { pre.append(document.createTextNode(rec.text)); box.append(pre); return { box, mark: null }; }   // whole-record view, no quote to highlight
    if (rs < 0 || re > rec.text.length || re <= rs) {
      pre.append(document.createTextNode(rec.text));
      box.append(pre, el("p", { class: "error", role: "alert", "data-testid": "sbs-highlight-missing" }, "The exact position of this quote could not be found in the record, so nothing is highlighted. Check the whole record."));
      return { box, mark: null };
    }
    const mark = el("mark", { "data-testid": "sbs-highlight", tabindex: "-1" }, rec.text.slice(rs, re));
    pre.append(document.createTextNode(rec.text.slice(0, rs)), mark, document.createTextNode(rec.text.slice(re)));
    box.append(pre);
    return { box, mark };
  }

  function build() {
    const host = ZL.$("#view-review"); if (!host || pane) return;
    titleEl = el("h3", { id: "sbs-title", "data-testid": "sbs-title" }, "Source record");
    body = el("div", { class: "sbs-body", tabindex: "0", role: "region", "aria-label": "Source record text", "data-testid": "sbs-body" });
    flagsBar = el("p", { class: "sbs-flags small", "data-testid": "sbs-flags" });
    pane = el("section", { class: "sbs-pane", "data-testid": "sbs-pane", "aria-labelledby": "sbs-title" },
      el("div", { class: "sbs-head" }, titleEl, flagsBar, el("span", { class: "muted small" }, "Follows the selected item. Press p to move here, Esc to return.")), body);
    host.append(pane);
  }

  // Flag summary in the always-visible pane: the queue is long, so the gap flag is one click away instead of a page of scrolling.
  function refreshFlags() {
    if (!flagsBar) return;
    const flags = Array.from(document.querySelectorAll('[data-testid="flags-panel"] [data-item-id][data-flag-type]'));
    clear(flagsBar); flagsBar.hidden = !flags.length; if (!flags.length) return;
    const gaps = flags.filter((f) => f.getAttribute("data-flag-type") === "gap"), first = gaps[0] || flags[0];
    const word = (n, w) => n + " " + w + (n === 1 ? "" : "s");
    flagsBar.append(document.createTextNode(word(flags.length, "flag") + (gaps.length ? " (" + word(gaps.length, "gap") + ")" : "") + " "),
      el("button", { type: "button", class: "btn btn--sm", "data-testid": "sbs-show-flag" }, gaps.length ? "Show gap flag" : "Show first flag"));
    flagsBar.querySelector("button").addEventListener("click", () => {
      const row = document.querySelector('[data-testid="flags-panel"] [data-item-id="' + first.getAttribute("data-item-id") + '"]'); if (!row) return;
      if (!row.hasAttribute("tabindex")) row.setAttribute("tabindex", "-1");
      row.scrollIntoView({ block: "center" }); row.focus(); show(row.getAttribute("data-item-id"));
    });
  }

  function empty(msg) { clear(body); body.append(el("p", { class: "muted", "data-testid": "sbs-empty" }, msg)); titleEl.textContent = "Source record"; }

  function show(id) {
    if (!pane || !mq.matches) return;
    const c = ZL.state.get().case, rv = ZL.rv;
    if (!c || c.status !== "ready" || !rv) return;
    const f = rv.find(c, id); if (!f) return;
    const t = rv.sourceTargets(f.item, f.kind);
    current = { id };
    document.querySelectorAll(".sbs-current").forEach((n) => n.classList.remove("sbs-current"));
    const row = document.querySelector('[data-item-id="' + id + '"]'); if (row) row.classList.add("sbs-current");
    if (!t.spans.length) { empty("This item has no source record to show."); return; }
    clear(body);
    const marks = [], seqs = [];
    t.spans.forEach((sp) => {
      const rec = c.records.find((r) => r.id === sp.record_id); if (!rec) return;
      const v = recordSection(rec, sp, t.spans.length > 1); body.append(v.box); seqs.push(rec.seq); if (v.mark) marks.push(v.mark);
    });
    const only = c.records.find((r) => r.id === t.spans[0].record_id);
    titleEl.textContent = seqs.length > 1 ? "Records " + seqs.join(" and ") : (only ? "Record " + only.seq + ": " + only.source_label : "Source record");
    body.scrollTop = 0;
    if (marks[0]) {   // scroll inside the pane only; never move the page
      const b = body.getBoundingClientRect(), m = marks[0].getBoundingClientRect();
      body.scrollTop += (m.top - b.top) - (body.clientHeight - m.height) / 2;
    }
  }

  // Selection follows focus (keyboard: j/k, Tab) and click on any item. Dialogs and the pane itself are ignored.
  function pick(ev) {
    if (!mq.matches || !pane) return;
    const t = ev.target; if (!t || !t.closest || t.closest("dialog") || t.closest(".sbs-pane")) return;
    const row = t.closest("[data-item-id]"); if (!row) return;
    const id = row.getAttribute("data-item-id"); if (id && (!current || current.id !== id || ev.type === "click")) show(id);
  }
  document.addEventListener("focusin", pick);
  document.addEventListener("click", pick);

  // p moves focus into the pane (so it can be scrolled by keyboard); Esc returns to the selected item.
  document.addEventListener("keydown", (ev) => {
    if (!mq.matches || !pane || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    if (ev.key === "Enter" && t && t.hasAttribute && t.hasAttribute("data-item-id") && !t.closest("dialog") && !t.closest(".sbs-pane")) {
      show(t.getAttribute("data-item-id"));   // Enter on a focused row (re)selects it into the pane; buttons inside the row keep their own Enter
    } else if (ev.key === "Escape" && t && t.closest && t.closest(".sbs-pane") && current) {
      const row = document.querySelector('[data-testid="queue"] [data-item-id="' + current.id + '"]') || document.querySelector('[data-item-id="' + current.id + '"]');
      if (row) { ev.preventDefault(); if (!row.hasAttribute("tabindex")) row.setAttribute("tabindex", "0"); row.focus(); }
    } else if (ev.key.toLowerCase() === "p" && !pane.hidden && body && ZL.rv && ZL.rv.itemRowOf(t)) {   // only from an item row (WCAG 2.1.4): never from Export or the page body
      if (document.querySelector("dialog[open]")) return;
      ev.preventDefault(); body.focus();
    }
  });

  function sync(s) {
    build(); if (!pane) return;
    const ready = !!(s.case && s.case.status === "ready");
    pane.hidden = !ready; if (ready) requestAnimationFrame(refreshFlags);
    document.body.classList.toggle("sbs-on", ready && mq.matches);
    const tok = ready ? s.token : null;
    if (tok !== lastToken) { lastToken = tok; current = null; if (ready) empty("Select an item to see its source record here."); return; }
    if (ready && current) requestAnimationFrame(() => show(current.id));   // after renderReview rebuilt the rows: refresh text and re-mark the row
  }
  document.addEventListener("DOMContentLoaded", () => { build(); ZL.state.subscribe(sync); sync(ZL.state.get()); });
  mq.addEventListener("change", () => { sync(ZL.state.get()); if (mq.matches && current) show(current.id); });
})();
