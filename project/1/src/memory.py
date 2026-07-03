"""
Lightweight per-session chat history.

We deliberately avoid LangChain's deprecated `ConversationBufferMemory` and
instead keep a simple in-process dict mapping `session_id -> [messages]`.
This is enough for a single-instance deployment on Streamlit Cloud.

For a multi-replica deployment, swap the `_STORE` for a Redis-backed
`RedisChatMessageHistory` — the public API of this module won't change.
"""

from __future__ import annotations

import threading
from collections import defaultdict, deque
from typing import Deque

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage


_MAX_MESSAGES = 20  # last 10 turns (human + AI)
_lock = threading.Lock()
_STORE: dict[str, Deque[BaseMessage]] = defaultdict(
    lambda: deque(maxlen=_MAX_MESSAGES)
)


class InMemoryHistory(BaseChatMessageHistory):
    """A `BaseChatMessageHistory` impl backed by the module-level dict."""

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id

    @property
    def messages(self) -> list[BaseMessage]:  # type: ignore[override]
        with _lock:
            return list(_STORE[self.session_id])

    def add_message(self, message: BaseMessage) -> None:
        with _lock:
            _STORE[self.session_id].append(message)

    def clear(self) -> None:
        with _lock:
            _STORE.pop(self.session_id, None)


def get_history(session_id: str) -> InMemoryHistory:
    """Return (or lazily create) the history for `session_id`."""
    return InMemoryHistory(session_id)


def add_user_message(session_id: str, content: str) -> None:
    get_history(session_id).add_message(HumanMessage(content=content))


def add_ai_message(session_id: str, content: str) -> None:
    get_history(session_id).add_message(AIMessage(content=content))


def clear_history(session_id: str) -> None:
    get_history(session_id).clear()


def all_sessions() -> list[str]:
    with _lock:
        return list(_STORE.keys())
