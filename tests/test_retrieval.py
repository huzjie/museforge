import unittest

from museforge.config import Config
from museforge.memory import Encoder, MemoryStore, Retriever
from museforge.memory.types import SEMANTIC


class TestRetrieval(unittest.TestCase):
    def setUp(self):
        self.cfg = Config().memory
        self.enc = Encoder(self.cfg.embed_dim)
        self.store = MemoryStore(self.cfg, self.enc)
        self.ret = Retriever(self.cfg, self.enc)

    def test_top_k_size(self):
        for i in range(20):
            self.store.add("memory %d" % i, kind=SEMANTIC)
        hits = self.ret.retrieve("anything", self.store, k=5)
        self.assertEqual(len(hits), 5)

    def test_matching_ranks_first(self):
        self.store.add("project monitoring dashboard", kind=SEMANTIC)
        for i in range(5):
            self.store.add("unrelated filler %d" % i, kind=SEMANTIC)
        hits = self.ret.retrieve("project monitoring dashboard", self.store, k=3)
        self.assertIn("project monitoring", hits[0][0].content)

    def test_token_budget(self):
        self.store.add("x" * 2000, kind=SEMANTIC)
        self.store.add("short", kind=SEMANTIC)
        hits = self.ret.retrieve("x", self.store, k=10, budget=10)
        # the 2000-token memory cannot fit under budget 10; 'short' can
        contents = [m.content for m, _s in hits]
        self.assertTrue(any(c == "short" for c in contents))


if __name__ == "__main__":
    unittest.main()
