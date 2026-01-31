# sages_stone_runtime/core/runtime.py
"""
Sages Stone Runtime Core

This file defines the authoritative runtime spine.
It does NOT assert truth.
It executes constrained exploration over supplied symbolic material.

Pre-Sages_Stone = input field (dreams)
Sages_Stone      = validated core logic
Runtime          = executor + constraint enforcer
"""

from __future__ import annotations

import uuid
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable


# ----------------------------
# Runtime Artifacts
# ----------------------------

@dataclass
class DreamSeed:
    """
    A DreamSeed is a symbolic input.
    It may be speculative, poetic, or incomplete.
    It carries NO implicit truth value.
    """
    source: str
    payload: Dict[str, Any]
    seed_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class RuntimeArtifact:
    """
    Output of runtime execution.
    This is the *only* thing downstream systems may consume.
    """
    artifact_id: str
    seed_id: str
    constraints_applied: List[str]
    result: Dict[str, Any]


# ----------------------------
# Constraint System
# ----------------------------

class Constraint:
    """
    A constraint is a callable filter or transformer.
    It must be explicit and nameable.
    """

    def __init__(self, name: str, fn: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self.name = name
        self.fn = fn

    def apply(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.fn(data)


# ----------------------------
# Runtime Core
# ----------------------------

class SagesStoneRuntime:
    """
    The runtime executes DreamSeeds under explicit constraints.
    Nothing passes through implicitly.
    """

    def __init__(self) -> None:
        self._constraints: List[Constraint] = []
        self._artifacts: Dict[str, RuntimeArtifact] = {}

    # ---- Constraint Management ----

    def register_constraint(self, constraint: Constraint) -> None:
        self._constraints.append(constraint)

    def clear_constraints(self) -> None:
        self._constraints.clear()

    # ---- Execution ----

    def execute(self, seed: DreamSeed) -> RuntimeArtifact:
        data = dict(seed.payload)
        applied: List[str] = []

        for constraint in self._constraints:
            data = constraint.apply(data)
            applied.append(constraint.name)

        artifact = RuntimeArtifact(
            artifact_id=str(uuid.uuid4()),
            seed_id=seed.seed_id,
            constraints_applied=applied,
            result=data,
        )

        self._artifacts[artifact.artifact_id] = artifact
        return artifact

    # ---- Persistence ----

    def export_artifact(self, artifact_id: str) -> str:
        """
        Export artifact as JSON string.
        Runtime never exports raw DreamSeeds.
        """
        artifact = self._artifacts.get(artifact_id)
        if not artifact:
            raise KeyError(f"No artifact with id {artifact_id}")

        return json.dumps({
            "artifact_id": artifact.artifact_id,
            "seed_id": artifact.seed_id,
            "constraints_applied": artifact.constraints_applied,
            "result": artifact.result,
        }, indent=2)

    # ---- Introspection ----

    def list_artifacts(self) -> List[str]:
        return list(self._artifacts.keys())


# ----------------------------
# Default Safety Constraints
# ----------------------------

def no_physical_assertions(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strip or tag claims that assert physical reality.
    This keeps runtime 'physically honest'.
    """
    cleaned = {}
    for k, v in data.items():
        if isinstance(v, dict) and v.get("asserts_physical_truth"):
            cleaned[k] = {
                "value": v.get("value"),
                "note": "physical assertion stripped by runtime"
            }
        else:
            cleaned[k] = v
    return cleaned


DEFAULT_CONSTRAINTS = [
    Constraint("no_physical_assertions", no_physical_assertions),
]
