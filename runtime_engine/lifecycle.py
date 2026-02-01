"""
Runtime Lifecycle Spine
======================

Defines canonical runtime lifecycle phases and legal transitions.

This module:
- Describes when execution is allowed to occur
- Defines legal phase transitions
- Does NOT execute runtime logic
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Dict, Any, Set


class RuntimePhase(Enum):
    CREATED = auto()
    CONFIGURED = auto()
    PRIMED = auto()
    EXECUTING = auto()
    SCORING = auto()
    FINALIZED = auto()
    ABORTED = auto()
    FAILED = auto()


# ----------------------------------------------------------------------
# Legal lifecycle transitions
# ----------------------------------------------------------------------

LEGAL_TRANSITIONS: Dict[RuntimePhase, Set[RuntimePhase]] = {
    RuntimePhase.CREATED: {RuntimePhase.CONFIGURED},
    RuntimePhase.CONFIGURED: {RuntimePhase.PRIMED},
    RuntimePhase.PRIMED: {RuntimePhase.EXECUTING},
    RuntimePhase.EXECUTING: {
        RuntimePhase.SCORING,
        RuntimePhase.ABORTED,
        RuntimePhase.FAILED,
    },
    RuntimePhase.SCORING: {
        RuntimePhase.FINALIZED,
        RuntimePhase.FAILED,
    },
    RuntimePhase.FINALIZED: set(),
    RuntimePhase.ABORTED: set(),
    RuntimePhase.FAILED: set(),
}


@dataclass(frozen=True)
class RuntimeState:
    """
    Immutable snapshot of runtime state at a lifecycle phase.
    """

    phase: RuntimePhase
    metadata: Dict[str, Any]
    message: Optional[str] = None
    error: Optional[BaseException] = None

    def is_terminal(self) -> bool:
        return self.phase in {
            RuntimePhase.FINALIZED,
            RuntimePhase.ABORTED,
            RuntimePhase.FAILED,
        }

    def can_transition_to(self, next_phase: RuntimePhase) -> bool:
        return next_phase in LEGAL_TRANSITIONS.get(self.phase, set())

    def assert_can_transition_to(self, next_phase: RuntimePhase):
        if not self.can_transition_to(next_phase):
            raise RuntimeError(
                f"Illegal lifecycle transition: "
                f"{self.phase.name} → {next_phase.name}"
            )
