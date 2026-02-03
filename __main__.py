"""
Sages_Stone_Runtime
Canonical Runtime Entry Point

This file is the ONLY sanctioned entry into the runtime.
All execution MUST flow through this boundary.

If you are seeing this file invoked indirectly, incorrectly,
or without explicit intent, that is a contract violation.
"""

import sys
from typing import NoReturn


def _fail(message: str) -> NoReturn:
    print(f"[RUNTIME HALT] {message}", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    """
    Canonical runtime entry.

    This function exists solely to:
    - Assert intentional invocation
    - Enforce single-entry semantics
    - Delegate only after validation

    It does NOT:
    - Parse complex arguments
    - Auto-discover behaviors
    - Guess user intent
    """

    argv = sys.argv[1:]

    if not argv:
        _fail(
            "Runtime invoked without intent.\n"
            "Explicit instruction is required to execute Sages_Stone_Runtime."
        )

    if len(argv) != 1:
        _fail(
            "Runtime accepts exactly one instruction.\n"
            "Parallel or compound invocation is forbidden."
        )

    instruction = argv[0]

    # At this layer, we do NOT interpret.
    # Interpretation is delegated deeper into the runtime,
    # under contract and invariant enforcement.
    try:
        from runtime_driver import dispatch
    except ImportError as exc:
        _fail(f"Runtime driver unavailable: {exc}")

    dispatch(instruction)


if __name__ == "__main__":
    main()
