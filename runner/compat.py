# Runtime — New File: runner/compat.py
#
# Enforces compatibility between core expectations and runtime
#

from runner.errors import ExecutionFailed


def check_compat(runtime_info: dict, core_requires: dict | None):
    """
    core_requires example:
    {
        "result_schema": "v1",
        "process_isolation": True
    }
    """
    if not core_requires:
        return

    runtime_api = runtime_info.get("api", {})

    for key, required in core_requires.items():
        if key not in runtime_api:
            raise ExecutionFailed(
                f"Runtime missing required capability: {key}"
            )

        if runtime_api[key] != required:
            raise ExecutionFailed(
                f"Incompatible runtime capability '{key}': "
                f"required={required}, runtime={runtime_api[key]}"
            )
