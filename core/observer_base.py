# /Sages_Stone/core/observer_base.py

"""
Observer Base — The Act of Witnessing
------------------------------------

Observers do not transform like lenses.
They monitor, stabilize, and respond.

Where lenses ask:
    "What does this mean?"

Observers ask:
    "What is happening to the system itself?"
"""

from typing import Any, Dict
from .kernel import Event, Kernel


class Observer:
    """
    Base class for all observers.

    Responsibilities:
    - monitor event stream
    - maintain coherence metrics
    - trigger stabilizing actions
    """

    name: str = "abstract_observer"

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.metrics: Dict[str, Any] = {}

        # Hear everything by default
        self.kernel.bus.subscribe_all(self.on_event)

    # ------------------------------------------------------------------
    # Core protocol
    # ------------------------------------------------------------------

    def on_event(self, event: Event):
        """
        Entry point for all system activity.
        """
        self.observe(event)

    def observe(self, event: Event):
        """
        Override in subclasses to react to events.
        """
        pass

    # ------------------------------------------------------------------
    # Metric surface
    # ------------------------------------------------------------------

    def set_metric(self, key: str, value: Any):
        self.metrics[key] = value

        self.kernel.bus.emit(
            Event(
                "observer.metric",
                {
                    "observer": self.name,
                    "key": key,
                    "value": value,
                },
                source=self.name,
            )
        )

    def get_metric(self, key: str, default: Any = None):
        return self.metrics.get(key, default)

    # ------------------------------------------------------------------
    # Stabilization hooks
    # ------------------------------------------------------------------

    def request_action(self, action: str, payload: Any = None):
        """
        Ask the runtime to do something corrective.
        """
        self.kernel.bus.emit(
            Event(
                "observer.action.request",
                {
                    "observer": self.name,
                    "action": action,
                    "payload": payload,
                },
                source=self.name,
            )
        )


# ----------------------------------------------------------------------
# Composite Observer
# ----------------------------------------------------------------------

class CompositeObserver(Observer):
    """
    An observer made of observers.
    """

    name = "composite_observer"

    def __init__(self, kernel: Kernel):
        super().__init__(kernel)
        self.children: list[Observer] = []

    def add(self, observer: Observer):
        self.children.append(observer)

    def observe(self, event: Event):
        for child in self.children:
            child.observe(event)

