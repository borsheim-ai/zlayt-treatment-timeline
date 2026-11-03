/* Flags panel (T-043): four groups plus "Record warnings" (R-FL-6),
   unmerged conflicts shown side by side (D-017), reviewer note only (D-010), confirm_date control for ambiguous dates.
   All server text is inserted as text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const RV = ZL.rv, el = (...a) => ZL.el(...a);

  const GROUPS = [
    ["gap", "Treatment gaps", "No gap over 30 days found."],
    ["conflict", "Conflicts between records", ""],
    ["pre_existing", "Pre-existing conditions", "No earlier conditions mentioned."],
    ["causation", "Causation language", "No causation wording found."],
    ["record_warning", "Record warnings", "No record warnings."],
  ];
  const joinList = (a) => (a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]);
  const recOf = (c, id) => (c.records || []).find((r) => r.id === id);
  const recSeq = (c, id) => { const r = recOf(c, id); return r ? r.seq : String(id).replace(/^r/, ""); };

  // One block per record (a gap names two records, each with a Date and a Source line: two blocks, side by side, not four stacked boxes).
  function evidence(c, f) {
    const ul = el("ul", { class: "rv-evidence" + (f.type === "conflict" ? " rv-side" : ""), "data-testid": "flag-evidence", "aria-label": "Quoted evidence" });
    const byRec = [], at = {};
    (f.evidence || []).forEach((e) => { if (!(e.record_id in at)) { at[e.record_id] = byRec.length; byRec.push({ id: e.record_id, lines: [] }); } byRec[at[e.record_id]].lines.push(e.excerpt); });
    byRec.forEach((g) => {
      const r = recOf(c, g.id);
      const li = el("li", { class: "rv-ev" },
        el("span", { class: "rv-ev-cap" }, "Record " + recSeq(c, g.id) + (r ? " · " + r.source_label : "")),
        el("blockquote", { class: "rv-quote" }, g.lines.map((t) => el("span", { class: "rv-line" }, t))));
      if (f.type === "conflict") {
        // Show the entry's own quoted line from the same record so both sides can be read without opening it.
        const en = (c.entries || []).concat(c.undated_entries || []).find((x) => (x.record_ids || []).includes(g.id));
        if (en && en.excerpt && !g.lines.includes(en.excerpt)) li.append(el("span", { class: "rv-ev-more" }, "Quoted line from this record: " + en.excerpt));
      }
      ul.append(li);
    });
    return ul;
  }

  function dateControl(c, f) {
    const rid = ((f.evidence || [])[0] || {}).record_id;
    const row = (c.dates_to_confirm || []).find((d) => d.record_id === rid);
    if (!row) return null;
    const raw = row.raw || row.date_raw || "";
    if (!(row.candidates || []).length)
      return el("p", { class: "rv-note" }, "No readable date was found for this record, so it stays off the timeline and out of the gap checks.");
    // T-096: the suggested reading (T-088) is pre-selected with its reason; the paralegal still clicks Confirm date.
    return ZL.sg.dateForm(row, { legend: "The date “" + raw + "” can be read two ways. Choose how this record is dated:", onConfirm: async (cand) => {
      await ZL.confirmDate(rid, cand);   // timeline, gaps and warnings are recomputed by the backend; changed gap figures are announced
    } });
  }

  // T-114 r3: a gap whose figure moved after a date was confirmed says so on its own card, with the old and new numbers, for as long as the card shows the new figure.
  function gapChangeLine(c, f) {
    const g = ZL.gapChanges && ZL.gapChanges.forFlag(c, f); if (!g) return null;
    return el("p", { class: "rv-gap-change", "data-testid": "gap-change-card" }, el("strong", {}, g.sentence || "This figure changed after you confirmed a date."), " ", g.lines.join(" "));
  }

  // The "why" can carry sentences the card's explanation already says (the paperwork note on a gap): show each sentence once.
  function whyOnce(f) {
    const exp = String(f.explanation || "");
    return String(f.why || "").split(/(?<=[.!?])\s+/).filter((t) => t && !exp.includes(t.trim())).join(" ");
  }

  function card(c, f) {
    const seqs = (RV.sourceTargets(f, "flag").ids || []).map((id) => recSeq(c, id));
    const note = f.reviewer_note || (f.edited && f.edited.note);
    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
      el("div", { class: "rv-head" }, el("h4", { class: "rv-title" }, f.title), RV.chips(f)),
      gapChangeLine(c, f),
      el("p", { class: "rv-text-body" }, f.explanation),
      f.state === "needs_review" && f.review_status !== "dismissed" && whyOnce(f) ? el("p", { class: "rv-reason-line" }, el("strong", {}, "Needs review: "), whyOnce(f)) : null,   // the "quote found word for word..." sentence is in Why this status, not repeated on every card
      evidence(c, f));
    if (f.category === "date_ambiguous") { const dc = dateControl(c, f); if (dc) a.append(dc); }
    if (note) a.append(el("p", { class: "rv-usernote", "data-testid": "flag-note-text" }, el("strong", {}, f.review_status === "dismissed" ? "Dismissed because: " : "Your note: "), note));
    // T-166 F11/F7: Open record stays on the card; Why this status, Audit and "Dismiss with reason" wait behind More (one dismiss path in view).
    const ctrl = RV.controls(f, "flag"), more = RV.moreActions([ZL.stepper ? ZL.stepper.traceButton(f.id, "btn btn--link") : null, ctrl.querySelector(".rv-audit"), ctrl.querySelector(".rv-dismiss-reason")], f.title, { testid: "btn-more", panelTestid: "flag-more-panel" });
    a.append(el("div", { class: "rv-actions rv-links" },
      seqs.length ? el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", onclick: () => RV.openSource(f, "flag") }, seqs.length > 1 ? "Open records " + joinList(seqs) : "Open record " + seqs[0]) : null,
      more.btn, more.panel));
    a.append(ctrl);
    return a;
  }

  // T-142 (legal nurse, GATE-M2 major 1): "No conflicts found." read as an all-clear. The code checks a few kinds of conflict and nothing else, so the group says which, from GET case `checks`
  // (T-141: {conflict_types, labels, not_checked}), and says the rest are not checked. With no `checks` it says that too, in fixed words that are true of every build.
  const FALLBACK_CHECKED = ["A stated plan of care against a later record where the course ended early", "A denial of prior problems against a prior condition, surgery or accident in another record", "A stated accident date against the dates of the records"];
  const FALLBACK_NOT = ["Left versus right across records", "A change in loss of consciousness history between records"];
  const humanType = (t) => { const s = String(t || "").replace(/_/g, " "); return s.charAt(0).toUpperCase() + s.slice(1); };
  const seqWords = (nos) => (nos.length === 1 ? "Record " + nos[0] + " was" : "Records " + nos.slice(0, -1).join(", ") + " and " + nos[nos.length - 1] + " were");
  // T-151 (T-141 r2): `checks.skipped[]` says which check did NOT run on this case, or not on every record, in the server's own words; `checks.notes[]` are info lines. Neither is a conflict.
  function skippedBox(ch) {
    const sk = ch && Array.isArray(ch.skipped) ? ch.skipped : [];
    if (!sk.length) return null;
    return el("div", { class: "rv-skipped", "data-testid": "conflict-skipped" },
      el("p", { class: "rv-help" }, el("strong", {}, "Did not run on this case, or not on every record (" + sk.length + "): "), "the group above says nothing about these."),
      el("ul", { class: "rv-cov-list" }, sk.map((x) => el("li", { "data-testid": "conflict-skipped-item", "data-skip-type": x.type, "data-reason-code": x.reason_code || null },
        el("strong", {}, x.label || humanType(x.type)), " ", x.reason || "",
        Array.isArray(x.record_nos) && x.record_nos.length ? el("span", { "data-testid": "conflict-skipped-records" }, " " + seqWords(x.record_nos) + " not read.") : null))));
  }
  function notesBox(ch) {
    const ns = ch && Array.isArray(ch.notes) ? ch.notes.filter((n) => n && n.text) : [];
    if (!ns.length) return null;
    return el("ul", { class: "rv-notes", "data-testid": "conflict-notes", "aria-label": "Notes about the conflict check, not conflicts" },
      ns.map((n) => el("li", { class: "rv-note", "data-testid": "conflict-note" }, el("span", { class: "chip chip--info", "data-icon": "info" }, "Note"), " ", n.text)));
  }
  // One line that is always on screen, with or without conflicts: the two kinds the legal nurse named, and everything else not listed under Checked.
  const notCheckedLine = () => el("p", { class: "rv-help rv-notchecked", "data-testid": "conflict-not-checked-line" }, el("strong", {}, "Not checked: "),
    "left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.");
  // T-151: the server's own list is authoritative even when it is empty: `conflict_types: []` means no conflict check ran on this case (the reasons are in `skipped`). Never an empty list.
  const hasChecks = (c) => !!(c.checks && Array.isArray(c.checks.conflict_types));
  const noneRan = (c) => hasChecks(c) && c.checks.conflict_types.length === 0;
  const NONE_RAN = "No conflict checks ran for this case.";
  function coverage(c, open) {
    const ch = noneRan(c) || hasChecks(c) ? c.checks : null;
    const skippedTypes = new Set(ch ? (ch.skipped || []).map((x) => x.type) : []);      // a check that did not run (or not on every record) is listed as skipped, never as checked
    const checked = ch ? ch.conflict_types.filter((t) => !skippedTypes.has(t)).map((t) => (ch.labels && ch.labels[t]) || humanType(t)) : FALLBACK_CHECKED;
    const not = ch ? (ch.not_checked || []).map((x) => x.label || humanType(x.type)) : FALLBACK_NOT;
    const d = el("details", { class: "rv-coverage", "data-testid": "conflict-coverage", open: open || null },
      el("summary", {}, "What the conflict check covers (" + (noneRan(c) ? "no checks ran" : checked.length + (checked.length === 1 ? " kind" : " kinds") + " checked") + ")"),
      el("p", { class: "rv-help" }, el("strong", {}, "Checked: "), noneRan(c) ? NONE_RAN : "the code compares records for these kinds of conflict only."),
      checked.length ? el("ul", { class: "rv-cov-list" }, checked.map((t) => el("li", { "data-testid": "conflict-checked-item" }, t))) : noneRan(c) ? null : el("p", { class: "rv-help" }, "None ran on every record of this case."),
      el("p", { class: "rv-help" }, el("strong", {}, "Not checked: "), (ch ? "anything not listed above, including these, is not looked for. Read the records for them." : "any other kind of conflict, including these. Read the records for them.")),
      not.length ? el("ul", { class: "rv-cov-list" }, not.map((t) => el("li", { "data-testid": "conflict-not-checked-item" }, t))) : null,
      ch ? null : el("p", { class: "rv-help", "data-testid": "conflict-coverage-note" }, "The server did not send its own list for this case, so this is the standing summary."));
    return d;
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "flags-panel");
    root.setAttribute("aria-labelledby", "rv-flags-h");
    root.append(el("h2", { id: "rv-flags-h" }, "Flags"),
      el("p", { class: "rv-help" }, "Flags point to things worth checking. Accepting one means you have seen it: it goes to the internal notes, never into the letter."));
    if (c.injection && c.injection.banner) root.append(el("p", { class: "rv-banner", role: "note" }, c.injection.banner));
    if (ZL.sg) root.append(ZL.sg.dismissalBox(c));
    const flags = (c.flags || []).filter((f) => f.review_status !== "dismissed"), gone = (c.flags || []).filter((f) => f.review_status === "dismissed");
    GROUPS.forEach(([type, title, empty]) => {
      const list = RV.needsReviewFirst(flags.filter((f) => f.type === type));
      const g = el("section", { class: "rv-group", "data-group": type, "aria-labelledby": "rv-g-" + type },
        el("h3", { id: "rv-g-" + type }, title + " (" + list.length + ")"));
      if (type === "gap" && ZL.gapChanges) ZL.gapChanges.removed(c).forEach((t) => g.append(el("p", { class: "rv-gap-change", "data-testid": "gap-change-removed" }, t)));
      if (type === "conflict") {
        const dropped = gone.filter((f) => f.type === "conflict").length;
        if (!list.length && noneRan(c)) g.append(el("p", { class: "rv-empty", "data-testid": "conflict-empty" }, NONE_RAN + ((c.checks.skipped || []).length ? " The reasons are listed below." : "")));
        else if (!list.length) g.append(el("p", { class: "rv-empty", "data-testid": "conflict-empty" }, dropped ? "No open conflicts among the kinds checked (" + dropped + " dismissed, below). Other kinds are not checked." : "No conflicts found among the kinds checked. Other kinds of conflict are not checked."));
      } else if (!list.length) g.append(el("p", { class: "rv-empty" }, empty));
      list.forEach((f) => g.append(card(c, f)));
      if (type === "conflict") g.append(...[notesBox(c.checks), skippedBox(c.checks), notCheckedLine(), coverage(c, !list.length)].filter(Boolean));
      root.append(g);
    });
    if (gone.length) root.append(RV.dismissedBox("flags", gone.length, el("div", { class: "rv-dismissed-list", "data-testid": "dismissed-flags" }, gone.map((f) => card(c, f)))));   // T-136 (pass 5 F2)
  }
  RV.registerPanel("flags", render);
  RV.renderFlags = render;
})();
