# sages_stone_runtime/runtime_result.py
"""
Runtime Result Contract
=======================

Defines the immutable output of a Sages Stone runtime execution.

This object is:
- Serializable
- Observer-friendly
- CLI-agnostic
- Safe to persist or diff

No execution logic lives here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class RuntimeViolation:
    """
    Represents a constraint violation.
    """
    constraint: str
    message: str


@dataclass(frozen=True)
class RuntimeResult:
    """
    Final product of running a Dream through the runtime.
    """
    success: bool
    final_state: Dict[str, Any]

    violations: List[RuntimeViolation] = field(default_factory=list)
    trace: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "final_state": self.final_state,
            "violations": [
                {
                    "constraint": v.constraint,
                    "message": v.message,
                }
                for v in self.violations
            ],
            "trace": list(self.trace),
        }
