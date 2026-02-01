"""
trace_replay.py

Runtime Trace Replay Tool
-------------------------
Loads and replays RuntimeTrace JSON artifacts.

Purpose:
- Human inspection
- Debugging
- Demonstrations
- Post-mortem analysis
- Schema compatibility awareness
"""

import json
import argparse
from typing import Dict, Any, List, Optional


# ---------------------------------------------------------------------------
# Compatibility
# ---------------------------------------------------------------------------

SUPPORTED_TRACE_SCHEMA_VERSION = "1"


def check_compatibility(trace_data: Dict[str, Any]) -> None:
    runtime = trace_data.get("runtime")

    if not runtime:
        print("⚠️  Warning: Trace has no runtime identity (legacy trace).")
        return

    schema_version = runtime.get("trace_schema_version")
    name = runtime.get("name", "<unknown>")
    version = runtime.get("version", "<unknown>")

    if schema_version != SUPPORTED_TRACE_SCHEMA_VERSION:
        print(
            "⚠️  Warning: Trace schema version mismatch\n"
            f"    Runtime: {name} {version}\n"
            f"    Trace schema: {schema_version}\n"
            f"    Supported: {SUPPORTED_TRACE_SCHEMA_VERSION}\n"
            "    Replay may be incomplete."
        )


# ---------------------------------------------------------------------------
# Replay Logic
# ---------------------------------------------------------------------------

def replay_trace(
    trace_data: Dict[str, Any],
    *,
    show_payloads: bool = True,
) -> None:
    trace_id = trace_data.get("trace_id", "<unknown>")
    events: List[Dict[str, Any]] = trace_data.get("events", [])

    runtime = trace_data.get("runtime", {})
    runtime_name = runtime.get("name", "<unknown>")
    runtime_version = runtime.get("version", "<unknown>")

    print("\n=== TRACE REPLAY ===")
    print(f"Trace ID: {trace_id}")
    print(f"Runtime: {runtime_name} {runtime_version}")
    print(f"Events: {len(events)}\n")

    prev_ts: Optional[float] = None

    for idx, event in enumerate(events, start=1):
        name = event.get("name", "<unnamed>")
        ts = event.get("timestamp")
        payload = event.get("payload", {})

        delta = None
        if prev_ts is not None and ts is not None:
            delta = ts - prev_ts

        line = f"[{idx:03d}] {name}"
        if delta is not None:
            line += f" (+{delta:.6f}s)"

        print(line)

        if show_payloads and payload:
            for k, v in payload.items():
                print(f"      {k}: {v}")

        prev_ts = ts

    print("\n=== END TRACE ===\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replay a Sage's Stone Runtime trace",
    )
    parser.add_argument(
        "trace_file",
        metavar="TRACE.json",
        help="Path to trace JSON file",
    )
    parser.add_argument(
        "--no-payloads",
        action="store_true",
        help="Suppress payload output",
    )

    args = parser.parse_args()

    with open(args.trace_file, "r", encoding="utf-8") as f:
        trace_data = json.load(f)

    check_compatibility(trace_data)

    replay_trace(
        trace_data,
        show_payloads=not args.no_payloads,
    )


if __name__ == "__main__":
    main()
