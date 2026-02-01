"""
Sages Stone Runtime — Runner Contract
====================================

This module defines the canonical execution lifecycle
for the Sages Stone Runtime.

No concrete execution occurs here.

A Runner answers one question:

    "Given a system, how does law become motion?"

Execution is strictly phased:

    1. validate  — Is the system well-formed?
    2. plan      — What *would* happen?
    3. execute   — Make it real.

Nothing may skip a phase.
Nothing may reorder a phase.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


# --- Execution Artifacts ----------------------------------------------------


@dataclass(frozen=True)
class ExecutionPlan:
    """
    A concrete, immutable plan describing what execution would do.

    This must be safe to inspect, serialize, and diff.
    """
    steps: tuple
    metadata: Optional[dict[str, Any]] = None


@dataclass
class ExecutionResult:
    """
    The outcome of execution.

    Runners may extend this, but must not weaken it.
    """
    success: bool
    output: Optional[Any] = None
    error: Optional[Exception] = None


# --- Runner Contract --------------------------------------------------------


class Runner(ABC):
    """
    Abstract base class for all Sages Stone runtime runners.

    A Runner is stateful across a single invocation,
    but must not retain global or cross-run state.
    """

    def __init__(self, *, trace: bool = False) -> None:
        self.trace = trace

    # --- Phase 1: Validation ------------------------------------------------

    @abstractmethod
    def validate(self, system_path: str) -> None:
        """
        Validate the system definition.

        Must raise an exception on failure.
        Must not mutate state.
        """
        raise NotImplementedError

    # --- Phase 2: Planning --------------------------------------------------

    @abstractmethod
    def plan(self, system_path: str) -> ExecutionPlan:
        """
        Produce an execution plan without performing execution.

        Must be deterministic.
        Must not cause side effects.
        """
        raise NotImplementedError

    # --- Phase 3: Execution -------------------------------------------------

    @abstractmethod
    def execute(self, plan: ExecutionPlan) -> ExecutionResult:
        """
        Execute a previously generated plan.

        All side effects occur here and only here.
        """
        raise NotImplementedError

    # --- Orchestration ------------------------------------------------------

    def run(self, system_path: str, *, dry_run: bool = False) -> ExecutionResult:
        """
        Canonical orchestration of the execution lifecycle.
        This method must not be overridden.
        """
        if self.trace:
            print("[runner] validate")

        self.validate(system_path)

        if self.trace:
            print("[runner] plan")

        plan = self.plan(system_path)

        if dry_run:
            if self.trace:
                print("[runner] dry-run complete")
            return ExecutionResult(success=True, output=plan)

        if self.trace:
            print("[runner] execute")

        return self.execute(plan)
