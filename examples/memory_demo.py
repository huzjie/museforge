"""Active Memory standalone demo."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from museforge import Config
from museforge.memory import Encoder, MemoryStore, Retriever


def main():
    cfg = Config()
    enc = Encoder(cfg.memory.embed_dim)
    store = MemoryStore(cfg.memory, enc)
    ret = Retriever(cfg.memory, enc)

    store.add("用户偏好简洁的要点式回答", kind="semantic", importance=0.9)
    store.add("用户正在搭建项目监控看板", kind="semantic", importance=0.8)
    store.add("昨天用户问过周报模板", kind="episodic", importance=0.5)

    for q in ["帮我写周报", "监控看板进度"]:
        hits = ret.retrieve(q, store, k=3)
        print("Query:", q)
        for m, s in hits:
            print("   [%.3f] (%s) %s" % (s, m.kind, m.content[:60]))
        print()


if __name__ == "__main__":
    main()
