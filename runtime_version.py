"""
runtime_version.py

Sage's Stone Runtime — Version & Identity
-----------------------------------------

This module defines the canonical identity of the runtime.
All external-facing tools (CLI, traces, demos) should read from here.

Keep this boring. Boring is stability.
"""

from dataclasses import dataclass
from typing import Dict


# ---------------------------------------------------------------------------
# Version Info
# ---------------------------------------------------------------------------

RUNTIME_NAME = "Sage's Stone Runtime"

# Semantic-ish versioning (you control the meaning)
RUNTIME_VERSION = "0.1.0"

# Trace / protocol compatibility version
TRACE_SCHEMA_VERSION = "1"


# ---------------------------------------------------------------------------
# Structured Identity
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RuntimeIdentity:
    name: str
    version: str
    trace_schema_version: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "version": self.version,
            "trace_schema_version": self.trace_schema_version,
        }


# Canonical identity object
IDENTITY = RuntimeIdentity(
    name=RUNTIME_NAME,
    version=RUNTIME_VERSION,
    trace_schema_version=TRACE_SCHEMA_VERSION,
)
