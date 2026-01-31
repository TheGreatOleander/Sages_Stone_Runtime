"""
Runner → Adapter bridge.

This lets the existing runner call into the runtime adapter
without changing runner/run.py internals.

Drop-in entry_fn for runner.run(...)
"""

from typing import Any, Dict

from runtime.adapter import run_from_config, AdapterError
from runner.errors import ExecutionFailed


def adapter_entry(config: Dict[str, Any]) -> Any:
    """
    Standard entry function signature expected by runner.run.

    runner.run passes config → entry_fn(config)
    """
    try:
        return run_from_config(config)
    except AdapterError as e:
        raise ExecutionFailed(f"Adapter failure: {e}") from e
    except Exception as e:
        raise ExecutionFailed(f"Core execution failure: {e}") from e
