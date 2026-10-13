import unittest

from museforge.cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_put_get(self):
        c = LRUCache(2)
        c.put("a", 1)
        c.put("b", 2)
        self.assertEqual(c.get("a"), 1)
        c.put("c", 3)  # evicts b (least recently used)
        self.assertIsNone(c.get("b"))
        self.assertEqual(c.get("c"), 3)

    def test_contains(self):
        c = LRUCache(2)
        c.put("a", 1)
        self.assertIn("a", c)


if __name__ == "__main__":
    unittest.main()
