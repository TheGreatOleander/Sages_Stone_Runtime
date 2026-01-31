"""
runtime.py
----------

Primary entrypoint for executing Sages Stone as a runtime system.

This module binds:
- Core (Sages_Stone)
- Runtime orchestration (scheduler)

Nothing here defines physics.
It only decides *how the stone is allowed to run*.
"""

from typing import Optional

from Sages_Stone.state import State
from Sages_Stone.constraint import Constraint
from Sages_Stone.laws import Law
from Sages_Stone.lens import Lens

from Sages_Stone_Runtime.scheduler import RuntimeScheduler


class SagesStoneRuntime:
    """
    High-level runtime wrapper.

    This is the object external systems interact with.
    """

    def __init__(self, initial_state: State):
        self.scheduler = RuntimeScheduler(initial_state)

    # -------------------------
    # Registration passthrough
    # -------------------------

    def add_law(self, law: Law):
        self.scheduler.add_law(law)

    def add_constraint(self, constraint: Constraint):
        self.scheduler.add_constraint(constraint)

    def add_lens(self, lens: Lens):
        self.scheduler.add_lens(lens)

    # -------------------------
    # Execution
    # -------------------------

    def step(self):
        return self.scheduler.step()

    def run(self, steps: Optional[int] = None):
        return self.scheduler.run(steps)

    def stop(self):
        self.scheduler.stop()

    # -------------------------
    # Introspection
    # -------------------------

    @property
    def state(self) -> State:
        return self.scheduler.state

    def snapshot(self) -> dict:
        return self.scheduler.snapshot()
