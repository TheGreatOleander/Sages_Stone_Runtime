class MockStone:
    """
    Minimal Stone implementation that satisfies the Runtime interface.
    No intelligence. No shortcuts. Just compliance.
    """

    def identity(self):
        return "mock-stone"

    def constraint(self):
        return {}

    def evaluate(self, input_data):
        return self.result(input_data)

    def result(self, value):
        return value

    def version(self):
        return "0.1.0"
