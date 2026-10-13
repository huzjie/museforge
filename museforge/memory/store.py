"""Persistent memory store: episodic + semantic memory with JSON persistence."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import List, Optional

from .types import Memory, EPISODIC, SEMANTIC
from .encoder import Encoder
from ..utils.hash import stable_hash


class MemoryStore:
    def __init__(self, cfg, encoder: Optional[Encoder] = None):
        self.cfg = cfg
        self.encoder = encoder or Encoder(cfg.embed_dim)
        self.episodic: List[Memory] = []
        self.semantic: List[Memory] = []
        self._counter = 0

    # -- write ------------------------------------------------------------
    def add(self, content: str, kind: str = EPISODIC, source: str = "user",
            importance: float = 0.5) -> Memory:
        self._counter += 1
        m = Memory(
            id="mem-%08x-%d" % (stable_hash(content + str(time.time())) & 0xFFFFFFFF, self._counter),
            kind=kind,
            content=content,
            source=source,
            created_at=time.time(),
            importance=max(0.0, min(1.0, importance)),
            embed=self.encoder.encode(content),
        )
        if kind == SEMANTIC:
            self.semantic.append(m)
        else:
            self.episodic.append(m)
        self._trim()
        return m

    def _trim(self):
        if len(self.episodic) > self.cfg.max_episodes:
            self.episodic = self.episodic[-self.cfg.max_episodes:]
        if len(self.semantic) > self.cfg.max_semantic:
            self.semantic = self.semantic[-self.cfg.max_semantic:]

    # -- read -------------------------------------------------------------
    def all(self) -> List[Memory]:
        return self.semantic + self.episodic

    def get(self, mem_id: str) -> Optional[Memory]:
        for m in self.all():
            if m.id == mem_id:
                return m
        return None

    def __len__(self) -> int:
        return len(self.episodic) + len(self.semantic)

    # -- persistence ------------------------------------------------------
    def save(self, path: Optional[str] = None):
        path = path or self.cfg.persistence_path
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "counter": self._counter,
            "episodic": [m.to_dict() for m in self.episodic],
            "semantic": [m.to_dict() for m in self.semantic],
        }
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load(self, path: Optional[str] = None):
        path = path or self.cfg.persistence_path
        p = Path(path)
        if not p.exists():
            return
        data = json.loads(p.read_text(encoding="utf-8"))
        self._counter = data.get("counter", 0)
        self.episodic = [Memory.from_dict(d) for d in data.get("episodic", [])]
        self.semantic = [Memory.from_dict(d) for d in data.get("semantic", [])]
        # re-embed on load (encoder is cheap/deterministic)
        for m in self.all():
            m.embed = self.encoder.encode(m.content)
