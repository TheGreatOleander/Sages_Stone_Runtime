# sages_stone_runtime/observers/json_trace_observer.py
"""
JSON Trace Observer
===================

Concrete observer that records runtime events
into a structured, JSON-serializable trace.

This observer:
- Never mutates state
- Records before/after snapshots shallowly
- Is safe for persistence and diffing
"""

from __future__ import annotations

from typing import Any, Dict, List


class JSONTraceObserver:
    """
    Records execution as a list of structured events.
    """

    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def on_start(self, *, dream: Any, initial_state: Dict[str, Any]) -> None:
        self.events.append({
            "event": "start",
            "initial_state": dict(initial_state),
        })

    def on_lens_applied(
        self,
        *,
        lens_name: str,
        before_state: Dict[str, Any],
        after_state: Dict[str, Any],
    ) -> None:
        self.events.append({
            "event": "lens_applied",
            "lens": lens_name,
            "before_state": dict(before_state),
            "after_state": dict(after_state),
        })

    def on_constraint_violation(
        self,
        *,
        constraint_name: str,
        message: str,
        state_snapshot: Dict[str, Any],
    ) -> None:
        self.events.append({
            "event": "constraint_violation",
            "constraint": constraint_name,
            "message": message,
            "state_snapshot": dict(state_snapshot),
        })

    def on_finish(
        self,
        *,
        success: bool,
        final_state: Dict[str, Any],
    ) -> None:
        self.events.append({
            "event": "finish",
            "success": success,
            "final_state": dict(final_state),
        })

    def export(self) -> List[Dict[str, Any]]:
        """
        Return a copy of the recorded trace.
        """
        return list(self.events)
