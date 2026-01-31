"""
Sages Stone Runtime
==================

The Runtime is not the Stone.
The Runtime does not define truth.
The Runtime *hosts* experiences that must obey the Stone.

Pre-Sages Stone dreams are allowed here —
but only insofar as they survive contact with law.

CLI-first. Deterministic by default.
Play is permitted. Chaos is constrained.
"""

from importlib.metadata import version, PackageNotFoundError

__all__ = [
    "__runtime_name__",
    "__runtime_version__",
    "__core_dependency__",
]

__runtime_name__ = "sages-stone-runtime"

# Resolve runtime version
try:
    __runtime_version__ = version(__runtime_name__)
except PackageNotFoundError:
    # Running from source / editable install
    __runtime_version__ = "0.0.0-dev"

# Hard declaration of allegiance
__core_dependency__ = "sages-stone"


def runtime_banner() -> str:
    """
    Single source of truth for runtime identity.
    Safe to print. Safe to log. Safe to show users.
    """
    return (
        f"Sages Stone Runtime v{__runtime_version__}\n"
        f"Bound to core: {__core_dependency__}\n"
        f"Mode: CLI-first | Network: none"
    )
