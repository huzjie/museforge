"""LangChain adapter: expose museforge memory as a chat history backend.

Degrades gracefully: if langchain is not installed, the class is still
importable and raises a helpful message only when instantiated.
"""
from __future__ import annotations


def _is_available():
    try:
        import langchain  # noqa: F401
        return True
    except Exception:
        return False


class MuseMemoryChatMessageHistory:
    """A minimal chat-message-history-compatible wrapper over MemoryStore."""

    def __init__(self, store):
        self.store = store

    @property
    def messages(self):
        return [m.content for m in self.store.all()]

    def add_user_message(self, message: str):
        self.store.add(message, kind="episodic", source="user")

    def add_ai_message(self, message: str):
        self.store.add(message, kind="episodic", source="assistant")

    def clear(self):
        self.store.episodic = []
        self.store.semantic = []


def make_langchain_memory(store):
    if not _is_available():
        raise ImportError("langchain is not installed; install it to use this adapter")
    return MuseMemoryChatMessageHistory(store)
