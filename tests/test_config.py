import os
import tempfile
import unittest

from museforge.config import Config, load_config


class TestConfig(unittest.TestCase):
    def test_defaults(self):
        c = Config()
        self.assertEqual(c.model.name, "mock")
        self.assertEqual(c.memory.embed_dim, 64)
        self.assertEqual(c.focus.max_subgoals, 8)

    def test_from_dict(self):
        c = Config.from_dict({"model": {"skill": 0.8}, "memory": {"top_k": 3}})
        self.assertEqual(c.model.skill, 0.8)
        self.assertEqual(c.memory.top_k, 3)

    def test_load_yaml_fallback(self):
        # write a small yaml and load it without pyyaml (yamlish fallback)
        fd, path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("model:\n  name: mock\n  skill: 0.9\nmemory:\n  top_k: 5\n")
            c = load_config(path)
            self.assertEqual(c.model.skill, 0.9)
            self.assertEqual(c.memory.top_k, 5)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
