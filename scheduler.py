"""
scheduler.py
------------

Runtime scheduler for Sages Stone.

This module is responsible for orchestrating execution over the
Sages_Stone core without redefining its physics.

Core philosophy:
- Sages_Stone defines *what is possible*
- Runtime defines *when and how it unfolds*
"""

from typing import List, Optional
import time

from Sages_Stone.state import State
from Sages_Stone.constraint import Constraint
from Sages_Stone.laws import Law
from Sages_Stone.lens import Lens


class RuntimeStep:
    """
    Represents a single executed step in runtime.
    Stored for replay, scoring, or dream-branching.
    """

    def __init__(self, index: int):
        self.index = index
        self.timestamp = time.time()

    def __repr__(self):
        return f"<RuntimeStep {self.index}>"


class RuntimeScheduler:
    """
    Central runtime orchestrator.

    This does NOT mutate core class definitions.
    It simply coordinates them.
    """

    def __init__(
        self,
        initial_state: State,
        laws: Optional[List[Law]] = None,
        constraints: Optional[List[Constraint]] = None,
        lenses: Optional[List[Lens]] = None,
    ):
        self.state = initial_state

        self.laws: List[Law] = laws or []
        self.constraints: List[Constraint] = constraints or []
        self.lenses: List[Lens] = lenses or []

        self.step_index = 0
        self.history: List[RuntimeStep] = []
        self.running = False

    # -------------------------
    # Registration
    # -------------------------

    def add_law(self, law: Law):
        self.laws.append(law)

    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    def add_lens(self, lens: Lens):
        self.lenses.append(lens)

    # -------------------------
    # Execution
    # -------------------------

    def step(self) -> RuntimeStep:
        """
        Execute a single runtime step.
        """
        step = RuntimeStep(self.step_index)

        # 1. Enforce laws (hard invariants)
        for law in self.laws:
            law.apply(self.state)

        # 2. Apply constraints (soft / competing forces)
        for constraint in self.constraints:
            constraint.apply(self.state)

        # 3. Observe / transform via lenses
        for lens in self.lenses:
            lens.observe(self.state)

        self.history.append(step)
        self.step_index += 1
        return step

    def run(self, steps: Optional[int] = None):
        """
        Run the scheduler.

        If steps is None, runs indefinitely.
        """
        self.running = True

        while self.running:
            self.step()

            if steps is not None and self.step_index >= steps:
                break

    def stop(self):
        self.running = False

    # -------------------------
    # Introspection
    # -------------------------

    def snapshot(self) -> dict:
        """
        Lightweight snapshot of runtime state.
        Deep cloning is intentionally external.
        """
        return {
            "step_index": self.step_index,
            "history_length": len(self.history),
            "state": self.state,
        }
