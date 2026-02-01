"""
Runtime Result
==============

Canonical immutable container for the outcome of a runtime execution.

This object is designed to:
- Carry execution outputs
- Preserve runtime metadata (trace, scores, audits)
- Be safely serialized or stored
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class RuntimeResult:
    """
    Immutable runtime execution result.
    """

    value: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: Optional[Any] = None

    # --------------------------------------------------------------
    # Convenience helpers
    # --------------------------------------------------------------

    def with_metadata(self, **entries) -> "RuntimeResult":
        """
        Return a new RuntimeResult with merged metadata.
        """
        merged = dict(self.metadata)
        merged.update(entries)
        return RuntimeResult(
            value=self.value,
            metadata=merged,
            score=self.score,
        )

    def with_score(self, score: Any) -> "RuntimeResult":
        """
        Return a new RuntimeResult with an attached score.
        """
        return RuntimeResult(
            value=self.value,
            metadata=dict(self.metadata),
            score=score,
        )

    # --------------------------------------------------------------
    # Introspection helpers
    # --------------------------------------------------------------

    def has_trace(self) -> bool:
        return "runtime_trace" in self.metadata

    def get_trace(self):
        return self.metadata.get("runtime_trace")
