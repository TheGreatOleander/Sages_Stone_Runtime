# /Sages_Stone/core/rcf_bridge.py

"""
RCF Bridge — Law Made Operational
---------------------------------

This is NOT the full RCF theory.
This is the runtime membrane where:

    ideas → constraints → actions

Lenses propose.
Observers warn.
RCF decides what is allowed to persist.
"""

from typing import Any, Dict, List, Callable
from .kernel import Event, Kernel


class RCFLaw:
    """
    Minimal executable representation of an RCF law.
    """

    def __init__(self, name: str, rule: Callable[[Any], bool], weight: float = 1.0):
        self.name = name
        self.rule = rule
        self.weight = weight

    def evaluate(self, data: Any) -> bool:
        try:
            return bool(self.rule(data))
        except Exception:
            return False


class RCFBridge:
    """
    Runtime gateway for constraint reasoning.
    """

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.laws: Dict[str, RCFLaw] = {}

        # Listen to everything that claims to be insight
        self.kernel.bus.subscribe("lens.insight", self._on_insight)

    # ------------------------------------------------------------------
    # Law management
    # ------------------------------------------------------------------

    def register_law(self, law: RCFLaw):
        self.laws[law.name] = law

        self.kernel.bus.emit(
            Event(
                "rcf.law.registered",
                {"law": law.name, "weight": law.weight},
                source="rcf_bridge",
            )
        )

    def remove_law(self, name: str):
        if name in self.laws:
            del self.laws[name]

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def evaluate(self, data: Any) -> Dict[str, bool]:
        results = {}
        for name, law in self.laws.items():
            results[name] = law.evaluate(data)
        return results

    def score(self, data: Any) -> float:
        """
        Weighted coherence score 0..1
        """
        if not self.laws:
            return 1.0

        total = 0.0
        possible = 0.0

        for law in self.laws.values():
            possible += law.weight
            if law.evaluate(data):
                total += law.weight

        return total / possible if possible else 1.0

    # ------------------------------------------------------------------
    # Event reactions
    # ------------------------------------------------------------------

    def _on_insight(self, event: Event):
        payload = event.payload
        insight = payload.get("insight")

        result = self.evaluate(insight)
        score = self.score(insight)

        self.kernel.bus.emit(
            Event(
                "rcf.evaluated",
                {
                    "lens": payload.get("lens"),
                    "result": result,
                    "score": score,
                    "insight": insight,
                },
                source="rcf_bridge",
            )
        )

        # If reality violates too much — observers should know
        if score < 0.5:
            self.kernel.bus.emit(
                Event(
                    "rcf.violation",
                    {
                        "lens": payload.get("lens"),
                        "score": score,
                        "insight": insight,
                    },
                    source="rcf_bridge",
                )
            )


# ----------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------

def attach_rcf(kernel: Kernel) -> RCFBridge:
    bridge = RCFBridge(kernel)
    kernel.register("rcf", bridge)
    return bridge


if __name__ == "__main__":
    from .kernel import boot_default

    k = boot_default()
    r = attach_rcf(k)

    # Example law
    r.register_law(
        RCFLaw("no_void", lambda d: d is not None)
    )

    k.bus.subscribe_all(lambda e: print("EVENT:", e))

    k.bus.emit(
        Event("lens.insight", {"lens": "demo", "insight": {"x": 1}})
    )

