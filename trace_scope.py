"""
trace_scope.py

Runtime Trace Scopes
--------------------
Context manager and decorator utilities for RuntimeTrace.

Purpose:
- Provide structured entry/exit tracing
- Capture duration and errors
- Avoid invasive instrumentation

This file intentionally depends ONLY on runtime_trace.
"""

import time
import functools
from typing import Callable, Optional, Any, Dict

from .runtime_trace import RuntimeTrace


# ---------------------------------------------------------------------------
# Context Manager
# ---------------------------------------------------------------------------

class TraceScope:
    """
    Context manager for tracing a logical execution scope.

    Example:
        with TraceScope(trace, "evaluation", candidate=x):
            score = engine.evaluate(x)
    """

    def __init__(
        self,
        trace: Optional[RuntimeTrace],
        name: str,
        **payload: Any,
    ):
        self.trace = trace
        self.name = name
        self.payload = payload
        self.start_time: Optional[float] = None

    # ---------------------------------------------------------------------

    def __enter__(self):
        self.start_time = time.time()
        if self.trace:
            self.trace.record(
                f"{self.name}:enter",
                **self.payload,
            )
        return self

    # ---------------------------------------------------------------------

    def __exit__(self, exc_type, exc, tb):
        end_time = time.time()
        duration = None
        if self.start_time is not None:
            duration = end_time - self.start_time

        if self.trace:
            event_payload: Dict[str, Any] = {
                "duration": duration,
            }

            if exc is not None:
                event_payload["error"] = repr(exc)
                self.trace.record(f"{self.name}:error", **event_payload)
            else:
                self.trace.record(f"{self.name}:exit", **event_payload)

        # DO NOT swallow exceptions
        return False


# ---------------------------------------------------------------------------
# Decorator
# ---------------------------------------------------------------------------

def traced(
    name: Optional[str] = None,
):
    """
    Decorator for tracing function execution.

    The wrapped function MUST accept a `trace=` keyword argument
    or ignore it safely.

    Example:
        @traced("score_candidate")
        def score(x, trace=None):
            ...
    """

    def decorator(func: Callable):
        trace_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            trace: Optional[RuntimeTrace] = kwargs.get("trace")

            with TraceScope(trace, trace_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator
