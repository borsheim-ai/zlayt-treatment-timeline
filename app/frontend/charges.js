/* Charges panel (T-043): accepted total from the API (never summed here), "detected, not yet accepted" labelled as not a total,
   unclear tray for rates / estimates / damages / unreadable amounts (R-CH-3, R-CH-5, D-019). Charges: accept or dismiss only (D-010). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const RV = ZL.rv, el = (...a) => ZL.el(...a);
  const KIND = { charge: "Charge", rate: "Rate", estimate: "Estimate", damages: "Damages mention", unclear: "Unclear" };
  const recSeq = (c, id) => { const r = (c.records || []).find((x) => x.id === id); return r ? r.seq : String(id).replace(/^r/, ""); };
  const reasonIs = (a, code) => (a.reasons || []).includes(code);

  // "12 planned; discharged at visit 9" for a per-visit rate, read from the record headers/text the API returned (or a.rate_note when the backend sends it).
  function rateContext(c, a) {
    const n = a.rate_note || {};
    let planned = n.planned, last = n.last_visit;
    if (planned == null && last == null) {
      const prefix = (s) => String(s || "").split(",")[0].trim().toLowerCase();
      const me = (c.records || []).find((r) => r.id === (a.record_ids || [])[0]);
      const same = me ? (c.records || []).filter((r) => prefix(r.source_label) === prefix(me.source_label)) : [];
      same.forEach((r) => {
        const p = /Plan of care:\s*(\d+)\s*visits?/i.exec(r.text || ""); if (p && planned == null) planned = p[1];
        const v = /\bvisit\s+(\d+)/i.exec(r.source_label || ""); if (v && (last == null || +v[1] > +last)) last = v[1];
      });
    }
    const bits = (planned != null ? [planned + " planned"] : []).concat(last != null ? ["discharged at visit " + last] : []);
    return bits.join("; ");
  }
  // One-line description for the unclear tray. Wording comes from the amount's kind and the quoted line; nothing is computed.
  function unclearNote(c, a) {
    const bits = [];
    if (a.kind === "rate") {
      const m = /\bper\s+([A-Za-z]+)/i.exec(a.excerpt || "") || /\/\s*([A-Za-z]+)/.exec(a.excerpt || "");
      const unit = m ? m[1].toLowerCase() : null;
      bits.push("rate " + a.text + (unit ? "/" + unit : "") + "; " + (unit ? unit + " count" : "count") + " not stated");
      const ctx = a.note || a.detail || rateContext(c, a);
      if (ctx) bits[0] += " (" + ctx + ")";
    } else if (a.kind === "estimate") bits.push("estimate; not a bill");
    else if (a.kind === "damages") bits.push("mention of damages; not a bill");
    else if (a.value_cents == null) bits.push("unreadable amount; request clean copy of bill");
    else bits.push("unclear; not a bill");
    if (reasonIs(a, "INJECTION_SUSPECTED")) bits.push("appears inside instruction-like text");
    return bits.join("; ");
  }

  // Plain status words for the Status column. The reason itself is the code's (unclearNote); nothing is computed here.
  const STATUS_WORDS = { rate: "Not counted: a rate, not a bill", estimate: "Not counted: an estimate", damages: "Not counted: a damages mention", unclear: "Not counted: can't tell if this is a bill" };
  // T-166 F3/F24: the sentence of the quote that holds the amount, with the amount marked, so the row always shows its own figure and never ends mid-sentence. A short quote is shown whole. If that sentence
  // is itself very long, a window around the amount is shown with an ellipsis. The full quote is one click away (Open record) and stays in the title.
  function snippet(a) {
    const q = String(a.excerpt || ""), amt = String(a.text || ""), i = amt ? q.indexOf(amt) : -1;
    const box = el("blockquote", { class: "rv-quote", title: q, "data-testid": "charge-quote" });
    if (i < 0) { box.append(q); return box; }
    let from = 0, to = q.length, cut = false;
    if (q.length > 140) {
      const bounds = []; const re = /[.!?]\s+/g; let m;
      while ((m = re.exec(q))) bounds.push([m.index + 1, m.index + m[0].length]);   // [end of a sentence, start of the next]
      const s0 = bounds.filter((b) => b[1] <= i).pop(), e0 = bounds.find((b) => b[0] >= i + amt.length);
      from = s0 ? s0[1] : 0; to = e0 ? e0[0] : q.length;
      if (to - from > 240) {   // one very long sentence: a window around the amount
        cut = true; from = Math.max(from, i - 70); to = Math.min(to, i + amt.length + 50);
        if (from > 0) { const sp = q.indexOf(" ", from); if (sp >= 0 && sp < i) from = sp + 1; }
        if (to < q.length) { const sp = q.lastIndexOf(" ", to); if (sp > i + amt.length) to = sp; }
      }
    }
    box.append((cut && from > 0 ? "\u2026 " : "") + q.slice(from, i), el("mark", {}, amt), q.slice(i + amt.length, to) + (cut && to < q.length ? " \u2026" : ""));
    return box;
  }

  // D-059 (T-154): a charge the code flagged (likely duplicate / likely total) shows the flag and the server's sentence in its row; it is counted only after a confirm that names the flag.
  const flagName = (f) => (f && (f.name || (f.flag || "").replace(/_/g, " "))) || "Flagged";
  // The flag's own sentence in plain words. The server's refusal sentence wraps it ("Name: sentence It is not counted unless you confirm that flag by name (token)."), and its
  // duplicate sentence names the other charge by an internal id; neither belongs on screen (claims adjuster, T-154 r1). The other line is told by its service, amount, date and record that follow.
  function plain(msg, f) {
    let m = String(msg || ""); const nm = flagName(f);
    if (m.startsWith(nm + ": ")) m = m.slice(nm.length + 2);
    m = m.replace(/\s*It is not counted unless you confirm that flag by name\s*\([a-z_]+\)\.?(\s*The confirm you sent does not name this flag\.)?/i, "").replace(/\s*\([a-z]+(?:_[a-z]+)+\)/g, "");
    return m.replace(/(same charge as) [a-z]+\d+(?:_\d+)?(?=[:,.]|\s)/i, "$1 this earlier line").trim();   // net for an old server that named the other line by its internal id (a3, ax2_1); the T-159 backend names it by what the record says
  }
  const isDone = (a) => a.review_status === "accepted" && !!(a.flag && a.flag.confirmed_at);
  // T-174 r2: a line SHE counted (flag `separate_charge`) is her own decision, not a code flag she was shown: a neutral "Counted by you" with her confirm in plain words, said once. No amber box,
  // no "flag" wording. If she took the count back (Undo), the line says so and what accepting it again asks. Every other flag (likely duplicate, likely total) keeps the warning line.
  const isOwnCount = (a) => !!(a.kind === "charge" && a.flag && a.flag.flag === "separate_charge");
  function ownCountLine(a) {
    const done = isDone(a);
    return el("p", { class: "rv-counted-line", "data-testid": "charge-counted", "data-flag": "separate_charge" },
      done ? el("span", { class: "chip chip--info", "data-icon": "check", "data-testid": "counted-by-you" }, "Counted by you") : el("span", { class: "chip chip--muted", "data-testid": "count-taken-back" }, "Count taken back"), " ",
      done ? "You confirmed it is a separate charge for a service. No AI check was asked about it." : "You took back your count. Accept it to count this line again; you confirm it is a separate charge for a service.");
  }
  function chargeFlag(a) {
    const f = a.kind === "charge" ? a.flag : a.countable ? a.count_confirm || a.flag : null;   // D-064: a line she can count carries the flag she must confirm as `count_confirm` (the server's own object), shown before she clicks anything
    if (!f || a.review_status === "dismissed") return null;   // D-064: a line she can count may already carry the code's flag (likely duplicate / likely total)
    if (isOwnCount(a)) return ownCountLine(a);
    return el("p", { class: "rv-reason-line", "data-testid": "charge-flag", "data-flag": f.flag },
      el("span", { class: "chip chip--warn", "data-icon": "alert" }, flagName(f)), " ", isDone(a) ? "You confirmed this flag and counted the charge." : plain(f.message, f));
  }
  const chargeOf = (id) => { const c = RV.caseNow(); return c ? (c.amounts || []).find((x) => x.id === id && x.kind === "charge" && x.flag) || null : null; };
  // The code's flag and her named confirm, for the places that tell how an item was checked (the Audit drawer, the "How this was checked" dialog). Read from the case item, which the page already holds;
  // the trace and the audit events do not carry it yet (backend card T-159), and the page then uses theirs.
  ZL.chargeFlagNote = function (id, testid) {
    const a = chargeOf(id); if (!a) return null;
    const f = a.flag, name = flagName(f), done = isDone(a), dismissed = a.review_status === "dismissed";
    if (isOwnCount(a) && !dismissed) {   // her own count, not a code flag
      const t = done ? "You counted this line as a separate charge and confirmed it by name at " + f.confirmed_at + ". No AI check was asked about it." : "You counted this line, then took the count back. Accepting it again asks you to confirm it is a separate charge for a service.";
      return el("p", { class: "rv-counted-line", "data-testid": testid, "data-flag": f.flag, "data-confirmed": String(done) }, el("span", { class: "chip chip--info" }, done ? "Counted by you" : "Count taken back"), " ", t);
    }
    const text = dismissed ? "The code flagged this charge: " + name.toLowerCase() + ". You dismissed it, so it is not counted."
      : done ? "The code flagged this charge: " + name.toLowerCase() + ". You confirmed that flag by name at " + f.confirmed_at + ", so the charge is counted."
      : "The code flagged this charge: " + name.toLowerCase() + ". " + plain(f.message, f) + " It needs your named confirm before it counts.";
    return el("p", { class: "rv-reason-line", "data-testid": testid, "data-flag": f.flag, "data-confirmed": String(done) }, el("span", { class: "chip chip--warn", "data-icon": "alert" }, name), " ", text);
  };
  ZL.chargeConfirmWord = (id) => { const a = chargeOf(id); return a && isDone(a) ? "confirmed " + flagName(a.flag) : null; };
  let confirmDlg = null;
  // Resolves true when she confirms the named flag; false on Cancel or Escape. Cancel has focus, so Enter alone never counts the charge.
  ZL.confirmCharge = function (f, item) {
    const name = flagName(f), lower = name.charAt(0).toLowerCase() + name.slice(1);
    if (!confirmDlg) {
      confirmDlg = el("dialog", { class: "dlg dlg--sm", "data-testid": "charge-confirm", "aria-labelledby": "cc-title" },
        el("div", { class: "dlg-head" }, el("h2", { id: "cc-title" }, "Count this flagged charge?")),
        el("div", { class: "dlg-body" }, el("p", {}, "The code flagged it: ", el("strong", { id: "cc-flag", "data-testid": "charge-confirm-flag" })), el("p", { id: "cc-msg", "data-testid": "charge-confirm-msg" }),
          el("p", { class: "muted", id: "cc-amount" })),
        el("div", { class: "dlg-foot" }, el("button", { type: "button", class: "btn", id: "cc-cancel", "data-testid": "btn-charge-cancel" }, "Cancel"), el("button", { type: "button", class: "btn btn--primary", id: "cc-ok", "data-testid": "btn-charge-confirm" })));   // Cancel first: it has focus, and Tab reaches Confirm next
      document.body.append(confirmDlg);
    }
    const d = confirmDlg, q = (i) => d.querySelector(i);
    q("#cc-flag").textContent = name; q("#cc-msg").textContent = plain(f.message, f);
    q("#cc-amount").textContent = item && item.text ? "Charge: " + item.text + ". It is not counted unless you confirm the flag by name." : "It is not counted unless you confirm the flag by name.";
    q("#cc-ok").textContent = "Confirm " + lower + " and accept"; q("#cc-ok").setAttribute("aria-label", "Confirm " + lower + " and accept the charge");
    if (d.open) d.close();
    return new Promise((resolve) => {
      const done = (v) => { d.removeEventListener("close", onClose); d.removeEventListener("cancel", onCancel); q("#cc-ok").onclick = q("#cc-cancel").onclick = null; if (d.open) d.close(); resolve(v); };
      const onClose = () => { if (!d.open) done(false); };   // a close event queued by the PREVIOUS use can arrive after this use has opened the window again: it must not shut it
      const onCancel = (ev) => { ev.preventDefault(); done(false); };   // Escape: settle now, in the same task that hides the window, not in the later close event (the item stays "busy" until then, and a key pressed right after Escape was dropped)
      d.addEventListener("close", onClose); d.addEventListener("cancel", onCancel);
      q("#cc-ok").onclick = () => done(true); q("#cc-cancel").onclick = () => done(false);
      d.showModal(); q("#cc-cancel").focus();
    });
  };

  // D-064 (T-172): an amount held back only for a missing detail (a.countable) can be counted by her, after a confirm that names what she checked. A rule-excluded one (countable false) shows its
  // reason and offers nothing. The reason and the sentence are the server's (amounts.not_counted); nothing is worked out here.
  const NAMED_CONFIRM = "I checked this is a separate charge for a service";
  let countDlg = null;
  // The flag she must name before this line is counted: `count_confirm` (the case view, read before any dialog opens), else a `flag` already on the amount.
  const heldFlag = (a) => { const f = a.count_confirm || a.flag; return f && f.flag && f.flag !== "separate_charge" && !f.confirmed_at && f.confirm_with ? f : null; };
  function confirmCount(a) {
    if (!countDlg) {
      countDlg = el("dialog", { class: "dlg dlg--sm", "data-testid": "count-confirm", "aria-labelledby": "cn-title" },
        el("div", { class: "dlg-head" }, el("h2", { id: "cn-title" }, "Count this charge?")),
        el("div", { class: "dlg-body" }, el("p", { id: "cn-amount", "data-testid": "count-confirm-amount" }), el("p", { class: "muted", id: "cn-reason", "data-testid": "count-confirm-reason" }), el("div", { id: "cn-quote" }),
          el("p", { class: "muted" }, "It is added to the total only if this line is a charge for one service. A summary, balance or payment line is not.")),
        el("div", { class: "dlg-foot" }, el("button", { type: "button", class: "btn", id: "cn-cancel", "data-testid": "btn-count-cancel" }, "Cancel"),
          el("button", { type: "button", class: "btn btn--primary", id: "cn-ok", "data-testid": "btn-count-confirm" }, NAMED_CONFIRM)));   // Cancel first: it has focus, and Tab reaches the named confirm next
      document.body.append(countDlg);
    }
    const d = countDlg, q = (i) => d.querySelector(i);
    q("#cn-amount").textContent = "Amount: " + a.text; q("#cn-reason").textContent = "Not counted now: " + a.not_counted_reason;
    q("#cn-quote").replaceChildren(a.excerpt ? snippet(a) : "");   // the sentence of the record that holds the figure, so she checks the line itself
    q("#cn-ok").setAttribute("aria-label", NAMED_CONFIRM + ": count " + a.text);
    if (d.open) d.close();
    return new Promise((resolve) => {
      const done = (v) => { d.removeEventListener("close", onClose); d.removeEventListener("cancel", onCancel); q("#cn-ok").onclick = q("#cn-cancel").onclick = null; if (d.open) d.close(); resolve(v); };
      const onClose = () => { if (!d.open) done(false); };   // same rule as confirmCharge: settle on cancel, and ignore a stale close event from the previous use
      const onCancel = (ev) => { ev.preventDefault(); done(false); };
      d.addEventListener("close", onClose); d.addEventListener("cancel", onCancel);
      q("#cn-ok").onclick = () => done(true); q("#cn-cancel").onclick = () => done(false);
      d.showModal(); q("#cn-cancel").focus();
    });
  }
  const counting = new Set();
  const countError = (id, msg) => {
    const row = document.querySelector('[data-item-id="' + id + '"]'), host = row && row.querySelector('[data-testid="count-host"]'); if (!host) return;
    host.querySelector('[data-testid="count-error"]').textContent = msg; host.querySelector('[data-testid="count-error"]').hidden = !msg;
  };
  async function countIt(a, btn) {
    const id = a.id, c = RV.caseNow(); if (!c || counting.has(id)) return;
    counting.add(id);
    try {
      const held = heldFlag(a);   // a likely duplicate (or likely total) is asked for FIRST, by name, with the flag shown: she never meets the flag only after the separate-charge confirm
      let body = { action: "count", confirm: "separate_charge" }, resp = null;
      if (held && ZL.confirmCharge) {   // the T-154 flagged-charge dialog
        if (!(await ZL.confirmCharge(held, a))) { if (btn && btn.isConnected) btn.focus(); return; }
        body.confirm_flag = held.confirm_with;
      }
      if (!(await confirmCount(a))) { if (btn && btn.isConnected) btn.focus(); return; }
      for (let tries = 0; tries < 2 && !resp; tries++) {
        try { resp = await ZL.api.review(c.token, id, body); }
        catch (e) {
          const d = (e && e.detail) || {};
          if (tries === 0 && e && String(e.code).toUpperCase() === "CONFIRM_REQUIRED" && d.flag && d.flag !== "separate_charge" && d.confirm_with && ZL.confirmCharge) {   // it would double another charge: the same flag confirm as a flagged charge
            const ok = await ZL.confirmCharge({ flag: d.flag, name: d.name, message: d.message || e.message, confirm_with: d.confirm_with }, a);
            if (!ok) { if (btn && btn.isConnected) btn.focus(); return; }
            body = Object.assign({}, body, { confirm_flag: d.confirm_with });
          } else { countError(id, (e && e.message) || "That did not work. Try again."); RV.say((e && e.message) || "That did not work. Try again.", true); return; }
        }
      }
      const cur = ZL.state.get().case;   // applyReview keeps an amount's own kind; counting changes it to charge, so take the case-view shape the server sent
      if (resp.amount) { const i = (cur.amounts || []).findIndex((x) => x.id === id); if (i >= 0) cur.amounts[i] = Object.assign({}, cur.amounts[i], resp.amount); }
      ZL.state.applyReview(resp);
      RV.say("Counted " + a.text + " as a separate charge. Accepted charges now " + RV.money((((ZL.state.get().case || {}).totals || {}).accepted || {}).cents || 0) + ".");
      const row = document.querySelector('[data-item-id="' + id + '"]'); if (row) { row.focus(); if (row.scrollIntoView) row.scrollIntoView({ block: "center" }); }
    } finally { counting.delete(id); }
  }
  function countAction(a) {
    if (!a.countable || a.kind === "charge" || a.review_status === "dismissed") return null;
    const btn = el("button", { type: "button", class: "btn rv-count", "data-testid": "btn-count-charge", "aria-label": "Count this charge: " + a.text, onclick: () => countIt(a, btn) }, "Count this charge");
    return el("div", { class: "rv-count-host", "data-testid": "count-host" }, btn, el("p", { class: "rv-error", role: "alert", hidden: true, "data-testid": "count-error" }));
  }
  // The plain "Not counted: <reason>" line for every amount that is not a charge. The server's sentence is shown as sent.
  const notCounted = (a) => a.kind !== "charge" && a.not_counted_reason ? el("p", { class: "rv-reason-line rv-not-counted", "data-testid": "not-counted-reason" }, el("strong", {}, "Not counted: "), a.not_counted_reason) : null;

  function row(c, a, inTray, boiler) {
    const isCharge = a.kind === "charge";
    const rs = a.review_status || "pending";
    const seq = recSeq(c, (a.record_ids || [])[0]);
    const tr = el("tr", { class: "rv-card rv-amount", tabindex: "0", "data-testid": "amount-" + a.text, "data-item-id": a.id, "data-amount-kind": a.kind,
      "data-state": a.state, "data-review": rs, "aria-label": "Amount " + a.text });
    const first = el("td", { class: "rv-c-amount", "data-label": "Amount" }, el("strong", { class: "rv-money", title: "As written in the record: " + a.text }, a.value_cents != null ? RV.money(a.value_cents) : a.text), el("span", { class: "rv-kind" }, KIND[a.kind] || a.kind));
    const ctrl = RV.controls(a, "amount");
    // T-166 F11/F7: Open record stays; Why this status and Audit wait behind More.
    // T-174 F21: ONE Not counted reason in the row (the code's plain sentence). The kind-and-detail line ("rate $185/visit; visit count not stated") waits behind More, so it adds to the reason and never repeats it.
    const detail = inTray && a.kind !== "charge" && a.not_counted_reason ? el("span", { class: "rv-unclear-note rv-detail", "data-testid": "charge-detail" }, unclearNote(c, a)) : null;
    const more = RV.moreActions([ZL.stepper ? ZL.stepper.traceButton(a.id, "btn btn--link") : null, ctrl.querySelector(".rv-audit"), detail], a.text, { testid: "btn-more", panelTestid: "charge-more-panel" });
    const src = el("td", { class: "rv-c-src", "data-label": "From the record" },
      snippet(a),
      el("div", { class: "rv-src-links" },
        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": "Open record " + seq + " for the amount " + a.text, onclick: () => RV.openSource(a, "amount") }, "Open record " + seq),
        more.btn, more.panel));
    // one reason line (the code's). The server's longer sentence is shown only when it adds something and is not a notice every row repeats.
    const nc = notCounted(a);
    let why = a.why && !boiler.has(a.why) && !(isOwnCount(a) && isDone(a)) ? a.why : null;   // a counted line's own sentence is already said by its "Counted by you" line
    if (why && nc) { why = why.split(a.not_counted_reason).join("").replace(/\s+/g, " ").trim() || null; }   // the reason is already on its own line; keep only what the server adds to it (for example the second check's note)
    const gone = rs === "dismissed";   // T-060 r5: a dismissed amount is decided; it keeps its quote, the word Dismissed and Undo, and no "Needs review" reason
    const fl = chargeFlag(a);
    const status = el("td", { class: "rv-c-status", "data-label": "Status" }, RV.chips(a), fl,
      nc && !gone ? nc : null,
      inTray && !gone && !nc ? el("span", { class: "rv-unclear-note" }, STATUS_WORDS[a.kind] || STATUS_WORDS.unclear, ". ", unclearNote(c, a)) : null,
      !isCharge && (rs === "accepted") ? el("span", { class: "rv-noted" }, "Kept in the internal notes only; not in the letter or the total.") : null,
      why && !gone ? el("p", { class: a.state === "needs_review" ? "rv-reason-line" : "rv-why" }, why) : null);
    const act = el("td", { class: "rv-c-act", "data-label": "Decision" }, countAction(a), ctrl);
    tr.append(first, src, status, act);
    return tr;
  }

  function table(c, list, caption, inTray, boiler) {
    return el("table", { class: "rv-table", "data-group": inTray ? "unclear-amounts" : "charges" }, el("caption", { class: "rv-sr" }, caption),
      el("thead", {}, el("tr", {}, ["Amount", "From the record", "Status", "Decision"].map((h) => el("th", { scope: "col" }, h)))),
      el("tbody", {}, RV.needsReviewFirst(list).map((a) => row(c, a, inTray, boiler))));
  }
  // A sentence that several rows carry (for example the Spanish-record notice) is shown once above the table and left out of the rows.
  function repeated(list) {
    const n = {}; list.forEach((a) => { if (a.why) n[a.why] = (n[a.why] || 0) + 1; });
    return new Set(Object.keys(n).filter((k) => n[k] > 1));
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "charges-panel");
    root.setAttribute("aria-labelledby", "rv-charges-h");
    const amounts = c.amounts || [], t = c.totals || {};
    const live = amounts.filter((a) => a.review_status !== "dismissed"), gone = amounts.filter((a) => a.review_status === "dismissed");   // T-136 (pass 5 F2): dismissed amounts wait under "Dismissed (n)"
    const charges = live.filter((a) => a.kind === "charge"), unclear = live.filter((a) => a.kind !== "charge");
    const acc = (t.accepted && t.accepted.cents) != null ? t.accepted.cents : 0;
    const pendObj = t.pending || t.detected_not_a_total || { cents: 0 };
    root.append(el("h2", { id: "rv-charges-h" }, "Charges"),
      el("p", { class: "rv-help" }, "Only charges you accept are counted. Rates, estimates, damages and unreadable amounts are listed below and never added."),
      el("div", { class: "rv-totals" },
        el("p", { class: "rv-total rv-total-main", "data-testid": "accepted-total", "aria-live": "polite" }, el("span", { class: "rv-total-label" }, "Accepted charges: "), el("strong", {}, RV.money(acc))),
        el("p", { class: "rv-total rv-total-pending", "data-testid": "pending-total" }, "Detected, not yet accepted: " + RV.money(pendObj.cents || 0) + " (not a total)")));
    const overlap = ZL.sg ? ZL.sg.overlapBox(c) : null; if (overlap) root.append(overlap);
    root.append(el("h3", {}, "Detected charges (" + charges.length + ")"));
    const chBoil = repeated(charges), unBoil = repeated(unclear);
    if (charges.length) { chBoil.forEach((t) => root.append(el("p", { class: "rv-tray-note" }, t))); root.append(table(c, charges, "Detected charges", false, chBoil)); } else root.append(el("p", { class: "rv-empty" }, "No charges were found."));
    const tray = el("section", { class: "rv-tray", "data-testid": "unclear-tray", "aria-labelledby": "rv-unclear-h" },
      el("h3", { id: "rv-unclear-h" }, "Unclear — not totaled (" + unclear.length + ")"));
    if (unclear.length) { unBoil.forEach((t) => tray.append(el("p", { class: "rv-tray-note", "data-testid": "tray-notice" }, t))); tray.append(table(c, unclear, "Unclear amounts, not totaled", true, unBoil)); } else tray.append(el("p", { class: "rv-empty" }, "Nothing unclear."));
    root.append(tray);
    if (gone.length) {
      const boil = repeated(gone);
      root.append(RV.dismissedBox("amounts", gone.length, el("table", { class: "rv-table", "data-testid": "dismissed-amounts" }, el("caption", { class: "rv-sr" }, "Dismissed amounts"),
        el("thead", {}, el("tr", {}, ["Amount", "From the record", "Status", "Decision"].map((h) => el("th", { scope: "col" }, h)))),
        el("tbody", {}, gone.map((a) => row(c, a, a.kind !== "charge", boil))))));
    }
  }
  RV.registerPanel("charges", render);
  RV.renderCharges = render;
})();
