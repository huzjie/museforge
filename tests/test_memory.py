import os
import tempfile
import unittest

from museforge.config import Config
from museforge.memory import Encoder, MemoryStore
from museforge.memory.types import EPISODIC, SEMANTIC


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.cfg = Config().memory
        self.store = MemoryStore(self.cfg, Encoder(self.cfg.embed_dim))

    def test_add_and_all(self):
        self.store.add("hello", kind=SEMANTIC)
        self.store.add("world", kind=EPISODIC)
        self.assertEqual(len(self.store), 2)

    def test_get(self):
        m = self.store.add("find me")
        self.assertIsNotNone(self.store.get(m.id))

    def test_save_load_roundtrip(self):
        self.store.add("fact one", kind=SEMANTIC)
        self.store.add("event one", kind=EPISODIC)
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        try:
            self.store.save(path)
            store2 = MemoryStore(self.cfg, Encoder(self.cfg.embed_dim))
            store2.load(path)
            self.assertEqual(len(store2), 2)
            self.assertEqual(store2.all()[0].content, "fact one")
        finally:
            os.remove(path)

    def test_embed_assigned(self):
        m = self.store.add("embedded")
        self.assertEqual(len(m.embed), self.cfg.embed_dim)


if __name__ == "__main__":
    unittest.main()
