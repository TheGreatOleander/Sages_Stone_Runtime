class StoneIncompatibleError(Exception):
    pass


class StoneAdapter:
    """
    Runtime-facing adapter.
    This is the ONLY allowed entry point to Stone.
    """

    REQUIRED_PRIMITIVES = {
        "identity",
        "constraint",
        "evaluate",
        "result",
        "version",
    }

    def __init__(self, stone_module):
        self.stone = stone_module
        self._verify_interface()

    def _verify_interface(self):
        missing = [
            name for name in self.REQUIRED_PRIMITIVES
            if not hasattr(self.stone, name)
        ]
        if missing:
            raise StoneIncompatibleError(
                f"Stone missing required primitives: {missing}"
            )

    def version(self):
        return self.stone.version()

    def evaluate(self, input_data):
        return self.stone.evaluate(input_data)
