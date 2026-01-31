"""
Reference Runtime Engine for Sages Stone
=======================================

This module provides a strict, transparent implementation of the
RuntimeEngine contract.

It favors correctness and observability over performance or cleverness.
"""

from __future__ import annotations

from typing import Iterable

from .runtime_contract import (
    RuntimeEngine,
    RuntimeContext,
    RuntimePhase,
    Dream,
    Lens,
    Constraint,
    Observer,
    RuntimeResult,
)


class ReferenceRuntimeEngine(RuntimeEngine):
    """
    Canonical runtime execution engine.

    This engine:
    - Executes lenses in order
    - Checks constraints before each phase
    - Records every transition
    - Never swallows violations
    """

    def run(
        self,
        dream: Dream,
        lenses: Iterable[Lens],
        constraints: Iterable[Constraint],
        observers: Iterable[Observer],
    ) -> RuntimeResult:

        context = RuntimeContext(dream=dream)
        context.trace.append("Runtime initialized")

        def enforce_constraints() -> bool:
            for constraint in constraints:
                violation = constraint.check(context)
                if violation:
                    context.violations.append(violation)
            return len(context.violations) == 0

        # INGEST → SANITIZE
        context.advance(RuntimePhase.SANITIZE)
        if not enforce_constraints():
            return self._abort(context)

        # SANITIZE → EXECUTE
        context.advance(RuntimePhase.EXECUTE)
        if not enforce_constraints():
            return self._abort(context)

        # EXECUTE lenses
        for idx, lens in enumerate(lenses):
            context.trace.append(f"Applying lens {idx}: {lens.__class__.__name__}")
            lens.apply(context)

            if not enforce_constraints():
                return self._abort(context)

        # EXECUTE → COLLAPSE
        context.advance(RuntimePhase.COLLAPSE)
        if not enforce_constraints():
            return self._abort(context)

        # COLLAPSE → OBSERVE
        context.advance(RuntimePhase.OBSERVE)
        for observer in observers:
            observer.observe(context)

        # OBSERVE → COMPLETE
        context.advance(RuntimePhase.COMPLETE)

        return RuntimeResult(
            success=True,
            final_state=dict(context.state),
            violations=tuple(context.violations),
            trace=tuple(context.trace),
        )

    # ------------------------------------------------------------------

    def _abort(self, context: RuntimeContext) -> RuntimeResult:
        """
        Abort execution due to constraint violation.
        """
        context.trace.append("Execution aborted due to constraint violation")
        return RuntimeResult(
            success=False,
            final_state=dict(context.state),
            violations=tuple(context.violations),
            trace=tuple(context.trace),
        )
