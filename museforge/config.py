"""Configuration for museforge.

Loads YAML via PyYAML when available, otherwise falls back to a tiny built-in
YAML-subset parser (utils.yamlish) so the package stays zero-dependency.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class MemoryConfig:
    max_episodes: int = 10000
    max_semantic: int = 5000
    token_budget: int = 2048
    top_k: int = 8
    half_life_hours: float = 24.0
    embed_dim: int = 64
    w_rel: float = 0.5
    w_rec: float = 0.2
    w_imp: float = 0.2
    w_freq: float = 0.1
    consolidate_after: int = 200
    persistence_path: str = ".museforge/memory.json"


@dataclass
class FocusConfig:
    max_subgoals: int = 8
    staleness_threshold: int = 3
    max_alternatives: int = 5
    persistence_budget: int = 10
    difficulty_threshold: float = 0.6


@dataclass
class ModelConfig:
    name: str = "mock"
    dim: int = 64
    skill: float = 0.5
    temperature: float = 0.7
    max_tokens: int = 256
    api_base: str = ""
    api_key: str = ""
    model_id: str = ""


@dataclass
class ServingConfig:
    host: str = "127.0.0.1"
    port: int = 8000


@dataclass
class Config:
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    focus: FocusConfig = field(default_factory=FocusConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    serving: ServingConfig = field(default_factory=ServingConfig)
    seed: int = 42

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Config":
        d = d or {}
        memory = MemoryConfig(**_numify(d.get("memory", {})))
        focus = FocusConfig(**_numify(d.get("focus", {})))
        model = ModelConfig(**_stringify(d.get("model", {})))
        serving = ServingConfig(**_stringify(d.get("serving", {})))
        seed = d.get("seed", 42)
        return cls(memory=memory, focus=focus, model=model, serving=serving, seed=seed)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _numify(mapping: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for k, v in mapping.items():
        if isinstance(v, str) and _is_num(v):
            out[k] = float(v) if ("." in v or "e" in v.lower()) else int(v)
        else:
            out[k] = v
    return out


def _stringify(mapping: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for k, v in mapping.items():
        if isinstance(v, str) and _is_num(v):
            out[k] = float(v) if ("." in v or "e" in v.lower()) else int(v)
        else:
            out[k] = v
    return out


def _is_num(s: str) -> bool:
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def load_config(path: Optional[str] = None) -> Config:
    """Load Config from a .yaml / .json path, or return defaults."""
    if not path:
        return Config()
    p = Path(path)
    if not p.exists():
        return Config()
    raw = p.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(raw)
    except Exception:
        from .utils.yamlish import parse
        data = parse(raw)
    if data is None:
        data = {}
    if p.suffix == ".json":
        data = json.loads(raw)
    return Config.from_dict(data)
