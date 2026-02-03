#!/usr/bin/env python3
"""
Sages Stone Runtime — Canonical CLI

This is the blessed human-facing entrypoint to the runtime.

Rules:
- No execution logic lives here.
- No policy is defined here.
- This file only orchestrates:
    input → guard → runner → result → exit

The runtime is law.
This file is ceremony.
"""

import sys
import argparse
from typing import Optional


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sages-stone",
        description="Sages Stone Runtime (canonical CLI)",
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

    parser = _build_parser()
    args = parser.parse_args(argv)

    # --- Lazy imports to keep CLI pure ---
    from sages_stone_runtime.runtime.guard import guard_system
    from sages_stone_runtime.runtime.runner import run_system
    from sages_stone_runtime.runtime.result import emit_result

    # Step 1: Guard
    guard_report = guard_system(
        system_path=args.system,
        mode=args.mode,
        trace=args.trace,
    )

    if not guard_report.ok:
        emit_result(guard_report)
        return 1

    if args.dry_run:
        emit_result(guard_report)
        return 0

    # Step 2: Execute
    result = run_system(
        system_path=args.system,
        guard_report=guard_report,
        mode=args.mode,
        trace=args.trace,
    )

    # Step 3: Emit
    emit_result(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
