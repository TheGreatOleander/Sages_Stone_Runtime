# /Sages_Stone/core/state_model.py

"""
State Model — The Shared Reality Fabric
---------------------------------------

Not metaphysical truth.
Operational truth.

A structured memory that lenses can read,
observers can guard, and RCF can constrain.
"""

import time
from typing import Any, Dict, Optional
from .kernel import Event, Kernel


class StateModel:
    """
    Central structured memory for the runtime.
    """

    def __init__(self, kernel: Kernel):
        self.kernel = kernel

        # hierarchical world model
        self.data: Dict[str, Any] = {}

        # provenance tracking
        self.meta: Dict[str, Dict[str, Any]] = {}

        # listen for writes from the system
        self.kernel.bus.subscribe("kernel.state.set", self._on_kernel_write)

    # ------------------------------------------------------------------
    # Core access
    # ------------------------------------------------------------------

    def set(self, path: str, value: Any, source: str = "unknown"):
        self.data[path] = value

        self.meta[path] = {
            "source": source,
            "timestamp": time.time(),
        }

        self.kernel.bus.emit(
            Event(
                "state.changed",
                {
                    "path": path,
                    "value": value,
                    "source": source,
                },
                source="state_model",
            )
        )

    def get(self, path: str, default: Any = None) -> Any:
        return self.data.get(path, default)

    def exists(self, path: str) -> bool:
        return path in self.data

    # ------------------------------------------------------------------
    # Structured helpers
    # ------------------------------------------------------------------

    def update_dict(self, path: str, values: Dict[str, Any], source: str):
        base = self.data.get(path, {})
        if not isinstance(base, dict):
            base = {}

        base.update(values)
        self.set(path, base, source)

    def append_list(self, path: str, value: Any, source: str):
        base = self.data.get(path, [])
        if not isinstance(base, list):
            base = []

        base.append(value)
        self.set(path, base, source)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "data": dict(self.data),
            "meta": dict(self.meta),
        }

    # ------------------------------------------------------------------
    # Event bridge
    # ------------------------------------------------------------------

    def _on_kernel_write(self, event: Event):
        p = event.payload
        self.set(p["key"], p["value"], source="kernel")



# ----------------------------------------------------------------------
# Convenience registration
# ----------------------------------------------------------------------

def attach_state_model(kernel: Kernel) -> StateModel:
    model = StateModel(kernel)
    kernel.register("state", model)
    return model


if __name__ == "__main__":
    from .kernel import boot_default

    k = boot_default()
    s = attach_state_model(k)

    s.set("demo.value", 42, source="example")
    print(s.snapshot())

