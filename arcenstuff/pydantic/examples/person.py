from typing import Any, Optional

from arcenstuff.pydantic.normalizable_model import NormalizableModel

from .job import Job
from .pet import Pet

__all__ = ("Person",)


class Person(NormalizableModel):
    name: str
    job: Optional[Job]
    pets: Optional[list[Pet]]

    @classmethod
    def __normalize__(cls, value: Any) -> Any:
        if isinstance(value, str):
            return dict(name=value)
        return value
