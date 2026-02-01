"""
Runtime Tracing Hook
====================

A lightweight lifecycle observer that records runtime transitions.

Design goals:
- No logging framework required
- No side effects on execution
- Safe to enable by default
- Serializable trace output
"""

from datetime import datetime
from typing import List, Dict, Any

from ..lifecycle import RuntimeState
from ..lifecycle_hooks import RuntimeLifecycleHook


class RuntimeTraceHook(RuntimeLifecycleHook):
    """
    Collects a chronological trace of runtime lifecycle transitions.
    """

    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def on_transition(self, state: RuntimeState) -> None:
        self.events.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "phase": state.phase.name,
                "message": state.message,
                "error": repr(state.error) if state.error else None,
                "metadata": dict(state.metadata),
            }
        )

    def export(self) -> List[Dict[str, Any]]:
        """
        Return a copy of the collected trace.
        """
        return list(self.events)

    def clear(self):
        """
        Reset trace history.
        """
        self.events.clear()
