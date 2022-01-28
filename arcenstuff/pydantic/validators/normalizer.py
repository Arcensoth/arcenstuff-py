from dataclasses import dataclass
from typing import Any, Callable

__all__ = ("Normalizer",)


@dataclass
class Normalizer:
    callback: Callable[[Any], Any]

    def __call__(self, value: Any) -> Any:
        if (normalized := self.callback(value)) is not None:
            return normalized
        return value
