import unittest

from museforge.config import Config
from museforge.model.backends import get_backend
from museforge.bench import memory_bench, focus_bench


class TestBench(unittest.TestCase):
    def test_recall_increases_with_skill(self):
        cfg = Config().model
        low = get_backend("mock", cfg)
        low.skill = 0.5
        r_low = memory_bench.run_recall(low, n_queries=40)
        high = get_backend("mock", cfg)
        high.skill = 1.0
        r_high = memory_bench.run_recall(high, n_queries=40)
        self.assertGreater(r_high["recall@1"], r_low["recall@1"])

    def test_focus_increases_with_skill(self):
        cfg = Config().model
        low = get_backend("mock", cfg)
        low.skill = 0.5
        f_low = focus_bench.run_focus(low, n_goals=30)
        high = get_backend("mock", cfg)
        high.skill = 1.0
        f_high = focus_bench.run_focus(high, n_goals=30)
        self.assertGreater(f_high["goal_completion_rate"], f_low["goal_completion_rate"])
        self.assertGreater(f_high["persistence"], f_low["persistence"])


if __name__ == "__main__":
    unittest.main()
