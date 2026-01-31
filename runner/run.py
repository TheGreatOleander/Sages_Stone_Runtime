# Runtime — Patch File: runner/run.py
#
# Inject runtime info + enforce core compatibility
#

import multiprocessing as mp
import time
import traceback

from runner.errors import LimitExceeded, ExecutionFailed
from runner.limits import Limits
from runner.core_adapter import adapt_entry
from runner.memory import set_memory_limit_mb
from runner.result_schema import build_result
from runner.signals import install_signal_handlers
from runner.trace import Trace
from runner.sanitize import sanitize_config
from runner.capabilities import get_capabilities
from runner.version import get_runtime_info
from runner.compat import check_compat


def _worker(entry_fn, config, queue, step_counter, max_memory_mb, trace):
    try:
        install_signal_handlers()
        set_memory_limit_mb(max_memory_mb)

        safe_entry = adapt_entry(entry_fn)

        config = sanitize_config(config)

        runtime_info = get_runtime_info()
        core_requires = config.get("_core_requires")

        check_compat(runtime_info, core_requires)

        config["_steps"] = step_counter
        config["_trace"] = trace
        config["_runtime"] = {
            "info": runtime_info,
            "capabilities": get_capabilities(),
        }

        trace.emit("runtime.start", runtime=runtime_info)

        result = safe_entry(config)

        trace.emit("runtime.finish")

        queue.put({
            "ok": True,
            "result": result,
            "steps_used": step_counter.value,
            "trace": trace.dump(),
        })

    except Exception as e:
        queue.put({
            "ok": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        })


def run(config: dict, limits: Limits, entry_fn):
    start_time = time.time()
    limits.validate(config)

    queue = mp.Queue()
    step_counter = limits.make_step_counter()
    trace = Trace()

    proc = mp.Process(
        target=_worker,
        args=(
            entry_fn,
            config,
            queue,
            step_counter,
            limits.max_memory_mb,
            trace,
        ),
        daemon=True,
    )

    proc.start()
    proc.join(timeout=limits.max_seconds)

    if proc.is_alive():
        proc.terminate()
        proc.join()
        raise LimitExceeded("Execution time limit exceeded")

    if queue.empty():
        if proc.exitcode not in (0, None):
            raise ExecutionFailed(
                f"Worker exited with code {proc.exitcode}"
            )
        raise ExecutionFailed("Execution finished without result payload")

    payload = queue.get(timeout=0.5)
    elapsed = time.time() - start_time

    if not payload.get("ok"):
        raise ExecutionFailed(payload.get("error", "Unknown worker error"))

    result = build_result(
        status="success",
        elapsed_seconds=round(elapsed, 4),
        steps_used=payload.get("steps_used", 0),
        result=payload["result"],
    )

    if "trace" in payload:
        result["trace"] = payload["trace"]

    return result
