import unittest

from museforge.config import Config
from museforge.focus import FocusManager


class TestFocus(unittest.TestCase):
    def setUp(self):
        self.fm = FocusManager(Config().focus)

    def test_new_goal_decomposes(self):
        g = self.fm.new_goal("build a dashboard")
        self.assertGreaterEqual(len(g.subgoals), 3)

    def test_step_success_completes(self):
        g = self.fm.new_goal("build a dashboard")
        n = len(g.subgoals)
        for _ in range(n):
            self.fm.step(g, True)
        self.assertTrue(g.is_done())
        self.assertEqual(g.progress(), 1.0)

    def test_focus_score_range(self):
        g = self.fm.new_goal("build a dashboard")
        self.fm.step(g, True)
        score = self.fm.focus_score(g)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_deterministic_decompose(self):
        a = self.fm.new_goal("same goal text")
        b = self.fm.new_goal("same goal text")
        self.assertEqual(a.subgoals, b.subgoals)


if __name__ == "__main__":
    unittest.main()
