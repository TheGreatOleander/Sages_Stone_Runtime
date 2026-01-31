# Runtime — New File: runner/result_schema.py
#
# Normalized runtime result envelope.
# Guarantees stable fields regardless of core behavior.
#

from typing import Dict, Any


def build_result(
    *,
    status: str,
    elapsed_seconds: float,
    steps_used: int,
    result: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "status": status,
        "runtime": {
            "elapsed_seconds": elapsed_seconds,
            "steps_used": steps_used,
        },
        "result": result,
    }
