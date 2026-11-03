"""Loader for app/llm/lexicon.yaml (read as a data file; no app.llm import, so deterministic modules stay LLM-free)."""
import functools
import pathlib
import re

import yaml

LEXICON_PATH = pathlib.Path(__file__).resolve().parents[1] / "llm" / "lexicon.yaml"


@functools.lru_cache(maxsize=1)
def load() -> dict:
    return yaml.safe_load(LEXICON_PATH.read_text(encoding="utf-8"))


def code_list(name: str) -> list:
    """Entries of a `code_lists` category as [{id, regex}] (compiled IGNORECASE)."""
    return list(_compiled(name))


@functools.lru_cache(maxsize=None)
def _compiled(name: str) -> tuple:
    entries = load()["code_lists"][name]["entries"]
    return tuple({"id": e["id"], "regex": re.compile(e["pattern"], re.IGNORECASE)} for e in entries)
