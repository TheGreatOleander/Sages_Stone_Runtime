"""
collapse_oracle.py

Collapse / Arbitration Layer
----------------------------
Resolves conflicts between lens outputs BEFORE runtime execution.

This is where incompatible meanings are detected,
ranked, or collapsed — explicitly, not implicitly.

Design goals:
- Deterministic
- Explainable
- Runtime-visible failure modes
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

from .lens_binding import BoundIntent


# ---------------------------------------------------------------------------
# Collapse Result
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CollapseResult:
    """
    Outcome of lens arbitration.
    """
    allowed: bool
    reason: str
    resolved_lenses: Dict[str, Dict[str, Any]]


# ---------------------------------------------------------------------------
# Oracle
# ---------------------------------------------------------------------------

class CollapseOracle:
    """
    Evaluates lens outputs for incompatibilities.

    This class does NOT decide meaning.
    It decides whether meaning can coexist.
    """

    def __init__(self, strict: bool = True):
        self.strict = strict

    # ------------------------------------------------------------------

    def evaluate(self, bound: BoundIntent) -> CollapseResult:
        lens_results = bound.lens_results

        conflicts = self._detect_conflicts(lens_results)

        if conflicts:
            if self.strict:
                return CollapseResult(
                    allowed=False,
                    reason=f"Lens conflict detected: {conflicts}",
                    resolved_lenses={},
                )
            else:
                resolved = self._soft_resolve(lens_results, conflicts)
                return CollapseResult(
                    allowed=True,
                    reason=f"Conflicts soft-resolved: {conflicts}",
                    resolved_lenses=resolved,
                )

        return CollapseResult(
            allowed=True,
            reason="No conflicts detected",
            resolved_lenses=lens_results,
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _detect_conflicts(
        self,
        lens_results: Dict[str, Dict[str, Any]],
    ) -> List[str]:
        """
        Naive but explicit conflict detection.

        Conflict rule:
        - Two lenses assert different values for the same key
        - Key starts with 'assert_'
        """
        assertions: Dict[str, Any] = {}
        conflicts: List[str] = []

        for lens_name, data in lens_results.items():
            for key, value in data.items():
                if not key.startswith("assert_"):
                    continue

                if key in assertions and assertions[key] != value:
                    conflicts.append(
                        f"{key}: {assertions[key]} vs {value}"
                    )
                else:
                    assertions[key] = value

        return conflicts

    def _soft_resolve(
        self,
        lens_results: Dict[str, Dict[str, Any]],
        conflicts: List[str],
    ) -> Dict[str, Dict[str, Any]]:
        """
        Soft resolution strategy:
        - Drop conflicting assertions
        - Preserve non-conflicting data
        """
        resolved: Dict[str, Dict[str, Any]] = {}

        for lens_name, data in lens_results.items():
            clean = {}
            for key, value in data.items():
                if key.startswith("assert_"):
                    if any(key in c for c in conflicts):
                        continue
                clean[key] = value
            resolved[lens_name] = clean

        return resolved


# ---------------------------------------------------------------------------
# Convenience helper
# ---------------------------------------------------------------------------

def collapse(bound: BoundIntent, strict: bool = True) -> CollapseResult:
    oracle = CollapseOracle(strict=strict)
    return oracle.evaluate(bound)
