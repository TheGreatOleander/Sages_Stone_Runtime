"""
Lightweight config validation for Sages_Stone_Runtime.

Keeps runtime failures clean and early instead of deep inside execution.
No heavy deps — simple structural checks only.
"""

from typing import Any, Dict


class ConfigError(ValueError):
    pass


REQUIRED_TOP_LEVEL = {"entry"}
OPTIONAL_TOP_LEVEL = {"runtime", "kwargs", "meta"}


def normalize_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize config into canonical runtime shape.

    Accepts either:
        entry + kwargs
    or:
        runtime.entry + runtime.kwargs
    """

    if not isinstance(config, dict):
        raise ConfigError("Config must be a dict/object")

    runtime_block = config.get("runtime", {})

    entry = runtime_block.get("entry") or config.get("entry")
    kwargs = runtime_block.get("kwargs") or config.get("kwargs") or {}

    if not entry or not isinstance(entry, str):
        raise ConfigError("Missing required 'entry' callable path")

    if not isinstance(kwargs, dict):
        raise ConfigError("'kwargs' must be a dict/object")

    normalized = dict(config)
    normalized["entry"] = entry
    normalized["kwargs"] = kwargs

    return normalized


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Full validation pass.
    Returns normalized config.
    """

    cfg = normalize_config(config)

    # guard unknown top-level keys only if strict mode enabled later
    # (kept permissive for now by design)

    return cfg
