# /Sages_Stone/core/action_router.py

"""
Action Router — From Warning to Motion
--------------------------------------

Observers do not act directly.
They request.

This router decides:

- who may act
- how strongly
- through what channel
- with what safeguards
"""

from typing import Any, Callable, Dict, List

from .kernel import Event, Kernel


class ActionRouter:
    """
    Central executor of system intentions.
    """

    def __init__(self, kernel: Kernel):
        self.kernel = kernel

        # action_name -> handlers
        self.handlers: Dict[str, List[Callable[[Any], None]]] = {}

        # listen for requests
        self.kernel.bus.subscribe(
            "observer.action.request",
            self._on_request
        )

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, action: str, fn: Callable[[Any], None]):
        self.handlers.setdefault(action, []).append(fn)

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def _on_request(self, event: Event):
        payload = event.payload or {}
        action = payload.get("action")
        data = payload.get("payload")

        if not action:
            return

        # announce intention
        self.kernel.bus.emit(
            Event(
                "action_router.invoked",
                {"action": action, "payload": data},
                source="action_router",
            )
        )

        # dispatch
        for fn in self.handlers.get(action, []):
            try:
                fn(data)
            except Exception as e:
                self.kernel.bus.emit(
                    Event(
                        "action_router.error",
                        {"action": action, "error": str(e)},
                        source="action_router",
                    )
                )

    # ------------------------------------------------------------------
    # Standard handlers
    # ------------------------------------------------------------------

    def install_default_handlers(self):
        """
        Gentle built-ins so the Stone can survive alone.
        """

        self.register("increase_stability", self._increase_stability)
        self.register("emergency_brake", self._emergency_brake)
        self.register("dream_throttle", self._dream_throttle)

    # ------------------------------------------------------------------
    # Built-in strategies
    # ------------------------------------------------------------------

    def _increase_stability(self, payload: Any):
        self.kernel.set(
            "runtime.stability_mode",
            "elevated"
        )

    def _emergency_brake(self, payload: Any):
        self.kernel.set(
            "runtime.stability_mode",
            "lockdown"
        )

    def _dream_throttle(self, payload: Any):
        self.kernel.set(
            "runtime.dreams.throttled",
            True
        )


# ----------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------

def attach_action_router(kernel: Kernel) -> ActionRouter:
    router = ActionRouter(kernel)
    router.install_default_handlers()
    kernel.register("action_router", router)
    return router


if __name__ == "__main__":
    from .kernel import boot_default
    from .coherence_observer import attach_coherence_observer

    k = boot_default()
    attach_coherence_observer(k)
    attach_action_router(k)

    k.bus.subscribe_all(lambda e: print("EVENT:", e))

    # simulate a request
    k.bus.emit(
        Event(
            "observer.action.request",
            {"action": "increase_stability", "payload": {"avg": 0.5}},
        )
    )

