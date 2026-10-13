import unittest

from museforge import MuseAgent, Config
from museforge.memory.types import SEMANTIC


class TestEngine(unittest.TestCase):
    def setUp(self):
        self.agent = MuseAgent(Config())

    def test_respond(self):
        self.agent.remember("user prefers bullets", kind=SEMANTIC)
        out = self.agent.respond("what do I prefer")
        self.assertIn("response", out)
        self.assertIn("retrieved", out)

    def test_remember_recall(self):
        self.agent.remember("unique fact 12345", kind=SEMANTIC, importance=0.9)
        hits = self.agent.recall("unique fact 12345", k=1)
        self.assertGreaterEqual(len(hits), 1)

    def test_train_bumps_skill(self):
        before = self.agent.backend.skill
        self.agent.train(delta=0.1)
        self.assertGreaterEqual(self.agent.backend.skill, before)


if __name__ == "__main__":
    unittest.main()
