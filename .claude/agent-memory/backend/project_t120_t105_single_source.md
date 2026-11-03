---
name: t120-t105-single-source
description: T-120 history-source attribution strip rule and T-105 lexicon single-source views in grounding; review lessons (stop guessing, structural guard)
metadata:
  type: project
---

T-120 (lexicon_scan._is_source_sentence): do NOT guess whether a sentence "names a condition" (colon/digit/'of' proxies failed two reviews). Strip only the
attribution phrase after the history word (verb + via/from/per + closed list of people/channels + optional ", who interpreted") and keep the Hx hit if any
word is left in the sentence; a newline does not end the sentence; "Dr." is part of the name. Unknown source noun = nothing stripped = flag kept (safe).
**Why:** r1/r2 reviewers kept finding a new wording that lost a prior flag. **How to apply:** any "skip when X" guard on a flag: strip X, then run the normal scan.
Bare word "History" has no lexicon hit at all (needs a researcher entry), so "History provided by wife, notable for ..." cannot flag.

T-105 (grounding views): app/llm/lexicon.yaml code_lists.added_qualifier is the only word-list home. grounding.view(*ids) unions families; helpers
hedge_in_quote/has_hedge/attribution_in_quote/attribution_carried/approximation_hits/negation_words/has_negation(ignore=)/is_negation_word/lateral_words.
Spanish 'no' must be ignored in has_negation (it is the cue-list word, "No se descarta" is a hedge). Guard test: tests/unit/test_t105_added_qualifier_lexicon.py
duplicated_word_lists (AST, tokens matched against lexicon regexes, named allowlist of Spanish tables). Editing lexicon.yaml makes calibration.json stale: regenerate
from a clean worktree of the final commit (`git worktree add <dir> <sha>`; `python -m evals.run --write-calibration` there, fixture backend like T-090).
Mutant harness idea: edit file, run -k subset with env PYTHONPATH=. and a bare PATH, restore in finally.
