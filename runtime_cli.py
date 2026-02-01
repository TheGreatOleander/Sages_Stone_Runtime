"""
runtime_cli.py

Sage's Stone Runtime — Minimal CLI
---------------------------------
Demonstration-grade entrypoint for Sages_Stone_Runtime.

Goals:
- Prove executability
- Emit structured runtime traces
- Allow trace export to disk
- Avoid leaking engine internals
"""

import json
import argparse
from typing import Any, Optional

from .runtime_trace import RuntimeTrace
from .trace_scope import TraceScope


# ---------------------------------------------------------------------------
# Placeholder Runtime Hook
# ---------------------------------------------------------------------------

def runtime_entrypoint(*, trace: Optional[RuntimeTrace] = None) -> Any:
    """
    Black-box runtime entrypoint.

    Replace or extend this call internally without changing CLI semantics.
    """
    with TraceScope(trace, "runtime_entrypoint"):
        result = {
            "status": "ok",
            "message": "Sages_Stone_Runtime executed successfully",
        }

        if trace:
            trace.record("runtime_result", **result)

        return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sage's Stone Runtime CLI",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable execution tracing",
    )
    parser.add_argument(
        "--dump-trace",
        metavar="PATH",
        help="Write trace JSON to file instead of stdout",
    )

    args = parser.parse_args()

    trace = RuntimeTrace() if (args.trace or args.dump_trace) else None

    with TraceScope(trace, "cli_session"):
        result = runtime_entrypoint(trace=trace)

    # ------------------------------------------------------------------
    # Output result
    # ------------------------------------------------------------------

    print(json.dumps(result, indent=2))

    # ------------------------------------------------------------------
    # Output or dump trace
    # ------------------------------------------------------------------

    if trace:
        trace_data = trace.to_dict()

        if args.dump_trace:
            with open(args.dump_trace, "w", encoding="utf-8") as f:
                json.dump(trace_data, f, indent=2)
            print(f"\nTrace written to: {args.dump_trace}")
        else:
            print("\n--- TRACE ---")
            print(json.dumps(trace_data, indent=2))


if __name__ == "__main__":
    main()
