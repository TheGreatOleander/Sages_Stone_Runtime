"""
LAW — Sealed Runtime Authority

This module defines the immutable laws governing the Sages_Stone runtime.
It contains NO execution engine, NO I/O, and NO mutation pathways.

Purpose:
- Provide a single, authoritative vocabulary of what is permitted.
- Define invariants that must ALWAYS hold.
- Serve as the only reference the Gate may consult.

This file is intentionally minimal and weight-bearing.
"""

from dataclasses import dataclass
from typing import Tuple, FrozenSet


# -------------------------
# Core Invariants
# -------------------------

# These invariants are absolute. Violation is fatal to integrity.
INVARIANTS: Tuple[str, ...] = (
    "ALL_EXECUTION_MUST_ROUTE_THROUGH_GATE",
    "NO_SIDE_EFFECTS_OUTSIDE_LAW",
    "STATE_MUST_BE_EXPLICIT_AND_FINITE",
    "LIMITS_ARE_ENFORCED_PRE_EXECUTION",
    "DETERMINISM_IS_MANDATORY",
)


# -------------------------
# Permitted Operation Classes
# -------------------------

# These are categories, not implementations.
PERMITTED_OPERATION_CLASSES: FrozenSet[str] = frozenset({
    "OBSERVE",      # Read-only inspection
    "EVALUATE",     # Constraint checking without mutation
    "TRANSITION",   # State change (must be gated and lawful)
    "ABORT",        # Deterministic halt on violation
})


# -------------------------
# Forbidden Operation Classes
# -------------------------

FORBIDDEN_OPERATION_CLASSES: FrozenSet[str] = frozenset({
    "SELF_MODIFY",
    "BYPASS_GATE",
    "IMPLICIT_STATE",
    "UNBOUNDED_EXECUTION",
    "NON_DETERMINISTIC_BEHAVIOR",
})


# -------------------------
# Law Container
# -------------------------

@dataclass(frozen=True)
class Law:
    """
    Immutable container for runtime law.

    This object may be imported and inspected,
    but it cannot be altered, extended, or replaced.
    """
    invariants: Tuple[str, ...]
    permitted_ops: FrozenSet[str]
    forbidden_ops: FrozenSet[str]


# The single lawful instance.
LAW = Law(
    invariants=INVARIANTS,
    permitted_ops=PERMITTED_OPERATION_CLASSES,
    forbidden_ops=FORBIDDEN_OPERATION_CLASSES,
)


# -------------------------
# Validation (Pure, Non-Executable)
# -------------------------

def assert_law_integrity(law: Law) -> None:
    """
    Pure integrity check.
    No I/O. No state. No mutation.

    Raises ValueError if LAW is internally inconsistent.
    """
    if not law.invariants:
        raise ValueError("LAW must define at least one invariant.")

    overlap = law.permitted_ops.intersection(law.forbidden_ops)
    if overlap:
        raise ValueError(f"Operation classes both permitted and forbidden: {overlap}")

    if "BYPASS_GATE" in law.permitted_ops:
        raise ValueError("LAW cannot permit gate bypass.")


# Integrity is checkable, but NOT auto-executed.
# The Gate will decide when and whether to invoke this.
