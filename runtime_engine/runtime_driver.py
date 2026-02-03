"""
Runtime Driver
==============

Primary entry point for executing a Sages Stone runtime.

Responsibilities:
- Orchestrate runtime phases
- Invoke dream execution
- Ensure trace honesty
- Avoid implicit behavior

This driver declares phases descriptively.
It does NOT enforce phase ordering correctness.
"""

from __future__ import annotations

from typing import Any, Optional

from runtime_engine.runtime_phase import RuntimePhase
from runtime_engine.runtime_phase_scope import runtime_phase_scope
from runtime_trace.trace_recorder import record_event

from .dream_adapter import adapt_dream
from .runtime_contract import RuntimeContract


class RuntimeDriver:
    """
    Orchestrates a single runtime execution.
    """

    def __init__(self, contract: RuntimeContract):
        self.contract = contract

    def run(
        self,
        dream: Any,
        *,
        seed: Optional[Any] = None,
    ) -> Any:
        """
        Execute a dream under the runtime contract.
        """

        record_event("runtime.start")

        # --- BOOTSTRAP ---
        with runtime_phase_scope(RuntimePhase.BOOTSTRAP):
            record_event("runtime.bootstrap")
            self.contract.validate_environment()

        # --- SEED LOAD ---
        with runtime_phase_scope(RuntimePhase.SEED_LOAD):
            record_event("runtime.seed_load", {"has_seed": seed is not None})
            adapted_dream = adapt_dream(dream, seed=seed)

        # --- INITIALIZE ---
        with runtime_phase_scope(RuntimePhase.INITIALIZE):
            record_event("runtime.initialize")
            self.contract.initialize(adapted_dream)

        # --- EXECUTION ---
        with runtime_phase_scope(RuntimePhase.EXECUTION):
            record_event("runtime.execution.start")
            result = adapted_dream.execute()
            record_event("runtime.execution.end")

        # --- OBSERVATION ---
        with runtime_phase_scope(RuntimePhase.OBSERVATION):
            record_event("runtime.observe")
            self.contract.observe(result)

        # --- FINALIZE ---
        with runtime_phase_scope(RuntimePhase.FINALIZE):
            record_event("runtime.finalize")
            self.contract.finalize(result)

        record_event("runtime.end")
        return result
