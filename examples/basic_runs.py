"""
Basic Runtime Examples
======================

These examples demonstrate canonical Sages Stone runtime usage.
They are intended to be read, run, and modified.
"""

from sages_stone_runtime.runtime_runner import run_dream
from sages_stone_runtime.dreams.basic_dreams import query, scenario
from sages_stone_runtime.lenses.state_lenses import (
    InitializeStateLens,
    ProjectMetadataLens,
    InjectConstantLens,
    FilterStateLens,
)
from sages_stone_runtime.constraints.base_constraints import (
    MaxLensApplications,
    MaxStateKeys,
)
from sages_stone_runtime.observers.trace_observer import TraceObserver


# ---------------------------------------------------------------------------
# Example 1: Simple Query
# ---------------------------------------------------------------------------

def example_simple_query():
    dream = query(
        "What is the stable shape of this system?",
        domain="introspection",
    )

    lenses = [
        InitializeStateLens(),
        ProjectMetadataLens(),
        InjectConstantLens("answered", False),
    ]

    constraints = [
        MaxLensApplications(10),
        MaxStateKeys(10),
    ]

    observer = TraceObserver()

    result = run_dream(
        dream=dream,
        lenses=lenses,
        constraints=constraints,
        observers=[observer],
    )

    print("=== Simple Query Result ===")
    print("Success:", result.success)
    print("Final State:", result.final_state)
    print("Trace:", *result.trace, sep="\n")


# ---------------------------------------------------------------------------
# Example 2: Scenario Projection
# ---------------------------------------------------------------------------

def example_scenario():
    dream = scenario(
        description="A system evolves under bounded mutation",
        initial_state={"energy": 10, "entropy": 1},
    )

    lenses = [
        InitializeStateLens(),
        InjectConstantLens("stability", "unknown"),
        FilterStateLens({"energy", "entropy", "stability"}),
    ]

    constraints = [
        MaxLensApplications(5),
        MaxStateKeys(5),
    ]

    observer = TraceObserver()

    result = run_dream(
        dream=dream,
        lenses=lenses,
        constraints=constraints,
        observers=[observer],
    )

    print("\n=== Scenario Result ===")
    print("Success:", result.success)
    print("Final State:", result.final_state)
    print("Trace:", *result.trace, sep="\n")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    example_simple_query()
    example_scenario()
