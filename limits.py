"""
LIMITS — Deterministic Execution Boundaries

This module defines hard limits that must be satisfied
BEFORE any execution is permitted.

Limits are declarative, explicit, and non-negotiable.
They are not configuration knobs and are not advisory.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Limits:
    """
    Immutable execution limits.

    These values define the maximum allowable scope
    for any gated execution attempt.
    """
    max_steps: int
    max_seconds: float
    max_memory_mb: int


# The single lawful limits instance.
LIMITS = Limits(
    max_steps=1_000,
    max_seconds=5.0,
    max_memory_mb=256,
)


def validate_limits(limits: Limits) -> None:
    """
    Pure validation of limit coherence.
    No execution. No mutation. No I/O.
    """
    if limits.max_steps <= 0:
        raise ValueError("max_steps must be positive.")

    if limits.max_seconds <= 0:
        raise ValueError("max_seconds must be positive.")

    if limits.max_memory_mb <= 0:
        raise ValueError("max_memory_mb must be positive.")
