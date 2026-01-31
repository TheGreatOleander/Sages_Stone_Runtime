"""
runtime_contracts.py

Runtime Contract Validator
--------------------------
Centralized enforcement of Sages_Stone_Runtime invariants.

This module answers one question:
"Is this runtime state allowed to exist?"

It does not execute.
It does not mutate.
It only judges.
"""

from typing import Dict, Any

from .dream_adapter import DreamIntent
from .lens_binding import BoundIntent
from .collapse_oracle import CollapseResult
from .runtime_result import RuntimeResult


# ---------------------------------------------------------------------------
# Contract Violations
# ---------------------------------------------------------------------------

class ContractViolation(Exception):
    """
    Raised when a runtime invariant is violated.
    """
    pass


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def validate_intent(intent: DreamIntent) -> None:
    if not intent.intent_id:
        raise ContractViolation("Intent must have an intent_id")

    if not isinstance(intent.payload, dict):
        raise ContractViolation("Intent payload must be a dict")

    if "max_steps" not in intent.limits:
        raise ContractViolation("Intent missing max_steps limit")

    if "max_seconds" not in intent.limits:
        raise ContractViolation("Intent missing max_seconds limit")


def validate_bound_intent(bound: BoundIntent) -> None:
    validate_intent(bound.intent)

    if not isinstance(bound.lens_results, dict):
        raise ContractViolation("Lens results must be a dict")

    for lens_name, data in bound.lens_results.items():
        if not isinstance(lens_name, str):
            raise ContractViolation("Lens name must be a string")
        if not isinstance(data, dict):
            raise ContractViolation(
                f"Lens '{lens_name}' output must be a dict"
            )


def validate_collapse(collapse: CollapseResult) -> None:
    if not isinstance(collapse.allowed, bool):
        raise ContractViolation("Collapse.allowed must be bool")

    if not isinstance(collapse.reason, str):
        raise ContractViolation("Collapse.reason must be string")

    if collapse.allowed and not isinstance(collapse.resolved_lenses, dict):
        raise ContractViolation(
            "Resolved lenses must be dict when collapse is allowed"
        )


def validate_result(result: RuntimeResult) -> None:
    if not isinstance(result.success, bool):
        raise ContractViolation("Result.success must be bool")

    if result.steps < 0:
        raise ContractViolation("Result.steps must be >= 0")

    if result.duration < 0:
        raise ContractViolation("Result.duration must be >= 0")

    if not isinstance(result.output, dict):
        raise ContractViolation("Result.output must be dict")


# ---------------------------------------------------------------------------
# Composite Check
# ---------------------------------------------------------------------------

def validate_runtime_state(
    *,
    bound: BoundIntent,
    collapse: CollapseResult,
    result: RuntimeResult,
) -> None:
    """
    Validate an entire runtime invocation as a single state.
    """
    validate_bound_intent(bound)
    validate_collapse(collapse)
    validate_result(result)
