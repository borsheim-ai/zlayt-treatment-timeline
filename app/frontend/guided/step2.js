/* Step 2: Check the timeline (/case/<token>/timeline[?item=<id>]). OWNER: frontend-B. Spec 5 (5.1 queue, 5.2 line, 5.3 fix the wording, 5.4 compare confirm, 5.5 could not check, 5.6 date, 5.7 warning, 5.8 done);
   D-066 (a disputed or still-to-check item is accepted only with the box ticked, sent as compared:true), D-065 (tags), D-067 (no narrative), T-178 (version + expected_status on every write: review.js).
   The frame, the queue, Undo, the keyboard and every write are in review.js; this file says what each item looks like and which call each button makes. Record text is inserted with textContent only. */
(function () {
  const G = window.G, { h } = G, R = G.review;

  /* ---------- the queue (5.1): entries, undated entries, warnings and could-not-check items, in the order of the next_action timeline rule; frozen when the step opens ---------- */
  const recById = (c) => Object.fromEntries((c.records || []).map((r) => [r.id, r]));
  function citedIds(it) {
    const ids = new Set([].concat(it.record_ids || [], (it.computed && it.computed.record_ids) || [], (it.evidence || []).map((e) => e.record_id)).filter(Boolean));
    if (!ids.size && /^e\d+/.test(it.id || "")) ids.add("r" + /^e(\d+)/.exec(it.id)[1]);
    return [...ids];
  }
  function rankOf(c, it, group) {
    const recs = recById(c);
    const keys = citedIds(it).map((id) => recs[id]).filter(Boolean).map((r) => [r.date_iso || "9999-99-99", r.seq]).sort((a, b) => (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : a[1] - b[1]));
    const k = keys[0] || ["9999-99-99", 9999];
    return [k[0], k[1], group === "flag" ? 1 : 0, it.id];
  }
  function buildQueue(c) {
    const out = [];
    (c.entries || []).forEach((it) => out.push([it, "entry", false]));
    (c.undated_entries || []).forEach((it) => out.push([it, "entry", false]));
    (c.flags || []).forEach((it) => out.push([it, "flag", false]));
    (c.tray || []).filter((it) => it.kind === "entry" || it.kind === "flag").forEach((it) => out.push([it, it.kind === "flag" ? "flag" : "entry", true]));
    out.forEach((o) => { o.key = rankOf(c, o[0], o[1]); });
    out.sort((a, b) => { for (let i = 0; i < 4; i++) { if (a.key[i] < b.key[i]) return -1; if (a.key[i] > b.key[i]) return 1; } return 0; });
    return out.map(([it, , tray]) => ({ id: it.id, optional: tray }));
  }
  function find(c, id) { return [].concat(c.entries || [], c.undated_entries || [], c.flags || [], c.tray || []).find((i) => i.id === id) || null; }
  const groupOf = (c, it) => ((c.tray || []).includes(it) ? "tray" : (c.undated_entries || []).includes(it) ? "undated" : (c.flags || []).includes(it) ? "flag" : "entry");

  /* ---------- words ---------- */
  const FLAG_HEAD = [
    [(f) => f.type === "gap", (f) => (f.computed && f.computed.conditional ? "A possible break in treatment" : "A break in treatment")],
    [(f) => f.type === "conflict" && /^accident_date/.test(f.category || ""), () => "The records disagree about the accident date"],
    [(f) => f.type === "conflict" && f.category === "treatment_plan_vs_actual", () => "The plan and what happened differ"],
    [(f) => f.type === "conflict" && f.category === "provider_name_variant", () => "The provider's name is written differently"],
    [(f) => f.type === "conflict", () => "The records disagree"],
    [(f) => f.type === "pre_existing" && f.category === "degenerative_language", () => "Wording about wear and tear"],
    [(f) => f.type === "pre_existing", () => "An earlier health problem is mentioned"],
    [(f) => f.type === "causation" && f.category === "patient_report", () => "The patient, not a doctor, says what caused it"],
    [(f) => f.type === "causation" && f.category === "speculative_language", () => "Hedged wording (“may”, “possible”)"],
    [(f) => f.type === "causation" && f.category === "missed_care", () => "Missed or ended treatment"],
    [(f) => f.type === "causation" && f.category === "new_onset", () => "Wording about a new problem"],
    [(f) => f.type === "causation" && f.category === "accident_date_provenance", () => "Where the accident date comes from"],
    [(f) => f.type === "causation" && f.category === "credibility_language", () => "Wording about the patient's effort or credibility"],
    [(f) => f.type === "causation", () => "Wording the other side could use"],
    [(f) => f.type === "record_warning" && f.category === "injection_suspected", () => "This record contains text that looks like instructions to a computer"],
    [(f) => f.type === "record_warning" && f.category === "date_ambiguous", () => "This record's date is unclear"],
    [(f) => f.type === "record_warning" && f.category === "analysis_incomplete", () => "We couldn't finish comparing these records"],
    [(f) => f.type === "record_warning", () => "Something to check in this record"],
  ];
  const flagHeading = (f) => (FLAG_HEAD.find(([t]) => t(f)) || [null, () => "A warning for the attorney"])[1](f);
  const CODE_CHECK = new Set(["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_NUMBER_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CHARGE_TEXT_IN_ENTRY", "GROUNDING_EXCERPT_NOT_VERBATIM"]);
  const isCodeFail = (it) => (it.reasons || []).some((r) => CODE_CHECK.has(r) || /^EXCERPT_/.test(r));
  const quoteFail = (it) => (it.reasons || []).some((r) => /^EXCERPT_/.test(r) || r === "GROUNDING_EXCERPT_NOT_VERBATIM");
  const recLabel = (r) => `Record ${r.seq} · ${r.source_label || "Record"} · ${r.date_iso ? R.longDate(r.date_iso) : r.date_raw ? r.date_raw : "no date"}`;
  const lineHead = (it, rec) => [it.date ? R.longDate(it.date) : (rec && rec.date_raw) || "No date", it.provider || (rec && rec.source_label)].filter(Boolean).join(" · ");

  /* ---------- source card ---------- */
  function uncoveredNote(recs, marks) {
    const rows = [];
    recs.forEach((r) => (r.uncovered || []).forEach((u) => { if (!marks.some(([a, b]) => u.start >= a && u.end <= b)) rows.push(u.text); }));
    if (!rows.length) return [];
    return [h("div", { class: "also", "data-testid": "uncovered" }, h("b", {}, "Also in this record, outside the highlighted words:"), ...rows.map((t) => h("div", {}, h("q", {}, t))))];
  }
  /* the part of a record to show when several records share the card: the highlighted words with about 80 characters of the record on each side, cut at a space or line end */
  function windowOf(rec, marks) {
    const t = rec.text || "", a = Math.min(...marks.map((m) => m[0])) - rec.char_start, b = Math.max(...marks.map((m) => m[1])) - rec.char_start;
    let from = Math.max(t.lastIndexOf("\n", Math.max(0, a - 1)) + 1, a - 80), to = b + 80;
    if (from > 0 && t[from - 1] !== "\n") { const sp = t.indexOf(" ", from); if (sp >= 0 && sp < a) from = sp + 1; }
    const nl = t.indexOf("\n", b); if (nl >= 0 && nl < to) to = nl;
    if (to < t.length && t[to] !== "\n") { const sp = t.lastIndexOf(" ", to); if (sp > b) to = sp; }
    to = Math.min(t.length, to);
    return from <= 0 && to >= t.length ? null : [Math.max(0, from), to];
  }
  function sourceFor(S, recs, marks, opt) {
    opt = opt || {};
    S.whole = S.whole || new Set();
    return () => {
      const many = recs.length > 1, nodes = [];
      if (opt.hint) nodes.push(h("p", { class: "muted src-hint" }, opt.hint));
      recs.forEach((r) => {
        const mine = marks.filter(([a]) => a >= r.char_start && a < r.char_end), win = many && mine.length && !opt.sentencesOf && !S.whole.has(r.id) ? windowOf(r, mine) : null;
        nodes.push(...R.recBlock(r, { marks: mine, win, head: many ? recLabel(r) : null, sentences: opt.sentencesOf === r.id ? r.sentences : null, picked: opt.picked, onPick: opt.onPick }));
        if (many && mine.length && !opt.sentencesOf && (win || S.whole.has(r.id))) {          // several records: each shows its highlighted sentence, so every highlight is on screen without scrolling
          nodes.push(h("button", { type: "button", class: "btn quiet src-toggle", "data-testid": "btn-whole-record", "aria-expanded": win ? "false" : "true",
            onclick: () => { win ? S.whole.add(r.id) : S.whole.delete(r.id); S.renderSource(); } }, win ? `Show the whole of record ${r.seq}` : `Show only the highlighted part of record ${r.seq}`));
        }
      });
      if (!opt.sentencesOf && opt.uncovered !== false) nodes.push(...uncoveredNote(recs, marks));
      return nodes;
    };
  }
  function headFor(recs) { const n = recs.map((r) => r.seq); return recs.length === 1 ? recLabel(recs[0]) : "Records " + n.slice(0, -1).join(", ") + " and " + n[n.length - 1]; }

  /* ---------- sentence picking (fix the wording, write it yourself): whole sentences that follow each other ---------- */
  function pickedRange(rec, picked) {
    const sents = (rec.sentences || []).filter((s) => picked.has(s.start));
    if (!sents.length) return { error: "Pick at least one sentence." };
    const all = rec.sentences, idx = sents.map((s) => all.findIndex((x) => x.start === s.start)).sort((a, b) => a - b);
    if (idx.some((v, i) => i && v !== idx[i - 1] + 1)) return { error: "Pick sentences that follow each other." };
    const a = all[idx[0]], b = all[idx[idx.length - 1]];
    return { excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
  }
  function togglePick(S, sent) { const p = S.ui.picked || (S.ui.picked = new Set()); p.has(sent.start) ? p.delete(sent.start) : p.add(sent.start); S.renderSource(); }
  const warningsFoot = (S) => (S.ui.warnings || []).map((w) => h("p", { class: "foot-warn", "data-testid": "save-warning" }, R.plain(w.message || String(w))));

  /* ---------- the words of a line that are not in the highlighted words (code, no AI): a deterministic word diff so she sees what to check (paralegal review T-181 major) ---------- */
  const WORD = /[\p{L}\p{N}]+(?:['’][\p{L}]+)?/gu;
  const SKIP = new Set("a an the of to and or is are was were be been for with by at in on as it its that this".split(" "));
  const ABBR = { pt: "patient", dx: "diagnosis", rx: "prescription", hx: "history", tx: "treatment", sx: "symptom" };      // chart shorthand reads as the word it stands for (paralegal r2 nit: "Pt" in the quote, "Patient" in the line)
  const stem = (w) => { const x = w.toLowerCase().replace(/['’]s$/, "").replace(/s$/, ""); return w === "PT" ? x : ABBR[x] || x; };      // "PT" in capitals is physical therapy, not a patient: it stays a word of its own, so a "Patient" in the line is still underlined
  function outsideParts(summary, quote) {
    const inQuote = new Set((String(quote || "").match(WORD) || []).map(stem)), parts = [];
    let last = 0, any = false;
    for (const m of String(summary || "").matchAll(WORD)) {
      const w = m[0], out = !SKIP.has(w.toLowerCase()) && !inQuote.has(stem(w));
      if (m.index > last) parts.push(summary.slice(last, m.index));
      parts.push(out ? h("u", { class: "out", "data-testid": "outside-word" }, w) : w); if (out) any = true;
      last = m.index + w.length;
    }
    if (last < summary.length) parts.push(summary.slice(last));
    return any ? parts : null;
  }

  /* ---------- presenting an item ---------- */
  function present(S, item, q) {
    const c = S.c, g = groupOf(c, item);
    if (g === "tray") return item.kind === "flag" ? trayFlag(S, item) : trayEntry(S, item);
    if (g === "flag") return warning(S, item);
    if (g === "undated") return undated(S, item);
    return line(S, item);
  }

  /* 5.2 / 5.3 / 5.4 a line */
  function line(S, item) {
    const ui = S.ui, recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), main = S.recOf(item.excerpt_start) || recs[0];
    const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
    if (ui.mode === "fix") return fixLine(S, item, main, recs);
    const srcRecs = recs.length ? recs : main ? [main] : [];
    const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null), refusal = isCodeFail(item), edited = !!item.edit_to_check;
    const need = !refusal && (!!disp || edited), decided = (item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited") && !edited;
    const foot = [];
    let cls = "plain";
    if (refusal) { cls = "attn"; foot.push(h("strong", { "data-testid": "refusal" }, R.plain(item.why))); }
    else if (need) {
      cls = "attn";
      foot.push(h("strong", { "data-testid": "compare-reason" }, edited ? "You changed the wording. Read it against the highlighted words once more." : R.disputeText(disp, item)));
      if (!edited) foot.push(" Read it against the highlighted words before you say yes.");
      foot.push(R.check(S, "compare", "I read this line against the highlighted words myself.", { focus: true }));
    } else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "left out of the letter." : "kept in the letter.", " You can change it."); }
    else if (S.part2.has(item.id)) foot.push(h("span", { class: "label-cap" }, "Part 2 of 2"), h("br"), "The date is set. Now check the line itself.");
    else if (item.state === "needs_review") { cls = "attn"; foot.push(R.plain(item.why)); }
    else foot.push(h("span", { class: "label-cap" }, "How it was checked"), h("br"), R.plain(item.why));
    foot.push(...warningsFoot(S));
    return {
      tag: R.tagFor(item), sub: lineHead(item, main),
      body: [h("p", { class: "line-text", "data-testid": "line-text" }, ...(((need && outsideParts(item.summary, item.excerpt)) || [item.summary || ""]))),
        need && outsideParts(item.summary, item.excerpt) ? h("p", { class: "muted out-note", "data-testid": "outside-note" }, "Underlined words are not in the highlighted words.") : null],
      foot: { cls, nodes: foot },
      question: "Does this line say the same thing as the highlighted words?",
      yes: { label: "Yes, this matches", why: refusal ? R.plain(item.why) : "", disabled: () => refusal || (need && !R.ticked(S, "compare")), run: () => S.decide(item, "accept", need && R.ticked(S, "compare") ? { compared: true } : undefined) },
      no: { label: "No, leave it out", run: () => S.decide(item, "dismiss") },
      third: { label: quoteFail(item) ? "Change the words" : "Fix the wording", hint: refusal, run: () => { ui.mode = "fix"; ui.draft = null; ui.picked = null; S.err = null; S.say(null, null); S.render(); } },
      src: { head: headFor(srcRecs), nodes: sourceFor(S, srcRecs, marks) },
    };
  }

  function fixLine(S, item, rec, recs) {
    const ui = S.ui;
    if (!ui.picked) ui.picked = new Set((rec.sentences || []).filter((s) => item.excerpt_start != null && s.start < item.excerpt_end && s.end > item.excerpt_start).map((s) => s.start));
    if (ui.draft == null) ui.draft = item.summary || "";
    const ta = h("textarea", { class: "edit", "data-testid": "edit-summary", "aria-label": "Your wording for this line", "data-autofocus": "" });
    ta.value = ui.draft; ta.addEventListener("input", () => { ui.draft = ta.value; });
    const save = () => {
      const r = pickedRange(rec, ui.picked);
      if (r.error) { S.err = { text: r.error }; S.render(true); return; }
      const summary = (ui.draft || "").trim();
      if (!summary) { S.err = { text: "Write the line first." }; S.render(true); return; }
      const qChanged = r.excerpt !== item.excerpt, sChanged = summary !== (item.summary || "").trim();
      if (!qChanged && !sChanged) { S.err = { text: "Nothing has changed yet." }; S.render(true); return; }
      return S.act(async () => {
        S.lastEdit = { excerpt: r.excerpt, summary, before: item.summary };       // a refusal that names dropped words reads these (review.js droppedText)
        const edits = {};                                   // one call: the server checks the new wording against the new quote together (two calls would test the old wording against the new quote)
        if (qChanged) edits.excerpt = r.excerpt;
        if (sChanged) edits.summary = summary;
        const resp = await S.post(item, "edit", { edits });
        S.c = await S.ctx.refresh(); ui.mode = "view"; ui.picked = null; ui.draft = null; ui.warnings = resp.warnings || [];
        S.say("Saved: your wording is in. Read it once more against the highlighted words.", null);
        S.render(false);
      });
    };
    return {
      tag: { cls: "you", text: "Your wording" }, sub: lineHead(item, rec), focus: "field", how: false,
      body: [h("p", { class: "muted fix-hint" }, "Change the line so it says only what the highlighted words say. Numbers, left or right, and words like “no” or “possible” must match."), ta],
      foot: { cls: "plain", nodes: [R.plain(item.why)] },
      question: "Change the line, then save it.",
      yes: { label: "Save my wording", run: save }, no: { label: "Cancel", run: () => { ui.mode = "view"; ui.picked = null; ui.draft = null; S.err = null; S.render(); } },
      third: null,
      src: { head: recLabel(rec), nodes: sourceFor(S, [rec], [], { hint: "To change which words are highlighted, tap whole sentences below.", sentencesOf: rec.id, picked: ui.picked, onPick: (s) => togglePick(S, s), uncovered: false }) },
    };
  }

  /* 5.6 a date to pick */
  function undated(S, item) {
    const rec = S.record((item.record_ids || [])[0]), dtc = (S.c.dates_to_confirm || []).find((d) => d.record_id === (rec && rec.id));
    const cands = (dtc && dtc.candidates) || [];
    const raw = (dtc && dtc.raw) || (rec && rec.date_raw) || "";
    const at = rec && raw ? rec.text.indexOf("Date: " + raw) : -1, marks = at >= 0 ? [[rec.char_start + at, rec.char_start + at + 6 + raw.length]] : [];
    const src = { head: rec ? recLabel(rec) : "", nodes: sourceFor(S, rec ? [rec] : [], marks, { uncovered: false }) };
    if (!cands.length) {
      return {
        tag: { cls: "warn", text: "No date found" }, sub: item.provider || (rec && rec.source_label), src,
        body: [h("p", { class: "warn-title" }, "We couldn't find a date"), h("p", { class: "explain" }, "We couldn't find a date in this record, so it can't go on the timeline."),
          h("p", { class: "explain muted gap-top" }, "The line waiting for a date: “", item.summary || "", "”")],
        foot: { cls: "attn", nodes: ["Without a date the line cannot be placed between the other records. Leaving it out keeps it out of the timeline."] },
        question: "Read the record. Leave this line out?",
        yes: { label: "OK, leave it out", run: () => S.decide(item, "dismiss") }, no: { label: "Decide later", run: () => S.skip() }, third: null, later: false,
      };
    }
    const sug = dtc.suggestion && dtc.suggestion.iso, first = (/^(\d{1,2})[/.\-]/.exec(raw) || [])[1];
    const reading = (iso) => (first && +first === +iso.slice(5, 7) ? "month first" : first && +first === +iso.slice(8, 10) ? "day first" : "");
    const pick = (iso) => S.act(async () => {
      const resp = await G.api.confirmDate(S.token, rec.id, iso);
      S.c = await S.ctx.refresh(); S.part2.add(item.id); S.ui = {};
      const sentences = (resp.gap_changes || []).map((x) => x.sentence).filter(Boolean);
      S.say(sentences.length ? sentences.join(" ") : `Saved: record ${rec.seq} is dated ${R.longDate(iso)}.`, null);
      S.render(false);
    });
    const ans = (iso) => ({ label: R.longDate(iso), sub: [reading(iso), iso === sug ? "Suggested" : ""].filter(Boolean).join(" · "), plain: true, run: () => pick(iso) });
    const a = ans(cands[0]), b = ans(cands[1] || cands[0]);
    return {
      tag: { cls: "warn", text: "Pick the date" }, sub: item.provider || (rec && rec.source_label), src,
      body: [h("p", { class: "warn-title" }, "Which date is right?"), h("p", { class: "explain" }, "The record says ", h("b", {}, raw), ". That could be two different dates."),
        h("p", { class: "explain muted gap-top" }, "The line waiting for this date: “", item.summary || "", "”")],
      foot: { cls: "plain", nodes: sug ? [h("span", { class: "label-cap" }, "Suggested: " + R.longDate(sug)), h("br"), dtc.suggestion.reason] : ["Pick the reading that matches how the other dates in these records are written."] },
      question: "Which date is right for this record?", yes: a, no: cands.length > 1 ? b : null, third: null, later: { run: () => S.skip() },
    };
  }

  /* 5.7 a warning for the attorney */
  function warning(S, item) {
    const ui = S.ui;
    const evid = item.evidence || [], ids = [...new Set(evid.map((e) => e.record_id))];
    const recs = (ids.length ? ids : item.record_ids || []).map((id) => S.record(id)).filter(Boolean).sort((a, b) => a.seq - b.seq);
    const marks = evid.map((e) => [e.start, e.end]);
    const src = { head: recs.length ? headFor(recs) : "", nodes: sourceFor(S, recs, marks) };
    const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null), edited = !!item.edit_to_check;
    const noteMode = ui.mode === "note";
    const decided = (item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited") && !edited;
    const body = [h("p", { class: "warn-title", "data-testid": "warning-heading" }, flagHeading(item)),
      item.title && !(item.explanation || "").startsWith(item.title) ? h("p", { class: "explain", "data-testid": "warning-title" }, h("b", {}, item.title)) : null,
      h("p", { class: "explain", "data-testid": "warning-text" }, item.explanation || ""),
      item.gap_change && item.gap_change.sentence ? h("p", { class: "explain gap-top", "data-testid": "gap-change" }, item.gap_change.sentence) : null,
      item.reviewer_note && !noteMode ? h("p", { class: "explain muted gap-top" }, h("b", {}, "Your note: "), item.reviewer_note) : null];
    const tags = { tag: { cls: "warn", text: "Warning for the attorney" }, tag2: R.tagFor(item), src };
    if (noteMode) {
      const ta = h("textarea", { class: "edit", "data-testid": "edit-note", "aria-label": "Your note for the attorney", "data-autofocus": "" });
      ta.value = ui.draft != null ? ui.draft : item.reviewer_note || ""; ta.addEventListener("input", () => { ui.draft = ta.value; });
      return { ...tags, focus: "field", how: false, body: [h("p", { class: "warn-title" }, "Add a note for the attorney"), ta],
        foot: { cls: "plain", nodes: ["Your note goes in the notes for the attorney, next to this warning. It never goes in the letter."] },
        question: "Write your note, then save it.",
        yes: { label: "Save note", run: () => { const note = (ui.draft != null ? ui.draft : "").trim(); if (!note) { S.err = { text: "Write the note first." }; S.render(true); return undefined; } return S.decide(item, "edit", { edits: { note } }); } },
        no: { label: "Cancel", run: () => { ui.mode = "view"; ui.draft = null; S.err = null; S.render(); } }, third: null };
    }
    const foot = [];
    let cls = "plain";
    if (disp) {
      cls = "attn"; foot.push(h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), " Read it against the highlighted words before you say yes.", R.check(S, "compare", "I read this warning against the highlighted words myself.", { focus: true }));
    } else if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "not needed. It is listed as ruled out in the notes." : "the attorney will be told.", " You can change it."); }
    else foot.push("Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney can see it was checked.");
    return { ...tags, sub: "", body, foot: { cls, nodes: foot },
      question: "Should the attorney be told about this?",
      yes: { label: "Yes, tell the attorney", disabled: () => !!disp && !R.ticked(S, "compare"), run: () => S.decide(item, "accept", disp && R.ticked(S, "compare") ? { compared: true } : undefined) },
      no: { label: "No, not needed", run: () => S.decide(item, "dismiss") },
      third: { label: "Add a note", run: () => { ui.mode = "note"; ui.draft = null; S.err = null; S.say(null, null); S.render(); } } };
  }

  /* 5.5 could not check */
  function trayEntry(S, item) {
    const ui = S.ui, rec = S.record((item.record_ids || [])[0]) || S.record("r" + ((/^e(\d+)/.exec(item.id) || [])[1]));
    if (!rec) return { body: [h("p", {}, R.plain(item.why))], foot: { cls: "plain", nodes: [] }, question: "", yes: { label: "Skip it", run: () => S.decide(item, "dismiss") }, no: null, third: null };
    if (ui.mode === "write") {
      if (!ui.picked) ui.picked = new Set();
      if (ui.draft == null) ui.draft = "";
      const ta = h("textarea", { class: "edit", "data-testid": "edit-line", "aria-label": "Your line for the timeline", "data-autofocus": "" });
      ta.value = ui.draft; ta.addEventListener("input", () => { ui.draft = ta.value; });
      const save = () => {
        const r = pickedRange(rec, ui.picked), summary = (ui.draft || "").trim();
        if (r.error || !summary) { S.err = { text: r.error || "Write the line first." }; S.render(true); return undefined; }
        return S.act(async () => {
          const resp = await G.api.addEntry(S.token, rec.id, { summary, excerpt: r.excerpt });
          S.c = await S.ctx.refresh();
          const nid = (resp.item && resp.item.id) || (resp.entry && resp.entry.id);
          S.queue[S.idx] = { id: nid, optional: false }; S.ui = {}; S.screen = null;
          history.replaceState(history.state, "", G.url.timeline(S.token, nid));
          S.say("Saved: your line is in. Check it against the highlighted words once more.", null);
          S.render(false);
        });
      };
      return { tag: { cls: "you", text: "Written by you" }, sub: recLabel(rec), focus: "field", how: false,
        body: [h("label", { class: "sr", for: "mine" }, "Your line for the timeline"), ta],
        foot: { cls: "plain", nodes: ["Use only what the chosen sentences say. Numbers, left or right, and words like “no” or “possible” must match."] },
        question: "Write the line for the timeline, then save it.",
        yes: { label: "Save my line", run: save }, no: { label: "Cancel", run: () => { ui.mode = "view"; ui.picked = null; ui.draft = null; S.err = null; S.render(); } }, third: null,
        src: { head: recLabel(rec), nodes: sourceFor(S, [rec], [], { hint: "Tap the sentences your line is based on. They become the highlighted words.", sentencesOf: rec.id, picked: ui.picked, onPick: (s) => togglePick(S, s), uncovered: false }) } };
    }
    const tried = item.attempt && item.attempt.summary;
    return { tag: { cls: "warn", text: "We couldn't check this one" }, sub: recLabel(rec).replace(/^Record \d+ · /, ""),
      body: [h("p", { class: "explain", "data-testid": "tray-why" }, R.plain(item.why)), tried ? h("p", { class: "explain muted gap-top" }, "What was suggested (not used): “", tried, "”") : null],
      foot: { cls: "attn", nodes: ["Nothing from this suggestion goes in the letter unless you write the line yourself. Skipping it leaves this record out of the timeline."] },
      question: "Read the record. Do you want to write this line yourself?",
      yes: { label: "Write it myself", run: () => { ui.mode = "write"; ui.picked = null; ui.draft = null; S.err = null; S.render(); } },
      no: { label: "Skip it", run: () => S.decide(item, "dismiss") }, third: null,
      src: { head: recLabel(rec), nodes: sourceFor(S, [rec], [], { uncovered: false }) } };
  }
  function trayFlag(S, item) {
    const recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), a = item.attempt || {};
    return { tag: { cls: "warn", text: "We couldn't confirm this warning" }, sub: recs.length ? recLabel(recs[0]).replace(/^Record \d+ · /, "") : "",
      body: [h("p", { class: "explain", "data-testid": "tray-why" }, R.plain(item.why)), a.summary ? h("p", { class: "explain muted gap-top" }, h("b", {}, "The suggested warning: "), a.summary) : null,
        a.excerpt ? h("p", { class: "explain muted" }, "Its words in the record: “", a.excerpt, "”") : null],
      foot: { cls: "attn", nodes: ["This suggested warning is not in the notes for the attorney."] },
      question: "This warning can't go in the notes. Read it; if it matters, tell the attorney yourself.",
      yes: { label: "OK, leave it out", run: () => S.decide(item, "dismiss") }, no: { label: "Decide later", run: () => S.skip() }, third: null, later: false,
      src: { head: recs.length ? headFor(recs) : "", nodes: sourceFor(S, recs, [], { uncovered: false }) } };
  }

  /* T-211: the "You" row of "How this was checked": her decision in words (null = no decision yet) */
  function youText(S, item) {
    const st = item.review_status, flag = groupOf(S.c, item) === "flag" || item.kind === "flag" || !!item.type, tray = groupOf(S.c, item) === "tray";
    if (item.edit_to_check || !st || st === "pending") return null;
    if (st === "dismissed") return tray ? "You skipped it." : flag ? "You said the attorney does not need to be told." : "You left it out of the letter.";
    if (st === "edited") return flag ? "You added a note. The attorney will be told." : "You wrote your own wording and kept it in the letter.";
    return flag ? "You said the attorney should be told." : "You kept it in the letter.";
  }

  /* what the Saved line says */
  function statusFor(S, item, resp, action) {
    const q = S.queue.find((x) => x.id === (item && item.id)), flag = !!(item && (item.type || item.kind === "flag"));
    if (action === "dismiss") return q && q.optional ? "skipped. It stays out of the letter" : flag ? "marked not needed" : "left out of the letter";
    if (action === "edit") return "will go in the notes for the attorney, with your note";
    return flag ? "will go in the notes for the attorney" : "kept in the letter";
  }

  /* ---------- 5.8 done ---------- */
  function done(S) {
    const c = S.c, items = S.counted().map((q) => ({ q, it: S.item(q.id) })), left = items.filter(({ it }) => G.steps.undecided(it));
    const kept = items.filter(({ it }) => groupOf(c, it) !== "flag" && it.review_status !== "dismissed" && !G.steps.undecided(it)).length;
    const out = items.filter(({ it }) => groupOf(c, it) !== "flag" && it.review_status === "dismissed").length;
    const told = items.filter(({ it }) => groupOf(c, it) === "flag" && (it.review_status === "accepted" || it.review_status === "edited") && !it.edit_to_check).length;
    const notNeeded = items.filter(({ it }) => groupOf(c, it) === "flag" && it.review_status === "dismissed").length;
    const nextHref = (c.amounts || []).some(G.steps.live) ? G.url.bills(S.token) : G.url.letter(S.token);
    const nextLabel = (c.amounts || []).some(G.steps.live) ? "Go to step 3: Check the bills" : "Go to step 4: Get your letter";
    const first = left[0];
    const hero = left.length
      ? h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "!"), h("div", {}, h("h2", { "data-testid": "done-heading" }, `${left.length} item${left.length === 1 ? " still needs" : "s still need"} a decision.`),
        h("p", {}, "Items you don't decide stay out of the letter.")))
      : h("div", { class: "done-hero" }, h("div", { class: "big-check", "aria-hidden": "true" }, "✓"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "You checked every item on the timeline."),
        h("p", { "data-testid": "done-counts" }, `${kept} kept in the letter · ${out} left out · ${told} warning${told === 1 ? "" : "s"} for the attorney · ${notNeeded} not needed`)));
    const CHIP = { accepted: ["Kept", "ok"], edited: ["Kept", "ok"], dismissed: ["Left out", "never"] };
    const rows = items.map(({ q, it }, i) => {
      const fl = groupOf(c, it) === "flag", und = G.steps.undecided(it);
      const chip = und ? ["Not decided", "warn"] : fl ? (it.review_status === "dismissed" ? ["Not needed", "never"] : ["Tell the attorney", "warn"]) : CHIP[it.review_status] || ["Not decided", "warn"];
      const rec = S.record((citedIds(it)[0]));
      const label = fl ? flagHeading(it) : it.provider || (rec && rec.source_label) || "Line";
      return R.answerRow(i + 1, R.shortDate(it.date || (rec && rec.date_iso)), label, chip[0], chip[1], G.url.timeline(S.token, it.id));
    });
    const trayDone = S.queue.filter((q) => q.optional).map((q) => S.item(q.id)).filter(Boolean);
    const filtered = c.tray_filtered && c.tray_filtered.count > 0 ? c.tray_filtered : null, checks = c.checks;
    const labels = (checks && checks.labels) || {};
    return R.doneFrame(2, "Check the timeline",
      h("div", { class: "panel" }, hero, h("div", { class: "row-actions" },
        first ? h("a", { class: "btn primary lg", href: G.url.timeline(S.token, first.q.id), "data-testid": "btn-first-undecided" }, "Go to the first one") : null,
        h("a", { class: "btn lg " + (first ? "" : "primary"), href: nextHref, "data-testid": "btn-next-step" }, nextLabel))),
      h("div", { class: "panel" }, h("h2", {}, "Your answers"), h("p", { class: "muted" }, "Every item in the order you saw it. Change any answer here."), h("ol", { class: "answers", "data-testid": "answers-list" }, rows),
        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. " + (G.provenance().kind === "prepared" ? "" : "“AI draft” means an AI wrote it. ") + "“Written by you” means you did. A second AI check read each one against the record, unless the line says it was not double-checked.")),
      trayDone.length ? h("div", { class: "panel", "data-testid": "tray-done" }, h("h2", {}, "Items we couldn't check"), h("p", { class: "muted" }, "These are optional. They stay out of the letter unless you wrote the line yourself."),
        h("ul", { class: "plain-list" }, trayDone.map((t) => h("li", {}, h("a", { href: G.url.timeline(S.token, t.id) }, t.kind === "flag" ? "A suggested warning we couldn't confirm" : "A record with no line"), t.review_status === "dismissed" ? " (skipped)" : "")))) : null,
      filtered ? h("div", { class: "panel", "data-testid": "filtered-rules" }, h("h2", {}, "Suggestions a rule ruled out (nothing to do)"),
        ...(filtered.rules || []).map((r) => h("div", { class: "rule-out" }, h("p", {}, h("b", {}, r.label || r.rule), " ", r.explanation || ""), ...(r.items || []).map((i) => h("p", { class: "muted" }, "“", (i.attempt && i.attempt.excerpt) || "", "”"))))) : null,
      checks ? h("div", { class: "panel", "data-testid": "checks-panel" }, h("h2", {}, "What we compared between records"),
        h("p", {}, h("b", {}, "We checked for: "), (checks.conflict_types || []).map((t) => labels[t] || t).join("; ") || "nothing yet", "."),
        (checks.not_checked || []).length ? h("p", { class: "gap-top" }, h("b", {}, "Not checked: "), checks.not_checked.map((n) => n.label).join("; "), ".") : null) : null);
  }
  function empty(S) {
    return R.doneFrame(2, "Check the timeline", h("div", { class: "panel" }, h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "–"), h("div", {}, h("h2", { "data-testid": "done-heading" }, "There are no timeline lines in this case."), h("p", {}, "Nothing here needs checking."))),
      h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: (S.c.amounts || []).some(G.steps.live) ? G.url.bills(S.token) : G.url.letter(S.token), "data-testid": "btn-next-step" }, (S.c.amounts || []).some(G.steps.live) ? "Go to step 3: Check the bills" : "Go to step 4: Get your letter"))));
  }

  G.pages.timeline = function (ctx) {
    return R.run(ctx, { step: 2, title: "Check the timeline", unit: "Item", chip: false, buildQueue, find, present, statusFor, done, empty, youText });
  };
  G.step2 = { buildQueue, find, flagHeading, outsideParts };
})();
