# sages_stone_runtime/core/seed_loader.py
"""
DreamSeed Loader

Responsible for importing symbolic material from Pre-Sages_Stone
WITHOUT interpreting, validating, or believing it.

This module only:
- Reads structured data
- Wraps it as DreamSeeds
- Tags provenance explicitly
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .runtime import DreamSeed


class DreamSeedLoader:
    """
    Loads DreamSeeds from disk.
    Accepts JSON only by design.
    """

    def __init__(self, base_path: str | Path) -> None:
        self.base_path = Path(base_path)

    def load_seed_file(self, relative_path: str | Path) -> DreamSeed:
        """
        Load a single DreamSeed from a JSON file.
        """
        full_path = self.base_path / relative_path
        if not full_path.exists():
            raise FileNotFoundError(full_path)

        with open(full_path, "r", encoding="utf-8") as f:
            payload: Dict[str, Any] = json.load(f)

        return DreamSeed(
            source=str(full_path),
            payload=payload,
        )

    def load_all(self, subdir: str | Path) -> List[DreamSeed]:
        """
        Load all JSON DreamSeeds from a directory tree.
        """
        root = self.base_path / subdir
        if not root.exists():
            raise FileNotFoundError(root)

        seeds: List[DreamSeed] = []

        for path in root.rglob("*.json"):
            try:
                seeds.append(self.load_seed_file(path.relative_to(self.base_path)))
            except Exception:
                # Runtime does not crash on malformed dreams
                continue

        return seeds
