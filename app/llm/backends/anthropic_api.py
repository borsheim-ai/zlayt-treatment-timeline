"""anthropic-api backend: Anthropic SDK, temperature 0, schema via a forced tool call. ADR-004. One attempt, no retry."""
import json
import os
import time

from app.llm._types import LLMError, LLMResult

TIMEOUT_S = 120.0
MAX_TOKENS = 4096


def make_client():
    """SDK retries are off (audited.py owns retries) and the timeout is explicit (CONTRACT 5.2)."""
    import anthropic
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"), max_retries=0, timeout=TIMEOUT_S)


def call(model: str, system: str, user: str, json_schema: dict, *, key: str = "", client=None) -> LLMResult:
    if client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise LLMError("BACKEND_UNAVAILABLE anthropic-api has no key")
        client = make_client()
    t0 = time.monotonic()
    try:
        r = client.messages.create(
            model=model, max_tokens=MAX_TOKENS, temperature=0, system=system,
            messages=[{"role": "user", "content": user}],
            tools=[{"name": "emit", "description": "Return the answer as this JSON object.", "input_schema": json_schema}],
            tool_choice={"type": "tool", "name": "emit"})
    except Exception as e:                                   # SDK errors may echo request data: keep only the class
        raise LLMError(f"BACKEND_FAILED anthropic-api {type(e).__name__}") from None
    blocks = [b for b in (getattr(r, "content", None) or []) if getattr(b, "type", "") == "tool_use"]
    if not blocks or not isinstance(blocks[0].input, dict):
        raise LLMError("INVALID_JSON: no tool_use object in reply")
    out = blocks[0].input
    u = getattr(r, "usage", None)
    return LLMResult(output=out, backend="anthropic-api", model_resolved=getattr(r, "model", model) or model,
                     latency_ms=int((time.monotonic() - t0) * 1000), tokens_in=int(getattr(u, "input_tokens", 0) or 0),
                     tokens_out=int(getattr(u, "output_tokens", 0) or 0), raw=json.dumps(out))
