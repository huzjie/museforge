import unittest

from museforge.utils.hash import stable_hash, stable_float
from museforge.utils.vectors import stable_vector, cosine, normalize, norm


class TestVectors(unittest.TestCase):
    def test_stable_hash_deterministic(self):
        self.assertEqual(stable_hash("abc"), stable_hash("abc"))
        self.assertNotEqual(stable_hash("abc"), stable_hash("abd"))

    def test_stable_float_range(self):
        for i in range(100):
            v = stable_float("k%d" % i, 0, 1)
            self.assertGreaterEqual(v, 0.0)
            self.assertLess(v, 1.0)

    def test_stable_vector_dim(self):
        v = stable_vector("hello", 64)
        self.assertEqual(len(v), 64)

    def test_cosine_self_one(self):
        v = stable_vector("hello", 32)
        self.assertAlmostEqual(cosine(v, v), 1.0, places=6)

    def test_normalize_unit_norm(self):
        v = stable_vector("hello", 32)
        n = normalize(v)
        self.assertAlmostEqual(norm(n), 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
