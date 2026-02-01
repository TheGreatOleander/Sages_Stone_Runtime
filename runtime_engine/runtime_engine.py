"""
Runtime Engine
==============

Core execution orchestrator for Sages Stone Runtime.

Now includes lifecycle transition enforcement.
"""

from typing import Any, Dict, Optional, List

from .lifecycle import RuntimePhase, RuntimeState
from .lifecycle_hooks import RuntimeLifecycleHook


class RuntimeEngine:
    """
    Primary runtime execution engine.
    """

    def __init__(
        self,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        enforce_lifecycle: bool = True,
    ):
        self._state = RuntimeState(
            phase=RuntimePhase.CREATED,
            metadata=metadata or {},
        )
        self._hooks: List[RuntimeLifecycleHook] = []
        self._enforce_lifecycle = enforce_lifecycle

    # ------------------------------------------------------------------
    # Hook management
    # ------------------------------------------------------------------

    def add_hook(self, hook: RuntimeLifecycleHook):
        self._hooks.append(hook)

    def _notify(self):
        for hook in self._hooks:
            try:
                hook.on_transition(self._state)
            except Exception:
                # Hooks must never break execution
                pass

    # ------------------------------------------------------------------
    # Lifecycle helpers
    # ------------------------------------------------------------------

    @property
    def state(self) -> RuntimeState:
        return self._state

    def _transition(
        self,
        phase: RuntimePhase,
        *,
        message: Optional[str] = None,
        error: Optional[BaseException] = None,
    ):
        if self._enforce_lifecycle:
            self._state.assert_can_transition_to(phase)

        self._state = RuntimeState(
            phase=phase,
            metadata=self._state.metadata,
            message=message,
            error=error,
        )
        self._notify()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def configure(self, **kwargs):
        self._transition(RuntimePhase.CONFIGURED)
        return self

    def prime(self):
        self._transition(RuntimePhase.PRIMED)
        return self

    def execute(self):
        self._transition(RuntimePhase.EXECUTING)

        try:
            result = self._execute_internal()

            self._transition(RuntimePhase.SCORING)
            scored = self._score(result)

            self._transition(RuntimePhase.FINALIZED)
            return scored

        except Exception as exc:
            self._transition(
                RuntimePhase.FAILED,
                message=str(exc),
                error=exc,
            )
            raise

    # ------------------------------------------------------------------
    # Internal hooks
    # ------------------------------------------------------------------

    def _execute_internal(self):
        raise NotImplementedError

    def _score(self, result):
        return result
