/* Mock-only overlay (T-043): adds the sample's conflict / pre-existing / causation flags to ZL.mock so ?api=mock shows all four groups.
   Wraps ZL.mock.handle; flags it adds keep their own review state here. Not used when API_MODE is "real". */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  if (!ZL.mock || !ZL.mock.handle) return;
  const orig = ZL.mock.handle.bind(ZL.mock);
  const extra = {};   // token -> flags
  const clone = (o) => JSON.parse(JSON.stringify(o));
  const find = (recs, rn, sub) => { const r = recs.find((x) => x.seq === rn); const i = r ? r.text.indexOf(sub) : -1; if (i < 0) return null; return { record_id: r.id, excerpt: sub, start: r.char_start + i, end: r.char_start + i + sub.length }; };
  function build(recs) {
    const mk = (id, type, category, title, explanation, ev, o) => ev.every(Boolean) ? Object.assign({ id, type, category, source_kind: "record", title, explanation, computed: {}, evidence: ev, origin: "code", reviewer_note: null,
      state: "verified", reasons: [], why: "Calculated by code; every quote is word for word in the records.", review_status: "pending", edited: null, ladder: { item_id: id, state: "verified", backend: "fixture", generator: null, judge: null, human: { action: null } } }, o || {}) : null;
    return [
      mk("f_acc_1", "conflict", "accident_date_after_treatment", "Stated accident date is later than recorded treatment",
        "Stated accident date 2026-01-19 (“Date of accident per intake form: 2026-01-19.”) is later than the first recorded treatment, 2026-01-09 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them.",
        [find(recs, 7, "Date of accident per intake form: 2026-01-19."), find(recs, 1, "Date: 2026-01-09"), find(recs, 2, "Date: 2026-01-09")]),
      mk("f_plan_4_6", "conflict", "treatment_plan_vs_actual", "Planned visits differ from visits attended",
        "Plan of care lists 12 visits (Capital PT, initial evaluation); discharge is recorded at visit 9 after two missed appointments.",
        [find(recs, 4, "Plan of care: 12 visits."), find(recs, 6, "Discharged from PT after two missed appointments.")], { state: "needs_review", reasons: ["LEXICON_ONLY"], why: "The phrase list and the model disagree on this flag." }),
      mk("f_pre_3", "pre_existing", "pre_existing", "Earlier complaint mentioned", "Dr. Alvarez, primary care (January 16, 2026) mentions low back pain in 2023.",
        [find(recs, 3, "Patient reports low back pain in 2023, resolved.")], { state: "needs_review", reasons: ["LLM_ONLY"], why: "The model found this; the phrase list did not." }),
      mk("f_deg_8", "pre_existing", "degenerative_language", "Degenerative wording in imaging", "Austin Imaging, cervical MRI (May 29, 2026): “Findings may represent degenerative change; correlate clinically.”",
        [find(recs, 8, "Findings may represent degenerative change; correlate clinically.")]),
      mk("f_pat_9", "causation", "patient_report", "Reported onset", "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
        [find(recs, 9, "Patient states symptoms began after the January collision.")]),
    ].filter(Boolean);
  }
  ZL.mock.handle = async function (method, path, body) {
    const m = /^\/cases\/([^/]+)(\/.*)?$/.exec(path);
    const token = m ? decodeURIComponent(m[1]) : "", sub = m ? m[2] || "" : "";
    if (!m) return orig(method, path, body);
    const r = /^\/items\/([^/]+)\/review$/.exec(sub);
    if (method === "POST" && r && extra[token]) {
      const f = extra[token].find((x) => x.id === decodeURIComponent(r[1]));
      if (f) {
        const a = body && body.action;
        if (a === "accept") f.review_status = "accepted";
        else if (a === "dismiss") { f.review_status = "dismissed"; if (body.note) f.reviewer_note = body.note; }
        else if (a === "reset") { f.review_status = "pending"; f.reviewer_note = null; f.edited = null; }
        else if (a === "edit" && body.edits && typeof body.edits.note === "string") { f.reviewer_note = body.edits.note; f.edited = { note: body.edits.note }; f.review_status = "edited"; }
        else return { status: 422, body: { error: { code: "invalid_edit", message: "That edit is not allowed.", detail: {} } } };
        const g = await orig("GET", "/cases/" + token);
        return { status: 200, body: { item: clone(f), totals: g.body.totals, review: g.body.review, warnings: [] } };
      }
    }
    const out = await orig(method, path, body);
    if (out.status >= 400) return out;
    if (method === "GET" && sub === "" && out.body && out.body.name === "Rivera sample" && out.body.status === "ready" && out.body.flags) {
      if (!extra[token]) extra[token] = build(out.body.records);
      out.body.flags = out.body.flags.concat(clone(extra[token]));
      out.body.review.queue = extra[token].filter((f) => f.state === "needs_review").map((f) => f.id).concat(out.body.review.queue, extra[token].filter((f) => f.state !== "needs_review").map((f) => f.id));
    }
    return out;
  };
})();
