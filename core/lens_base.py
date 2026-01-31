# /Sages_Stone/core/lens_base.py

"""
Lens Base — The Way of Seeing
-----------------------------

A Lens is a disciplined perspective that can:

- observe state
- transform representation
- emit insight
- remain composable with other lenses

This is the pure contract beneath:
    quantum_informational_lens
    thermodynamic_lens
    category_theoretic_lens
    network_theoretic_lens
    game_theoretic_lens
"""

from typing import Any, Dict, Optional
from .kernel import Event, Kernel


class Lens:
    """
    Base class for all lenses.
    A lens does NOT own reality — it interprets it.
    """

    name: str = "abstract"

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.state: Dict[str, Any] = {}

        # Auto subscribe to dreams if desired
        self.kernel.bus.subscribe("kernel.dream", self.on_dream)

    # ------------------------------------------------------------------
    # Core protocol
    # ------------------------------------------------------------------

    def observe(self, data: Any) -> Any:
        """
        Receive raw material from the world.
        Override in subclasses.
        """
        return data

    def transform(self, observation: Any) -> Any:
        """
        Convert observation into lens-specific structure.
        Override in subclasses.
        """
        return observation

    def insight(self, transformed: Any) -> Optional[Dict[str, Any]]:
        """
        Produce meaning.
        Override in subclasses.
        """
        return None

    # ------------------------------------------------------------------
    # Runtime flow
    # ------------------------------------------------------------------

    def process(self, data: Any):
        obs = self.observe(data)
        t = self.transform(obs)
        i = self.insight(t)

        if i is not None:
            self.emit_insight(i)

        return i

    # ------------------------------------------------------------------
    # Integration surface
    # ------------------------------------------------------------------

    def emit_insight(self, insight: Dict[str, Any]):
        self.kernel.bus.emit(
            Event(
                "lens.insight",
                {
                    "lens": self.name,
                    "insight": insight,
                },
                source=self.name,
            )
        )

    # ------------------------------------------------------------------
    # Dream interface
    # ------------------------------------------------------------------

    def on_dream(self, event: Event):
        """
        Lenses may react to dreams from Pre-Sages space.
        Override selectively.
        """
        pass

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def remember(self, key: str, value: Any):
        self.state[key] = value

    def recall(self, key: str, default: Any = None):
        return self.state.get(key, default)


# ----------------------------------------------------------------------
# Composite Lens
# ----------------------------------------------------------------------

class CompositeLens(Lens):
    """
    A lens made of lenses.
    """

    name = "composite"

    def __init__(self, kernel: Kernel):
        super().__init__(kernel)
        self.children: list[Lens] = []

    def add(self, lens: Lens):
        self.children.append(lens)

    def process(self, data: Any):
        results = {}
        for child in self.children:
            r = child.process(data)
            if r is not None:
                results[child.name] = r
        return results

