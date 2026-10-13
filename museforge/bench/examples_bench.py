"""Run the full benchmark: before vs after training."""
from museforge.config import load_config
from museforge.model.backends import get_backend
from museforge.bench import memory_bench, focus_bench, format_report, summarize
from museforge.train import Trainer


def main():
    cfg = load_config()
    backend = get_backend("mock", cfg.model)

    print("skill before:", backend.skill)
    before = summarize(memory_bench.run_recall(backend), focus_bench.run_focus(backend))
    print(format_report(before))

    traj = Trainer(backend).train(steps=10, delta=0.05)
    print("\nskill after: %.3f (trajectory %s)" % (backend.skill, ", ".join("%.2f" % s for s in traj[:5]) + " ..."))

    after = summarize(memory_bench.run_recall(backend), focus_bench.run_focus(backend))
    print(format_report(after))


if __name__ == "__main__":
    main()
