import unittest

from museforge.config import Config
from museforge.memory import Encoder, MemoryStore
from museforge.memory import eviction


class TestEviction(unittest.TestCase):
    def setUp(self):
        self.cfg = Config().memory
        self.store = MemoryStore(self.cfg, Encoder(self.cfg.embed_dim))
        for i in range(10):
            self.store.add("mem %d" % i)

    def test_lru_keeps(self):
        kept = eviction.evict_lru(self.store.all(), 5)
        self.assertEqual(len(kept), 5)

    def test_fifo_keeps_oldest(self):
        kept = eviction.evict_fifo(self.store.all(), 3)
        self.assertEqual(len(kept), 3)
        self.assertIn("mem 0", [m.content for m in kept])


if __name__ == "__main__":
    unittest.main()
