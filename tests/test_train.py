import unittest

from museforge.config import Config
from museforge.model.backends import get_backend
from museforge.train import Trainer


class TestTrain(unittest.TestCase):
    def test_skill_monotonic(self):
        b = get_backend("mock", Config().model)
        traj = Trainer(b).train(steps=10, delta=0.05)
        for i in range(1, len(traj)):
            self.assertGreaterEqual(traj[i], traj[i - 1])
        self.assertAlmostEqual(traj[-1], 1.0, places=4)


if __name__ == "__main__":
    unittest.main()
