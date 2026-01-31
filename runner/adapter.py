"""
Runtime adapter layer.

Purpose:
- Decouple Sages_Stone_Runtime from hard-coded core entry names
- Allow config-driven binding to Sages_Stone main repo functions
- Provide a stable callable for runner.run → entry_fn
"""

from importlib import import_module
from typing import Any, Callable, Dict


class AdapterError(RuntimeError):
    pass


def resolve_callable(path: str) -> Callable:
    """
    Resolve dotted path to callable.

    Example:
        sages_stone.engine.core:run_model
        sages_stone.api.entry:execute
    """
    if ":" not in path:
        raise AdapterError("Callable path must be module:callable")

    module_name, fn_name = path.split(":", 1)

    try:
        module = import_module(module_name)
    except Exception as e:
        raise AdapterError(f"Import failed for module '{module_name}': {e}") from e

    try:
        fn = getattr(module, fn_name)
    except AttributeError:
        raise AdapterError(f"Callable '{fn_name}' not found in {module_name}")

    if not callable(fn):
        raise AdapterError(f"Resolved object '{path}' is not callable")

    return fn


def run_from_config(config: Dict[str, Any]) -> Any:
    """
    Expected config shape:

    runtime:
        entry: "module.path:callable"
        kwargs: {...}

    or

    entry: "module.path:callable"
    kwargs: {...}
    """

    entry_path = (
        config.get("runtime", {}).get("entry")
        or config.get("entry")
    )

    if not entry_path:
        raise AdapterError("No entry callable specified in config")

    kwargs = (
        config.get("runtime", {}).get("kwargs")
        or config.get("kwargs")
        or {}
    )

    fn = resolve_callable(entry_path)

    return fn(**kwargs)
