"""
Canonical Runtime Execution

This module performs execution strictly through
the canonical runtime spine.

No policy is defined here.
No shortcuts are taken.
All authority flows through the spine.
"""

from typing import Any, Dict, Optional

from sages_stone_runtime.runtime.bindings import CANONICAL_SPINE


def execute_system(
    system_path: str,
    *,
    mode: str = "safe",
    trace: bool = False,
    dry_run: bool = False,
) -> Any:
    """
    Execute a system via the canonical runtime spine.

    Flow:
        guard → (optional halt) → runner → emitter
    """

    spine = CANONICAL_SPINE

    # Step 1: Guard
    guard_report = spine.guard(
        system_path=system_path,
        mode=mode,
        trace=trace,
    )

    if not getattr(guard_report, "ok", False):
        spine.emitter(guard_report)
        return guard_report

    if dry_run:
        spine.emitter(guard_report)
        return guard_report

    # Step 2: Execute
    result = spine.runner(
        system_path=system_path,
        guard_report=guard_report,
        mode=mode,
        trace=trace,
    )

    # Step 3: Emit
    spine.emitter(result)
    return result
