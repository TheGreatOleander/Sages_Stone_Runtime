"""
trace_recorder.py

Runtime Trace Recorder
----------------------
Captures a complete, inspectable record of a runtime invocation.

This is not logging.
This is memory.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
import time
import json

from .dream_adapter import DreamIntent
from .lens_binding import BoundIntent
from .collapse_oracle import CollapseResult
from .runtime_result import RuntimeResult


# ---------------------------------------------------------------------------
# Trace
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RuntimeTrace:
    intent_id: str
    timestamp: float
    intent: Dict[str, Any]
    lenses: Dict[str, Dict[str, Any]]
    collapse: Dict[str, Any]
    result: Dict[str, Any]


# ---------------------------------------------------------------------------
# Recorder
# ---------------------------------------------------------------------------

class TraceRecorder:
    """
    Creates immutable runtime traces.
    """

    def record(
        self,
        *,
        bound: BoundIntent,
        collapse: CollapseResult,
        result: RuntimeResult,
    ) -> RuntimeTrace:
        return RuntimeTrace(
            intent_id=bound.intent.intent_id,
            timestamp=time.time(),
            intent=self._safe_intent(bound.intent),
            lenses=bound.lens_results,
            collapse=asdict(collapse),
            result=self._safe_result(result),
        )

    # ------------------------------------------------------------------

    def to_json(self, trace: RuntimeTrace) -> str:
        """
        Serialize trace for storage or inspection.
        """
        return json.dumps(asdict(trace), indent=2, sort_keys=True)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _safe_intent(self, intent: DreamIntent) -> Dict[str, Any]:
        return {
            "intent_id": intent.intent_id,
            "description": intent.description,
            "payload": intent.payload,
            "limits": intent.limits,
            "created_at": intent.created_at,
            "checksum": intent.checksum,
        }

    def _safe_result(self, result: RuntimeResult) -> Dict[str, Any]:
        return {
            "success": result.success,
            "steps": result.steps,
            "duration": result.duration,
            "output": result.output,
            "score": result.score,
        }
