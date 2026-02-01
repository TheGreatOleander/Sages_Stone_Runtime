"""
Phase Timing Extension
=====================

Observer-only extension that measures wall-clock duration of runtime phases.

Key properties:
- Uses monotonic time (no clock skew issues)
- Does NOT affect scheduling, limits, or execution
- Records durations via trace recorder if present
- Safe to enable in production diagnostics
"""

import time
from typing import Dict

from ..extension_registry import RuntimeExtension, ExtensionContext
from ..extension_contract_guard import ExtensionCapabilities


class PhaseTiming(RuntimeExtension):
    name = "phase_timing"

    def __init__(self, trace_recorder=None):
        self._trace = trace_recorder
        self._phase_start: Dict[str, float] = {}

    def capabilities(self):
        # Explicit observer-only contract
        return ExtensionCapabilities(
            allow_state_read=True,
            allow_state_write=False,
            allow_timing_access=False,   # cannot influence timing
            allow_error_suppression=False,
        )

    def on_phase_enter(self, context: ExtensionContext) -> None:
        self._phase_start[context.phase] = time.monotonic()

    def on_phase_exit(self, context: ExtensionContext) -> None:
        start = self._phase_start.pop(context.phase, None)
        if start is None:
            return

        duration = time.monotonic() - start

        if self._trace:
            self._trace.record(
                kind="runtime_extension",
                payload={
                    "extension": self.name,
                    "event": "phase_duration",
                    "phase": context.phase,
                    "seconds": duration,
                },
            )
