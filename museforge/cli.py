"""Command-line interface for museforge."""
from __future__ import annotations

import argparse

from .config import load_config
from .engine.agent import MuseAgent


def _build(args):
    cfg = load_config(args.config)
    return MuseAgent(cfg)


def cmd_doctor(args):
    from .doctor import run_doctor
    run_doctor(args.config)


def cmd_demo(args):
    agent = _build(args)
    out = agent.respond(args.query)
    print("Q:", out["query"])
    print("A:", out["response"])
    print("Retrieved:")
    for content, score in out["retrieved"]:
        print("   [%.3f] %s" % (score, content[:70]))


def cmd_bench(args):
    from .model.backends import get_backend
    from .bench import memory_bench, focus_bench, summarize, format_report
    from .train import Trainer
    cfg = load_config(args.config)
    backend = get_backend("mock", cfg.model)
    print("skill before: %.3f" % backend.skill)
    print(format_report(summarize(memory_bench.run_recall(backend), focus_bench.run_focus(backend))))
    Trainer(backend).train(steps=args.steps, delta=0.05)
    print("\nskill after: %.3f" % backend.skill)
    print(format_report(summarize(memory_bench.run_recall(backend), focus_bench.run_focus(backend))))


def cmd_train(args):
    from .train import Trainer
    from .model.backends import get_backend
    cfg = load_config(args.config)
    backend = get_backend("mock", cfg.model)
    traj = Trainer(backend).train(steps=args.steps, delta=0.05)
    print("skill trajectory: %s -> %s" % (traj[0], traj[-1]))


def cmd_serve(args):
    cfg = load_config(args.config)
    agent = MuseAgent(cfg)
    from .serving.http_server import run
    run(agent, cfg.serving.host, cfg.serving.port)


def main(argv=None):
    p = argparse.ArgumentParser(prog="museforge", description="Active Memory + Active Focus agent engine")
    p.add_argument("--config", default=None, help="path to config.yaml")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("doctor", help="run self-check across all components/backends")
    d = sub.add_parser("demo", help="run a one-shot memory-augmented query")
    d.add_argument("query")
    b = sub.add_parser("bench", help="run memory + focus benchmarks")
    b.add_argument("--steps", type=int, default=10)
    t = sub.add_parser("train", help="train the mock backend skill")
    t.add_argument("--steps", type=int, default=10)
    sub.add_parser("serve", help="start the HTTP server")

    args = p.parse_args(argv)
    if args.cmd == "doctor":
        cmd_doctor(args)
    elif args.cmd == "demo":
        cmd_demo(args)
    elif args.cmd == "bench":
        cmd_bench(args)
    elif args.cmd == "train":
        cmd_train(args)
    elif args.cmd == "serve":
        cmd_serve(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
