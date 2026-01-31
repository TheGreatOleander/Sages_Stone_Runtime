"""
evolution.py
------------

Evolutionary execution loop for Sages Stone Runtime.

This module ties together:
- Runtime
- Dreaming
- Scoring

It enables adaptive, goal-seeking behavior without
embedding any domain semantics.
"""

from typing import Callable, List, Optional

from Sages_Stone_Runtime.runtime import SagesStoneRuntime
from Sages_Stone_Runtime.dream import DreamEngine, DreamResult
from Sages_Stone_Runtime.scoring import DreamScorer, ScoredDream


class EvolutionResult:
    """
    Represents the outcome of an evolutionary run.
    """

    def __init__(self, generations: int, best_dreams: List[ScoredDream]):
        self.generations = generations
        self.best_dreams = best_dreams

    def __repr__(self):
        return (
            f"<EvolutionResult generations={self.generations} "
            f"best={len(self.best_dreams)}>"
        )


class EvolutionEngine:
    """
    High-level evolutionary controller.

    Pattern:
        dream → score → select → mutate → repeat
    """

    def __init__(
        self,
        runtime: SagesStoneRuntime,
        scorer: DreamScorer,
    ):
        self.runtime = runtime
        self.scorer = scorer
        self.dream_engine = DreamEngine(runtime)

    # -------------------------
    # Evolution
    # -------------------------

    def evolve(
        self,
        generations: int,
        dreams_per_generation: int,
        steps_per_dream: int,
        selector: Optional[Callable[[List[ScoredDream]], List[ScoredDream]]] = None,
        mutator: Optional[Callable[[SagesStoneRuntime, ScoredDream], None]] = None,
    ) -> EvolutionResult:
        """
        Execute an evolutionary process.

        Parameters:
        - generations: number of evolution cycles
        - dreams_p_
