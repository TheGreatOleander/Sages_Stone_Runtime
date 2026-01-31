# Runtime — New File: runner/version.py
#
# Runtime identity + compatibility contract
#

RUNTIME_NAME = "sages_stone_runtime"
RUNTIME_VERSION = "0.1.0"

# Minimal core expectations this runtime guarantees
RUNTIME_API = {
    "result_schema": "v1",
    "config_injection": True,
    "process_isolation": True,
}


def get_runtime_info() -> dict:
    return {
        "name": RUNTIME_NAME,
        "version": RUNTIME_VERSION,
        "api": dict(RUNTIME_API),
    }
