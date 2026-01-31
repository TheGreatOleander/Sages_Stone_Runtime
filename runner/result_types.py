"""
Structured result helpers for Sages_Stone_Runtime.

Keeps outputs consistent across adapters and runners.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class RuntimeResult:
    status: str
    result: Any = None
    error: Optional[str] = None
    steps: Optional[int] = None
    elapsed: Optional[float] = None
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def ok(result: Any, *, steps=None, elapsed=None, meta=None) -> RuntimeResult:
    return RuntimeResult(
        status="ok",
        result=result,
        steps=steps,
        elapsed=elapsed,
        meta=meta,
    )


def fail(error: str, *, steps=None, elapsed=None, meta=None) -> RuntimeResult:
    return RuntimeResult(
        status="error",
        error=error,
        steps=steps,
        elapsed=elapsed,
        meta=meta,
    )
