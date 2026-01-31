"""
Basic Dream Constructors
========================

This module provides canonical helpers for creating Dreams.

These helpers impose *shape*, not *meaning*.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable

from ..runtime_contract import Dream


# ---------------------------------------------------------------------------
# Generic Dreams
# ---------------------------------------------------------------------------

def raw(payload: Any, **metadata: Any) -> Dream:
    """
    Create a raw dream with arbitrary payload.
    """
    return Dream(payload=payload, metadata=dict(metadata))


# ---------------------------------------------------------------------------
# Query Dreams
# ---------------------------------------------------------------------------

def query(question: str, domain: str | None = None, **metadata: Any) -> Dream:
    """
    A dream representing a question posed to the system.
    """
    meta: Dict[str, Any] = {"type": "query"}
    if domain:
        meta["domain"] = domain
    meta.update(metadata)

    return Dream(payload=question, metadata=meta)


# ---------------------------------------------------------------------------
# Scenario Dreams
# ---------------------------------------------------------------------------

def scenario(
    description: str,
    initial_state: Dict[str, Any] | None = None,
    **metadata: Any,
) -> Dream:
    """
    A dream representing a hypothetical or simulated scenario.
    """
    meta: Dict[str, Any] = {"type": "scenario"}
    meta.update(metadata)

    payload = {
        "description": description,
        "initial_state": initial_state or {},
    }

    return Dream(payload=payload, metadata=meta)


# ---------------------------------------------------------------------------
# Intent Dreams
# ---------------------------------------------------------------------------

def intent(
    goal: str,
    constraints: Iterable[str] | None = None,
    **metadata: Any,
) -> Dream:
    """
    A dream representing a desired outcome or intention.
    """
    meta: Dict[str, Any] = {"type": "intent"}
    meta.update(metadata)

    payload = {
        "goal": goal,
        "constraints": list(constraints) if constraints else [],
    }

    return Dream(payload=payload, metadata=meta)
