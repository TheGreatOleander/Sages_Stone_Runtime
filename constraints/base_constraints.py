"""
Base Runtime Constraints
========================

Foundational constraints for Sages Stone runtime execution.

Constraints are:
- Read-only
- Deterministic
- Enforced at every phase boundary
"""

from __future__ import annotations

import time
from typing import Optional

from ..runtime_contract import Constraint, RuntimeContext, RuntimePhase


# ---------------------------------------------------------------------------
# Time Constraint
# ---------------------------------------------------------------------------

class MaxRuntimeSeconds(Constraint):
    """
    Prevents execution from exceeding wall-clock time.
    """

    def __init__(self, max_seconds: float):
        self.max_seconds = max_seconds
        self._start_time: Optional[float] = None

    def check(self, context: RuntimeContext) -> Optional[str]:
        if self._start_time is None:
            self._start_time = time.time()
            return None

        elapsed = time.time() - self._start_time
        if elapsed > self.max_seconds:
            return f"Max runtime exceeded ({elapsed:.2f}s > {self.max_seconds:.2f}s)"

        return None


# ---------------------------------------------------------------------------
# Step Constraint
# ---------------------------------------------------------------------------

class MaxLensApplications(Constraint):
    """
    Limits the number of lens applications.
    """

    def __init__(self, max_lenses: int):
        self.max_lenses = max_lenses

    def check(self, context: RuntimeContext) -> Optional[str]:
        applied = sum(
            1 for entry in context.trace
            if entry.startswith("Applying lens")
        )
        if applied > self.max_lenses:
            return f"Lens application limit exceeded ({applied} > {self.max_lenses})"
        return None


# ---------------------------------------------------------------------------
# Phase Constraint
# ---------------------------------------------------------------------------

class AllowedPhasesOnly(Constraint):
    """
    Restricts execution to a subset of phases.
    """

    def __init__(self, allowed: set[RuntimePhase]):
        self.allowed = allowed

    def check(self, context: RuntimeContext) -> Optional[str]:
        if context.phase not in self.allowed:
            return f"Phase {context.phase.name} is not permitted"
        return None


# ---------------------------------------------------------------------------
# State Growth Constraint
# ---------------------------------------------------------------------------

class MaxStateKeys(Constraint):
    """
    Limits the size of runtime state.
    """

    def __init__(self, max_keys: int):
        self.max_keys = max_keys

    def check(self, context: RuntimeContext) -> Optional[str]:
        size = len(context.state)
        if size > self.max_keys:
            return f"Runtime state size exceeded ({size} > {self.max_keys})"
        return None
