"""Self-check across all backends, components, and benchmarks."""
from __future__ import annotations

from .config import load_config
from .model.backends import list_backends, get_backend
from .memory import Encoder, MemoryStore, Retriever, Consolidator
from .focus import FocusManager
from .engine.agent import MuseAgent


def run_doctor(config_path=None):
    cfg = load_config(config_path)
    print("config: model=%s dim=%d skill=%.2f embed_dim=%d top_k=%d" % (
        cfg.model.name, cfg.model.dim, cfg.model.skill, cfg.memory.embed_dim, cfg.memory.top_k))

    for name in list_backends():
        try:
            b = get_backend(name, cfg.model)
            g = b.generate("hello")
            print("  [backend] %-14s ok (generate=%r)" % (name, g[:24]))
        except Exception as e:
            print("  [backend] %-14s FAIL %s" % (name, e))

    enc = Encoder(cfg.memory.embed_dim)
    store = MemoryStore(cfg.memory, enc)
    store.add("hello world", kind="semantic")
    ret = Retriever(cfg.memory, enc)
    hits = ret.retrieve("hello", store, k=1)
    print("  [memory]  store=%d retrieve=%d" % (len(store), len(hits)))

    con = Consolidator(cfg.memory)
    print("  [memory]  consolidate_after=%d (should_consolidate=%s)" % (cfg.memory.consolidate_after, con.should_consolidate(store)))

    fm = FocusManager(cfg.focus)
    g = fm.new_goal("test goal")
    st = fm.step(g, True)
    print("  [focus]   subgoals=%d progress=%.2f is_done=%s" % (len(g.subgoals), st["progress"], st["is_done"]))

    agent = MuseAgent(cfg)
    out = agent.respond("测试")
    print("  [engine]  respond ok (retrieved=%d)" % len(out["retrieved"]))
    print("doctor OK")


if __name__ == "__main__":
    run_doctor()
