"""
Sages Stone Runtime — Smoke Test

This test exists to prove:
- the canonical execution path is importable
- the runtime can be invoked without structural failure

It does NOT test behavior.
It does NOT test outcomes.
It only tests that the spine holds.
"""

import pathlib

from sages_stone_runtime.runtime.execute import execute_system


def test_runtime_smoke(tmp_path: pathlib.Path):
    # Create a minimal dummy system file
    system_file = tmp_path / "dummy.system"
    system_file.write_text("# dummy system for smoke test\n")

    try:
        result = execute_system(
            system_path=str(system_file),
            dry_run=True,
        )
    except Exception as exc:
        raise AssertionError(
            f"Canonical runtime execution failed structurally: {exc}"
        ) from exc

    # If a result object exists, it must at least be inspectable
    assert result is not None
