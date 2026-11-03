"""Versioned prompt files (app/llm/prompts/<name>_v<N>.md) and nonce helper. Prompt text is data; no model call here."""
import functools
import hashlib
import pathlib
import re
from dataclasses import dataclass

PROMPT_DIR = pathlib.Path(__file__).resolve().parent / "prompts"
_CHANGELOG = re.compile(r"^<!--\s*changelog:.*-->\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Prompt:
    name: str       # e.g. "extract_v1" (also the prompt_version stored in the ladder)
    text: str       # system text without the changelog line
    sha256: str     # hash of the whole file, changelog included (what evals record)


@functools.lru_cache(maxsize=None)
def load(name: str) -> Prompt:
    raw = (PROMPT_DIR / f"{name}.md").read_text(encoding="utf-8")
    if not _CHANGELOG.search(raw):
        raise ValueError(f"prompt {name} has no changelog line")
    return Prompt(name, _CHANGELOG.sub("", raw).strip(), hashlib.sha256(raw.encode()).hexdigest())


def nonce(*parts: str) -> str:
    """First 12 hex of sha256 over the parts (ADR-008.5: case text + step + item id). Deterministic so fixtures match."""
    h = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()
    return h[:12]
