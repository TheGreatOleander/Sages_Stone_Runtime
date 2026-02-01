"""
Extension Contract Guard
========================

This module enforces runtime invariants on extensions.

Purpose:
- Ensure extensions are OBSERVERS unless explicitly allowed
- Prevent state mutation, timing interference, or contract bypass
- Provide a single choke-point for extension trust elevation

This guard is intentionally conservative.
"""

from typing import Set
from dataclasses import dataclass


@dataclass(frozen=True)
class ExtensionCapabilities:
    """
    Declares what an extension is allowed to do.

    Default = observer-only.
    """
    allow_state_read: bool = True
    allow_state_write: bool = False
    allow_timing_access: bool = False
    allow_error_suppression: bool = False


class ExtensionContractViolation(RuntimeError):
    pass


class ExtensionContractGuard:
    """
    Enforces declared capabilities for runtime extensions.
    """

    def __init__(self) -> None:
        self._capabilities: dict[str, ExtensionCapabilities] = {}

    def declare_capabilities(
        self,
        extension_name: str,
        capabilities: ExtensionCapabilities,
    ) -> None:
        self._capabilities[extension_name] = capabilities

    def capabilities_for(self, extension_name: str) -> ExtensionCapabilities:
        return self._capabilities.get(
            extension_name,
            ExtensionCapabilities()
        )

    def assert_observer_only(self, extension_name: str) -> None:
        caps = self.capabilities_for(extension_name)
        if caps.allow_state_write or caps.allow_error_suppression:
            raise ExtensionContractViolation(
                f"Extension '{extension_name}' exceeds observer-only contract"
            )
