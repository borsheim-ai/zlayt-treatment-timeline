/* Export view (T-044): two separate copy blocks built by the SERVER (letter_text / internal_notes_text); the UI only displays and copies them verbatim.
   Count line sits outside both blocks (R-EX-5). Copy asks for one confirmation when anything is pending (names pending flags separately). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let open = false, data = null, timer = null, confirmFor = null, style = "standard";   // T-121: "standard" (two lines per entry, the golden layout) or "oneline"

  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  function countLine(c) {
    return `${plural(c.entries, "entry", "entries")}, ${plural(c.charges, "charge", "charges")} in letter · ${plural(c.flags_in_notes, "flag", "flags")} in internal notes · ${c.records_in_letter} of ${c.records_total} records in letter · ${plural(c.pending, "item", "items")} pending (${plural(c.pending_flags, "flag", "flags")})`;
  }
  function status(msg, bad) { const s = ZL.$("#export-status"); if (s) { s.textContent = msg || ""; s.className = bad ? "error" : "muted"; s.setAttribute("role", bad ? "alert" : "status"); } }
  async function copy(text, which) {
    try { await navigator.clipboard.writeText(text); status(`Copied the ${which}.`); }
    catch (_) { status("The browser blocked copying. Select the text in the box and copy it by hand.", true); }
  }
  // A plain-text file of exactly the text the server built (no editing, no re-assembly here).
  function download(text, name, which) {
    const url = URL.createObjectURL(new Blob([text || ""], { type: "text/plain;charset=utf-8" })), a = el("a", { href: url, download: name });
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    status(`Downloaded the ${which} as ${name}.`);
  }
  // What is pending, by name ("2 charges, 1 flag") from the case on screen; falls back to the export's own counts.
  function pendingWords(c) {
    const cs = ZL.state.get().case, pend = (i) => (i.review_status || "pending") === "pending";
    if (!cs) return null;
    const bits = [[(cs.entries || []).concat(cs.undated_entries || []).filter(pend).length, "entry", "entries"], [(cs.amounts || []).filter((a) => pend(a) && a.kind === "charge").length, "charge", "charges"],
      [(cs.amounts || []).filter((a) => pend(a) && a.kind !== "charge").length, "unclear amount", "unclear amounts"], [c.pending_flags, "flag", "flags"]].filter(([n]) => n);
    const edits = ZL.editCount(cs);   // T-060 r5 (paralegal M2): her reworded entries that are still marked Needs review
    const open = (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).map((e) => { const r = (cs.records || []).find((x) => x.id === (e.record_ids || [])[0]); return (r ? "Record " + r.seq + ", " : "") + e.provider; });   // T-136 r2 (paralegal F-5): name them
    return bits.map(([n, one, many]) => plural(n, one, many) + " not reviewed").concat(edits ? [plural(edits, "edited entry", "edited entries") + " still marked Needs review (compare with the quote)" + (open.length ? ": " + open.join("; ") : "")] : []);
  }
  const editsToCheck = () => { const cs = ZL.state.get().case; return cs ? ZL.editCount(cs) : 0; };
  // One primary button for one task: while the confirmation is showing, Copy letter steps down and Copy anyway is the primary.
  function askConfirm(c, then, verb) {
    verb = verb || "Copy";
    const box = ZL.$("#export-confirm"), main = ZL.$('[data-testid="btn-copy-letter"]'); clear(box); box.hidden = false;
    if (main) main.classList.remove("btn--primary");
    const parts = pendingWords(c) || [plural(c.pending, "item", "items") + " not reviewed"];
    const close = () => { box.hidden = true; if (main) { main.classList.add("btn--primary"); main.focus(); } };
    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. " + verb + " the letter anyway?"),
      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-anyway", onclick: () => { close(); then(); } }, verb + " anyway"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-copy-cancel", onclick: close }, "Go back")));
    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
  }
  function render() {
    const root = ZL.$("#export-body"); clear(root);
    ZL.$("#view-export").hidden = !open;
    if (!open || !data) return;
    const c = data.counts;
    root.append(...[
      el("p", { class: "ex-back" }, el("button", { type: "button", class: "btn", "data-testid": "btn-back-to-review", onclick: () => ZL.sections && ZL.sections.back() }, "Back to review")),   // T-174 F13: the first control in the view
      el("p", { class: "count-line", "data-testid": "count-line", role: "status" }, countLine(c)),
      (data.warnings || []).length ? el("ul", { class: "ex-warn" }, data.warnings.map((w) => el("li", {}, typeof w === "string" ? w : (w.message || w.code)))) : null,
      el("fieldset", { class: "ex-style", "data-testid": "letter-style" }, el("legend", {}, "Letter layout"),
        [["standard", "Two lines per entry (summary, then source)"], ["oneline", "One line per entry (date, provider, quote)"]].map(([v, t]) => el("label", { class: "ex-style-opt" },
          el("input", { type: "radio", name: "letter-style", value: v, checked: style === v ? true : null, "data-testid": "letter-style-" + v,
            onchange: () => { style = v; load(false).then(() => { const r = ZL.$('[data-testid="letter-style-' + v + '"]'); if (r) r.focus(); }); } }), " " + t))),
      el("p", { id: "export-status", class: "muted small", role: "status" }),
      el("div", { id: "export-confirm", hidden: true }),
      el("section", { class: "ex-block", "aria-labelledby": "ex-h1" },
        el("div", { class: "toolbar" }, el("h3", { id: "ex-h1" }, "Treatment section (paste into the letter)"),
          el("div", { class: "row ex-btns" },
            el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-letter", disabled: !data.letter_text, onclick: () => { const go = () => copy(data.letter_text, "treatment section"); c.pending > 0 || editsToCheck() ? askConfirm(c, go) : go(); } }, "Copy letter"),
            el("button", { type: "button", class: "btn", "data-testid": "btn-download-letter", disabled: !data.letter_text, onclick: () => { const go = () => download(data.letter_text, "treatment-section.txt", "treatment section"); c.pending > 0 || editsToCheck() ? askConfirm(c, go, "Download") : go(); } }, "Download .txt"))),
        el("pre", { class: "ex-text", tabindex: "0", "data-testid": "export-letter" }, data.letter_text)),
      el("section", { class: "ex-block", "aria-labelledby": "ex-h2" },
        el("div", { class: "toolbar" }, el("h3", { id: "ex-h2" }, "Internal review notes — do not send"),
          el("div", { class: "row ex-btns" },
            el("button", { type: "button", class: "btn", "data-testid": "btn-copy-notes", onclick: () => copy(data.internal_notes_text, "internal notes") }, "Copy notes"),
            el("button", { type: "button", class: "btn", "data-testid": "btn-download-notes", onclick: () => download(data.internal_notes_text, "internal-review-notes.txt", "internal notes") }, "Download .txt"))),
        el("pre", { class: "ex-text", tabindex: "0", "data-testid": "export-notes" }, data.internal_notes_text))].filter(Boolean));
  }
  async function load(scroll) {
    const s = ZL.state.get(); if (!s.token) return;
    try { data = await ZL.api.exportCase(s.token, style); open = true; render(); if (ZL.stepper) ZL.stepper.clearExportNotice(); if (scroll) { const h = ZL.$("#h-export"); h.setAttribute("tabindex", "-1"); h.scrollIntoView({ block: "start" }); h.focus({ preventScroll: true }); } }
    catch (e) {
      data = null;
      // A refused export (422 judge_not_run / export_blocked) is shown beside the Export button, scrolled into view and focused, with the blocker list and the rerun button.
      if (ZL.stepper && ZL.stepper.showExportBlocked(e, scroll)) { open = false; render(); return; }
      open = true; render(); ZL.$("#export-body").append(el("p", { class: "ex-back" }, el("button", { type: "button", class: "btn", "data-testid": "btn-back-to-review", onclick: () => ZL.sections && ZL.sections.back() }, "Back to review")), el("p", { class: "error", role: "alert" }, e.message, " ", el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-error-action", onclick: () => ZL.openExport() }, "Try again")));   // T-174 F15
    }
  }
  ZL.openExport = () => load(true);
  ZL.closeExport = () => { open = false; render(); };
  // keep an open export in step with review decisions made after it was opened
  ZL.state.subscribe((s) => { if (!s.case) { open = false; data = null; render(); return; } if (open) { clearTimeout(timer); timer = setTimeout(() => load(false), 250); } });
})();
