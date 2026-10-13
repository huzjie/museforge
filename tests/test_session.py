import unittest

from museforge.session import SessionManager


class TestSession(unittest.TestCase):
    def test_get_or_create(self):
        sm = SessionManager()
        s1 = sm.get_or_create("a")
        s2 = sm.get_or_create("a")
        self.assertIs(s1, s2)
        self.assertEqual(len(sm), 1)

    def test_close(self):
        sm = SessionManager()
        sm.get_or_create("a")
        sm.close("a")
        self.assertEqual(len(sm), 0)

    def test_expire(self):
        sm = SessionManager(ttl=0.0)
        sm.get_or_create("a")
        self.assertEqual(sm.expire(), 1)
        self.assertEqual(len(sm), 0)


if __name__ == "__main__":
    unittest.main()
