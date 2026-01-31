# sages_stone_runtime/observers/base_observer.py
"""
Observer Base Contract
======================

Observers are passive listeners.
They MAY record, log, or trace execution,
but they MUST NOT mutate runtime state.

Observers are optional and order-independent.
"""

from __future__ import annotations

from typing import Any, Dict, Protocol


class RuntimeObserver(Protocol):
    """
    Structural contract for runtime observers.
    """

    def on_start(self, *, dream: Any, initial_state: Dict[str, Any]) -> None:
        ...

    def on_lens_applied(
        self,
        *,
        lens_name: str,
        before_state: Dict[str, Any],
        after_state: Dict[str, Any],
    ) -> None:
        ...

    def on_constraint_violation(
        self,
        *,
        constraint_name: str,
        message: str,
        state_snapshot: Dict[str, Any],
    ) -> None:
        ...

    def on_finish(
        self,
        *,
        success: bool,
        final_state: Dict[str, Any],
    ) -> None:
        ...
