"""
Controlled execution runner.

Responsibilities:
- Validate config early
- Enforce limits
- Execute entry_fn safely
- Return structured result
"""

import time
import traceback
from typing import Any, Callable, Dict

from runner.limits import Limits
from runner.errors import LimitExceeded, ExecutionFailed
from runner.config_schema import validate_config


def run(
    *,
    config: Dict[str, Any],
    limits: Limits,
    entry_fn: Callable[[Dict[str, Any]], Any],
) -> Dict[str, Any]:
    """
    Main runtime execution wrapper.
    """

    started = time.time()
    steps = 0

    def step():
        nonlocal steps
        steps += 1
        if limits.max_steps is not None and steps > limits.max_steps:
            raise LimitExceeded(f"Step limit exceeded ({limits.max_steps})")

        if limits.max_seconds is not None:
            if (time.time() - started) > limits.max_seconds:
                raise LimitExceeded(
                    f"Time limit exceeded ({limits.max_seconds}s)"
                )

    try:
        cfg = validate_config(config)

        step()  # pre-exec step charge

        result = entry_fn(cfg)

        step()  # post-exec step charge

        return {
            "status": "ok",
            "result": result,
            "steps": steps,
            "elapsed": time.time() - started,
        }

    except LimitExceeded:
        raise

    except Exception as e:
        raise ExecutionFailed(
            f"{e}\n{traceback.format_exc()}"
        ) from e
