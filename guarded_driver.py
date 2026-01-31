"""
guarded_driver.py

Guarded Runtime Driver
----------------------
Wraps RuntimeDriver with collapse arbitration.

Flow:
BoundIntent
    ↓
CollapseOracle
    ↓ (allowed?)
RuntimeDriver
    ↓
RuntimeResult OR explicit failure

No engine rewrites.
No silent collapse.
"""

from typing import Optional

from .lens_binding import BoundIntent
from .collapse_oracle import CollapseOracle, CollapseResult
from .runtime_driver import RuntimeDriver
from .runtime_result import RuntimeResult


# ---------------------------------------------------------------------------
# Guarded Driver
# ---------------------------------------------------------------------------

class GuardedRuntimeDriver:
    """
    Runtime driver with explicit collapse arbitration.

    If collapse fails, execution does not occur.
    """

    def __init__(
        self,
        *,
        strict: bool = True,
        driver: Optional[RuntimeDriver] = None,
    ):
        self.oracle = CollapseOracle(strict=strict)
        self.driver = driver or RuntimeDriver()

    # ------------------------------------------------------------------

    def run(self, bound: BoundIntent) -> RuntimeResult:
        """
        Run a BoundIntent through collapse arbitration,
        then execute if allowed.
        """

        collapse_result: CollapseResult = self.oracle.evaluate(bound)

        if not collapse_result.allowed:
            # Explicit, truthful failure
            return RuntimeResult(
                intent_id=bound.intent.intent_id,
                success=False,
                steps=0,
                duration=0.0,
                output={
                    "error": "collapse",
                    "reason": collapse_result.reason,
                },
                score=0.0,
            )

        # Re-bind intent with resolved lenses if soft resolution occurred
        if collapse_result.resolved_lenses is not bound.lens_results:
            bound = BoundIntent(
                intent=bound.intent,
                lens_results=collapse_result.resolved_lenses,
            )

        return self.driver.run(bound)


# ---------------------------------------------------------------------------
# Convenience helper
# ---------------------------------------------------------------------------

def run_guarded(bound: BoundIntent, strict: bool = True) -> RuntimeResult:
    """
    Stateless guarded execution.
    """
    driver = GuardedRuntimeDriver(strict=strict)
    return driver.run(bound)
