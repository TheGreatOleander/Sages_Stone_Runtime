# /Sages_Stone/core/thermodynamic_lens.py

"""
Thermodynamic Lens — Change as Energy
-------------------------------------

Interprets events as if they were:

- energy reservoirs
- gradients
- dissipation flows
- equilibrium seeking

Metaphor executed as math.
"""

from typing import Any, Dict

from .kernel import Kernel
from .lens_base import Lens


class ThermodynamicLens(Lens):

    name = "thermodynamic"

    # ------------------------------------------------------------------
    # Observation
    # ------------------------------------------------------------------

    def observe(self, data: Any) -> Dict[str, Any]:
        """
        Convert arbitrary input into numeric potentials.
        """

        # Try to extract numeric content
        if isinstance(data, (int, float)):
            magnitude = float(data)

        elif isinstance(data, dict):
            # energy as size of structure
            magnitude = float(len(data))

        elif isinstance(data, (list, tuple, set)):
            magnitude = float(len(data))

        else:
            # fallback: length of representation
            magnitude = float(len(str(data)))

        return {
            "magnitude": magnitude,
            "raw": data,
        }

    # ------------------------------------------------------------------
    # Transformation
    # ------------------------------------------------------------------

    def transform(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        m = observation["magnitude"]

        # simple pseudo-thermo metrics
        potential = m
        gradient = m / (1.0 + m)
        dissipation = 1.0 - gradient

        return {
            "potential": round(potential, 5),
            "gradient": round(gradient, 5),
            "dissipation": round(dissipation, 5),
        }

    # ------------------------------------------------------------------
    # Insight
    # ------------------------------------------------------------------

    def insight(self, transformed: Dict[str, Any]):
        g = transformed["gradient"]
        d = transformed["dissipation"]
        p = transformed["potential"]

        claims = []

        if g > 0.8:
            claims.append("high_gradient")
        elif g < 0.2:
            claims.append("near_equilibrium")
        else:
            claims.append("moderate_flow")

        if d > 0.7:
            claims.append("strong_damping")

        if p > 100:
            claims.append("large_reservoir")
        elif p < 5:
            claims.append("micro_state")

        return {
            "metrics": transformed,
            "claims": claims,
        }

    # ------------------------------------------------------------------
    # Dreams
    # ------------------------------------------------------------------

    def on_dream(self, event):
        """
        Dreams carry energetic weight.
        """

        data = event.payload.get("data")
        intent = event.payload.get("intent")

        result = self.process({
            "intent": intent,
            "data": data,
        })

        # remember last energetic signature
        self.remember("last_energy", result)


# ----------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------

def attach_thermodynamic_lens(kernel: Kernel) -> ThermodynamicLens:
    lens = ThermodynamicLens(kernel)
    kernel.register("lens.thermodynamic", lens)
    return lens


if __name__ == "__main__":
    from .kernel import boot_default
    from .rcf_bridge import attach_rcf
    from .coherence_observer import attach_coherence_observer

    k = boot_default()
    attach_rcf(k)
    attach_coherence_observer(k)

    lens = attach_thermodynamic_lens(k)

    k.bus.subscribe_all(lambda e: print("EVENT:", e))

    lens.process([1, 2, 3, 4, 5])

    k.dream("heat_test", {"value": 12})

