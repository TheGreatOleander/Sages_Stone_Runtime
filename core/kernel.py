# /Sages_Stone/core/kernel.py

"""
Sages Stone — Core Kernel
-------------------------

This is the minimal gravitational center of the system.

Everything orbits this:
- lenses
- observers
- RCF laws
- runtime bridges to Pre-Sages dreams

No metaphysics here — only structure capable of holding metaphysics.
"""

import time
import uuid
import threading
from typing import Any, Callable, Dict, List, Optional


class Event:
    def __init__(self, type_: str, payload: Any = None, source: str = "kernel"):
        self.id = str(uuid.uuid4())
        self.type = type_
        self.payload = payload
        self.source = source
        self.timestamp = time.time()

    def __repr__(self):
        return f"<Event {self.type} from {self.source}>"


class EventBus:
    """
    Nervous system of the Stone.
    Everything speaks through here.
    """

    def __init__(self):
        self.listeners: Dict[str, List[Callable[[Event], None]]] = {}
        self.wildcard: List[Callable[[Event], None]] = []
        self.lock = threading.RLock()

    def subscribe(self, event_type: str, fn: Callable[[Event], None]):
        with self.lock:
            self.listeners.setdefault(event_type, []).append(fn)

    def subscribe_all(self, fn: Callable[[Event], None]):
        with self.lock:
            self.wildcard.append(fn)

    def emit(self, event: Event):
        with self.lock:
            for fn in self.listeners.get(event.type, []):
                fn(event)

            for fn in self.wildcard:
                fn(event)


class Kernel:
    """
    The runtime nucleus.

    Responsibilities:
    - lifecycle
    - registration
    - coordination
    - shared state
    """

    def __init__(self):
        self.bus = EventBus()
        self.services: Dict[str, Any] = {}
        self.running = False
        self.state: Dict[str, Any] = {}

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def boot(self):
        self.running = True
        self.bus.emit(Event("kernel.boot"))
        return self

    def shutdown(self):
        self.bus.emit(Event("kernel.shutdown"))
        self.running = False

    # ------------------------------------------------------------------
    # Service Registry
    # ------------------------------------------------------------------

    def register(self, name: str, service: Any):
        self.services[name] = service
        self.bus.emit(Event("kernel.service.registered", name))

    def get(self, name: str) -> Optional[Any]:
        return self.services.get(name)

    # ------------------------------------------------------------------
    # State surface
    # ------------------------------------------------------------------

    def set(self, key: str, value: Any):
        self.state[key] = value
        self.bus.emit(Event("kernel.state.set", {"key": key, "value": value}))

    def get_state(self, key: str, default: Any = None):
        return self.state.get(key, default)

    # ------------------------------------------------------------------
    # Runtime bridge
    # ------------------------------------------------------------------

    def dream(self, intent: str, data: Any = None):
        """
        Entry point from Pre-Sages space.
        Dreams enter here and become events.
        """
        self.bus.emit(Event("kernel.dream", {
            "intent": intent,
            "data": data
        }))


# ----------------------------------------------------------------------
# Default global kernel (optional but convenient)
# ----------------------------------------------------------------------

KERNEL = Kernel()


def boot_default():
    return KERNEL.boot()


if __name__ == "__main__":
    k = boot_default()

    k.bus.subscribe_all(lambda e: print("EVENT:", e))
    k.dream("hello_stone", {"msg": "first light"})

