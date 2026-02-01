"""
Sages Stone Runtime — Entry Point
================================

This module defines the canonical entrypoint for the
Sages Stone Runtime.

Execution is delegated to a Runner.
This file never performs execution itself.
"""

import sys
import argparse
from typing import Optional

from .runner import Runner
from .null_runner import NullRunner


# --- Runner Resolution -----------------------------------------------------


def resolve_runner(*, trace: bool) -> Runner:
    """
    Resolve and return a concrete Runner implementation.

    For now, the runtime installs a NullRunner by default.
    This allows safe end-to-end execution without side effects.
    """
    return NullRunner(trace=trace)


# --- CLI ------------------------------------------------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sages-stone-runtime",
        description="Canonical runtime for executing Sages Stone systems",
    )

    parser.add_argument(
        "system",
        nargs="?",
        help="Path to a system definition to execute",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and plan execution without running",
    )

    parser.add_argument(
        "--trace",
        action="store_true",
        help="Emit detailed execution trace",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Print runtime version and exit",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.version:
        print("Sages Stone Runtime v0.1.0")
        return 0

    if not args.system:
        parser.print_help()
        return 1

    try:
        runner = resolve_runner(trace=args.trace)
        result = runner.run(
            args.system,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"[runtime:error] {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print("[runtime] dry-run successful")
        return 0 if result.success else 3

    return 0 if result.success else 4


if __name__ == "__main__":
    raise SystemExit(main())
