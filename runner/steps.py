# Runtime — New File: runner/steps.py
#
# Lightweight, cross-process step accounting.
# Core calls step() explicitly; runtime enforces limits.
#

import multiprocessing as mp

from runner.errors import LimitExceeded


class StepCounter:
    def __init__(self, max_steps: int):
        self.max_steps = max_steps
        self._value = mp.Value("i", 0)

    def step(self, n: int = 1):
        with self._value.get_lock():
            self._value.value += n
            if self._value.value > self.max_steps:
                raise LimitExceeded(
                    f"Step limit exceeded: {self._value.value} > {self.max_steps}"
                )

    @property
    def value(self) -> int:
        return self._value.value
