"""
GATE — Singular Runtime Choke Point

This module defines the mandatory entry gate for all runtime activity.
It performs evaluation ONLY. No execution, no mutation, no I/O.

All future execution surfaces MUST route through this gate.
"""

from typing import Iterable
from law import LAW, Law


class GateViolation(Exception):
    """Raised when a request violates LAW or gate invariants."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GateViolation(message)


def validate_law(law: Law) -> None:
    """
    Validate internal consistency of LAW.
    Pure check. No side effects.
    """
    _require(bool(law.invariants), "LAW must define invariants.")
    overlap = law.permitted_ops.intersection(law.forbidden_ops)
    _require(not overlap, f"Conflicting operation classes: {overlap}")
    _require(
        "BYPASS_GATE" not in law.permitted_ops,
        "LAW cannot permit gate bypass."
    )


def gate_check(
    *,
    requested_ops: Iterable[str],
    deterministic: bool,
    routes_through_gate: bool,
) -> None:
    """
    Mandatory pre-execution check.

    Parameters are descriptive, not executable.
    No action is taken beyond validation.
    """

    # Absolute invariants
    _require(routes_through_gate, "Execution must route through the gate.")
    _require(deterministic, "Non-deterministic behavior is forbidden.")

    # Operation class checks
    for op in requested_ops:
        _require(
            op in LAW.permitted_ops,
            f"Operation not permitted by LAW: {op}"
        )
        _require(
            op not in LAW.forbidden_ops,
            f"Operation explicitly forbidden by LAW: {op}"
        )


# Perform a self-check of LAW integrity.
# This does NOT authorize execution; it only ensures coherence.
validate_law(LAW)
