"""
trace_store.py

Runtime Trace Store
-------------------
Append-only persistence for RuntimeTrace objects.

This module is intentionally simple:
- File-backed
- JSON Lines format
- No mutation
- Replayable

Memory without mythology.
"""

from pathlib import Path
from typing import Iterable
import json

from .trace_recorder import RuntimeTrace


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------

class TraceStore:
    """
    Append-only trace storage.
    """

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------

    def append(self, trace: RuntimeTrace) -> None:
        """
        Append a single trace to the store.
        """
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(trace.__dict__, sort_keys=True))
            f.write("\n")

    # ------------------------------------------------------------------

    def load_all(self) -> Iterable[RuntimeTrace]:
        """
        Load all traces from the store.
        """
        if not self.path.exists():
            return []

        traces = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                traces.append(RuntimeTrace(**data))
        return traces

    # ------------------------------------------------------------------

    def clear(self) -> None:
        """
        Explicit wipe. No silent deletes elsewhere.
        """
        if self.path.exists():
            self.path.unlink()
