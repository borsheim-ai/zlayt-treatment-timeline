/* Step 3: Check the bills (/case/<token>/bills[?item=<id>]). OWNER: frontend-B. Spec 6 (6.1 charge, 6.2 countable with a check, 6.3 never counted, 6.4 done); D-059 (a flagged charge needs its named confirm), D-060/D-064 (a line held back
   only for a missing detail is counted with count + confirm separate_charge), D-062 (the letter's total line), D-066 (compare box when the second check disputed the amount), T-178 (version + expected_status: review.js).
   Charges are never batched: there is no "count all". Record text, figures and reasons go in with textContent only. */
(function () {
  const G = window.G, { h } = G, R = G.review;

  /* ---------- the queue (6): charges and countable amounts first (record order, then position), then the amounts that are never counted ---------- */
  const live = (c) => (c.amounts || []).filter(G.steps.live);
  const kindOf = (a) => (a.kind === "charge" ? "charge" : a.countable ? "count" : "never");
  function buildQueue(c) {
    const recs = Object.fromEntries((c.records || []).map((r) => [r.id, r]));
    const seq = (a) => { const r = recs[(a.record_ids || [])[0]]; return r ? r.seq : 9999; };
    return live(c).slice().sort((a, b) => (kindOf(a) === "never") - (kindOf(b) === "never") || seq(a) - seq(b) || (a.excerpt_start || 0) - (b.excerpt_start || 0) || (a.id < b.id ? -1 : 1)).map((a) => ({ id: a.id }));
  }
  const find = (c, id) => (c.amounts || []).find((a) => a.id === id) || null;
  const cents = (a) => (a.value_cents == null ? null : a.value_cents);
  const hasDollar = (t) => /\$\s*\d|\d\s*(?:USD|dollars)/i.test(t || "");
  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the record date whenever it is not that day. Code only, no guessing. */
  const sdOf = (a) => (a && a.service_date && typeof a.service_date === "object" ? a.service_date : null);
  const stmtOnly = (sd) => !!sd && !!sd.statement_date_iso && !(sd.state === "stated" && sd.date_iso === sd.statement_date_iso && !sd.end_iso);      // a bill's date, not the day of the service
  /* T-206: a record's date is shown bare only when it is a certain service date. An amount with no service_date of its own (a ledger line not counted yet, a UB-04 or invoice total) never has one: a bill document's date is its statement's. */
  const BILL_DOC = /\b(ledger|invoice|statement|UB-?04|CMS-?1500|HCFA|EOB|explanation of benefits|itemi[sz]ed|billing|bill)\b/i;
  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === "count" || BILL_DOC.test((rec && rec.source_label) || "")));
  /* D-075 (T-202 r7): the record's own date is always called "record dated"; the app never classifies a source as a bill or a clinical record. */
  const dateWord = () => "record";
  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (st ? st + " dated " + d : d) : "no date"; };      // st: false, or the word "statement" | "record"
  const recLabel = (r, st) => `Record ${r.seq} · ${r.source_label || "Record"} · ${recDate(r, st)}`;
  const figure = (a) => (cents(a) != null ? R.money(cents(a)) : a.text || "");
  const FLAG_BOX = { likely_duplicate: "I checked: this is a separate charge, not the same one counted twice.", likely_total: "I checked: this is a charge of its own, not a total of the others." };
  const flagBox = (f) => FLAG_BOX[f.flag] || `I checked: ${String(f.name || f.flag || "this is right").replace(/\.$/, "")}.`;

  /* the date of service exactly as the letter prints it; the statement date, when different, is named as that */
  const dateLine = (sd) => h("p", { class: "svc-date gap-top", "data-testid": "service-date", "data-state": sd.state },
    /^date of service/i.test(sd.text || "") ? null : h("span", { class: "label-cap" }, "Date of service "), h("b", { "data-testid": "service-date-text" }, sd.text || ""),
    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso)}`) : null);
  const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
  /* T-206/T-209 r3: the note above states the specific reason; this sentence is the same for every reason that is not certain, so it can never contradict the note: find the date outside this card's guess, write it in the letter's blank. The card has no control to type a date. */
  const confirmNext = (sd) => {
    const paren = /\(record dated/.test((sd && sd.text) || ""), stmt = paren ? " The date in parentheses is the record date, not the service date." : "";
    return h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank ", h("b", {}, "\u201Cdate of service [__________]\u201D"), " in your letter." + stmt,
      " Counting it adds the amount to the bill total.");
  };

  function present(S, item) {
    const kind = kindOf(item), recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), rec = recs[0];
    const sd = sdOf(item), st = stmtDated(item, sd, rec) && dateWord(sd);
    const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r) && dateWord(sd)) : null }));
    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, st) : "", nodes: srcNodes };
    const sub = rec ? [rec.source_label, rec.date_iso ? (st ? st + " dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
    const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null);
    const decided = item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited";
    const flag = item.flag && item.confirm_required ? item.flag : null;
    const note = item.duplicate_note ? h("p", { class: "explain muted gap-top", "data-testid": "duplicate-note" }, R.plain(item.duplicate_note)) : null;
    const compareBox = () => R.check(S, "compare", "I read this amount against the highlighted words myself.");
    const compareFoot = () => [h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), " Read it against the highlighted words before you decide.", compareBox()];
    const ticked = (k) => R.ticked(S, k);

    if (kind === "charge") {
      const foot = []; let cls = "plain";
      if (flag) { cls = "attn"; foot.push(h("strong", { "data-testid": "flag-message" }, R.plain(flag.message)), R.check(S, "flag", flagBox(flag))); }
      if (disp) { cls = "attn"; if (flag) foot.push(h("hr", { class: "foot-rule" })); foot.push(...compareFoot()); }
      if (!flag && !disp) {
        if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "not counted." : "counted in the bill total.", " You can change it."); }
        else if (!(sd && sd.confirm_note)) foot.push("If you count it, it's added to the bill total in the letter, with the highlighted words as its source.");
      }
      return { tag: { cls: "ok", text: "Charge" }, sub, src,
        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), sd ? dateLine(sd) : null, h("p", { class: "explain muted gap-top" }, "Written in the record as ", h("b", {}, item.text || ""), "."), note],
        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), confirmNext(sd), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain: the note leads the foot, in plain words, under the highlighted quote
        question: "Should this charge count toward the bill total?",
        yes: { label: "Yes, count it", disabled: () => (!!flag && !ticked("flag")) || (!!disp && !ticked("compare")),
          run: () => S.decide(item, "accept", { ...(flag ? { confirm: flag.confirm_with } : {}), ...(disp && ticked("compare") ? { compared: true } : {}) }) },
        no: { label: "No, don't count it", run: () => S.decide(item, "dismiss") }, third: null };
    }

    if (kind === "count") {
      const cc = item.count_confirm, foot = [h("span", { "data-testid": "count-hint" }, "You can still count it if you checked the ledger yourself."), R.check(S, "separate", "I checked this is a separate charge for a service.")];
      if (cc) foot.push(h("p", { class: "foot-warn", "data-testid": "count-confirm-message" }, R.plain(cc.message)), R.check(S, "flag", flagBox(cc)));
      if (disp) foot.push(h("hr", { class: "foot-rule" }), h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), compareBox());
      return { tag: { cls: "warn", text: "Not counted yet" }, sub, src,
        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), h("p", { class: "explain gap-top", "data-testid": "reason" }, R.plain(item.not_counted_reason || item.why)), note],
        foot: { cls: "attn", nodes: foot },
        question: "Should this amount count toward the bill total?",
        yes: { label: "Yes, count it", disabled: () => !ticked("separate") || (!!cc && !ticked("flag")), run: () => S.decide(item, "count", { confirm: "separate_charge", ...(cc ? { confirm_flag: cc.confirm_with } : {}) }) },
        no: { label: "No, don't count it", disabled: () => !!disp && !ticked("compare"), run: () => S.decide(item, "accept", disp && ticked("compare") ? { compared: true } : undefined) }, third: null };
    }

    const foot = [];
    let cls = "plain";
    if (disp) { cls = "attn"; foot.push(...compareFoot()); }
    else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "left out of the notes." : "listed in the notes for the attorney.", " It is never added to the bill total."); }
    else foot.push("Either way, it is never added to the bill total.");
    const money = hasDollar(item.text);
    return { tag: { cls: "never", text: "Never counted" }, sub, src,
      body: [money ? h("p", { class: "money", "data-testid": "figure" }, item.text) : h("p", { class: "line-text", "data-testid": "figure" }, h("span", { class: "muted" }, "Not a money amount: "), item.text || ""),
        h("p", { class: "explain gap-top", "data-testid": "reason" }, R.plain(item.not_counted_reason || item.why)), note],
      foot: { cls, nodes: foot },
      question: "This amount is never added to the total. List it in the notes for the attorney?",
      yes: { label: "Yes, list it", disabled: () => !!disp && !ticked("compare"), run: () => S.decide(item, "accept", disp && ticked("compare") ? { compared: true } : undefined) },
      no: { label: "No, leave it out", run: () => S.decide(item, "dismiss") }, third: null };
  }

  /* T-211: the "You" row of "How this was checked" (null = no decision yet) */
  function youText(S, item) {
    const st = item.review_status, k = kindOf(item);
    if (!st || st === "pending") return null;
    if (st === "dismissed") return k === "charge" ? "You chose not to count it." : k === "count" ? "You left it out of the notes." : "You left it out of the notes for the attorney.";
    return k === "charge" ? "You counted it in the bill total." : k === "count" ? "You did not count it. It is noted for the attorney." : "You listed it in the notes for the attorney. It is never added to the total.";
  }

  function statusFor(S, item, resp, action) {
    const f = item ? figure(item) : "this amount", kind = item ? kindOf(item) : "never";
    if (action === "count") return `${f} counted in the bill total`;
    if (action === "dismiss") return kind === "never" ? `${f} left out of the notes` : `${f} not counted`;
    if (kind === "charge") return `${f} counted in the bill total`;
    if (kind === "count") return `${f} not counted. It is noted for the attorney`;
    return `${f} listed in the notes for the attorney`;
  }

  /* ---------- 6.4 done ---------- */
  function letterLine(c) { const t = c.totals || {}; return t.letter_line || `Billed charges accepted from these records: ${R.money((t.accepted || {}).cents || 0)}`; }
  function done(S) {
    const c = S.c, items = S.counted().map((q) => S.item(q.id)), recs = Object.fromEntries((c.records || []).map((r) => [r.id, r]));
    const left = items.filter(G.steps.undecided), changeHref = (a) => G.url.bills(S.token, a.id);
    const from = (a) => { const r = recs[(a.record_ids || [])[0]]; return r ? r.source_label || "" : ""; }, when = (a) => {
      const sd = sdOf(a); if (sd && sd.text) return sd.text;          // the letter's own date text
      const r = recs[(a.record_ids || [])[0]], d = r && r.date_iso ? R.longDate(r.date_iso) : "", by = a.ladder && a.ladder.code_checks && a.ladder.code_checks.classified_by;
      return d && /^reviewer:counted/.test(by || "") ? `No date of service (record dated ${d})` : d;          // a ledger line she counted states no date of service
    };
    const counted = items.filter((a) => a.kind === "charge" && (a.review_status === "accepted" || a.review_status === "edited") && !a.edit_to_check);
    const notCounted = items.filter((a) => (a.kind === "charge" && a.review_status === "dismissed") || (a.kind !== "charge" && a.countable));
    const never = items.filter((a) => a.kind !== "charge" && !a.countable);
    const row = (a, cols) => h("tr", { "data-testid": "bill-row", "data-item": a.id }, h("td", { class: "amt" }, !(a.kind === "charge" || a.countable) ? (hasDollar(a.text) ? a.text : "Not a money amount: " + (a.text || "")) : figure(a)), ...cols.map((x) => h("td", {}, x)), h("td", {}, h("a", { class: "btn", href: changeHref(a), "data-testid": "btn-change" }, "Change")));
    const table = (head, rows) => {
      rows.forEach((tr) => [...tr.children].forEach((td, i) => td.setAttribute("data-label", i < head.length ? head[i] : "")));       // phones show each row as a small card: the label comes from here
      return h("table", { class: "mini" }, h("thead", {}, h("tr", {}, ...head.map((x) => h("th", {}, x)), h("th", {}))), h("tbody", {}, rows));
    };
    const overlaps = ((c.totals || {}).possible_overlaps || []);
    const hero = left.length
      ? h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "!"), h("div", {}, h("h2", { "data-testid": "done-heading" }, `${left.length} amount${left.length === 1 ? " still needs" : "s still need"} a decision.`), h("p", {}, "Amounts you don't decide stay out of the bill total.")))
      : h("div", { class: "done-hero" }, h("div", { class: "big-check", "aria-hidden": "true" }, "✓"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "You checked every bill amount."), h("p", {}, "This is the total line your letter will carry:")));
    return R.doneFrame(3, "Check the bills",
      h("div", { class: "panel" }, hero, h("p", { class: "total-line num", "data-testid": "letter-line" }, letterLine(c)),
        h("div", { class: "row-actions" }, left.length ? h("a", { class: "btn primary lg", href: G.url.bills(S.token, left[0].id), "data-testid": "btn-first-undecided" }, "Go to the first one") : null,
          h("a", { class: "btn lg " + (left.length ? "" : "primary"), href: G.url.letter(S.token), "data-testid": "btn-next-step" }, "Go to step 4: Get your letter"))),
      ...overlaps.map((o) => h("div", { class: "note-box overlap", "data-testid": "overlap" }, h("div", { class: "nb-text" }, "Check these two amounts", h("span", {}, R.plain(o.message))),
        h("div", { class: "row-actions tight" }, [o.statement_amount_id, o.covered_amount_id].map((id, i) => h("a", { class: "btn", href: G.url.bills(S.token, id) }, `Change ${i ? o.covered_text : o.statement_text}`))))),
      h("div", { class: "panel", "data-testid": "list-counted" }, h("h2", {}, `Counted (${counted.length})`),
        counted.length ? table(["Amount", "From", "Date of service"], counted.map((a) => row(a, [from(a), when(a)]))) : h("p", { class: "muted" }, "You didn't count any charge.")),
      h("div", { class: "panel", "data-testid": "list-not-counted" }, h("h2", {}, `Not counted by you (${notCounted.length})`),
        notCounted.length ? table(["Amount", "From", "Why"], notCounted.map((a) => row(a, [from(a), a.kind === "charge" ? "You chose not to count it." : R.plain(a.not_counted_reason || "")]))) : h("p", { class: "muted" }, "You didn't leave out any charge.")),
      h("div", { class: "panel", "data-testid": "list-never" }, h("h2", {}, `Never counted (${never.length})`), h("p", { class: "muted" }, "These are never added to the total. The ones you listed go in the notes for the attorney."),
        never.length ? table(["Amount", "From", "Why it's never counted"], never.map((a) => row(a, [from(a), R.plain(a.not_counted_reason || "")]))) : null));
  }
  function empty(S) {
    return R.doneFrame(3, "Check the bills", h("div", { class: "panel" }, h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "–"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "We didn't find any bill amounts in these records."), h("p", {}, "There is nothing to count."))),
      h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: G.url.letter(S.token), "data-testid": "btn-next-step" }, "Go to step 4: Get your letter"))));
  }

  G.pages.bills = function (ctx) {
    return R.run(ctx, { step: 3, title: "Check the bills", unit: "Amount", chip: true, buildQueue, find, present, statusFor, done, empty, youText });
  };
})();
