"""Run benchmarks before/after training."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from museforge import Config
from museforge.model.backends import get_backend
from museforge.bench import memory_bench, focus_bench, summarize, format_report
from museforge.train import Trainer


def main():
    cfg = Config().model
    backend = get_backend("mock", cfg)
    print("skill before: %.3f" % backend.skill)
    print(format_report(summarize(memory_bench.run_recall(backend), focus_bench.run_focus(backend))))

    Trainer(backend).train(steps=10, delta=0.05)
    print()
    print("skill after: %.3f" % backend.skill)
    print(format_report(summarize(memory_bench.run_recall(backend), focus_bench.run_focus(backend))))


if __name__ == "__main__":
    main()
