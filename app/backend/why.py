"""One fixed plain-language sentence per reason code (LLM_VS_CODE row 18, api.md appendix). Never model text."""
_WHY = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "The quoted text is not word for word in the record, so this item was rejected and cannot be used.",
    "GROUNDING_AMOUNT_NOT_IN_TEXT": "The amount shown does not appear in the record text, so this item was rejected and cannot be used.",
    "SCHEMA_INVALID": "The AI output was malformed after several attempts, so this item was rejected.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
    "EXCERPT_OMITS_QUALIFIER": "The record has a hedge sentence that qualifies this quote, but the quote leaves it out.",
    "EXCERPT_NOT_WHOLE_SENTENCE": "The quote starts or ends in the middle of a sentence.",
    "CHARGE_TEXT_IN_ENTRY": "The summary or quote states a dollar amount, which goes only in the internal notes, so this entry is held out of the letter. Dismiss it, or pick a quote without the amount and edit the summary to match.",
    "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
    "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
    "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
    "JUDGE_DISAGREES": "A second AI check disagreed with the first result for this item.",
    "JUDGE_UNSURE": "A second AI check could not decide whether this item is supported.",
    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this item has not been double-checked.",
    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
    "DATE_AMBIGUOUS": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.",
    "DATE_MISSING": "The record has no readable date, so it is left out of gap checks.",
    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
    "AMOUNT_RATE_NOT_TOTALED": "This figure is a rate, not a charge, so it is not added to the total.",
    "AMOUNT_ESTIMATE": "This figure is an estimate, not a billed charge, so it is not added to the total.",
    "AMOUNT_DAMAGES": "This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.",
    "AMOUNT_UNCLEAR": "This figure could not be read or labelled with confidence, so it is not added to the total.",
    "LEXICON_ONLY": "The phrase list found this flag but the AI did not; check that it applies.",
    "LLM_ONLY": "The AI found this flag but the phrase list did not; check that it applies.",
    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
    "SPLIT_AMBIGUOUS": "It is not certain where this record begins and ends in the pasted text.",
    "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
    "CONFLICT_CHECK_INCOMPLETE": "The check for conflicts between records did not finish or had no recorded answer, so conflicts between records may be missing.",
    "LANGUAGE_UNCERTAIN": "The language of this record could not be identified with confidence (it may not be English or Spanish), so the summary is an AI translation that has not been verified; read the original quote yourself.",
    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
    "SUMMARY_NOT_IN_QUOTE": "Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.",
    "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no AI-made entry. Read the record yourself or write the entry by hand.",
    "AI_TRANSLATION": "AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.",
    "OCR_DERIVED": "This record was read from a scanned page by OCR, which can misread letters and digits. Check it against the page image.",
}


# T-113 r2 (F5): a model-proposed CONFLICT sits in the tray under the reason code LLM_ONLY (the code is a closed contract list), but "the phrase list did not
# find it" is not why: conflicts never come from the phrase list. The cause is the rule that only a pair the software's own rules pick can be a conflict.
MODEL_CONFLICT = ("The AI suggested a conflict between two passages, but the software only raises a conflict for pairs its own fixed rules pick, "
                  "and they did not pick this one. Read both passages; add it by hand if it matters.")


# T-146 r2 / T-145 / T-167: JUDGE_UNAVAILABLE is one closed reason code with three causes, and the sentence follows the judge record (the code itself is unchanged and stays in the
# API fields; no code is ever printed in a sentence). A judge that never ran (deadline, or no judge record yet) keeps the "did not run" sentence. A judge that was asked and
# got no recorded answer is the demo (no live model): say so and say what she can do. A judge that was asked and failed live is "not available right now".
JUDGE_DEMO = ("The AI second check is not available in this demo, so this item has not been double-checked. "
              "Compare the summary with the quote yourself; if they match, accept it.")
JUDGE_FAILED = ("The second check is not available right now, so this item has not been double-checked. "
                "Compare the summary with the quote; if they match, accept it.")


def judge_failed(judge) -> bool:
    return bool(judge) and judge.get("verdict") == "unavailable" and judge.get("reason_code") != "JUDGE_NOT_RUN"


def judge_in_demo(judge) -> bool:
    """The judge was asked and no recorded answer existed (fixture replay = the demo). The error class is the audited call's, never model text."""
    return judge_failed(judge) and "FixtureMiss" in str(judge.get("error_class") or "")


# D-069 (T-177 r4): wording is chosen by provenance. `prep` is the item's (or case's) `prepared` field: the first answer is a hand-checked fixture, or none at all under the curated set.
# Every sentence below that would name an AI, a model or a drafter has a hand-written prepared twin; nothing is produced by rewriting the AI sentence. A code with no AI or model wording
# has no twin and reads the same either way. tests/unit/test_prepared_property.py is the guard.
_WHY_PREPARED = {
    "SCHEMA_INVALID": "The prepared answer for this step could not be used, so this item was rejected.",
    "JUDGE_PARTIAL": "A second check found the summary only partly supported by the quoted text.",
    "JUDGE_UNSUPPORTED": "A second check found the summary not supported by the quoted text.",
    "JUDGE_DISAGREES": "A second check disagreed with the first result for this item.",
    "JUDGE_UNSURE": "A second check could not decide whether this item is supported.",
    "JUDGE_UNAVAILABLE": "The second check did not run or did not finish, so this item has not been double-checked.",
    "FIXTURE_MISS": "The demo has no prepared answer for this step, so this item has not been checked.",
    "LEXICON_ONLY": "The phrase list found this flag but the prepared answers did not; check that it applies.",
    "LLM_ONLY": "The prepared answers include this flag but the phrase list does not; check that it applies.",
    "FILTERED_BY_RULE": "A prepared answer proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing a prepared answer proposed is hidden; it is not a flag and needs no action.",
    "LLM_SPLIT": "A prepared answer, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
    "LANGUAGE_UNCERTAIN": "The language of this record could not be identified with confidence (it may not be English or Spanish), so the summary is a prepared translation that has not been verified; read the original quote yourself.",
    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the checks; review it before relying on it.",
    "LLM_FAILED_AFTER_RETRIES": "The prepared answer for this record could not be used, so it has no entry.",
    "SUMMARY_NOT_IN_QUOTE": "Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.",
    "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no entry. Read the record yourself or write the entry by hand.",
    "AI_TRANSLATION": "Prepared translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.",
}
JUDGE_DEMO_PREPARED = ("The second check is not available in this demo, so this item has not been double-checked. "
                       "Compare the summary with the quote yourself; if they match, accept it.")
MODEL_CONFLICT_PREPARED = ("A prepared answer suggested a conflict between two passages, but the software only raises a conflict for pairs its own fixed rules pick, "
                           "and they did not pick this one. Read both passages; add it by hand if it matters.")


def unavailable_sentence(judge, prep=False) -> str:
    """The one sentence for a second check that gave no answer, by cause (used by the item's why and by the edit warning)."""
    if judge_in_demo(judge):
        return JUDGE_DEMO_PREPARED if prep else JUDGE_DEMO
    return JUDGE_FAILED if judge_failed(judge) else (_WHY_PREPARED if prep else _WHY)["JUDGE_UNAVAILABLE"]


def why(code: str, judge=None, prep=False) -> str:
    if code == "JUDGE_UNAVAILABLE":
        return unavailable_sentence(judge, prep)
    return (_WHY_PREPARED.get(code) if prep else None) or _WHY[code]


def join(reasons, judge=None, prep=False) -> str:
    """The sentences for a reason list. A recorded-answer miss (FIXTURE_MISS, demo) is not a failed call: no model was asked, so the 'did not run' sentence stays."""
    j = None if "FIXTURE_MISS" in (reasons or []) else judge
    return " ".join(why(c, j, prep) for c in reasons or [])


def conflict_in_tray(prep=False) -> str:
    return MODEL_CONFLICT_PREPARED if prep else MODEL_CONFLICT


def all_codes() -> list:
    return list(_WHY)


# D-028: judge reason codes (closed lists) -> fixed sentence. Model prose never reaches the UI.
_JUDGE_DETAIL = {
    "ADDS_DIAGNOSIS": "The summary adds a diagnosis the quote does not state.",
    "ADDS_SEVERITY": "The summary adds a severity the quote does not state.",
    "ADDS_CAUSATION": "The summary adds a cause the quote does not state.",
    "DROPS_QUALIFIER": "The summary leaves out a qualifier that the quote carries.",
    "NUMBER_MISMATCH": "A number in the summary does not match the quote.",
    "OTHER_UNSUPPORTED": "Part of the summary is not supported by the quote.",
    "SHOULD_BE_CHARGE": "The second check reads this figure as a billed charge.",
    "SHOULD_BE_RATE": "The second check reads this figure as a rate.",
    "SHOULD_BE_ESTIMATE": "The second check reads this figure as an estimate.",
    "SHOULD_BE_DAMAGES": "The second check reads this figure as a non-bill amount.",
    "SHOULD_BE_UNCLEAR": "The second check could not read this figure with confidence.",
    "TEXT_AMBIGUOUS": "The text does not settle the question.",
    "PLAN_VS_ACTUAL": "The second check reads the quotes as a plan and what followed.",
    "FACT_MISMATCH": "The second check reads the quotes as stating different facts.",
    "DIFFERENT_VISITS": "The second check reads the quotes as different visits that can both be true.",
    "CAN_BOTH_BE_TRUE": "The second check reads both quotes as possibly true together.",
    "WRONG_TYPE": "The second check does not think this flag type fits the quote.",
    "WRONG_CATEGORY": "The second check does not think this flag category fits the quote.",
    "NEGATED": "The second check reads the quote as negating the condition.",
    "NOT_SUPPORTED_BY_QUOTE": "The second check does not find this flag supported by the quote.",
}


def judge_detail(code) -> str:
    """Fixed sentence for a judge reason_code ('' for NONE / unknown)."""
    return _JUDGE_DETAIL.get(code, "")
