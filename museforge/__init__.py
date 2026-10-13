"""museforge - Active Memory + Active Focus engine for personal agents.

A zero-dependency reference implementation of the two core mechanisms behind
Meta's Muse Wonder family of personal agents:

* **Active Memory** (active-memory): cross-session context carrying + proactive
  retrieval. The agent persists user key context (facts, preferences, past
  decisions) and, at every turn, proactively pulls *only* the memories relevant
  to the current query under a token budget -- instead of dumping the whole
  history into the prompt.

* **Active Focus** (active-focus): a measurable signal of whether the agent can
  push toward a hard goal, try alternative paths when stuck, and adapt to new
  information instead of giving up.

Public API:
    from museforge import MuseAgent, Config, get_backend
"""

__version__ = "0.1.0"

from .config import Config, load_config
from .model.backends import get_backend, register_backend
from .engine.agent import MuseAgent

__all__ = [
    "Config",
    "load_config",
    "MuseAgent",
    "get_backend",
    "register_backend",
    "__version__",
]
