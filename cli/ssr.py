#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from runner.run import run
from runner.limits import Limits
from runner.errors import LimitExceeded, ExecutionFailed
from runner.entry_adapter import adapter_entry


EXIT_SUCCESS = 0
EXIT_LIMIT = 2
EXIT_FAILURE = 3


def load_config(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if path.suffix in (".yaml", ".yml"):
        if not HAS_YAML:
            raise RuntimeError("PyYAML not installed, cannot read YAML config")
        with path.open("r") as f:
            return yaml.safe_load(f)

    if path.suffix == ".json":
        with path.open("r") as f:
            return json.load(f)

    raise RuntimeError("Config must be .json or .yaml")


def main():
    parser = argparse.ArgumentParser(
        prog="ssr",
        description="Sage's Stone Runtime — controlled execution environment",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run a configuration safely")
    run_cmd.add_argument("config", help="Path to config (.json or .yaml)")
    run_cmd.add_argument("--max-steps", type=int, default=1_000)
    run_cmd.add_argument("--max-seconds", type=float, default=5.0)

    args = parser.parse_args()

    if args.command != "run":
        parser.error("Unknown command")

    try:
        config = load_config(Path(args.config))

        limits = Limits(
            max_steps=args.max_steps,
            max_seconds=args.max_seconds,
        )

        result = run(
            config=config,
            limits=limits,
            entry_fn=adapter_entry,
        )

        print(json.dumps(result, indent=2, default=str))
        sys.exit(EXIT_SUCCESS)

    except LimitExceeded as e:
        print(f"[LIMIT] {e}", file=sys.stderr)
        sys.exit(EXIT_LIMIT)

    except (ExecutionFailed, Exception) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()
