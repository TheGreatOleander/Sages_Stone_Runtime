"""
dream.py
--------

Dream / speculative execution layer for Sages Stone Runtime.

A Dream is a forked runtime that:
- Starts from a snapshot of reality
- Evolves independently
- Can be scored, compared, or discarded

This file intentionally avoids deep cloning policy.
That responsibility belongs to the caller.
"""

from typing import List, Callable, Any
import copy

from Sages_Stone_Runtime.runtime import SagesStoneRuntime
from Sages_Stone.state import State


class DreamResult:
    """
    Represents the outcome of a dream execution.
    """

    def __init__(self, final_state: State, steps: int, metadata: dict = None):
        self.final_state = final_state
        self.steps = steps
        self.metadata = metadata or {}

    def __repr__(self):
        return f"<DreamResult steps={self.steps}>"


class DreamEngine:
    """
    Executes speculative futures based on an existing runtime.
    """

    def __init__(self, runtime: SagesStoneRuntime):
        self.runtime = runtime

    # -------------------------
    # Dreaming
    # -------------------------

    def fork_state(self) -> State:
        """
        Fork the current runtime state.

        Uses deepcopy by default for safety.
        Advanced users may override this behavior.
        """
        return copy.deepcopy(self.runtime.state)

    def dream(
        self,
        steps: int,
        mutator: Callable[[SagesStoneRuntime], Any] = None,
        metadata: dict = None,
    ) -> DreamResult:
        """
        Execute a speculative future.

        Parameters:
        - steps: number of runtime steps to simulate
        - mutator: optional function to modify the dream runtime before execution
        - metadata: optional annotation for scoring / labeling
        """

        # 1. Fork state
        dream_state = self.fork_state()

        # 2. Create isolated runtime
        dream_runtime = SagesStoneRuntime(dream_state)

        # 3. Mirror scheduler configuration
        scheduler = self.runtime.scheduler
        dream_scheduler = dream_runtime.scheduler

        dream_scheduler.laws = list(scheduler.laws)
        dream_scheduler.constraints = list(scheduler.constraints)
        dream_scheduler.lenses = list(scheduler.lenses)

        # 4. Apply mutation (optional)
        if mutator is not None:
            mutator(dream_runtime)

        # 5. Run dream
        dream_runtime.run(steps)

        return DreamResult(
            final_state=dream_runtime.state,
            steps=steps,
            metadata=metadata,
        )

    def batch_dream(
        self,
        count: int,
        steps: int,
        mutators: List[Callable[[SagesStoneRuntime], Any]] = None,
    ) -> List[DreamResult]:
        """
        Execute multiple speculative futures.
        """
        results = []
        mutators = mutators or [None] * count

        for i in range(count):
            result = self.dream(
                steps=steps,
                mutator=mutators[i] if i < len(mutators) else None,
                metadata={"index": i},
            )
            results.append(result)

        return results
