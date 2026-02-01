"""
Trace Bridge Extension
=====================

Bridges runtime phase transitions into the existing trace recording system.

This extension is OBSERVER-ONLY:
- No state mutation
- No timing influence
- No error suppression

It translates runtime lifecycle events into structured trace entries.
"""

from typing import Any, Dict
from ..extension_registry import RuntimeExtension, ExtensionContext
from ..extension_contract_guard import ExtensionCapabilities


class TraceBridge(RuntimeExtension):
    name = "trace_bridge"

    def __init__(self, trace_recorder):
        self._trace = trace_recorder

    def capabilities(self):
        # Explicitly observer-only
        return ExtensionCapabilities(
            allow_state_read=True,
            allow_state_write=False,
            allow_timing_access=False,
            allow_error_suppression=False,
        )

    def on_phase_enter(self, context: ExtensionContext) -> None:
        self._emit(
            event="phase_enter",
            phase=context.phase,
            metadata=context.metadata,
        )

    def on_phase_exit(self, context: ExtensionContext) -> None:
        self._emit(
            event="phase_exit",
            phase=context.phase,
            metadata=context.metadata,
        )

    def on_runtime_error(self, context: ExtensionContext, error: Exception) -> None:
        self._emit(
            event="runtime_error",
            phase=context.phase,
            error_type=error.__class__.__name__,
            error=str(error),
        )

    def _emit(self, **payload: Dict[str, Any]) -> None:
        """
        Emit a structured trace entry.

        Failures here are intentionally swallowed by the registry.
        """
        if not self._trace:
            return

        self._trace.record(
            kind="runtime_extension",
            payload={
                "extension": self.name,
                **payload,
            },
        )
