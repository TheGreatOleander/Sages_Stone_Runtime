#!/usr/bin/env python3
"""
Sages Stone Runtime — Canonical CLI

This CLI executes systems strictly through the
canonical runtime execution path.

No execution logic lives here.
No policy lives here.
This file is a human-facing doorway only.
"""

import sys
import argparse
from typing import Optional

from sages_stone_runtime.runtime.execute import execute_system


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sages-stone",
        description="Sages Stone Runtime (canonical)",
    )

    parser.add_argument(
        "system",
        help="Path to the system definition to execute",
    )

    parser.add_argument(
        "--mode",
        default="safe",
        help="Execution mode (default: safe)",
    )

    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable execution tracing",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and guard without executing",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    result = execute_system(
        system_path=args.system,
        mode=args.mode,
        trace=args.trace,
        dry_run=args.dry_run,
    )

    # Exit code discipline
    if hasattr(result, "ok") and not result.ok:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
