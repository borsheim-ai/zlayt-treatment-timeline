"""LLM split fallback (D-031): ask the model for record-boundary character offsets when the code split found one unsplit block.

The model only points: it returns {records: [{start, end}]}. ingest.validate_split then checks by code that the spans cover the
text exactly and start on line starts; anything else keeps the single record. Every record made this way carries the
record_warning LLM_SPLIT (ingest.ingest). Fields (date, source, excerpt) never come from the model.
"""
from pydantic import ValidationError

from app.backend import ingest, injection, schemas
from app.llm import audited as AU, promptlib, provider as P


def make_splitter(call):
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id): the audited wrapper bound to the case."""
    def split(text: str):
        prompt = promptlib.load("split_v1")
        nonce = promptlib.nonce(text, "split", "all")
        user = injection.wrap(ingest.numbered(text), nonce) + f"\nTOTAL: {len(text)}\nReturn the JSON object."
        try:
            out, call_id = call("split", prompt.text, user, schemas.SplitOutput.model_json_schema(), item_id="split")
        except P.FixtureMiss:
            raise ingest.SplitFailed("FIXTURE_MISS") from None
        except AU.LLMFailed:
            raise ingest.SplitFailed("LLM_FAILED_AFTER_RETRIES") from None
        try:
            spans = [(s.start, s.end) for s in schemas.SplitOutput.model_validate(out).records]
        except (ValidationError, TypeError, ValueError):
            raise ingest.SplitFailed("SCHEMA_INVALID") from None
        return spans, call_id
    return split
