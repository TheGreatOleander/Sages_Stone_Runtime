"""
Sages Stone Runtime CLI
======================

Command-line interface for executing Sages Stone runtimes.

This CLI is intentionally minimal:
- Explicit arguments
- Predictable behavior
- No hidden execution paths
"""

from __future__ import annotations

import argparse
import json
import sys

from sages_stone_runtime.runtime_runner import run_dream
from sages_stone_runtime.runtime_contract import Dream
from sages_stone_runtime.lenses.state_lenses import (
    InitializeStateLens,
    ProjectMetadataLens,
)
from sages_stone_runtime.constraints.base_constraints import (
    MaxLensApplications,
    MaxStateKeys,
)
from sages_stone_runtime.observers.trace_observer import TraceObserver


# ---------------------------------------------------------------------------
# Argument Parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Sages Stone dream through the reference runtime"
    )

    parser.add_argument(
        "payload",
        help="Dream payload (string or JSON)",
    )

    parser.add_argument(
        "--metadata",
        help="Dream metadata as JSON",
        default="{}",
    )

    parser.add_argument(
        "--max-lenses",
        type=int,
        default=10,
        help="Maximum number of lens applications",
    )

    parser.add_argument(
        "--max-state-keys",
        type=int,
        default=20,
        help="Maximum number of keys allowed in runtime state",
    )

    parser.add_argument(
        "--trace",
        action="store_true",
        help="Print execution trace",
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------

def main() -> int:
    args = parse_args()

    # Parse payload
    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError:
        payload = args.payload

    # Parse metadata
    try:
        metadata = json.loads(args.metadata)
    except json.JSONDecodeError as exc:
        print(f"Invalid metadata JSON: {exc}", file=sys.stderr)
        return 1

    dream = Dream(payload=payload, metadata=metadata)

    lenses = [
        InitializeStateLens(),
        ProjectMetadataLens(),
    ]

    constraints = [
        MaxLensApplications(args.max_lenses),
        MaxStateKeys(args.max_state_keys),
    ]

    observer = TraceObserver()

    result = run_dream(
        dream=dream,
        lenses=lenses,
        constraints=constraints,
        observers=[observer],
    )

    # Output
    print("Success:", result.success)
    print("Final State:")
    print(json.dumps(result.final_state, indent=2))

    if result.violations:
        print("\nViolations:")
        for v in result.violations:
            print("-", v)

    if args.trace:
        print("\nTrace:")
        for entry in result.trace:
            print(entry)

    return 0 if result.success else 2


if __name__ == "__main__":
    raise SystemExit(main())
