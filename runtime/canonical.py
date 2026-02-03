"""
Canonical Runtime Spine Declaration

This module declares — without ambiguity — the single,
blessed execution flow of Sages Stone Runtime.

No logic is invented here.
No policy is defined here.
No execution is performed here.

This file exists so the runtime may point to itself and say:
"this is how execution proceeds."
"""

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class CanonicalSpine:
    """
    Immutable declaration of the runtime execution order.
    """

    guard: Callable
    runner: Callable
    emitter: Callable


def declare_spine(guard, runner, emitter) -> CanonicalSpine:
    """
    Declare the canonical runtime spine.

    This function does not validate behavior.
    It merely binds roles into law.
    """
    return CanonicalSpine(
        guard=guard,
        runner=runner,
        emitter=emitter,
    )
