import pytest
from runtime.stone_adapter import StoneAdapter, StoneIncompatibleError


class IncompleteStone:
    # Deliberately missing required primitives
    def version(self):
        return "0.0.0"


def test_runtime_rejects_incompatible_stone():
    with pytest.raises(StoneIncompatibleError):
        StoneAdapter(IncompleteStone())
