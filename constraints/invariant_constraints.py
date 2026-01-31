# sages_stone_runtime/constraints/invariant_constraints.py
"""
Invariant Constraints
=====================

Constraints that enforce global invariants over runtime state.

These constraints:
- Do NOT mutate state
- Only inspect and report violations
- Are safe to compose with any lenses
"""

from __future__ import annotations

from typing import Any, Dict, Iterable


class InvariantViolation(Exception):
    """
    Raised internally to signal invariant failure.
    """
    pass


class InvariantConstraint:
    """
    Base class for invariant-style constraints.
    """

    name: str = "InvariantConstraint"

    def check(self, state: Dict[str, Any]) -> Iterable[str]:
        """
        Inspect state and yield violation messages.
        Override in subclasses.
        """
        return []


class NoNoneValues(InvariantConstraint):
    """
    Enforces that runtime state contains no None values.
    """

    name = "NoNoneValues"

    def check(self, state: Dict[str, Any]) -> Iterable[str]:
        for key, value in state.items():
            if value is None:
                yield f"State key '{key}' has None value"


class MaxStateDepth(InvariantConstraint):
    """
    Enforces a maximum nesting depth for state dictionaries.
    """

    name = "MaxStateDepth"

    def __init__(self, max_depth: int = 5) -> None:
        self.max_depth = max_depth

    def check(self, state: Dict[str, Any]) -> Iterable[str]:
        def depth(obj: Any, current: int = 0) -> int:
            if not isinstance(obj, dict) or not obj:
                return current
            return max(depth(v, current + 1) for v in obj.values())

        actual = depth(state)
        if actual > self.max_depth:
            yield (
                f"State depth {actual} exceeds maximum allowed "
                f"depth {self.max_depth}"
            )
