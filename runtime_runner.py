"""
Runtime Runner
==============

High-level orchestration utilities for executing Sages Stone runtimes.

This module intentionally contains no execution logic.
It wires together engines, dreams, lenses, constraints, and observers.
"""

from __future__ import annotations

from typing import Iterable, Optional

from .runtime_contract import (
    Dream,
    Lens,
    Constraint,
    Observer,
    RuntimeResult,
)
from .runtime_engine import ReferenceRuntimeEngine


# ---------------------------------------------------------------------------
# Public Runner API
# ---------------------------------------------------------------------------

def run_dream(
    dream: Dream,
    lenses: Iterable[Lens],
    constraints: Iterable[Constraint] | None = None,
    observers: Iterable[Observer] | None = None,
) -> RuntimeResult:
    """
    Execute a dream using the reference runtime engine.

    This function is the canonical entry point for most users.
    """

    engine = ReferenceRuntimeEngine()

    return engine.run(
        dream=dream,
        lenses=list(lenses),
        constraints=list(constraints) if constraints else [],
        observers=list(observers) if observers else [],
    )


# ---------------------------------------------------------------------------
# Convenience Helpers
# ---------------------------------------------------------------------------

def run_simple(
    payload,
    lenses: Iterable[Lens],
    *,
    constraints: Iterable[Constraint] | None = None,
    observers: Iterable[Observer] | None = None,
    metadata: Optional[dict] = None,
) -> RuntimeResult:
    """
    Convenience wrapper for quick experiments.

    Accepts a raw payload and optional metadata.
    """

    from .runtime_contract import Dream  # local import to avoid cycles

    dream = Dream(
        payload=payload,
        metadata=metadata or {},
    )

    return run_dream(
        dream=dream,
        lenses=lenses,
        constraints=constraints,
        observers=observers,
    )
