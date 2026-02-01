"""
__main__.py

Module entrypoint for Sages_Stone_Runtime.

Enables:
    python -m Sages_Stone_Runtime

This file delegates ALL behavior to runtime_cli
to avoid duplication and drift.
"""

from .runtime_cli import main


if __name__ == "__main__":
    main()
