"""
lens_binding.py

Lens Binding Layer
------------------
Binds an immutable DreamIntent to one or more Core lenses
WITHOUT mutating the intent or the lenses.

This is the point where meaning is introduced,
but execution has not yet begun.

Design goals:
- No side effects
- No mutation
- Explicit contracts
- Runtime-visible structure
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol

from .dream_adapter import DreamIntent


# ---------------------------------------------------------------------------
# Lens Protocol (runtime-facing)
# ---------------------------------------------------------------------------

class RuntimeLens(Protocol):
    """
    Minimal runtime-facing lens contract.

    Core lenses may do more.
    Runtime only cares about this surface.
    """

    name: str

    def apply(self, intent: DreamIntent) -> Dict[str, Any]:
        """
        Apply lens semantics to a DreamIntent.

        Must NOT mutate intent.
        Must return structured data.
        """
        ...


# ---------------------------------------------------------------------------
# Bound Result
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BoundIntent:
    """
    DreamIntent + lens-derived semantic overlays.

    This is what the runtime engine consumes next.
    """
    intent: DreamIntent
    lens_results: Dict[str, Dict[str, Any]]


# ---------------------------------------------------------------------------
# Binder
# ---------------------------------------------------------------------------

class LensBinder:
    """
    Applies lenses to a DreamIntent in a controlled, ordered way.
    """

    def __init__(self, lenses: List[RuntimeLens]):
        self.lenses = lenses

    def bind(self, intent: DreamIntent) -> BoundIntent:
        results: Dict[str, Dict[str, Any]] = {}

        for lens in self.lenses:
            if lens.name in results:
                raise ValueError(f"Duplicate lens name: {lens.name}")

            output = lens.apply(intent)

            if not isinstance(output, dict):
                raise TypeError(
                    f"Lens '{lens.name}' must return a dict, got {type(output)}"
                )

            results[lens.name] = output

        return BoundIntent(
            intent=intent,
            lens_results=results,
        )


# ---------------------------------------------------------------------------
# Convenience helper
# ---------------------------------------------------------------------------

def bind_intent(
    intent: DreamIntent,
    lenses: List[RuntimeLens],
) -> BoundIntent:
    """
    Stateless helper for one-off binding.
    """
    binder = LensBinder(lenses)
    return binder.bind(intent)
