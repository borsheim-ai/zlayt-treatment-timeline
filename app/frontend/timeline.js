/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
   T-043 plugs in through ZL.registerRowActions(fn(entry,rowEl)) and ZL.registerPanel(fn(case, mountEl)). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let sortMode = "review"; // "review" = needs_review first, then by date; "date" = chronological

  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const STATE_LABEL = { verified: "Quote matches", needs_review: "Needs review", rejected: "Could not verify" };
  const REASON = { JUDGE_PARTIAL: "part of the summary isn't fully supported by the quote", JUDGE_UNSUPPORTED: "the summary isn't supported by the quote", DATE_AMBIGUOUS: "the date can be read two ways",
    LLM_CALL_FAILED: "could not process", GROUNDING_EXCERPT_NOT_VERBATIM: "the model's quote is not word for word in the record", AMOUNT_RATE_NOT_TOTALED: "a rate, not totaled",
    JUDGE_DISAGREES: "the second check did not agree", LLM_ONLY: "only the AI suggested it; the checks found nothing to match", AI_TRANSLATION: "translated by AI; read the original quote yourself", FIXTURE_MISS: "the demo has no recorded answer for this step" };
  // T-060 r5 (ux F1): the row and the tray say the backend's own plain sentence (`why`, written once per code in why.py). The short map below is only the fallback for an item
  // that arrives without one; a code is never printed, not even lowercased.
  // T-204 r2: for a prepared answer the fallback never names a model or an AI as the author (D-065)
  const PREPARED_REASON = { GROUNDING_EXCERPT_NOT_VERBATIM: "the prepared quote is not word for word in the record", LLM_ONLY: "only the prepared answers suggested it; the checks found nothing to match", AI_TRANSLATION: "translated for the demo; read the original quote yourself" };
  const reasonText = (r, prep) => (prep && PREPARED_REASON[r]) || REASON[r] || "this needs your check";
  const casePrepared = () => { const c = ZL.state.get().case; return !!(c && c.models && c.models.generator_prepared); };
  const firstSentence = (t) => String(t || "").trim().split(/(?<=[.!?])\s+/)[0];
  const plainReason = (it) => firstSentence(it.why) || (it.reasons || []).map((r) => reasonText(r, it.prepared || casePrepared())).join("; ");   // a row has room for one sentence; the whole text is in the tooltip and in Why this status
  const fullReason = (it) => String(it.why || "").trim() || plainReason(it);

  // T-136 r2: the reason line of an edit she compared with the quote and accepted: her act first, then what the second check did (the server's own first sentence when it is not "did not run").
  // D-065: a hand-checked demo answer is a "Prepared answer", never an AI draft; recorded and live answers keep the AI label.
  const aiTag = (e) => e.origin_label && !e.prepared ? el("span", { class: "tag", "data-testid": "tag-origin", title: "Found by a program, not drafted by an AI." }, e.origin_label) : !e.ai_drafted ? null : e.prepared
    ? el("span", { class: "tag", "data-testid": "tag-prepared", title: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." }, "Prepared answer")
    : el("span", { class: "tag", "data-icon": "ai", "data-testid": "tag-ai-draft", title: "Drafted by AI" }, "draft");
  const comparedReason = (e) => "Compared by you with the quote. " + ((e.reasons || []).includes("JUDGE_UNAVAILABLE") ? "The second AI check did not run." : plainReason(e));
  const STATE_TONE = { verified: ["info", "match"], needs_review: ["warn", "alert"], rejected: ["bad", "x"] };
  const DECISION = { accepted: ["ok", "check"], edited: ["ok", "pencil"], dismissed: ["muted", "dash"] };
  // Machine state and the human decision are two separate chips; an undecided item shows only the machine chip (the Accept button already says what is left).
  function chips(e) {
    const cmp = ZL.comparedEdit(e);   // T-136 r2 (paralegal F-1): she compared the edit with the quote and accepted it; "Needs review" beside "Accepted" would contradict her decision
    const t = cmp ? ["info", "check"] : STATE_TONE[e.state] || ["muted", "info"], d = DECISION[e.review_status];
    return el("span", { class: "entry-chips" },
      el("span", { class: "chip chip--" + t[0], "data-icon": t[1], "data-testid": "entry-state" }, cmp ? "Compared by you" : STATE_LABEL[e.state] || e.state),
      d ? el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-testid": "review-status" }, REVIEW_LABEL[e.review_status] || e.review_status) : null);
  }
  // T-166 F3: a decided row shows one line of its quote and a button directly under it that shows the whole quote; a row that still needs a decision always shows the whole quote (styles.css).
  const fullQuotes = new Set();
  function quote(e, rec) {
    const who = e.provider + (e.date ? ", " + ZL.fmtDate(e.date) : "");
    const fig = el("figure", { class: "quote" },
      el("figcaption", { class: "quote-cap" }, "Excerpt" + (rec ? " \u00b7 Record " + rec.seq + " \u00b7 " + rec.source_label : "")),
      el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt));
    const label = (full) => (full ? "Show less of the excerpt: " : "Show full excerpt: ") + who;
    const more = el("button", { type: "button", class: "btn btn--link quote-more", "data-testid": "btn-show-excerpt", "aria-expanded": String(fullQuotes.has(e.id)), "aria-label": label(fullQuotes.has(e.id)),
      onclick: () => { const on = !fullQuotes.has(e.id); if (on) fullQuotes.add(e.id); else fullQuotes.delete(e.id); fig.toggleAttribute("data-full", on); more.setAttribute("aria-expanded", String(on)); more.setAttribute("aria-label", label(on)); more.textContent = on ? "Show less" : "Show full excerpt"; } },
      fullQuotes.has(e.id) ? "Show less" : "Show full excerpt");
    if (fullQuotes.has(e.id)) fig.setAttribute("data-full", "");
    fig.append(more);
    return fig;
  }
  // T-060 r3: a row is compact (summary and excerpt side by side, each clamped) until the paralegal opens it; the choice survives a repaint, and nothing about it depends on focus.
  const openRows = new Set();
  function entryRow(e, c) {
    const rec = c.records.find((r) => r.id === e.record_ids[0]);
    const row = el("article", { class: "entry st-" + e.state + (openRows.has(e.id) ? " is-open" : ""), "data-testid": "entry-" + e.seq, "data-entry-id": e.id, "data-state": e.state });
    const cmp = ZL.comparedEdit(e);
    const reasonText_ = cmp ? comparedReason(e) : e.state === "needs_review" && e.review_status !== "dismissed" && (e.reasons.length || e.why) ? plainReason(e) : "";
    const who = e.provider + (e.date ? ", " + ZL.fmtDate(e.date) : "");
    row.append(...[
      el("div", { class: "entry-head" },
        e.date ? ZL.timeEl(e.date, { class: "date", "data-testid": "entry-date" }) : el("span", { class: "chip chip--warn", "data-icon": "calendar", "data-testid": "entry-date" }, "Date to confirm"),
        el("span", { class: "provider", "data-testid": "entry-provider" }, (!e.date && rec ? `Record ${rec.seq}: ` : "") + e.provider),
        e.date && rec ? el("span", { class: "chip chip--rec" }, "Rec " + rec.seq) : null,
        reasonText_ ? el("p", { class: "reason" + (e.reasons.includes("AI_TRANSLATION") ? " reason--caution" : ""), "data-testid": "entry-reasons", title: fullReason(e) }, reasonText_) : null,
        chips(e)),
      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, aiTag(e)),
      e.edited ? el("p", { class: "muted small note", "data-testid": "edited-note" }, e.edited.original_summary != null
        ? "Edited by you; the code checked your wording against the quote when you saved. Original: " + e.edited.original_summary
        : "Quote changed by you; the code checked the new quote against the record when you saved. Original quote: " + (e.edited.original_excerpt || "(not kept)")) : null,
      quote(e, rec),
      e.duplicate_note ? el("p", { class: "muted small note" }, e.duplicate_note) : null,
      el("div", { class: "row-actions", "data-testid": "row-actions" },
        el("button", { type: "button", class: "btn btn--link", "data-testid": "entry-why", "aria-label": "Why this status: " + e.provider + (e.date ? ", " + ZL.fmtDate(e.date) : ""), onclick: () => openWhy(e.id) }, "Why this status"),
        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": `Open record ${rec ? rec.seq : ""} for ${e.provider}`, onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : "Open record"),
        )].filter(Boolean));
    ZL.hooks.rowActions.forEach((fn) => fn(e, row));
    // T-166 F11/F7: Open record stays in the row; Why this status, Change quote and Audit wait behind More (the row opens with it, as before).
    const ra = row.querySelector(":scope > .row-actions");
    if (ra) {
      const rest = Array.from(ra.children).filter((b) => b.getAttribute("data-testid") !== "btn-source");
      const m = ZL.rv.moreActions(rest, who, { testid: "entry-toggle", open: openRows.has(e.id), panelTestid: "entry-more-panel",
        onToggle: (on) => { if (on) openRows.add(e.id); else openRows.delete(e.id); row.classList.toggle("is-open", on); } });
      ra.append(m.btn, m.panel); row.append(ra);   // the links follow the decision buttons in the DOM, as they do on screen, so Tab order matches what is seen
    }
    return row;
  }
  // T-060 r4: a dismissed entry leaves the queue and waits in a collapsed "Dismissed (n)" group right under it, each with Undo. It opens by itself for the entry the paralegal just
  // dismissed (so she sees where it went and can undo it), and stays as she leaves it. Dismissed entries are never in the letter.
  ZL.dismissedOpen = false;
  function dismissedGroup(c, rows) {
    if (!rows.length) return null;
    const body = el("div", { class: "timeline", "data-testid": "dismissed-queue" }, rows.map((e) => entryRow(e, c)));
    const d = el("details", { class: "dismissed-group", "data-testid": "dismissed-group", open: ZL.dismissedOpen || null },
      el("summary", { "data-testid": "dismissed-summary" }, `Dismissed (${rows.length})`, el("span", { class: "muted small" }, " Not in the letter. Open to read them or press Undo."), ZL.rv.rerunMarker(body)),
      body);
    d.addEventListener("toggle", () => { ZL.dismissedOpen = d.open; });
    return d;
  }
  function sortedEntries(c) {
    const byDate = (a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq);
    const list = c.entries.slice().sort(byDate);
    if (sortMode === "date") return list;
    const rank = (e) => ZL.firstRank(e.id, e.state);
    return list.sort((a, b) => rank(a) - rank(b) || byDate(a, b));
  }
  // The record's own quoted text (verbatim, as in the record body), shown so the date can be judged next to what the record says.
  function recordExcerpt(rec) {
    const m = /(?:^|\n)Excerpt:\s*"?([\s\S]*?)"?\s*$/.exec(rec.text || "");
    return m ? m[1].trim() : "";
  }
  ZL.recordExcerpt = recordExcerpt;
  // ---- confirm a date reading (used by Dates to confirm, the flag card's date form and the pre-selected form). T-114: the backend answers with gap_changes[]; every
  // one is shown in plain words above the timeline (it stays until dismissed) and announced, so a figure never changes silently. Focus then moves to the
  // entry's Accept button (a date that was just confirmed is the next thing to decide), or to the "no entry yet" card.
  let gapNote = null;   // {token, items: [sentence]}: the announcement above the timeline, dismissable
  // The same change is also kept per case (T-114 r3, paralegal): the gap card says "now 40 days (was 42)" after Got it, after a reload and on another day, until that gap changes again.
  // The backend has no stored field for it yet (filed as a card), so it is kept in this browser per case, next to "Keep showing". If a gap flag ever carries `gap_change`, that wins.
  const gapKey = (token) => "zlayt.gapchg." + token;
  const gapMem = {};
  function gapStore(token) {
    if (gapMem[token]) return gapMem[token];
    let v = []; try { v = JSON.parse(localStorage.getItem(gapKey(token)) || "[]"); } catch (_) { v = []; }
    return (gapMem[token] = Array.isArray(v) ? v : []);
  }
  function gapSave(token, changes) {
    const keep = gapStore(token).filter((x) => !changes.some((n) => n.flag_id === x.flag_id));
    gapMem[token] = keep.concat(changes.filter((n) => n && n.flag_id));
    try { localStorage.setItem(gapKey(token), JSON.stringify(gapMem[token])); } catch (_) { /* not remembered across reloads */ }
  }
  const dayWord = (n) => n + (n === 1 ? " day" : " days");
  const span = (a, b) => (a && b ? ZL.fmtDate(a) + " to " + ZL.fmtDate(b) : "");
  // What the gap card shows: the sentence the server wrote, then the old and new figures with their dates. Only while the card still shows the new figure.
  function gapChangeFor(c, f) {
    if (!f || f.type !== "gap") return null;
    const cur = f.computed || {};
    const g = f.gap_change || gapStore(c.token).find((x) => x.flag_id === f.id && x.new_days === cur.days && (x.new_from == null || x.new_from === cur.from));
    if (!g || g.new_days == null) return null;
    const lines = [];
    if (g.old_days != null) lines.push("Before: " + dayWord(g.old_days) + (span(g.old_from, g.old_to) ? " (" + span(g.old_from, g.old_to) + ")" : "") + ".");
    lines.push("Now: " + dayWord(g.new_days) + (span(g.new_from, g.new_to) ? " (" + span(g.new_from, g.new_to) + ")" : "") + ".");
    return { sentence: g.sentence || "", lines };
  }
  // A gap that no longer applies has no card; the panel keeps the sentence under Treatment gaps.
  function gapRemoved(c) {
    const have = new Set((c.flags || []).map((f) => f.id));
    return gapStore(c.token).filter((x) => x.change === "removed" && x.sentence && !have.has(x.flag_id)).map((x) => x.sentence);
  }
  ZL.gapChanges = { forFlag: gapChangeFor, removed: gapRemoved };
  ZL.confirmDate = async function (recordId, cand) {
    const s = ZL.state.get(), resp = await ZL.api.confirmDate(s.token, recordId, cand);
    const all = resp && Array.isArray(resp.gap_changes) ? resp.gap_changes.filter(Boolean) : [], changes = all.map((g) => g.sentence).filter(Boolean);
    gapNote = changes.length ? { token: s.token, items: changes } : null;
    if (all.length) gapSave(s.token, all);
    ZL.state.set({ case: await ZL.api.getCase(s.token) });
    const c = ZL.state.get().case, rec = c.records.find((r) => r.id === recordId), say = ZL.rv && ZL.rv.say ? ZL.rv.say : () => {};
    const en = c.entries.concat(c.undated_entries).find((x) => (x.record_ids || [])[0] === recordId);
    const left = ZL.$('[data-testid="missing-entry"][data-record-id="' + recordId + '"]');
    let msg = "Date confirmed: " + ZL.fmtDate(cand) + ".";
    if (left) msg += " Record " + (rec ? rec.seq : "") + " has no entry yet; it is listed under Records without an entry.";
    if (changes.length) msg += " " + changes.join(" ");
    say(msg);
    requestAnimationFrame(() => {
      const b = en && document.querySelector('[data-testid="queue"] [data-controls-for="' + en.id + '"] [data-action="accept"]');
      if (b) { b.focus({ preventScroll: true }); b.scrollIntoView({ block: "center" }); }
      else if (left) left.scrollIntoView({ block: "center" });
    });
    return resp;
  };
  function gapNoteNode(c) {
    if (!gapNote || gapNote.token !== c.token) return null;
    return el("section", { class: "notice notice--info", "data-testid": "gap-change-note", role: "status", "aria-label": "Gap figures changed" },
      el("div", { class: "notice-body" }, el("strong", {}, "A gap figure changed. "), gapNote.items.map((t) => el("span", { class: "gap-sentence" }, t + " "))),
      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-dismiss-gap-note", onclick: (ev) => { gapNote = null; ev.target.closest("section").remove(); } }, "Got it"));
  }
  function datesToConfirm(c) {
    const none = !c.undated_entries.length && !c.dates_to_confirm.some((d) => d.candidates.length);
    const box = el("section", { class: "group" + (none ? " group--empty" : ""), "data-testid": "dates-to-confirm", "aria-labelledby": "h-dates" }, el("h2", { id: "h-dates" }, "Dates to confirm"));
    if (none) { box.append(el("p", { class: "muted" }, "None. Every record has a readable date.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records are left off the timeline and the gap check until you pick the right date. The tool never guesses."));
    const confirmDate = (d, cand) => ZL.confirmDate(d.record_id, cand);
    const confirmBar = (d) => {
      const raw = d.raw || d.date_raw || "";
      // T-088/T-096: a suggested reading is pre-selected with its reason, and still needs the paralegal's Confirm click.
      if (ZL.sg && ZL.sg.usableSuggestion(d)) return ZL.sg.dateForm(d, { legend: `Written as “${raw}”. Which date?`, onConfirm: (cand) => confirmDate(d, cand) });
      const bar = el("div", { class: "row", role: "group", "aria-label": "Choose the date" }, el("span", {}, `Written as “${raw}”. Which date?`));
      d.candidates.forEach((cand) => bar.append(el("button", { type: "button", class: "btn", "data-testid": "confirm-date", "data-date": cand, onclick: async () => {
        try { await confirmDate(d, cand); } catch (er) { alert(er.message); }
      } }, ZL.fmtDate(cand))));
      if (d.suggestion && d.suggestion.reason) bar.append(el("p", { class: "muted small", "data-testid": "date-suggestion-reason" }, "Hint: " + d.suggestion.reason + ". It does not point to one date, so none is selected."));
      return bar;
    };
    const shown = {};
    c.undated_entries.forEach((e) => {
      const d = c.dates_to_confirm.find((x) => x.record_id === e.record_ids[0]);
      const rec = c.records.find((r) => r.id === e.record_ids[0]);
      const row = entryRow(e, c); row.classList.add("undated");
      if (d) shown[d.record_id] = true;
      if (d && d.candidates.length) row.insertBefore(confirmBar(d), row.querySelector(".row-actions"));
      else if (rec) row.insertBefore(el("p", { class: "reason" }, "No readable date in this record header; it stays off the timeline."), row.querySelector(".row-actions"));
      box.append(row);
    });
    // A record with an ambiguous date but no entry at all (no model entry for it): still list it here so the date can be confirmed.
    // Once confirmed it is not removed: it moves to "Records without an entry" (manual.js) with a note and the by-hand path.
    // A record with no readable date and no entry has no date to confirm; it is listed once, under "Records without an entry".
    c.dates_to_confirm.filter((d) => !shown[d.record_id] && d.candidates.length).forEach((d) => {
      const rec = c.records.find((r) => r.id === d.record_id);
      const quote = rec ? recordExcerpt(rec) : "";
      const row = el("article", { class: "entry undated", "data-testid": "date-to-confirm-item", "data-record-id": d.record_id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, rec ? `Record ${rec.seq}: ${rec.source_label}` : `Record ${d.record_id}`), el("span", { class: "chip chip--warn", "data-icon": "calendar" }, "Date to confirm")),
        quote ? el("blockquote", { class: "excerpt", "data-testid": "date-to-confirm-excerpt" }, quote) : null);
      row.append(confirmBar(d));
      row.append(el("p", { class: "muted small", "data-testid": "date-to-confirm-note" }, "No entry was drafted for this record. After you pick the date it is listed under Records without an entry, where you enter it by hand."));
      if (rec) row.append(el("div", { class: "row-actions" }, el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", onclick: () => ZL.openSource([{ record_id: rec.id, start: null, end: null }], `Record ${rec.seq}: ${rec.source_label}`) }, `Open record ${rec.seq}`)));
      box.append(row);
    });
    return box;
  }
  // D-053: a `flag` tray item is an AI-suggested flag the checks did not confirm. It is never in the flags list or the letter.
  // One plain sentence for both reasons (T-096 review F5): no internal terms. What the paralegal can do goes in a second line, once.
  const FLAG_NOT_CONFIRMED = "The AI suggested this flag. The checks did not support it, so it is left out of the letter.";
  const FLAG_NOT_FOUND = FLAG_NOT_CONFIRMED;
  const PREPARED_FLAG_NOT_CONFIRMED = "The prepared answers suggested this flag. The checks did not support it, so it is left out of the letter.";
  function tray(c) {
    const box = el("section", { class: "group tray" + (c.tray.length ? "" : " group--empty"), "data-testid": "rejected-tray", "aria-labelledby": "h-tray" }, el("h2", { id: "h-tray" }, `Could not verify (${c.tray.length})`));
    if (!c.tray.length) { box.append(el("p", { class: "muted" }, "Nothing here.")); return box; }
    box.append(el("p", { class: "muted small" }, "These items did not produce something you can use. They are not in the timeline and will not be in the letter. Open the record to read it yourself."));
    c.tray.forEach((t) => {
      const recs = t.record_ids.map((id) => c.records.find((r) => r.id === id)).filter(Boolean);
      const isFlag = t.kind === "flag", prep = !!t.prepared || casePrepared();
      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id, "data-tray-kind": t.kind || "entry" },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip chip--bad", "data-icon": "x" }, isFlag ? "Flag not confirmed" : "Could not verify")),
        isFlag ? el("p", { class: "summary", "data-testid": "tray-flag-lead" }, prep ? PREPARED_FLAG_NOT_CONFIRMED : (t.reasons || [])[0] === "LLM_ONLY" ? FLAG_NOT_FOUND : FLAG_NOT_CONFIRMED) : null,
        isFlag ? null : el("p", { class: "summary", "data-testid": "tray-reason" }, plainReason(t)),   // T-060 r5 (ux F5a): the reason once, as the backend's sentence; the short code wording above it said the same thing
        isFlag ? el("p", { class: "muted small" }, "Nothing to accept here. Read what " + (prep ? "was suggested" : "the AI suggested") + " below; if it applies, open the record and check.") : null,
        isFlag ? el("details", { class: "zs-more" }, el("summary", {}, "Why the checks left it out"), el("p", { class: "muted small", "data-testid": "tray-why" }, t.why)) : null,
        t.attempt && (t.attempt.summary || t.attempt.excerpt) ? el("p", { class: "muted small", "data-testid": "tray-attempt" }, (isFlag ? (prep ? "The flag that was suggested (not used): " : "The flag the AI suggested (not used): ") : (prep ? "The prepared attempt (not used): " : "The model's attempt (not used): ")) + (t.attempt.summary || "") + " — “" + (t.attempt.excerpt || "") + "”") : null,
        el("div", { class: "row-actions" }, ZL.stepper ? ZL.stepper.traceButton(t.id, "btn btn--link") : null, recs.map((r) => el("button", { type: "button", class: "btn btn--link", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], `Record ${r.seq}: ${r.source_label}`) }, `Open record ${r.seq}`))));
      box.append(item);
    });
    return box;
  }

  // D-057 (T-126): proposals that a fixed rule filtered out. Not flags, nothing to decide, never counted. Listed collapsed so nothing the AI proposed is hidden: the rule is named once with its
  // own explanation, then the quoted line of each item. No Accept, no data-item-id (the keyboard flow never reaches them).
  function trayFiltered(c) {
    const tf = c.tray_filtered; if (!tf || !(tf.count > 0) || !(tf.rules || []).length) return null;
    const recLabel = (ids) => (ids || []).map((id) => c.records.find((r) => r.id === id)).filter(Boolean).map((r) => "Record " + r.seq).join(", ");
    return el("details", { class: "group tray-filtered", "data-testid": "tray-filtered" },
      el("summary", { "data-testid": "tray-filtered-summary" }, `Filtered by rule (${tf.count})`, el("span", { class: "muted small" }, " Nothing to decide. These are not flags and are not in the letter.")),
      tf.rules.map((r) => el("section", { class: "tf-rule", "data-testid": "tray-filtered-rule", "data-rule": r.rule },
        el("h3", {}, `${r.label || r.rule} (${r.count != null ? r.count : (r.items || []).length})`),
        r.explanation ? el("p", { class: "muted small" }, r.explanation) : null,
        el("ul", { class: "tf-items" }, (r.items || []).map((it) => el("li", { "data-testid": "tray-filtered-item" },
          el("span", { class: "tf-rec" }, recLabel(it.record_ids)), it.attempt && it.attempt.excerpt ? el("span", {}, " “" + it.attempt.excerpt + "”") : null))))));
  }

  // ---- Why? panel
  const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
  async function openWhy(id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    const ent = [...s.case.entries, ...s.case.undated_entries].find((x) => x.id === id);
    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
    body.append(el("p", { class: "muted" }, "Loading…")); if (!dlg.open) dlg.showModal();
    try {
      const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
      clear(body);
      body.append(...[
        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
        ZL.stepper ? ZL.stepper.itemSection(s.token, id) : null,
        el("details", { class: "zs-more" }, el("summary", {}, "Recorded ladder (raw state and checks)"), el("dl", { class: "kv", "data-testid": "why-ladder" },
          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
          lad.generator ? [el("dt", {}, lad.generator.prepared ? "Prepared by" : "Drafted by"), el("dd", { "data-testid": "why-generator" }, lad.generator.prepared ? String(lad.generator.model) : `${lad.generator.model} · ${lad.generator.prompt_version}`),   // D-065: no prompt made a prepared answer
            el("dt", {}, lad.generator.prepared ? "Prepared answer" : "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)"))),
        r.calls && r.calls.length ? el("details", {}, el("summary", {}, `${r.calls.some((cl) => cl.prepared) || (lad.generator && lad.generator.prepared) ? "Calls" : "Model calls"} (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · " + cl.verdict : ""}`)))) : null].filter(Boolean));
    } catch (e) { clear(body); body.append(el("p", { class: "error", role: "alert" }, e.message)); }
  }
  ZL.openWhy = openWhy;

  // ---- "What you need to do": one strip above the work, in plain words, each open decision a jump control. Built from the case data, so it is there before the
  // case-checks trace has loaded. Rebuilt when a late panel (the dismissal suggestion) appears.
  let todoHost = null;
  function todoItems(c) {
    const open = (i) => ZL.undecided(i);
    const dated = c.undated_entries.filter(open).length + c.dates_to_confirm.filter((d) => d.candidates.length && !c.undated_entries.some((e) => (e.record_ids || [])[0] === d.record_id)).length;
    const dateless = new Set(c.undated_entries.map((e) => e.id));
    const eEntries = c.entries.filter((e) => open(e) && !dateless.has(e.id)), eEdits = Math.min(ZL.editCount(c), eEntries.length);   // the review's own count (T-134), never more than the open entries listed
    const flags = (c.flags || []).filter(open).length;
    const charges = (c.amounts || []).filter((a) => open(a) && a.kind === "charge").length;
    const unclear = (c.amounts || []).filter((a) => open(a) && a.kind !== "charge").length;
    const suggest = document.querySelectorAll('[data-testid="dismissal-suggestion"]').length;
    const n = (k, one, many) => k + " " + (k === 1 ? one : many);
    // each button counts what is left to decide in that list; the ONE "need review" number is the lead line above them (and the header and the Timeline chip say the same number)
    const out = [];
    if (dated) out.push(["dates", n(dated, "date to confirm", "dates to confirm"), "Choose the date for the record that has none"]);
    if (eEntries.length - eEdits) out.push(["review", n(eEntries.length - eEdits, "entry to decide", "entries to decide"), ""]);
    if (eEdits) out.push(["review", n(eEdits, "edit to check", "edits to check"), ""]);
    if (flags) out.push(["flags", n(flags, "flag to review", "flags to review"), ""]);
    if (suggest) out.push(["suggest", n(suggest, "dismissal suggestion", "dismissal suggestions") + " waiting in Flags", ""]);
    if (charges) out.push(["charges", n(charges, "charge to check", "charges to check"), ""]);
    if (unclear) out.push(["charges", n(unclear, "unclear amount", "unclear amounts") + " (not totaled)", ""]);
    return out;
  }
  let todoMoreOpen = false;
  function paintTodo() {
    const host = todoHost; if (!host || !host.isConnected) return;
    const c = ZL.state.get().case; if (!c || c.status !== "ready") return;
    ZL.clear(host);
    const items = todoItems(c), done = !items.length;
    host.className = "todo-strip" + (done ? " todo-strip--done" : "");
    const nr = ZL.progressOf(c).needs;
    host.append(el("h2", { id: "h-todo", class: done ? "" : "sr" }, done ? "Everything is decided" : "Open decisions"));
    if (done) host.append(el("p", { class: "todo-lead" }, "Nothing is waiting on you. Open Export to copy the treatment section; decisions you made are in the letter and the internal notes."),
      el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-todo-export", onclick: () => ZL.skipTo && ZL.skipTo("export") }, "Go to Export"));
    else {
      host.append(el("button", { type: "button", class: "btn btn--primary btn--sm", "data-testid": "btn-start-review", onclick: () => ZL.skipTo && ZL.skipTo("review") }, "Start review"));
      const ul = el("ul", { class: "todo-list", "data-testid": "todo-list" }, items.map(([id, text]) => el("li", {},
        el("button", { type: "button", class: "btn btn--sm", "data-testid": "todo-" + id, onclick: () => ZL.skipTo && ZL.skipTo(id) }, text))));
      if (window.matchMedia && window.matchMedia("(max-width: 768px)").matches) {   // a phone: the jump buttons wait behind one line, so the first entry stays near the top (T-149 r2)
        const det = el("details", { class: "todo-more", "data-testid": "todo-more" }, el("summary", { class: "btn btn--sm" }, "Jump to a list (" + items.length + ")"), ul);
        det.open = todoMoreOpen; det.addEventListener("toggle", () => { todoMoreOpen = det.open; });
        host.append(det);
      } else host.append(ul);
    }
  }
  document.addEventListener("zl:panels", () => requestAnimationFrame(paintTodo));

  ZL.renderReview = function (s) {
    const c = s.case, mount = ZL.$("#review-body");
    // a re-render rebuilds every row; keep keyboard focus on the same item and control (a stray repaint must never drop focus to the page)
    const ae = document.activeElement, rowEl = ae && ae.closest ? ae.closest("[data-item-id]") : null;
    const keep = ae && ae !== mount && mount.contains(ae) ? { row: rowEl ? rowEl.getAttribute("data-item-id") : null, self: ae === rowEl, tid: ae.getAttribute("data-testid"), action: ae.getAttribute("data-action") } : null;
    clear(mount);
    if (!c || c.status !== "ready") return;
    const shown = c.entries.concat(c.undated_entries), nNeeds = ZL.progressOf(c).needs, nVer = shown.filter((e) => e.state === "verified").length; // T-060 r5: the SAME need-review number as the header and the strip (everything still open that is marked Needs review); falls when one is decided or dismissed
    const wrap = el("div", { "data-testid": "timeline" }); mount.append(wrap);
    const head = ZL.caseHead ? ZL.caseHead(c) : null; if (head) wrap.append(head);   // T-149: ONE overview block first (progress, what to do, the open decisions, the case checks), then the breakdown
    const slot = head ? head.querySelector(".co-slot") : wrap;
    todoHost = el("section", { "data-testid": "todo-strip", "aria-labelledby": "h-todo" }); slot.append(todoHost); paintTodo();
    const gapN = gapNoteNode(c); if (gapN) wrap.append(gapN);
    // one card for the three "how was this checked" rows (case checks, what to do next, how the AI was checked) and the accuracy note: ~150 px instead of ~400, so the work starts on the first screen
    const checks = el("div", { class: "checks", "data-testid": "checks-card" }); slot.append(checks);
    if (ZL.stepper) ZL.stepper.mountCase(checks);
    const hasDates = c.undated_entries.length || c.dates_to_confirm.some((d) => d.candidates.length);
    const dates = datesToConfirm(c);
    const sorted = sortedEntries(c), liveRows = sorted.filter((e) => e.review_status !== "dismissed"), dismissedRows = sorted.filter((e) => e.review_status === "dismissed");
    wrap.append(...[
      el("div", { class: "toolbar" },
        el("h2", { id: "h-timeline" }, "Timeline"),
        el("span", { class: "toolbar-counts", "data-testid": "review-counts" },
          el("span", { class: "chip chip--muted" }, `${shown.length} ${shown.length === 1 ? "entry" : "entries"}`),
          el("span", { class: "chip chip--warn", "data-icon": "alert" }, `${nNeeds} ${nNeeds === 1 ? "item needs" : "items need"} review`),
          el("span", { class: "chip chip--info", "data-icon": "match" }, `${nVer} quote ${nVer === 1 ? "matches" : "match"}`),
          c.undated_entries.length ? el("span", { class: "muted small" }, `${c.undated_entries.length} in Dates to confirm`) : null),
        el("label", { class: "toolbar-sort" }, "Order ",
          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
      ZL.stepper ? ZL.stepper.exportNotice() : null,
      hasDates ? dates : null,
      el("div", { class: "timeline", "data-testid": "queue", role: "group", "aria-labelledby": "h-timeline" }, liveRows.map((e) => entryRow(e, c))),
      dismissedGroup(c, dismissedRows),
      hasDates ? null : dates, tray(c), trayFiltered(c), ZL.sg ? ZL.sg.calibration() : null].filter(Boolean));   // never hand append() a bare null: it prints the word null
    const side = el("div", { id: "side-panels", "data-testid": "side-panels" }); wrap.append(side);
    ZL.hooks.panels.forEach((fn, i) => { try { fn(c, side); } catch (err) { ZL.panelFailed(side, "side panel " + (i + 1), err); } });   // one panel throwing must not hide the rest, nor be swallowed
    if (keep) {   // put focus back where it was
      const row = keep.row && (mount.querySelector('[data-testid="queue"] [data-item-id="' + keep.row + '"]') || mount.querySelector('[data-item-id="' + keep.row + '"]'));
      const t = row ? (keep.self ? row : (keep.action && row.querySelector('[data-action="' + keep.action + '"]')) || (keep.tid && row.querySelector('[data-testid="' + keep.tid + '"]')) || row)
        : (!keep.row && keep.tid ? mount.querySelector('[data-testid="' + keep.tid + '"]') : null);
      if (t) { if (!t.hasAttribute("tabindex") && !/^(BUTTON|A|INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) t.setAttribute("tabindex", "0"); t.focus({ preventScroll: true }); }
    }
    document.dispatchEvent(new Event("zl:panels"));
  };
})();
