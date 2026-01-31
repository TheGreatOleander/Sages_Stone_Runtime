"""
runtime_driver.py

Runtime Driver
--------------
Connects BoundIntent -> runtime_engine -> scoring
WITHOUT altering existing engine semantics.

This is the execution spine:
DreamIntent -> lenses -> bounded execution -> scored result

Design goals:
- Zero mutation of intent or lens output
- Explicit handoff points
- One-way data flow
"""

from typing import Any, Dict, Optional

from .dream_adapter import DreamIntent
from .lens_binding import BoundIntent
from .runtime_engine import RuntimeEngine
from .runtime_result import RuntimeResult
from .scoring import score_execution


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

class RuntimeDriver:
    """
    High-level runtime orchestrator.

    This is the ONLY place where:
    - lenses
    - engine
    - scoring
    are aware of each other.
    """

    def __init__(self, engine: Optional[RuntimeEngine] = None):
        self.engine = engine or RuntimeEngine()

    # ------------------------------------------------------------------

    def run(self, bound: BoundIntent) -> RuntimeResult:
        """
        Execute a BoundIntent through the runtime engine
        and return a scored RuntimeResult.
        """

        intent = bound.intent

        # Enforce limits at the boundary
        limits = intent.limits

        # Combine execution payload
        execution_context = {
            "intent_id": intent.intent_id,
            "description": intent.description,
            "payload": intent.payload,
            "lenses": bound.lens_results,
        }

        # Execute
        execution_trace = self.engine.execute(
            context=execution_context,
            max_steps=limits.get("max_steps"),
            max_seconds=limits.get("max_seconds"),
        )

        # Score
        score = score_execution(
            execution_trace=execution_trace,
            lens_results=bound.lens_results,
            limits=limits,
        )

        # Return structured result
        return RuntimeResult(
            intent_id=intent.intent_id,
            success=execution_trace.success,
            steps=execution_trace.steps,
            duration=execution_trace.duration,
            output=execution_trace.output,
            score=score,
        )


# ---------------------------------------------------------------------------
# Convenience helper
# ---------------------------------------------------------------------------

def run_bound_intent(bound: BoundIntent) -> RuntimeResult:
    """
    Stateless helper for one-shot execution.
    """
    driver = RuntimeDriver()
    return driver.run(bound)
