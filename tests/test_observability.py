import unittest

from museforge.observability import Metrics, FocusTelemetry


class TestObservability(unittest.TestCase):
    def test_metrics(self):
        m = Metrics()
        m.inc("turns")
        m.inc("turns", 2)
        m.set("focus", 0.8)
        snap = m.snapshot()
        self.assertEqual(snap["counters"]["turns"], 3)
        self.assertEqual(snap["gauges"]["focus"], 0.8)

    def test_focus_telemetry(self):
        ft = FocusTelemetry(window=10)
        for s in [0.1, 0.2, 0.3]:
            ft.record(s)
        self.assertAlmostEqual(ft.recent_mean(3), 0.2)
        self.assertTrue(ft.below(0.5))


if __name__ == "__main__":
    unittest.main()
