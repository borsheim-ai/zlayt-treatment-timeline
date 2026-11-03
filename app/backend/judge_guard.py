"""Narrow judge-call guard (T-073). A judge that cannot answer for an EXPECTED reason (the LLM layer gave up, a fixture is missing, the
backend failed) never blocks the human: the result is 'unavailable' and the exception class is kept so the audit says why. Any other
exception is a bug in our code and propagates (audited_call no longer retries or hides those either).
judges._run turns LLMFailed into 'unavailable' without saying why, so the guard hands the judge a `call` that notes the expected error's class
on its way through; the class (LLMFailed, LLMError, FixtureMissing ...) is returned whichever layer swallowed the exception."""
from app.llm import audited as AU, provider as P

EXPECTED_JUDGE_ERRORS = (AU.LLMFailed, P.LLMError)


def guarded(fn, *args, **kwargs):
    """Run a judges.run_*_meta function. Returns (verdict, call_id, reason_code, error_class); error_class is None unless the judge could
    not answer for an expected reason (then verdict 'unavailable', reason_code 'NONE')."""
    seen = []
    call = kwargs.get("call")
    if call is not None:
        def noting(*a, **k):
            try:
                return call(*a, **k)
            except EXPECTED_JUDGE_ERRORS as e:
                seen.append(type(e).__name__)
                raise
        kwargs["call"] = noting
    try:
        verdict, call_id, code = fn(*args, **kwargs)
    except EXPECTED_JUDGE_ERRORS as e:
        return "unavailable", None, "NONE", type(e).__name__
    if seen and verdict == "unavailable":
        return verdict, call_id, code, seen[-1]
    return verdict, call_id, code, None
