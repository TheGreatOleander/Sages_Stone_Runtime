# --- existing imports ---
import os

# NEW: optional extensions
try:
    from runtime_engine.extensions.phase_logger import PhaseLogger
except Exception:
    PhaseLogger = None

try:
    from runtime_engine.extensions.trace_bridge import TraceBridge
except Exception:
    TraceBridge = None


class RuntimeRunner:
    """
    Entry point for executing a runtime-bound dream.
    """

    def __init__(self, *args, **kwargs):
        # --- existing init logic ---
        super().__init__(*args, **kwargs) if hasattr(super(), "__init__") else None

        self._extensions_enabled = (
            os.getenv("SAGES_STONE_ENABLE_EXTENSIONS", "0") == "1"
        )

    def _configure_runtime(self, scheduler):
        """
        Final, explicit runtime wiring step.
        """

        # --- existing configuration logic ---
        # (limits, adapters, contracts, trace_recorder, etc.)

        trace = getattr(self, "trace_recorder", None)

        # NEW: explicit, opt-in extension registration
        if self._extensions_enabled and getattr(scheduler, "extensions", None):

            # Phase logger (diagnostic only)
            if PhaseLogger:
                scheduler.extensions.register(PhaseLogger())

            # Trace bridge (only if trace recorder exists)
            if trace and TraceBridge:
                scheduler.extensions.register(TraceBridge(trace))
