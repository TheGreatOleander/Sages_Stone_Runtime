"""
scoring.py
----------

Dream outcome scoring and evaluation for Sages Stone Runtime.

This module defines a neutral framework for evaluating speculative
futures without embedding domain assumptions.

Scorers answer one question:
    "How well did this dream survive?"
"""

from typing import Callable, List, Dict, Any

from Sages_Stone_Runtime.dream import DreamResult
from Sages_Stone.state import State


class Score:
    """
    Represents a scored dream outcome.
    """

    def __init__(self, value: float, components: Dict[str, float] = None):
        self.value = float(value)
        self.components = components or {}

    def __repr__(self):
        return f"<Score {self.value:.4f}>"


class ScoredDream:
    """
    Wraps a DreamResult with an evaluation score.
    """

    def __init__(self, result: DreamResult, score: Score):
        self.result = result
        self.score = score

    def __repr__(self):
        return f"<ScoredDream score={self.score.value:.4f}>"


class DreamScorer:
    """
    Aggregates scoring functions and applies them to dreams.

    A scorer function has signature:
        fn(state: State) -> float
    """

    def __init__(self):
        self.scorers: Dict[str, Callable[[State], float]] = {}

    # -------------------------
    # Registration
    # -------------------------

    def add_scorer(self, name: str, fn: Callable[[State], float]):
        self.scorers[name] = fn

    # -------------------------
    # Evaluation
    # -------------------------

    def score(self, dream: DreamResult) -> ScoredDream:
        """
        Score a single dream result.
        """
        components = {}
        total = 0.0

        for name, fn in self.scorers.items():
            try:
                value = float(fn(dream.final_state))
            except Exception:
                value = float("-inf")

            components[name] = value
            total += value

        score = Score(total, components)
        return ScoredDream(dream, score)

    def score_many(self, dreams: List[DreamResult]) -> List[ScoredDream]:
        """
        Score multiple dreams.
        """
        return [self.score(dream) for dream in dreams]

    # -------------------------
    # Selection
    # -------------------------

    def select_best(
        self,
        scored_dreams: List[ScoredDream],
        top_k: int = 1,
    ) -> List[ScoredDream]:
        """
        Select the highest scoring dreams.
        """
        scored_dreams = sorted(
            scored_dreams,
            key=lambda d: d.score.value,
            reverse=True,
        )
        return scored_dreams[:top_k]
