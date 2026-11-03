"""Spanish-language records, model half (D-042, T-085): the prompts, step names and the translation judge. The code checks live in
spanish_text.py (re-exported here); the judge is an LLM and sits behind the same ladder as every other judge."""
from app.backend import judges, language, schemas
from app.backend.spanish_text import *      # noqa: F401,F403  (module_for, new_tokens, check_summary, check_excerpt, translation_info, ...)
from app.backend.spanish_text import LABEL, LABEL_EDITED, module_for, translation_info      # noqa: F401

EXTRACT_PROMPT = "extract_es_v1"
JUDGE_PROMPT = "judge_faithfulness_es_v1"
EXTRACT_STEP = "extract_es"
JUDGE_STEP = "judge_faithfulness_es"


def run_j1_meta(summary: str, excerpt: str, label: str, *, call, nonce=None, item_id=None, lang: str = "en"):
    """Judge 1 for an entry: the English judge for English records, the translation-faithfulness judge for Spanish records.
    Same return as judges.run_j1_meta: (verdict, call_id, reason_code)."""
    if not language.is_translated(lang):
        return judges.run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)
    return judges._run(JUDGE_STEP, JUDGE_PROMPT, schemas.Judge1, [excerpt], [("SOURCE LABEL", label), f"CANDIDATE SUMMARY: {summary}"],
                       call, nonce, item_id)


def judge_prompt_version(lang: str) -> str:
    return JUDGE_PROMPT if language.is_translated(lang) else "judge_faithfulness_v1"
