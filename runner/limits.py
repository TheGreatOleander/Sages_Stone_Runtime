from dataclasses import dataclass


@dataclass
class Limits:
    max_steps: int = 1_000
    max_seconds: float = 5.0
    max_memory_mb: int = 256  # advisory for now

    def __post_init__(self):
        if self.max_steps <= 0:
            raise ValueError("max_steps must be > 0")

        if self.max_seconds <= 0:
            raise ValueError("max_seconds must be > 0")

        if self.max_memory_mb <= 0:
            raise ValueError("max_memory_mb must be > 0")
