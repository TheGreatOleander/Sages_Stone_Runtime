"""
demo_minimal.py

Minimal End-to-End Demo
-----------------------
Proves the full Sages_Stone_Runtime pipeline:

Dream → Normalize → Bind → Collapse → Guarded Execute → Trace

This file is intentionally small and explicit.
"""

from typing import Dict, Any

from .dream_adapter import DreamAdapter
from .lens_binding import RuntimeLens, bind_intent
from .guarded_driver import GuardedRuntimeDriver
from .trace_recorder import TraceRecorder


# ---------------------------------------------------------------------------
# Example Lens
# ---------------------------------------------------------------------------

class SanityLens:
    """
    Minimal lens asserting a basic invariant.
    """

    name = "sanity"

    def apply(self, intent) -> Dict[str, Any]:
        payload = intent.payload
        return {
            "assert_payload_exists": bool(payload),
            "payload_keys": list(payload.keys()),
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def run_demo() -> None:
    # Step 1: Create a dream
    adapter = DreamAdapter(
        default_limits={
            "max_steps": 10,
            "max_seconds": 1.0,
        }
    )

    dream = adapter.normalize(
        description="Prove that dreams can run without lying",
        payload={
            "message": "Hello, Stone",
            "value": 42,
        },
        limits={},  # use defaults
    )

    # Step 2: Bind lenses
    bound = bind_intent(
        intent=dream,
        lenses=[SanityLens()],
    )

    # Step 3: Guarded execution
    driver = GuardedRuntimeDriver(strict=True)
    result = driver.run(bound)

    # Step 4: Record trace
    recorder = TraceRecorder()
    trace = recorder.record(
        bound=bound,
        collapse=driver.oracle.evaluate(bound),
        result=result,
    )

    print("=== RUNTIME RESULT ===")
    print(result)

    print("\n=== TRACE ===")
    print(recorder.to_json(trace))


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_demo()
