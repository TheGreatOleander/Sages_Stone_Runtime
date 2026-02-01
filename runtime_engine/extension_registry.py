# --- existing imports ---
from typing import Callable, Dict, List, Any
from dataclasses import dataclass, field
import traceback

# NEW: contract guard
try:
    from .extension_contract_guard import (
        ExtensionContractGuard,
        ExtensionCapabilities,
        ExtensionContractViolation,
    )
except Exception:
    ExtensionContractGuard = None
    ExtensionCapabilities = None
    ExtensionContractViolation = RuntimeError


@dataclass(frozen=True)
class ExtensionContext:
    phase: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class RuntimeExtension:
    """
    Base class for runtime extensions.

    Subclasses may optionally declare capabilities by overriding
    `capabilities()`.
    """

    name: str = "unnamed_extension"

    def capabilities(self):
        return None  # observer-only by default

    def on_phase_enter(self, context: ExtensionContext) -> None:
        pass

    def on_phase_exit(self, context: ExtensionContext) -> None:
        pass

    def on_runtime_error(self, context: ExtensionContext, error: Exception) -> None:
        pass


class ExtensionRegistry:
    """
    Central registry for runtime extensions with contract enforcement.
    """

    def __init__(self) -> None:
        self._extensions: List[RuntimeExtension] = []

        # NEW: contract guard (optional but preferred)
        self._guard = ExtensionContractGuard() if ExtensionContractGuard else None

    def register(self, extension: RuntimeExtension) -> None:
        # NEW: capability declaration (if provided)
        if self._guard:
            caps = extension.capabilities()
            if caps is not None:
                self._guard.declare_capabilities(extension.name, caps)

            # Enforce observer-only by default
            try:
                self._guard.assert_observer_only(extension.name)
            except ExtensionContractViolation:
                raise

        self._extensions.append(extension)

    def notify_phase_enter(self, phase: str, metadata: Dict[str, Any] | None = None) -> None:
        ctx = ExtensionContext(phase=phase, metadata=metadata or {})
        for ext in self._extensions:
            try:
                ext.on_phase_enter(ctx)
            except Exception:
                traceback.print_exc()

    def notify_phase_exit(self, phase: str, metadata: Dict[str, Any] | None = None) -> None:
        ctx = ExtensionContext(phase=phase, metadata=metadata or {})
        for ext in self._extensions:
            try:
                ext.on_phase_exit(ctx)
            except Exception:
                traceback.print_exc()

    def notify_runtime_error(self, phase: str, error: Exception) -> None:
        ctx = ExtensionContext(phase=phase)
        for ext in self._extensions:
            try:
                ext.on_runtime_error(ctx, error)
            except Exception:
                traceback.print_exc()
