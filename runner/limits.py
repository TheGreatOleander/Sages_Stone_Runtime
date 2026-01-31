from dataclasses import dataclass


@dataclass
class Limits:
    max_steps: int = 1_000
    max_seconds: float = 5.0
    max_memory_mb: int = 256  # advisory for now

    def validate(self, config: dict):
        steps = config.get("steps", 0)
        if steps > self.max_steps:
            raise ValueError(f"steps {steps} exceeds max_steps {self.max_steps}")
