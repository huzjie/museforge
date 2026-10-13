import unittest

from museforge.config import Config
from museforge.memory import MemoryStore, Encoder
from museforge.integrations.langchain import MuseMemoryChatMessageHistory


class TestIntegrations(unittest.TestCase):
    def test_langchain_adapter(self):
        cfg = Config().memory
        store = MemoryStore(cfg, Encoder(cfg.embed_dim))
        h = MuseMemoryChatMessageHistory(store)
        h.add_user_message("hello")
        h.add_ai_message("hi there")
        self.assertEqual(len(h.messages), 2)
        h.clear()
        self.assertEqual(len(h.messages), 0)


if __name__ == "__main__":
    unittest.main()
