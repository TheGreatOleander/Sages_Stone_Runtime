"""
Runtime Phases
==============

This module defines the canonical phases of a Sages Stone runtime
execution.

Important:
- This file is intentionally declarative.
- Defining a phase does NOT enforce sequencing.
- Enforcement belongs to the runtime engine and guards, not here.

This exists to:
- Make implicit structure explicit
- Provide a shared vocabulary across engine, tracing, and extensions
- Prevent phase-drift as the runtime hardens
"""

from __future__ import annotations

from enum import Enum, auto


class RuntimePhase(Enum):
    """
    Canonical execution phases of the Sages Stone Runtime.

    These phases describe *what kind of work* is occurring,
    not how it is implemented.
    """

    BOOTSTRAP = auto()
    """Runtime construction, capability checks, environment validation"""

    SEED_LOAD = auto()
    """Seed material ingestion and normalization"""

    INITIALIZE = auto()
    """Kernel, state model, and lens initialization"""

    EXECUTION = auto()
    """Bounded dream execution"""

    OBSERVATION = auto()
    """Observers, lenses, scoring, and trace capture"""

    FINALIZE = auto()
    """Result collation, invariant checks, teardown"""

    ABORTED = auto()
    """Early termination due to invariant or guard failure"""
