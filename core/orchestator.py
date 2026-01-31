# sages_stone_runtime/core/orchestrator.py
"""
Runtime Orchestrator

Coordinates:
- DreamSeed loading
- Constraint registration
- Execution flow
- Artifact emission

This is the minimal conductor. No interpretation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from .runtime import (
    SagesStoneRuntime,
    DreamSeed,
    RuntimeArtifact,
    DEFAULT_CONSTRAINTS,
)
from .seed_loader import DreamSeedLoader


class RuntimeOrchestrator:
    """
    High-level runtime controller.
    """

    def __init__(
        self,
        presages_root: str | Path,
        auto_constraints: bool = True,
    ) -> None:
        self.runtime = SagesStoneRuntime()
        self.loader = DreamSeedLoader(presages_root)

        if auto_constraints:
            for constraint in DEFAULT_CONSTRAINTS:
                self.runtime.register_constraint(constraint)

    # ---- Execution ----

    def run_seed(self, seed: DreamSeed) -> RuntimeArtifact:
        return self.runtime.execute(seed)

    def run_seeds(self, seeds: Iterable[DreamSeed]) -> List[RuntimeArtifact]:
        artifacts: List[RuntimeArtifact] = []
        for seed in seeds:
            artifacts.append(self.run_seed(seed))
        return artifacts

    def run_directory(self, relative_dir: str | Path) -> List[RuntimeArtifact]:
        seeds = self.loader.load_all(relative_dir)
        return self.run_seeds(seeds)

    # ---- Export ----

    def export_all(self) -> List[str]:
        """
        Export all artifacts as JSON strings.
        """
        exports: List[str] = []
        for artifact_id in self.runtime.list_artifacts():
            exports.append(self.runtime.export_artifact(artifact_id))
        return exports
