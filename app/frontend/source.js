/* Source-record modal (R-RV-9). ZL.openSource([{record_id, start, end}]) opens the full record text(s) with the span [start,end)
   (ABSOLUTE character offsets from the API, never computed from the model) highlighted. Used by entries here and by flags/charges in T-043. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  function recordView(rec, span, label, omitHead) {
    const box = el("section", { class: "src-rec", "data-testid": "record-section", "data-record-id": rec.id });
    if (!omitHead) box.append(el("h3", {}, label || `Record ${rec.seq}: ${rec.source_label}`));
    const pre = el("pre", { class: "src-text" });
    const rs = span.start - rec.char_start, re = span.end - rec.char_start;
    if (span.start == null) { pre.append(document.createTextNode(rec.text)); box.append(pre); return { box, mark: null }; } // whole-record view (no quote to highlight)
    if (rs < 0 || re > rec.text.length || re <= rs) {
      pre.append(document.createTextNode(rec.text));
      box.append(pre, el("p", { class: "error", role: "alert", "data-testid": "highlight-missing" }, "The exact position of this quote could not be found in the record, so nothing is highlighted. Check the whole record."));
      return { box, mark: null };
    }
    const mark = el("mark", { "data-testid": "record-highlight", tabindex: "-1" }, rec.text.slice(rs, re));
    pre.append(document.createTextNode(rec.text.slice(0, rs)), mark, document.createTextNode(rec.text.slice(re)));
    box.append(pre);
    return { box, mark };
  }
  ZL.openSource = function (spans, title) {
    const c = ZL.state.get().case; if (!c) return;
    const dlg = ZL.$("#source-modal"), body = ZL.$("#source-body"); clear(body);
    ZL.$("#source-title").textContent = title || "Source record";
    let first = null;
    spans.forEach((sp) => {
      const rec = c.records.find((r) => r.id === sp.record_id); if (!rec) return;
      const v = recordView(rec, sp, null, spans.length === 1 && title && title.startsWith(`Record ${rec.seq}`)); body.append(v.box); first = first || v.mark;
    });
    if (!dlg.open) dlg.showModal();
    if (first) first.scrollIntoView({ block: "center" });
  };
  ZL.entrySpans = (e) => e.record_ids.map((rid) => ({ record_id: rid, start: e.excerpt_start, end: e.excerpt_end }));
  document.addEventListener("DOMContentLoaded", () => {
    ZL.$("#source-close").addEventListener("click", () => ZL.$("#source-modal").close());
  });
})();
