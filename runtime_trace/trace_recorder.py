"""
Trace Recorder
==============

Responsible for recording runtime events as they occur.

Design constraints:
- Append-only
- Descriptive, not interpretive
- No enforcement logic
- No inference about correctness

This module records *what the runtime claims happened*,
not whether it was valid.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from runtime_engine.runtime_phase_context import get_current_phase
from .trace_store import store_trace_record


def _now() -> float:
    """
    Monotonic-ish timestamp for trace ordering.
    """
    return time.time()


def record_event(
    event: str,
    data: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Record a runtime trace event.

    Parameters:
    - event: short, explicit event name
    - data: optional structured payload
    """

    record: Dict[str, Any] = {
        "event": event,
        "timestamp": _now(),
        "data": data or {},
    }

    # Phase annotation is purely descriptive.
    # Absence is meaningful and preserved.
    phase = get_current_phase()
    if phase is not None:
        record["runtime_phase"] = phase.name

    store_trace_record(record)
