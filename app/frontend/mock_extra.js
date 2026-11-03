/* Mock-only overlay (T-055 / T-058): export_config and audit for ?api=mock. ?local=1 adds prompt/response text to the audit like ZLAYT_MODE=local. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  if (!ZL.mock || !ZL.mock.handle) return;
  const orig = ZL.mock.handle.bind(ZL.mock), cfg = {};
  const local = () => new URLSearchParams(location.search).get("local") === "1";
  const err = (status, code, message, detail) => ({ status, body: { error: { code, message, detail: detail || {} } } });
  ZL.mock.handle = async function (method, path, body) {
    const m = /^\/cases\/([^/]+)(\/.*)?$/.exec(path); if (!m) return orig(method, path, body);
    const token = decodeURIComponent(m[1]), sub = m[2] || "";
    if (sub === "/export_config") {
      if (method === "GET") return { status: 200, body: Object.assign({ exhibit: null, bates_prefix: null, bates_start: null }, cfg[token] || {}) };
      if (method === "PUT") { const b = body || {};
        if ((b.exhibit && !/^[A-Za-z0-9 ._-]{1,20}$/.test(b.exhibit)) || (b.bates_prefix && !/^[A-Za-z0-9 ._-]{1,20}$/.test(b.bates_prefix))) return err(422, "invalid_edit", "Use up to 20 letters, digits, spaces, dots, dashes or underscores.");
        cfg[token] = { exhibit: b.exhibit || null, bates_prefix: b.bates_prefix || null, bates_start: b.bates_start == null ? null : b.bates_start }; return { status: 200, body: cfg[token] }; }
      if (method === "DELETE") { delete cfg[token]; return { status: 204, body: null }; }
    }
    if (sub === "/audit" && method === "GET") {
      const g = (await orig("GET", "/cases/" + token)).body, calls = [];
      (g.entries || []).forEach((e, i) => {
        calls.push(Object.assign({ id: "c" + i * 2, role: "generator", step: "extract", backend: "fixture", model: "claude-sonnet-5-5", prompt_version: "extract_v1", prompt_sha256: "9f2c0a77" + i, item_id: e.id, attempt: 1, latency_ms: 5120, cost_usd: 0.0041, tokens_in: 812, tokens_out: 150, parsed_ok: true, verdict: null },
          local() ? { system_text: "You read one medical record ...", user_text: "<<<RECORD>>> " + e.excerpt, response_raw: "{\"summary\": \"…\"}", error: null } : {}));
        calls.push({ id: "c" + (i * 2 + 1), role: "judge", step: "judge_entries", backend: "fixture", model: "claude-haiku-5-5", prompt_version: "judge_faithfulness_v1", prompt_sha256: "77aa10c2" + i, item_id: e.id, attempt: 1, latency_ms: 2210, cost_usd: 0.0006, tokens_in: 300, tokens_out: 20, parsed_ok: true, verdict: "supported" });
      });
      return { status: 200, body: { token, calls, events: [], summary: { calls: calls.length, cost_usd: 0.05, latency_ms_total: 70000, by_backend: { fixture: calls.length } } } };
    }
    return orig(method, path, body);
  };
})();
