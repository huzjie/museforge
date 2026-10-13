"""Text helpers: token counting, truncation, deterministic summary."""
import re

_WS = re.compile(r"\s+")


def tokenize(text: str) -> list:
    """Very cheap whitespace tokenizer -- a rough stand-in for real tokenizers."""
    return _WS.split(text.strip()) if text and text.strip() else []


def truncate_text(text: str, max_tokens: int) -> str:
    """Truncate `text` to roughly `max_tokens` whitespace tokens."""
    toks = tokenize(text)
    if len(toks) <= max_tokens:
        return text
    return " ".join(toks[:max_tokens]) + " ..."


def summarize_text(text: str, max_tokens: int = 40) -> str:
    """Deterministic extractive summary: first sentence + head tokens."""
    toks = tokenize(text)
    if not toks:
        return ""
    head = " ".join(toks[:max_tokens])
    return head
