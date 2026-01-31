# /Sages_Stone/core/information_lens.py

"""
Information Lens — Meaning as Structure
--------------------------------------

Sees the world through:

- entropy
- novelty
- compressibility
- pattern density

Not physics.
Not mysticism.

Information geometry.
"""

import math
from typing import Any, Dict

from .kernel import Kernel
from .lens_base import Lens


class InformationLens(Lens):

    name = "information"

    # ------------------------------------------------------------------
    # Observation
    # ------------------------------------------------------------------

    def observe(self, data: Any) -> Any:
        """
        Normalize incoming material into something
        information-theoretic can digest.
        """

        # primitive normalization
        if isinstance(data, (str, bytes)):
            return data

        try:
            return str(data)
        except Exception:
            return repr(data)

    # ------------------------------------------------------------------
    # Transformation
    # ------------------------------------------------------------------

    def transform(self, observation: Any) -> Dict[str, Any]:
        text = observation

        length = len(text)

        # naive symbol histogram
        hist: Dict[str, int] = {}
        for ch in text:
            hist[ch] = hist.get(ch, 0) + 1

        # entropy estimate
        entropy = 0.0
        for c in hist.values():
            p = c / length
            entropy -= p * math.log2(p)

        # very rough compressibility proxy
        unique = len(hist)
        redundancy = 1.0 - (unique / max(1, length))

        return {
            "length": length,
            "unique_symbols": unique,
            "entropy": round(entropy, 5),
            "redundancy": round(redundancy, 5),
            "histogram": hist,
        }

    # ------------------------------------------------------------------
    # Insight
    # ------------------------------------------------------------------

    def insight(self, transformed: Dict[str, Any]):
        """
        Convert raw metrics into meaning claims.
        """

        e = transformed["entropy"]
        r = transformed["redundancy"]
        l = transformed["length"]

        claims = []

        if e < 1.0:
            claims.append("high_order")
        elif e > 4.0:
            claims.append("high_chaos")
        else:
            claims.append("mid_complexity")

        if r > 0.6:
            claims.append("highly_compressible")

        if l < 10:
            claims.append("tiny_signal")
        elif l > 500:
            claims.append("massive_signal")

        return {
            "metrics": transformed,
            "claims": claims,
        }

    # ------------------------------------------------------------------
    # Dreams
    # ------------------------------------------------------------------

    def on_dream(self, event):
        """
        Dreams become information to analyze.
        """

        data = event.payload.get("data")
        intent = event.payload.get("intent")

        result = self.process({
            "intent": intent,
            "data": data,
        })

        # remember last dream shape
        self.remember("last_dream", result)


# ----------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------

def attach_information_lens(kernel: Kernel) -> InformationLens:
    lens = InformationLens(kernel)
    kernel.register("lens.information", lens)
    return lens


if __name__ == "__main__":
    from .kernel import boot_default
    from .rcf_bridge import attach_rcf
    from .coherence_observer import attach_coherence_observer

    k = boot_default()
    attach_rcf(k)
    attach_coherence_observer(k)

    lens = attach_information_lens(k)

    k.bus.subscribe_all(lambda e: print("EVENT:", e))

    lens.process("hello hello hello structured world")

    k.dream("ponder", {"msg": "is this meaningful?"})

