"""
Core adapter layer.

Normalizes Sage's Stone core entrypoints so runtime
always calls a consistent interface.
"""

from typing import Callable, Dict, Any


def adapt_entry(entry_fn: Callable) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Wraps different possible core signatures into:

        fn(config: dict) -> dict
    """

    def _wrapped(config: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # preferred: entry_fn(config)
            result = entry_fn(config)
        except TypeError:
            # fallback: entry_fn(**config)
            result = entry_fn(**config)

        if not isinstance(result, dict):
            result = {"output": result}

        return result

    return _wrapped
