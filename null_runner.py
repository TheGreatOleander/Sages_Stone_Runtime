"""
Sages Stone Runtime — Null Runner
================================

A concrete Runner implementation that performs:

- Structural validation only
- Deterministic planning
- NO real execution

This runner is intended for:
- Smoke testing the runtime pipeline
- Dry-run validation
- Safe integration with Sages_Stone core

It must never produce side effects.
"""

from __future__ import annotations

from pathlib import Path

from .runner import Runner, ExecutionPlan, ExecutionResult


class NullRunner(Runner):
    """
    A runner that proves the runtime works without executing anything.
    """

    # --- Phase 1: Validation ------------------------------------------------

    def validate(self, system_path: str) -> None:
        path = Path(system_path)

        if not path.exists():
            raise FileNotFoundError(f"System not found: {system_path}")

        if not path.is_file():
            raise ValueError(f"System path is not a file: {system_path}")

        if self.trace:
            print(f"[null-runner] validated path: {path}")

    # --- Phase 2: Planning --------------------------------------------------

    def plan(self, system_path: str) -> ExecutionPlan:
        plan = ExecutionPlan(
            steps=(
                "load_system_definition",
                "analyze_structure",
                "prepare_execution_context",
            ),
            metadata={
                "system_path": system_path,
                "runner": "NullRunner",
                "executable": False,
            },
        )

        if self.trace:
            print(f"[null-runner] plan created: {plan}")

        return plan

    # --- Phase 3: Execution -------------------------------------------------

    def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        # Execution is intentionally inert.
        return ExecutionResult(
            success=True,
            output={
                "message": "NullRunner does not execute systems.",
                "plan": plan,
            },
        )
