import unittest

from museforge.utils.yamlish import parse


class TestYamlish(unittest.TestCase):
    def test_scalars(self):
        d = parse("a: 1\nb: 2.5\nc: hello\nd: true\n")
        self.assertEqual(d["a"], 1)
        self.assertEqual(d["b"], 2.5)
        self.assertEqual(d["c"], "hello")
        self.assertIs(d["d"], True)

    def test_nested(self):
        d = parse("memory:\n  top_k: 3\n  w_rel: 0.5\n")
        self.assertEqual(d["memory"]["top_k"], 3)
        self.assertEqual(d["memory"]["w_rel"], 0.5)

    def test_inline_comment(self):
        d = parse("name: mock  # the backend name\n")
        self.assertEqual(d["name"], "mock")

    def test_inline_list(self):
        d = parse("items: [a, b, c]\n")
        self.assertEqual(d["items"], ["a", "b", "c"])

    def test_block_list(self):
        d = parse("keywords:\n  - alpha\n  - beta\n")
        self.assertEqual(d["keywords"], ["alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
