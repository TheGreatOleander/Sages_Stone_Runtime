"""
Trace Observer
==============

A passive observer that records execution details
without influencing runtime behavior.
"""

from __future__ import annotations

from copy import deepcopy

from ..runtime_contract import Observer, RuntimeContext


class TraceObserver(Observer):
    """
    Records execution state at observation time.
    """

    def __init__(self):
        self.snapshots: list[dict] = []

    def observe(self, context: RuntimeContext) -> None:
        snapshot = {
            "phase": context.phase.name,
            "state": deepcopy(context.state),
            "violations": list(context.violations),
            "trace": list(context.trace),
        }
        self.snapshots.append(snapshot)
