"""
dream_adapter.py

Intent / Dream Normalization Layer
---------------------------------
This module bridges Pre_Sages_Stone "dreams" (raw intent artifacts)
into a bounded, runtime-safe execution payload.

It does NOT execute dreams.
It does NOT import Pre_Sages_Stone at runtime.
It only accepts structured intent and freezes it into a form
the Sages_Stone_Runtime engine can safely consume.

Design goals:
- Deterministic
- Side-effect free
- Explicit limits
- Runtime-visible invariants
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Callable, Optional
import time
import hashlib
import json


# ---------------------------------------------------------------------------
# Normalized Execution Payload
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DreamIntent:
    """
    Immutable, normalized intent object.

    This is the ONLY thing runtime_engine should ever see.
    """
    intent_id: str
    description: str
    payload: Dict[str, Any]
    limits: Dict[str, Any]
    created_at: float
    checksum: str


# ---------------------------------------------------------------------------
# Adapter
# ---------------------------------------------------------------------------

class DreamAdapter:
    """
    Converts raw dream / intent descriptions into a frozen DreamIntent.

    This class is intentionally boring.
    Boring == safe.
    """

    REQUIRED_LIMITS = {
        "max_steps": int,
        "max_seconds": (int, float),
    }

    def __init__(self, default_limits: Optional[Dict[str, Any]] = None):
        self.default_limits = default_limits or {}

    # -------------------------
    # Public API
    # -------------------------

    def normalize(
        self,
        *,
        description: str,
        payload: Dict[str, Any],
        limits: Optional[Dict[str, Any]] = None,
        intent_id: Optional[str] = None,
    ) -> DreamIntent:
        """
        Normalize a raw dream into a runtime-safe DreamIntent.

        Parameters:
            description : Human-readable intent summary
            payload     : Arbitrary structured data (no callables)
            limits      : Execution bounds (merged with defaults)
            intent_id   : Optional stable ID (otherwise derived)

        Returns:
            DreamIntent (immutable)
        """

        if not isinstance(payload, dict):
            raise TypeError("Dream payload must be a dict")

        merged_limits = self._merge_limits(limits or {})
        self._validate_limits(merged_limits)

        created_at = time.time()

        normalized_payload = self._freeze_payload(payload)
        checksum = self._checksum(description, normalized_payload, merged_limits)

        if intent_id is None:
            intent_id = checksum[:16]

        return DreamIntent(
            intent_id=intent_id,
            description=description.strip(),
            payload=normalized_payload,
            limits=merged_limits,
            created_at=created_at,
            checksum=checksum,
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _merge_limits(self, limits: Dict[str, Any]) -> Dict[str, Any]:
        merged = dict(self.default_limits)
        merged.update(limits)
        return merged

    def _validate_limits(self, limits: Dict[str, Any]) -> None:
        for key, expected_type in self.REQUIRED_LIMITS.items():
            if key not in limits:
                raise ValueError(f"Missing required limit: {key}")
            if not isinstance(limits[key], expected_type):
                raise TypeError(
                    f"Limit '{key}' must be {expected_type}, got {type(limits[key])}"
                )

    def _freeze_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure payload is JSON-serializable and free of callables.
        """
        try:
            encoded = json.dumps(payload, sort_keys=True)
            return json.loads(encoded)
        except Exception as e:
            raise ValueError("Dream payload must be JSON-serializable") from e

    def _checksum(
        self,
        description: str,
        payload: Dict[str, Any],
        limits: Dict[str, Any],
    ) -> str:
        h = hashlib.sha256()
        h.update(description.encode("utf-8"))
        h.update(json.dumps(payload, sort_keys=True).encode("utf-8"))
        h.update(json.dumps(limits, sort_keys=True).encode("utf-8"))
        return h.hexdigest()


# ---------------------------------------------------------------------------
# Convenience helper
# ---------------------------------------------------------------------------

def adapt_dream(
    *,
    description: str,
    payload: Dict[str, Any],
    limits: Dict[str, Any],
) -> DreamIntent:
    """
    Stateless helper for one-off normalization.
    """
    adapter = DreamAdapter()
    return adapter.normalize(
        description=description,
        payload=payload,
        limits=limits,
    )
