import multiprocessing as mp
import time
import traceback

from runner.errors import LimitExceeded, ExecutionFailed
from runner.limits import Limits
from runner.core_adapter import adapt_entry


def _worker(entry_fn, config, queue):
    """
    Runs inside a child process.
    """
    try:
        safe_entry = adapt_entry(entry_fn)
        result = safe_entry(config)

        queue.put({
            "ok": True,
            "result": result,
        })

    except Exception as e:
        queue.put({
            "ok": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        })


def run(config: dict, limits: Limits, entry_fn):
    """
    Controlled execution of the core.
    """

    start_time = time.time()
    limits.validate(config)

    queue = mp.Queue()

    proc = mp.Process(
        target=_worker,
        args=(entry_fn, config, queue),
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

    return {
        "status": "success",
        "elapsed_seconds": round(elapsed, 4),
        "result": payload["result"],
    }
