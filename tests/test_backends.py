import unittest

from museforge.config import Config
from museforge.model.backends import get_backend, list_backends


class TestBackends(unittest.TestCase):
    def test_list_backends(self):
        names = list_backends()
        self.assertIn("mock", names)
        self.assertIn("cpu", names)

    def test_mock_generate(self):
        cfg = Config().model
        b = get_backend("mock", cfg)
        out = b.generate("hello")
        self.assertIsInstance(out, str)
        self.assertTrue(out.startswith("mock:"))

    def test_rank_memories(self):
        cfg = Config().model
        b = get_backend("mock", cfg)
        cands = [
            {"id": "a", "content": "a", "is_correct": False},
            {"id": "b", "content": "b", "is_correct": True},
        ]
        ranked = b.rank_memories("q", cands)
        self.assertEqual(len(ranked), 2)

    def test_unknown_backend(self):
        with self.assertRaises(ValueError):
            get_backend("nope", Config().model)

    def test_cpu_skill_one(self):
        b = get_backend("cpu", Config().model)
        self.assertEqual(b.skill, 1.0)


if __name__ == "__main__":
    unittest.main()
