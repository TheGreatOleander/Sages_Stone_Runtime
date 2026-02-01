# --- existing imports ---
from typing import Any, Dict

# NEW: optional extension support
try:
    from .extension_registry import ExtensionRegistry
except Exception:
    ExtensionRegistry = None  # hard fail-safe


class RuntimeScheduler:
    """
    Coordinates runtime phases while enforcing limits and contracts.
    """

    def __init__(self, *args, **kwargs):
        # --- existing init logic ---
        super().__init__(*args, **kwargs) if hasattr(super(), "__init__") else None

        # NEW: extension registry (optional, inert by default)
        self.extensions = ExtensionRegistry() if ExtensionRegistry else None

    def _enter_phase(self, phase: str, metadata: Dict[str, Any] | None = None) -> None:
        # NEW: notify extensions (non-fatal)
        if self.extensions:
            self.extensions.notify_phase_enter(phase, metadata)

        # --- existing logic below ---
        self.current_phase = phase

    def _exit_phase(self, phase: str, metadata: Dict[str, Any] | None = None) -> None:
        # --- existing logic above ---
        if self.current_phase != phase:
            return

        # NEW: notify extensions (non-fatal)
        if self.extensions:
            self.extensions.notify_phase_exit(phase, metadata)

        self.current_phase = None

    def _handle_runtime_error(self, phase: str, error: Exception) -> None:
        # NEW: notify extensions first
        if self.extensions:
            self.extensions.notify_runtime_error(phase, error)

        # --- existing error handling logic ---
        raise error
