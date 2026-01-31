"""
State Lenses
============

Foundational lenses that operate on runtime state.

These lenses are:
- Deterministic
- Order-dependent
- Explicit in behavior
"""

from __future__ import annotations

from typing import Any, Dict

from ..runtime_contract import Lens, RuntimeContext


# ---------------------------------------------------------------------------
# Initialize State Lens
# ---------------------------------------------------------------------------

class InitializeStateLens(Lens):
    """
    Seeds runtime state from the dream payload if applicable.
    """

    def apply(self, context: RuntimeContext) -> None:
        payload = context.dream.payload

        if isinstance(payload, dict):
            for key, value in payload.items():
                context.state.setdefault(key, value)
        else:
            context.state.setdefault("value", payload)


# ---------------------------------------------------------------------------
# Metadata Projection Lens
# ---------------------------------------------------------------------------

class ProjectMetadataLens(Lens):
    """
    Projects dream metadata into runtime state under a namespace.
    """

    def __init__(self, namespace: str = "meta"):
        self.namespace = namespace

    def apply(self, context: RuntimeContext) -> None:
        context.state[self.namespace] = dict(context.dream.metadata)


# ---------------------------------------------------------------------------
# Key Rename Lens
# ---------------------------------------------------------------------------

class RenameKeyLens(Lens):
    """
    Renames a key in runtime state.
    """

    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    def apply(self, context: RuntimeContext) -> None:
        if self.source in context.state:
            context.state[self.target] = context.state.pop(self.source)


# ---------------------------------------------------------------------------
# Constant Injection Lens
# ---------------------------------------------------------------------------

class InjectConstantLens(Lens):
    """
    Injects a constant value into runtime state.
    """

    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value

    def apply(self, context: RuntimeContext) -> None:
        context.state[self.key] = self.value


# ---------------------------------------------------------------------------
# State Filter Lens
# ---------------------------------------------------------------------------

class FilterStateLens(Lens):
    """
    Retains only specified keys in runtime state.
    """

    def __init__(self, allowed_keys: set[str]):
        self.allowed_keys = allowed_keys

    def apply(self, context: RuntimeContext) -> None:
        context.state = {
            k: v for k, v in context.state.items()
            if k in self.allowed_keys
        }
