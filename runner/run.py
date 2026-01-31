import multiprocessing as mp
import time
import traceback

from runner.errors import LimitExceeded, ExecutionFailed
from runner.limits import Limits


def _worker(entry_fn, config, queue):
    """
    Runs inside a child process.
    """
    try:
        result = entry_fn(config)
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

    Parameters:
        config   : dict   - user run configuration
        limits   : Limits - hard safety limits
        entry_fn : callable(config) -> result

    Returns:
        dict - structured execution result
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
        raise ExecutionFailed("Execution failed without result")

    payload = queue.get()
    elapsed = time.time() - start_time

    if not payload["ok"]:
        raise ExecutionFailed(payload["error"])

    return {
        "status": "success",
        "elapsed_seconds": round(elapsed, 4),
        "result": payload["result"],
    }
