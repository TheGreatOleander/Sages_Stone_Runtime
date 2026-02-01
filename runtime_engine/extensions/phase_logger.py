"""
Phase Logger Extension
=====================

A minimal, read-only runtime extension that logs phase transitions.

This extension is intentionally boring:
- No mutation
- No timing influence
- No contract interaction
- Safe to remove at any time

It exists to validate the extension registry and scheduler hooks.
"""

from typing import Any
from ..extension_registry import RuntimeExtension, ExtensionContext


class PhaseLogger(RuntimeExtension):
    name = "phase_logger"

    def on_phase_enter(self, context: ExtensionContext) -> None:
        print(
            f"[runtime][enter] phase={context.phase} "
            f"meta={context.metadata}"
        )

    def on_phase_exit(self, context: ExtensionContext) -> None:
        print(
            f"[runtime][exit]  phase={context.phase} "
            f"meta={context.metadata}"
        )

    def on_runtime_error(self, context: ExtensionContext, error: Exception) -> None:
        print(
            f"[runtime][error] phase={context.phase} "
            f"error={error.__class__.__name__}: {error}"
        )
