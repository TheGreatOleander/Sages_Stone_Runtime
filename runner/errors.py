class RuntimeErrorBase(Exception):
    pass


class LimitExceeded(RuntimeErrorBase):
    def __init__(self, message):
        super().__init__(message)


class ExecutionFailed(RuntimeErrorBase):
    def __init__(self, message):
        super().__init__(message)
