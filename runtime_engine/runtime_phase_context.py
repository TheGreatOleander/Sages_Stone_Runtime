"""
Runtime Phase Context
=====================

Provides a lightweight, non-enforcing mechanism for tracking
the *declared* current runtime phase.

Important properties:
- No sequencing logic
- No validation
- No guards
- No side effects beyond context

This exists so that:
- Tracing can record phase without inference
- Guards can later *observe* phase, not guess it
- The runtime can speak clearly about what it is doing
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import Optional

from .runtime_phase import RuntimePhase


_current_phase: ContextVar[Optional[RuntimePhase]] = ContextVar(
    "current_runtime_phase",
    default=None,
)


def get_current_phase() -> Optional[RuntimePhase]:
    """
    Returns the currently declared runtime phase, if any.
    """
    return _current_phase.get()


def set_current_phase(phase: RuntimePhase) -> None:
    """
    Declare the current runtime phase.

    This does NOT:
    - enforce ordering
    - validate transitions
    - imply correctness

    It only makes the runtime's claim explicit.
    """
    _current_phase.set(phase)


class runtime_phase:
    """
    Context manager for temporarily declaring a runtime phase.

    Example:
        with runtime_phase(RuntimePhase.EXECUTION):
            run_dream(...)
    """

    def __init__(self, phase: RuntimePhase):
        self.phase = phase
        self._token = None

    def __enter__(self):
        self._token = _current_phase.set(self.phase)
        return self.phase

    def __exit__(self, exc_type, exc, tb):
        if self._token is not None:
            _current_phase.reset(self._token)
        return False
