"""
Canonical Runtime Bindings

This module binds concrete runtime implementations
to the declared canonical spine.

No execution occurs here.
No logic is defined here.
This is pure alignment.
"""

from sages_stone_runtime.runtime.canonical import declare_spine

# Import concrete implementations
from sages_stone_runtime.runtime.guard import guard_system
from sages_stone_runtime.runtime.runner import run_system
from sages_stone_runtime.runtime.result import emit_result


# The One True Runtime Spine
CANONICAL_SPINE = declare_spine(
    guard=guard_system,
    runner=run_system,
    emitter=emit_result,
)
