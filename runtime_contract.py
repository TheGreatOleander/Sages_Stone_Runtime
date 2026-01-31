"""
Sages Stone Runtime Contract
============================

This module defines the canonical runtime interfaces for executing
Sages Stone systems.

Nothing in this file performs execution.
Everything in this file defines *what execution means*.

If the Stone is philosophy,
this file is law.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional, Protocol
from enum import Enum, auto


# ---------------------------------------------------------------------------
# Runtime Phases
# ---------------------------------------------------------------------------

class RuntimePhase(Enum):
    """
    Distinct phases of a Stone execution lifecycle.
    These are observable, enforceable, and traceable.
    """
    INGEST = auto()      # Dream enters the system
    SANITIZE = auto()    # Input normalization / validation
    EXECUTE = auto()     # Lens traversal and transformation
    COLLAPSE = auto()    # Resolution into outcome
    OBSERVE = auto()     # Trace, metrics, explanation
    COMPLETE = auto()    # Terminal state


# ---------------------------------------------------------------------------
# Dream (Input)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Dream:
    """
    A Dream is a proposed state, question, or scenario.

    It is intentionally permissive.
    Meaning is imposed by lenses, not by the dream itself.
    """
    payload: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Runtime Context
# ---------------------------------------------------------------------------

@dataclass
class RuntimeContext:
    """
    Mutable execution context shared across the runtime.

    This is the ONLY mutable structure allowed to persist
    through runtime phases.
    """
    dream: Dream
    phase: RuntimePhase = RuntimePhase.INGEST
    state: Dict[str, Any] = field(default_factory=dict)
    violations: list[str] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)

    def advance(self, phase: RuntimePhase) -> None:
        self.phase = phase
        self.trace.append(f"→ {phase.name}")


# ---------------------------------------------------------------------------
# Lens Interface
# ---------------------------------------------------------------------------

class Lens(Protocol):
    """
    A Lens transforms runtime context.

    Lenses must:
    - Be deterministic
    - Respect constraints
    - Mutate ONLY via RuntimeContext
    """

    def apply(self, context: RuntimeContext) -> None:
        ...


# ---------------------------------------------------------------------------
# Constraints
# ---------------------------------------------------------------------------

class Constraint(ABC):
    """
    A Constraint guards execution.

    Constraints do not modify state.
    They only approve or reject progression.
    """

    @abstractmethod
    def check(self, context: RuntimeContext) -> Optional[str]:
        """
        Return None if allowed.
        Return a string describing the violation if not.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Observer
# ---------------------------------------------------------------------------

class Observer(ABC):
    """
    Observers witness execution without influencing it.
    """

    @abstractmethod
    def observe(self, context: RuntimeContext) -> None:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Execution Result
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RuntimeResult:
    """
    The terminal artifact of a Stone execution.
    """
    success: bool
    final_state: Dict[str, Any]
    violations: Iterable[str]
    trace: Iterable[str]


# ---------------------------------------------------------------------------
# Runtime Engine
# ---------------------------------------------------------------------------

class RuntimeEngine(ABC):
    """
    The Runtime Engine is the sole authority allowed
    to execute Sages Stone systems.
    """

    @abstractmethod
    def run(
        self,
        dream: Dream,
        lenses: Iterable[Lens],
        constraints: Iterable[Constraint],
        observers: Iterable[Observer],
    ) -> RuntimeResult:
        """
        Execute a dream through lenses under constraints
        while being observed.
        """
        raise NotImplementedError
