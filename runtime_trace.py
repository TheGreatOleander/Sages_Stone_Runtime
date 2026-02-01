"""
runtime_trace.py

Runtime Trace Utilities
-----------------------
Lightweight, opt-in execution tracing for Sages_Stone_Runtime.

Design principles:
- ZERO mutation of runtime behavior
- Structured, append-only events
- Human-readable AND machine-friendly
- No dependency on engine internals
- Self-identifying (runtime + schema versioned)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time
import uuid

from .runtime_version import IDENTITY


# ---------------------------------------------------------------------------
# Trace Event
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TraceEvent:
    """
    Immutable trace event.

    Events are intentionally generic:
    this avoids coupling to engine or scoring internals.
    """
    name: str
    timestamp: float
    payload: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Runtime Trace
# ---------------------------------------------------------------------------

class RuntimeTrace:
    """
    Append-only execution trace.

    This object is SAFE to pass around but OPTIONAL to use.
    Nothing in the runtime depends on it.
    """

    def __init__(self, trace_id: Optional[str] = None):
        self.trace_id: str = trace_id or str(uuid.uuid4())
        self.identity = IDENTITY
        self.created_at: float = time.time()
        self._events: List[TraceEvent] = []

    # ---------------------------------------------------------------------

    def record(self, name: str, **payload: Any) -> None:
        """
        Record a trace event.

        Example:
            trace.record("lens_applied", lens="stability", weight=0.7)
        """
        event = TraceEvent(
            name=name,
            timestamp=time.time(),
            payload=dict(payload),
        )
        self._events.append(event)

    # ---------------------------------------------------------------------

    @property
    def events(self) -> List[TraceEvent]:
        """
        Returns a COPY of recorded events.
        """
        return list(self._events)

    # ---------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize trace for storage or transport.
        """
        return {
            "trace_id": self.trace_id,
            "created_at": self.created_at,
            "runtime": self.identity.to_dict(),
            "events": [
                {
                    "name": e.name,
                    "timestamp": e.timestamp,
                    "payload": e.payload,
                }
                for e in self._events
            ],
        }

    # ---------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._events)

    def __repr__(self) -> str:
        return (
            f"<RuntimeTrace id={self.trace_id} "
            f"events={len(self._events)} "
            f"runtime={self.identity.version}>"
        )
