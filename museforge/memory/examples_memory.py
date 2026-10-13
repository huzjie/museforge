"""Small demo of the Active Memory subsystem (standalone, no server)."""
from museforge.config import load_config
from museforge.memory import Encoder, MemoryStore, Retriever, Consolidator


def main():
    cfg = load_config()
    enc = Encoder(cfg.memory.embed_dim)
    store = MemoryStore(cfg.memory, enc)
    ret = Retriever(cfg.memory, enc)
    con = Consolidator(cfg.memory)

    # Simulate a user session with durable facts + recent events
    store.add("User prefers concise, bullet-style answers.", kind="semantic", importance=0.9)
    store.add("User is building a project-monitoring dashboard for PMO.", kind="semantic", importance=0.8)
    store.add("Yesterday the user asked about a weekly report template.", kind="episodic", importance=0.5)
    store.add("User's team covers Shanghai, Zhejiang, Shandong regions.", kind="semantic", importance=0.7)

    results = ret.retrieve("帮我写一份周报", store, k=3)
    print("Proactive retrieval for query '帮我写一份周报':")
    for m, s in results:
        print("  [%.3f] (%s) %s" % (s, m.kind, m.content[:60]))

    print()
    print("Memory count:", len(store))
    store.save()
    print("Saved to", cfg.memory.persistence_path)


if __name__ == "__main__":
    main()
