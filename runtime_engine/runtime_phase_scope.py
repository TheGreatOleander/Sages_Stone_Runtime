"""
Runtime Phase Scope
===================

A composable context manager that:
- Declares the current runtime phase
- Opens a trace scope for that phase

This module does NOT:
- enforce phase ordering
- validate transitions
- assume correctness

It exists to give the runtime a single, honest
mechanism for saying:
    "We are now doing this kind of work."
"""

from __future__ import annotations

from typing import Optional

from runtime_engine.runtime_phase import RuntimePhase
from runtime_engine.runtime_phase_context import runtime_phase
from runtime_trace.trace_scope import trace_scope


class runtime_phase_scope:
    """
    Context manager that binds a runtime phase to a trace scope.

    Example:
        with runtime_phase_scope(RuntimePhase.EXECUTION):
            run_dream(...)
    """

    def __init__(
        self,
        phase: RuntimePhase,
        label: Optional[str] = None,
    ):
        self.phase = phase
        self.label = label or f"phase:{phase.name.lower()}"

        self._phase_ctx = None
        self._trace_ctx = None

    def __enter__(self):
        # Declare phase (purely contextual)
        self._phase_ctx = runtime_phase(self.phase)
        self._phase_ctx.__enter__()

        # Open trace scope (purely descriptive)
        self._trace_ctx = trace_scope(self.label)
        self._trace_ctx.__enter__()

        return self.phase

    def __exit__(self, exc_type, exc, tb):
        # Close trace scope first (inner)
        if self._trace_ctx is not None:
            self._trace_ctx.__exit__(exc_type, exc, tb)

        # Then reset phase context
        if self._phase_ctx is not None:
            self._phase_ctx.__exit__(exc_type, exc, tb)

        return False
