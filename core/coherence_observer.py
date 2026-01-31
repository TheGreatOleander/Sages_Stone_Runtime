# /Sages_Stone/core/coherence_observer.py

"""
Coherence Observer — Guardian of Sanity
---------------------------------------

Watches the runtime for:

- RCF violations
- dream storms
- lens conflicts
- state oscillations

Not judge.
Not tyrant.

Thermostat of meaning.
"""

import time
from collections import deque
from typing import Any, Deque, Dict

from .kernel import Event, Kernel
from .observer_base import Observer


class CoherenceObserver(Observer):

    name = "coherence"

    def __init__(self, kernel: Kernel, window: int = 50):
        super().__init__(kernel)

        self.window = window

        # recent history
        self.scores: Deque[float] = deque(maxlen=window)
        self.violations: Deque[Dict[str, Any]] = deque(maxlen=window)

        # subscribe to RCF evaluations
        self.kernel.bus.subscribe("rcf.evaluated", self._on_rcf)
        self.kernel.bus.subscribe("rcf.violation", self._on_violation)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_rcf(self, event: Event):
        score = event.payload.get("score", 1.0)
        self.scores.append(score)

        avg = sum(self.scores) / len(self.scores)

        self.set_metric("rcf_average", avg)

        # gentle drift warning
        if avg < 0.6:
            self.request_action(
                "increase_stability",
                {"average": avg}
            )

    def _on_violation(self, event: Event):
        record = {
            "time": time.time(),
            "lens": event.payload.get("lens"),
            "score": event.payload.get("score"),
            "insight": event.payload.get("insight"),
        }

        self.violations.append(record)

        self.set_metric("last_violation", record)

        # acute danger
        if record["score"] < 0.3:
            self.request_action(
                "emergency_brake",
                record
            )

    # ------------------------------------------------------------------
    # Generic observation
    # ------------------------------------------------------------------

    def observe(self, event: Event):
        """
        Light ambient awareness.
        """

        # watch dream intensity
        if event.type == "kernel.dream":
            count = self.get_metric("dreams", 0) + 1
            self.set_metric("dreams", count)

            if count > 20:
                self.request_action("dream_throttle", {"count": count})

        # watch state churn
        if event.type == "state.changed":
            churn = self.get_metric("state_churn", 0) + 1
            self.set_metric("state_churn", churn)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def report(self) -> Dict[str, Any]:
        return {
            "average_score": self.get_metric("rcf_average"),
            "recent_violations": list(self.violations),
            "metrics": dict(self.metrics),
        }


# ----------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------

def attach_coherence_observer(kernel: Kernel) -> CoherenceObserver:
    obs = CoherenceObserver(kernel)
    kernel.register("observer.coherence", obs)
    return obs


if __name__ == "__main__":
    from .kernel import boot_default
    from .rcf_bridge import attach_rcf, RCFLaw

    k = boot_default()
    attach_rcf(k)
    attach_coherence_observer(k)

    k.bus.subscribe_all(lambda e: print("EVENT:", e))

    # simulate some activity
    k.bus.emit(Event("rcf.evaluated", {"score": 0.4}))
    k.bus.emit(Event("rcf.violation", {"score": 0.2, "lens": "test"}))

    print(k.get("observer.coherence").report())

