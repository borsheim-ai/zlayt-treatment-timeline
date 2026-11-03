/* In-memory mock of the api.md contract (shapes copied from memory/contracts/api.md). Dev/test only: used while API_MODE === "mock".
   Parses `=== Record N ===` / Date: / Source: / Excerpt: blocks from the pasted text like the real ingest does (offsets are absolute).
   Mock switches (URL query): ?fail=4 makes the stub backend fail every call for record 4 (tray shows "could not process"). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const SAMPLE_SUMMARIES = {
    1: "Restrained driver rear-ended at approx. 35 mph; reported neck pain 7/10 and headache; transported to Central ER.",
    2: "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.",
    3: "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.",
    4: "Cervical range of motion reduced approx. 40%; plan of care is 12 visits.",
    5: "Pain 4/10, improving; patient reports missing 3 days of work.",
    6: "Discharged from PT after two missed appointments; pain 3/10.",
    7: "New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered.",
    8: "C5-C6 disc protrusion with mild right foraminal narrowing; findings may represent degenerative change; correlate clinically.",
    9: "Cervical epidural steroid injection recommended; the record says symptoms began after the January collision.",
  };
  const MAX_CHARS = 60000;
  let store = {};

  // ---- same sentence rule as the contract: split after . or ; unless an abbreviation / digit follows (approx. 35, 10 mg. Follow)
  function sentences(text, base) {
    const out = []; let start = 0;
    for (let i = 0; i < text.length; i++) {
      const ch = text[i];
      if ((ch === "." || ch === ";") && /\s/.test(text[i + 1] || " ")) {
        const prev = text.slice(Math.max(0, i - 6), i).split(/\s/).pop().toLowerCase();
        const next = text.slice(i + 1).trim()[0] || "";
        if (ch === "." && (["approx", "dr", "mg", "e.g"].includes(prev) || /\d|[a-z]/.test(next))) continue;
        if (ch === "." && prev === "mg") continue;
        out.push([start, i + 1]); start = i + 1;
      }
    }
    if (text.slice(start).trim()) out.push([start, text.length]);
    return out.map(([a, b]) => { const s = text.slice(a, b); const lead = s.length - s.trimStart().length; return { text: s.trim(), start: base + a + lead, end: base + b }; });
  }
  function parseDate(raw) {
    const iso = /^(\d{4})-(\d{2})-(\d{2})$/.exec(raw || "");
    if (iso) return { date_iso: raw, date_status: "parsed", date_candidates: [] };
    const us = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(raw || "");
    if (us) {
      const a = +us[1], b = +us[2], y = us[3], f = (m, d) => `${y}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
      if (a <= 12 && b <= 12 && a !== b) return { date_iso: null, date_status: "ambiguous", date_candidates: [f(a, b), f(b, a)] };
      return { date_iso: f(a, b), date_status: "parsed", date_candidates: [] };
    }
    return { date_iso: null, date_status: "missing", date_candidates: [] };
  }
  function parseRecords(text) {
    const recs = []; const re = /^=== Record (\d+) ===$/gm; let m; const heads = [];
    while ((m = re.exec(text))) heads.push({ n: +m[1], at: m.index });
    heads.forEach((h, i) => {
      const end = i + 1 < heads.length ? heads[i + 1].at : text.length;
      const block = text.slice(h.at, end).replace(/\s+$/, "");
      const get = (k) => { const mm = new RegExp("^" + k + ":\\s*(.*)$", "m").exec(block); return mm ? mm[1].trim() : ""; };
      const exLine = /^Excerpt:\s*"?(.*?)"?\s*$/m.exec(block);
      const exStart = exLine ? h.at + block.indexOf(exLine[1], block.indexOf("Excerpt:")) : null;
      recs.push(Object.assign({ id: "r" + h.n, seq: h.n, source_label: get("Source") || "(no source)", date_raw: get("Date"), duplicate_of: null,
        injection_tag: false, encounter: true, char_start: h.at, char_end: h.at + block.length, text: block,
        _ex: exLine ? exLine[1] : block, _exStart: exStart == null ? h.at : exStart }, parseDate(get("Date"))));
    });
    return recs;
  }
  function pickExcerpt(rec, sample) {
    const sents = sentences(rec._ex, rec._exStart).filter((s) => !/\$\d/.test(s.text) && !/Date of accident/.test(s.text));
    let use = sents;
    if (sample && rec.seq === 3) use = sents.slice(0, 2);
    if (!use.length) use = sentences(rec._ex, rec._exStart).slice(0, 1);
    return { start: use[0].start, end: use[use.length - 1].end, text: rec.text.slice(use[0].start - rec.char_start, use[use.length - 1].end - rec.char_start), sents: sentences(rec._ex, rec._exStart) };
  }
  function check(key, v) { return v; }
  function ladder(id, rec, ex, state, opts) {
    return { item_id: id, backend: "fixture",
      generator: { model: "claude-sonnet-5-5", prompt_version: "extract_v1", call_id: "c" + id, recorded_from: { backend: "claude-cli", model: "claude-sonnet-5-5", recorded_at: "2026-11-02T00:50:00Z" }, output: { summary: opts.summary, excerpt: ex.text } },
      code_checks: { excerpt_verbatim: true, excerpt_whole_sentence: true, qualifier_carried: true, date_provider_from_header: true, summary_tokens_not_in_excerpt: [], highlight_found: true },
      judge: { model: "claude-haiku-5-5", prompt_version: "judge_faithfulness_v1", call_id: "j" + id, verdict: opts.verdict },
      state, human: { action: null, edited_text: null, at: null } };
  }
  function build(token, name, text, sample, failN) {
    const records = parseRecords(text); const entries = [], undated = [], tray = [], amounts = [], flags = [], toConfirm = [];
    records.forEach((r) => {
      const sm = sample ? SAMPLE_SUMMARIES[r.seq] : null;
      if (failN && r.seq === failN) {
        tray.push({ id: "e" + r.seq + "x", kind: "entry", record_ids: [r.id], state: "rejected", reasons: ["LLM_CALL_FAILED"],
          why: "Could not process this record: the language model did not return a usable answer.", attempt: null, ladder: { item_id: "e" + r.seq + "x", state: "rejected" } });
        return;
      }
      const ex = pickExcerpt(r, sample);
      const summary = sm || ("AI summary (mock): " + ex.text.split(/(?<=[.;])\s/)[0]);
      const needs = sample && r.seq === 3; const state = needs ? "needs_review" : "verified";
      const e = { id: "e" + r.seq, seq: r.seq, record_ids: [r.id], date: r.date_iso, date_status: r.date_status, provider: r.source_label, summary, ai_drafted: true,
        source_kind: "record", excerpt: ex.text, excerpt_start: ex.start, excerpt_end: ex.end, state, reasons: needs ? ["JUDGE_PARTIAL"] : [],
        why: needs ? "The second check found part of the summary not fully supported by the quote." : "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
        review_status: "pending", edited: null, duplicate_note: null, ladder: ladder("e" + r.seq, r, ex, state, { summary, verdict: needs ? "partially" : "supported" }) };
      if (r.date_status === "parsed") entries.push(e);
      else { e.state = "needs_review"; e.reasons = ["DATE_AMBIGUOUS"]; e.why = "The date can be read two ways; confirm which one is right."; undated.push(e);
        toConfirm.push({ record_id: r.id, date_raw: r.date_raw, candidates: r.date_candidates, entry_id: e.id }); }
      r.sentences = ex.sents;
      (r.text.match(/\$[\d,]+(?:\.\d\d)?/g) || []).forEach((t, i) => {
        const at = r.char_start + r.text.indexOf(t); const sent = r.sentences.find((s) => s.start <= at && at < s.end) || { text: t, start: at, end: at + t.length };
        const rate = /per visit|\/visit/i.test(sent.text);
        amounts.push({ id: "a" + (amounts.length + 1), record_ids: [r.id], entry_id: "e" + r.seq, text: t, value_cents: Math.round(parseFloat(t.replace(/[$,]/g, "")) * 100), kind: rate ? "rate" : "charge",
          excerpt: sent.text, excerpt_start: sent.start, excerpt_end: sent.end, state: rate ? "needs_review" : "verified", reasons: rate ? ["AMOUNT_RATE_NOT_TOTALED"] : [],
          why: rate ? "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled." : "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
          review_status: "pending", edited: null, duplicate_note: null, ladder: { item_id: "a" + (amounts.length + 1), state: rate ? "needs_review" : "verified", backend: "fixture", generator: null,
            code_checks: { amount_in_text: true, classified_by: rate ? "rule:per_unit" : "rule:charge_label" }, judge: { model: "claude-haiku-5-5", verdict: "agrees" }, human: { action: null } } });
      });
    });
    entries.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq));
    const enc = records.filter((r) => r.date_status === "parsed").sort((a, b) => (a.date_iso < b.date_iso ? -1 : 1));
    for (let i = 1; i < enc.length; i++) {
      const days = Math.round((Date.parse(enc[i].date_iso) - Date.parse(enc[i - 1].date_iso)) / 864e5);
      if (days > 30) flags.push({ id: `f_gap_${enc[i - 1].id}_${enc[i].id}`, type: "gap", category: "gap_over_30", source_kind: "record", title: `Gap of ${days} days`,
        explanation: `Gap of ${days} days between ${ZL.fmtDate(enc[i - 1].date_iso)} (${enc[i - 1].source_label}) and ${ZL.fmtDate(enc[i].date_iso)} (${enc[i].source_label}).`,
        computed: { from: enc[i - 1].date_iso, to: enc[i].date_iso, days, threshold: 30 }, evidence: [enc[i - 1], enc[i]].map((r) => ({ record_id: r.id, excerpt: "Date: " + r.date_iso, start: r.char_start + r.text.indexOf("Date:"), end: r.char_start + r.text.indexOf("Date:") + 16 })),
        origin: "code", reviewer_note: null, state: "verified", reasons: [], why: "Calculated by code from two dates read from the record headers.", review_status: "pending", edited: null,
        ladder: { item_id: `f_gap_${enc[i - 1].id}_${enc[i].id}`, state: "verified", backend: "fixture", generator: null, code_checks: { dates_parsed: true, days, threshold: 30 }, judge: null, human: { action: null } } });
    }
    const queue = [...undated, ...entries].filter((e) => e.state === "needs_review").map((e) => e.id).concat(entries.filter((e) => e.state !== "needs_review").map((e) => e.id));
    const c = { token, name, status: "ingested", demo_mode: false, backend: "fixture", models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, records,
      undated_entries: undated, entries, amounts, totals: null, flags, tray, dates_to_confirm: toConfirm, injection: { records: [], banner: null }, review: null, warnings: [], created_at: new Date().toISOString(), updated_at: new Date().toISOString(), _queue: queue, _run: 0 };
    recompute(c); return c;
  }
  function recompute(c) {
    const acc = c.amounts.filter((a) => a.kind === "charge" && ["accepted", "edited"].includes(a.review_status));
    const pend = c.amounts.filter((a) => a.kind === "charge" && a.review_status === "pending");
    const det = c.amounts.filter((a) => a.kind === "charge" && a.review_status !== "dismissed");
    const sum = (l) => l.reduce((s, a) => s + a.value_cents, 0);
    c.totals = { accepted: { cents: sum(acc), count: acc.length, label: "Accepted charges" }, pending: { cents: sum(pend), count: pend.length, label: "Pending review" },
      detected_not_a_total: { cents: sum(det), count: det.length, label: "Detected (not a total)" }, not_totaled: c.amounts.filter((a) => a.kind !== "charge").map((a) => ({ id: a.id, kind: a.kind, text: a.text })) };
    const items = [...c.entries, ...c.undated_entries, ...c.amounts, ...c.flags];
    const n = (f) => items.filter(f).length;
    c.review = { queue: c._queue, counts: { pending: n((i) => i.review_status === "pending"), accepted: n((i) => i.review_status === "accepted"), edited: n((i) => i.review_status === "edited"),
      dismissed: n((i) => i.review_status === "dismissed"), needs_review: n((i) => i.state === "needs_review"), verified: n((i) => i.state === "verified"), rejected: c.tray.length,
      edit_to_check: n((i) => i.edit_to_check === true) }, ready_to_export: false };
  }
  const err = (status, code, message, detail) => ({ status, body: { error: { code, message, detail: detail || {} } } });
  const ok = (body, status) => ({ status: status || 200, body });
  const failN = () => +(new URLSearchParams(location.search).get("fail") || 0);
  const clone = (o) => JSON.parse(JSON.stringify(o));
  const view = (c) => { const v = clone(c); delete v._queue; delete v._run; if (c.status !== "ready") { if (c.status === "ingested") { v.entries = []; v.undated_entries = []; v.amounts = []; v.flags = []; v.tray = []; } } return v; };

  ZL.mock = {
    async handle(method, path, body) {
      await new Promise((r) => setTimeout(r, 30));
      let m;
      if (method === "GET" && path === "/health") return ok({ ok: true, version: "0.1.0-mock", synthetic_only: true, banner: "Synthetic data only — never paste real records", backend: "fixture", demo_mode: false, live_enabled: false,
        models: { generator: "claude-sonnet-5-5", judge: "claude-haiku-5-5" }, limits: { max_chars: MAX_CHARS, max_records: 40 }, retention_hours: 24,
        ai_banner: "Summaries and flags are drafted by AI and checked by code; you decide every item", sample_available: true });
      if (method === "POST" && path === "/cases") {
        let text = body && body.sample ? (ZL.MOCK_SAMPLE || "") : String((body && body.text) || "").replace(/\r\n?/g, "\n").trim();
        if (!text) return err(400, "bad_request", "There is no text to read. Paste records or upload a .txt file.");
        if (/^%PDF-/.test(text)) return err(400, "bad_request", "PDF files can't be read here. Save the records as plain text (.txt) or paste them.");
        if (text.length > MAX_CHARS) return err(413, "input_too_large", `That is more than ${MAX_CHARS.toLocaleString("en-US")} characters, which is the limit.`);
        const token = "mock" + Math.random().toString(36).slice(2, 12);
        const c = build(token, (body && body.sample) ? "Rivera sample" : "Pasted records", text, !!(body && body.sample), failN());
        if (!c.records.length) return err(400, "bad_request", "No records were found. Each record starts with a line like “=== Record 1 ===”.");
        store[token] = c;
        return ok({ token, name: c.name, status: "ingested", source: body && body.sample ? "sample" : "paste", demo_mode: false, record_count: c.records.length, split_method: "code",
          records: clone(c.records), dates_to_confirm: clone(c.dates_to_confirm), gap_flags: c.flags.filter((f) => f.type === "gap").map((f) => f.id), record_warning_flags: [], warnings: [] }, 201);
      }
      if (!(m = /^\/cases\/([^/]+)(\/.*)?$/.exec(path))) return err(404, "not_found", "Unknown endpoint.");
      const c = store[decodeURIComponent(m[1])]; const sub = m[2] || "";
      if (!c) return err(404, "not_found", "That case was not found.");
      if (method === "GET" && sub === "") return ok(view(c));
      if (method === "DELETE" && sub === "") { delete store[c.token]; return ok({ deleted: true }); }
      if (method === "POST" && sub === "/run") {
        if (c.status === "running") return err(409, "run_in_progress", "A run is already in progress.");
        c.status = "running"; c._run = Date.now(); setTimeout(() => { c.status = "ready"; recompute(c); }, 1800);
        return ok({ token: c.token, status: "running", stage: "extract", started_at: new Date().toISOString() }, 202);
      }
      if (method === "GET" && sub === "/status") {
        const frac = c.status === "running" ? Math.min(0.95, (Date.now() - c._run) / 1800) : c.status === "ready" ? 1 : 0; const total = c.records.length;
        return ok({ token: c.token, status: c.status, stage: c.status === "ready" ? "finalize" : "judge_entries", stages: ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"],
          progress: { done: Math.round(frac * total), total, label: `Checking summaries ${Math.round(frac * total)} of ${total}` }, counts: { entries: c.entries.length, amounts: c.amounts.length, flags: c.flags.length }, error: null, elapsed_ms: Date.now() - c._run });
      }
      if (method === "GET" && (m = /^\/items\/([^/]+)$/.exec(sub))) {
        const id = decodeURIComponent(m[1]); const it = [...c.entries, ...c.undated_entries, ...c.amounts, ...c.flags, ...c.tray].find((x) => x.id === id);
        if (!it) return err(404, "not_found", "That item was not found.");
        const recs = (it.record_ids || (it.evidence || []).map((e) => e.record_id)).filter((v, i, a) => a.indexOf(v) === i);
        const source = recs.map((rid) => { const r = c.records.find((x) => x.id === rid); return { record_id: rid, char_start: r.char_start, char_end: r.char_end, highlight_start: it.excerpt_start, highlight_end: it.excerpt_end }; });
        return ok({ item: { id, kind: it.kind || (id[0] === "e" ? "entry" : id[0] === "a" ? "amount" : "flag"), state: it.state, reasons: it.reasons, why: it.why, ladder: it.ladder }, source,
          calls: [{ id: "c1", role: "generator", step: "extract", backend: "fixture", model: "claude-sonnet-5-5", prompt_version: "extract_v1", attempt: 1, latency_ms: 5120, parsed_ok: !(it.state === "rejected"), verdict: null },
            { id: "c2", role: "judge", step: "judge_entries", backend: "fixture", model: "claude-haiku-5-5", prompt_version: "judge_faithfulness_v1", attempt: 1, latency_ms: 2210, parsed_ok: true, verdict: it.ladder && it.ladder.judge ? it.ladder.judge.verdict : null }], events: [] });
      }
      if (method === "POST" && (m = /^\/items\/([^/]+)\/review$/.exec(sub))) {
        const id = decodeURIComponent(m[1]); const it = [...c.entries, ...c.undated_entries, ...c.amounts, ...c.flags].find((x) => x.id === id);
        if (!it) return err(404, "not_found", "That item was not found.");
        const a = body && body.action;
        if (a === "accept") it.review_status = "accepted"; else if (a === "dismiss") it.review_status = "dismissed"; else if (a === "reset") { it.review_status = "pending"; it.edited = null; }
        else if (a === "edit" && body.edits && typeof body.edits.summary === "string" && id[0] === "e") { it.edited = { summary: body.edits.summary, original_summary: it.summary, at: new Date().toISOString(), kept_my_wording: false }; it.summary = body.edits.summary; it.review_status = "edited"; }
        else if (a === "edit" && body.edits && typeof body.edits.note === "string" && id[0] === "f") { it.reviewer_note = body.edits.note; it.review_status = "edited"; }
        else return err(422, "invalid_edit", "That edit is not allowed.");
        if (id[0] === "e") it.edit_to_check = it.review_status === "edited" && it.state === "needs_review";   // the server's flag (T-134)
        recompute(c);
        return ok({ item: clone(it), totals: clone(c.totals), review: clone(c.review), warnings: [] });
      }
      if (method === "POST" && sub === "/review/batch") {   // same verified-only, all-or-nothing rule as the server (api.md batch); no per-item route is called
        const ids = (body && body.item_ids) || [], act = body && body.action;
        if (!["accept", "reset"].includes(act) || !ids.length) return err(400, "bad_request", "A batch needs an action and item ids.");
        const bad = [], found = ids.map((id) => c.entries.find((x) => x.id === id) || (bad.push({ id, reason: "only entries can be decided in a batch" }), null));
        if (act === "accept") found.forEach((e) => { if (e && (e.state !== "verified" || e.review_status !== "pending")) bad.push({ id: e.id, reason: "only verified, not-yet-reviewed entries can be accepted in a batch" }); });
        if (bad.length) return err(422, "invalid_batch", "The batch was refused; nothing was changed.", { rejected: bad });
        found.forEach((e) => { if (act === "accept") e.review_status = "accepted"; else { e.review_status = "pending"; e.edited = null; } });
        recompute(c);
        return ok({ items: found.map((e) => ({ id: e.id, review_status: e.review_status })), totals: clone(c.totals), review: clone(c.review), warnings: [] });
      }
      if (method === "POST" && (m = /^\/records\/([^/]+)\/confirm_date$/.exec(sub))) {
        const r = c.records.find((x) => x.id === decodeURIComponent(m[1])); const d = body && body.date;
        if (!r || r.date_status !== "ambiguous") return err(422, "invalid_edit", "That record's date is not waiting for confirmation.");
        if (!r.date_candidates.includes(d)) return err(422, "date_invalid", "Choose one of the dates offered.");
        r.date_iso = d; r.date_status = "confirmed"; const i = c.undated_entries.findIndex((e) => e.record_ids[0] === r.id);
        const e = c.undated_entries.splice(i, 1)[0]; e.date = d; e.date_status = "confirmed"; e.state = "verified"; e.reasons = []; c.entries.push(e);
        c.entries.sort((x, y) => (x.date < y.date ? -1 : x.date > y.date ? 1 : x.seq - y.seq)); c.dates_to_confirm = c.dates_to_confirm.filter((x) => x.record_id !== r.id); recompute(c);
        return ok({ record: { id: r.id, date_iso: d, date_status: "confirmed", date_raw: r.date_raw }, entry: { id: e.id, date: d, moved_from: "undated_entries" }, gap_flags: [], removed_flag_ids: [], dates_to_confirm: clone(c.dates_to_confirm), warnings: [] });
      }
      return err(404, "not_found", "Unknown endpoint.");
    },
  };
})();
