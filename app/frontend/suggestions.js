/* Suggestions and confidence (T-096). Four small pieces, all built with textContent / text nodes only:
   ZL.sg.dateForm      dates to confirm: suggested reading pre-selected with its reason; one explicit Confirm click is still required (T-088)
   ZL.sg.dismissalBox  banner "You dismissed this kind of flag N times..." with Hide similar / Keep showing (T-089); never hides on load
   ZL.sg.calibration   measured precision: the backend's own sentences, a small-sample note, plain words when the file is missing or invalid (T-099)
   ZL.sg.overlapBox    possible overlap between a statement line and a separate charge, beside the case charge total (T-110)
   Nothing here computes a percentage, a total or a date; every number shown is one the API sent. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const el = (...a) => ZL.el(...a);
  const say = (m, bad) => { if (ZL.rv && ZL.rv.say) ZL.rv.say(m, bad); };
  const recOf = (c, id) => ((c && c.records) || []).find((r) => r.id === id);
  const recSeq = (c, id) => { const r = recOf(c, id); return r ? r.seq : String(id).replace(/^r/, ""); };
  const sg = (ZL.sg = {});

  // ---- 1. date convention suggestion --------------------------------------------------------------------------------------------
  // A usable suggestion names one of the code candidates (iso is null when the year is also ambiguous: then nothing is pre-selected).
  sg.usableSuggestion = function (d) {
    const s = d && d.suggestion;
    return s && s.iso && (d.candidates || []).includes(s.iso) ? s : null;
  };
  let formSeq = 0;
  // d = a dates_to_confirm row; onConfirm(date) is async and may throw (its message is shown, the choice stays).
  sg.dateForm = function (d, opts) {
    opts = opts || {};
    const sug = sg.usableSuggestion(d), n = ++formSeq, raw = d.raw || d.date_raw || "";
    const err = el("p", { class: "rv-error sg-error", role: "alert", "data-testid": "confirm-date-error" });
    const submit = el("button", { type: "submit", class: "btn btn--primary sg-confirm", "data-testid": "btn-confirm-date", disabled: !sug }, "Confirm date");
    const reasonId = "sg-reason-" + n;
    const radios = (d.candidates || []).map((cand) => {
      const input = el("input", { type: "radio", name: "cd-" + n, value: cand, "data-testid": "confirm-date", "data-date": cand, checked: !!sug && sug.iso === cand,
        onchange: () => { submit.disabled = false; } });
      return el("label", { class: "rv-radio sg-radio" }, input, el("span", {}, ZL.fmtDate(cand) + " (" + cand + ")"),
        sug && sug.iso === cand ? el("span", { class: "sg-tag", "data-testid": "date-suggested-tag" }, "Suggested" + (sug.label ? " · " + sug.label : "")) : null);
    });
    const hint = d.suggestion && d.suggestion.reason ? d.suggestion.reason : "";
    const form = el("form", { class: "rv-datefix sg-dateform", "data-record-id": d.record_id, onsubmit: (ev) => ev.preventDefault() },
      el("fieldset", { class: "rv-fieldset", "aria-describedby": hint ? reasonId : null },
        el("legend", {}, opts.legend || "Written as “" + raw + "”. Which date?"), radios),
      hint ? el("p", { class: "sg-reason", id: reasonId, "data-testid": "date-suggestion-reason" },
        el("strong", {}, sug ? "Why this reading is suggested: " : "Hint: "), hint + ".",
        sug ? " It is only a suggestion. Nothing is confirmed until you click Confirm date." : " It does not point to one date, so none is selected.") : null,
      el("div", { class: "rv-actions" }, submit), err);
    form.addEventListener("submit", async () => {
      const v = form.querySelector("input:checked"); if (!v) return;
      submit.disabled = true; err.textContent = "";
      try { await opts.onConfirm(v.value); }
      catch (e) { err.textContent = (e && e.message) || "That date could not be confirmed."; submit.disabled = false; say(err.textContent, true); }
    });
    return form;
  };

  // ---- 2. dismissal-pattern suggestions -----------------------------------------------------------------------------------------
  const ds = { token: null, list: [], sig: "" };   // last list the server sent for the case on screen
  const errs = {};
  // "Keep showing" is client-side only, and remembered for this browser per case + key (localStorage, wrapped: the page works without it).
  const keptKey = (k) => "zlayt.keepShowing." + k;
  const kept = new Proxy({}, {
    get: (_, k) => { try { return localStorage.getItem(keptKey(String(k))) === "1"; } catch (_e) { return false; } },
    set: (_, k, v) => { try { if (v) localStorage.setItem(keptKey(String(k)), "1"); else localStorage.removeItem(keptKey(String(k))); } catch (_e) { /* not remembered */ } return true; },
  });
  const pendingFlag = (c, id) => (c.flags || []).some((f) => f.id === id && (f.review_status || "pending") === "pending");
  const focusFlagsHeading = () => { const h = document.getElementById("rv-flags-h"); if (h) { h.setAttribute("tabindex", "-1"); h.focus(); } };
  sg.dismissalBox = function (c) {
    const box = el("div", { class: "sg-ds", "data-testid": "dismissal-suggestions" });
    if (ds.token !== c.token) { ds.token = c.token; ds.list = []; ds.sig = ""; }
    function item(s) {
      const here = (s.flag_ids || []).filter((id) => pendingFlag(c, id)).length;
      const ek = c.token + "|" + s.key;
      const err = el("p", { class: "rv-error sg-error", role: "alert", "data-testid": "dismissal-error" }, errs[ek] || "");   // survives the repaint that follows a failed apply
      const hide = el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-hide-similar", "data-key": s.key }, "Hide similar (" + here + ")");
      const keep = el("button", { type: "button", class: "btn", "data-testid": "btn-keep-showing", "data-key": s.key }, "Keep showing");
      hide.addEventListener("click", async () => {
        hide.disabled = keep.disabled = true; err.textContent = ""; delete errs[ek];
        try {
          const r = await ZL.api.applyDismissal(c.token, s.key);
          ds.list = r.suggestions || []; ds.sig = JSON.stringify(ds.list);
          const n = (r.dismissed_flag_ids || []).length;
          ZL.state.set({ case: await ZL.api.getCase(c.token) });
          say("Hid " + n + (n === 1 ? " similar flag" : " similar flags") + ". " + (n === 1 ? "It stays" : "They stay") + " under Dismissed and you can reset " + (n === 1 ? "it" : "them") + ".");
          focusFlagsHeading();
        } catch (e) {
          errs[ek] = ((e && e.message) || "Those flags could not be hidden.") + " Some may already be hidden; check the list below.";
          err.textContent = errs[ek]; hide.disabled = keep.disabled = false; say(errs[ek], true);
          try { ZL.state.set({ case: await ZL.api.getCase(c.token) }); } catch (_) { /* keep the message */ }
        }
      });
      keep.addEventListener("click", () => { kept[c.token + "|" + s.key] = true; draw(); say("Keeping those flags visible."); focusFlagsHeading(); });
      return el("section", { class: "sg-ds-item", role: "group", "aria-label": "Suggestion: hide similar flags", "data-testid": "dismissal-suggestion", "data-key": s.key },
        el("p", { class: "sg-ds-msg", "data-testid": "dismissal-message" }, s.message),
        el("p", { class: "sg-muted" }, "Kind of flag: " + s.label + ". Counted across: " + s.scope + ". " + here + (here === 1 ? " flag" : " flags") + " in this case still " + (here === 1 ? "matches" : "match") +
          ". Nothing is hidden unless you click Hide similar. Hidden flags stay under Dismissed."),
        el("div", { class: "rv-actions" }, hide, keep), err);
    }
    function draw() {
      ZL.clear(box);
      const show = ds.list.filter((s) => !kept[c.token + "|" + s.key] && (s.flag_ids || []).some((id) => pendingFlag(ZL.state.get().case || c, id)));
      show.forEach((s) => box.append(item(s)));
      box.hidden = !show.length;
      requestAnimationFrame(() => document.dispatchEvent(new Event("zl:panels")));   // the top strip and the skip links point at it once it exists
    }
    draw();
    ZL.api.dismissalSuggestions(c.token).then((r) => {
      const list = (r && r.suggestions) || [], sig = JSON.stringify(list);
      if (ds.token !== c.token || sig === ds.sig) return;
      ds.list = list; ds.sig = sig;
      if (box.isConnected) draw();
    }).catch(() => { /* suggestions are optional; no banner without them */ });
    return box;
  };

  // ---- 3. measured precision ----------------------------------------------------------------------------------------------------
  let cal = null, calLoading = null, calSubs = [];
  function loadCalibration() {
    if (cal || calLoading) return;
    calLoading = ZL.api.calibration().then((r) => { cal = r && r.status ? r : { status: "invalid", calibration: null, message: "" }; })
      .catch(() => { cal = { status: "error", calibration: null, message: "" }; })
      .then(() => { calLoading = null; const fns = calSubs.splice(0); fns.forEach((f) => f()); });
  }
  // "In testing on 10 synthetic cases, 84 of 85 verified items matched the record." Numbers are the report's own matched / total / case_count, printed as given.
  const plainCount = (c, state, what) => { const x = c && c.by_state && c.by_state[state]; return x && x.total != null && x.matched != null && c.case_count != null ? "In testing on " + c.case_count + " synthetic cases, " + x.matched + " of " + x.total + " " + what + " matched the record." : null; };
  sg.calibration = function () {
    if (cal && cal.status === "error") cal = null;   // a failed load is retried on the next paint
    const box = el("section", { class: "sg-cal", "data-testid": "calibration-line", "aria-label": "Measured precision" });
    function draw() {
      ZL.clear(box);
      if (!cal) { box.append(el("p", { class: "sg-muted" }, "Measured precision: loading.")); return; }
      box.setAttribute("data-status", cal.status); box.removeAttribute("data-stale");
      const c = cal.status === "ok" ? cal.calibration : null;
      if (!c || !c.sentences || !c.sentences.overall) {
        const why = cal.status === "missing" ? "No measurement file has been produced yet."
          : cal.status === "error" ? "The measurement could not be loaded."
          : "The measurement file is not valid, so it is not used.";
        box.append(el("p", { class: "sg-cal-none", "data-testid": "calibration-unavailable" }, el("strong", {}, "Measured precision is not available. "), why + " No accuracy figure is shown.",
          cal.message ? " " + cal.message : ""));
        return;
      }
      const o = c.sentences.overall; if (c.stale) box.setAttribute("data-stale", "true");
      box.append(...[
        // T-102: the counts were measured with other prompts than the ones the app runs now. Said once, ABOVE the numbers so the warning is read first; the changed-prompt detail sits behind a disclosure.
        c.stale ? el("div", { class: "sg-cal-stale", role: "note", "data-testid": "calibration-stale" }, el("strong", {}, "These counts were measured before the latest change to the AI checks."), " Treat them as a rough guide.",
          c.stale_reason ? el("details", { class: "sg-cal-why" }, el("summary", {}, "Technical detail"), el("p", {}, c.stale_reason)) : null) : null,
        // T-166 F7: the counts in plain words, from the measured numbers themselves; the report's own sentence (it names the test backend and the golden set) is kept in a Technical detail toggle, verbatim.
        el("p", { class: "sg-cal-s", "data-testid": "calibration-verified" }, plainCount(c, "verified", "verified items") || "Measured on synthetic test cases."),
        c.small_sample ? el("p", { class: "sg-muted", "data-testid": "calibration-small-sample" },
          "Small sample: " + c.case_count + " synthetic test cases, so these counts are a rough indication, not a promise about your records.") : null,
        el("details", { class: "sg-cal-more" }, el("summary", {}, "The other side of the measurement"),
          el("p", { class: "sg-cal-s", "data-testid": "calibration-needs-review" }, plainCount(c, "needs_review", "items marked needs review") || "Measured on synthetic test cases."),
          el("details", { class: "sg-cal-tech", "data-testid": "calibration-tech" }, el("summary", {}, "Technical detail"), el("p", { class: "sg-muted" }, [o.verified, o.needs_review].filter(Boolean).join(" "))),
          c.not_scored && c.not_scored.total ? el("p", { class: "sg-muted" }, c.not_scored.total + (c.not_scored.total === 1 ? " item was" : " items were") + " not scored.") : null)].filter(Boolean));
    }
    draw();
    if (!cal) { calSubs.push(() => { if (box.isConnected) draw(); }); loadCalibration(); }
    return box;
  };

  // ---- 4. possible overlap warning -------------------------------------------------------------------------------------------------
  function goToAmount(id) {
    const row = document.querySelector('[data-testid="charges-panel"] [data-item-id="' + String(id).replace(/"/g, "") + '"]');
    if (!row) return;
    row.scrollIntoView({ block: "center" }); row.focus();
  }
  sg.overlapBox = function (c) {
    const list = (c.totals && c.totals.possible_overlaps) || [];
    if (!list.length) return null;
    const box = el("section", { class: "sg-overlap", role: "note", "aria-labelledby": "sg-overlap-h", "data-testid": "overlap-warning" },
      el("h3", { id: "sg-overlap-h" }, "Possible double-counting (" + list.length + ")"),
      el("p", { class: "sg-muted" }, "The total above only adds the charges you accepted. It does not remove or compare anything. Check these by hand."));
    list.forEach((o) => {
      const a = recSeq(c, o.statement_record_id), b = recSeq(c, o.covered_record_id);
      const openRec = (rid, seq) => el("button", { type: "button", class: "btn", "data-testid": "btn-overlap-record", onclick: () => ZL.openSource([{ record_id: rid, start: null, end: null }], "Record " + seq) }, "Open record " + seq);
      box.append(el("article", { class: "sg-overlap-item", "data-testid": "overlap-item", "data-statement-amount": o.statement_amount_id, "data-covered-amount": o.covered_amount_id },
        el("p", { class: "sg-overlap-msg", "data-testid": "overlap-message" }, o.message),
        el("ul", { class: "sg-overlap-figs" },
          el("li", {}, "Statement line: " + o.statement_text + " (Record " + a + ")"),
          el("li", {}, "Separate charge: " + o.covered_text + " (Record " + b + ")")),
        el("p", { class: "sg-muted", "data-testid": "overlap-in-total" }, o.both_in_total ? "Both figures are in the accepted total right now. If the statement line already includes the charge, dismiss one of the two."
          : "The accepted total does not contain both of them yet. If the statement line already includes the charge, do not accept both."),
        el("div", { class: "rv-actions" },
          el("button", { type: "button", class: "btn", "data-testid": "btn-overlap-goto", onclick: () => goToAmount(o.statement_amount_id) }, "Go to the statement line"),
          el("button", { type: "button", class: "btn", "data-testid": "btn-overlap-goto", onclick: () => goToAmount(o.covered_amount_id) }, "Go to the charge"),
          openRec(o.statement_record_id, a), a === b ? null : openRec(o.covered_record_id, b))));
    });
    return box;
  };
})();
