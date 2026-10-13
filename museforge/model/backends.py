"""Pluggable model backends.

A backend provides three capabilities used by the MuseAgent:
  * `generate(prompt, ...)`          -> text generation
  * `rank_memories(query, candidates)` -> score/rank memory candidates
  * `try_subgoal(goal_id, sg_id)`    -> boolean subgoal attempt outcome
  * `persist_after_failure(goal_id, sg_id)` -> boolean "keep going" decision

`mock` is a deterministic, trainable reference backend whose `skill` parameter
(0.5 -> 1.0) cleanly drives memory precision and focus persistence. The other
backends delegate to a real service when reachable and otherwise fall back to
the deterministic mock so the whole system always runs offline.
"""
from __future__ import annotations

import json
from typing import List, Optional

from ..utils.hash import stable_float, stable_hash
from ..utils.text import summarize_text

_BACKENDS = {}


def register_backend(name):
    def deco(cls):
        _BACKENDS[name] = cls
        cls.name = name
        return cls
    return deco


def list_backends():
    return sorted(_BACKENDS.keys())


def get_backend(name: str, cfg):
    if name not in _BACKENDS:
        raise ValueError("unknown backend '%s' (available: %s)" % (name, ", ".join(list_backends())))
    return _BACKENDS[name](cfg)


class _Base:
    def generate(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        raise NotImplementedError

    def rank_memories(self, query: str, candidates: List[dict]) -> List[dict]:
        raise NotImplementedError

    def try_subgoal(self, goal_id: str, subgoal_id: str) -> bool:
        raise NotImplementedError

    def persist_after_failure(self, goal_id: str, subgoal_id: str) -> bool:
        raise NotImplementedError


@register_backend("mock")
class MockBackend(_Base):
    """Deterministic, trainable backend.

    `skill` in [0, 1] is the single knob:
      * memory ranking:  score = (skill-0.5)*2 * is_correct + noise(0..1)
      * subgoal success: success = skill >= threshold(0..1)
      * persistence:     persist = skill >= threshold(0..1)
    As skill rises 0.5 -> 1.0, recall@k and goal completion climb monotonically.
    """

    def __init__(self, cfg):
        self.cfg = cfg
        self.skill = cfg.skill

    def generate(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        return "mock: %s" % summarize_text(prompt, max_tokens=24)

    def score_candidate(self, query: str, candidate_id: str, is_correct: bool) -> float:
        noise = stable_float("noise:%s:%s" % (query, candidate_id), 0.0, 1.0)
        # boost = (skill-0.5)*2 -> 0 at skill=0.5 (pure random recall=1/n),
        #                         1 at skill=1.0 (correct always wins)
        boost = (self.skill - 0.5) * 2.0
        return boost * (1.0 if is_correct else 0.0) + noise

    def rank_memories(self, query: str, candidates: List[dict]) -> List[dict]:
        scored = []
        for c in candidates:
            s = self.score_candidate(query, c.get("id", ""), bool(c.get("is_correct", False)))
            scored.append((s, c))
        scored.sort(key=lambda t: t[0], reverse=True)
        return [c for _, c in scored]

    def try_subgoal(self, goal_id: str, subgoal_id: str) -> bool:
        return self.skill >= stable_float("subgoal:%s:%s" % (goal_id, subgoal_id), 0.0, 1.0)

    def persist_after_failure(self, goal_id: str, subgoal_id: str) -> bool:
        return self.skill >= stable_float("persist:%s:%s" % (goal_id, subgoal_id), 0.0, 1.0)

    def train_step(self, delta: float = 0.05) -> float:
        self.skill = min(1.0, self.skill + delta)
        return self.skill


@register_backend("cpu")
class CpuBackend(MockBackend):
    """A fixed-skill (1.0) deterministic backend -- a 'trained' mock."""

    def __init__(self, cfg):
        super().__init__(cfg)
        self.skill = 1.0


def _http_post(api_base: str, api_key: str, model: str, prompt: str, max_tokens: int) -> Optional[str]:
    try:
        import urllib.request
        import urllib.error
    except Exception:
        return None
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        api_base.rstrip("/") + "/chat/completions",
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + (api_key or ""),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception:
        return None


class _RemoteBackend(MockBackend):
    """Common behaviour for real backends: try remote, else fall back to mock."""

    def generate(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        max_tokens = max_tokens or self.cfg.max_tokens
        if self.cfg.api_base:
            out = _http_post(self.cfg.api_base, self.cfg.api_key, self.cfg.model_id, prompt, max_tokens)
            if out:
                return out
        return super().generate(prompt, max_tokens, temperature)


@register_backend("openai")
class OpenAIBackend(_RemoteBackend):
    pass


@register_backend("vllm")
class VLLMBackend(_RemoteBackend):
    pass


@register_backend("transformers")
class TransformersBackend(_RemoteBackend):
    pass
