# Runtime — New File: runner/capabilities.py
#
# Declares runtime features to the core
#

CAPABILITIES = {
    "steps": True,
    "trace": True,
    "memory_limit": True,
    "signal_handling": True,
    "process_isolation": True,
    "result_schema_v1": True,
}


def get_capabilities() -> dict:
    return dict(CAPABILITIES)
