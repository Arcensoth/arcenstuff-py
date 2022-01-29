from typing import Any, Optional

from arcenstuff.pydantic.transformable_model import TransformableModel

from .job import Job
from .pet import Pet

__all__ = ("Person",)


class Person(TransformableModel):
    name: str
    job: Optional[Job]
    pets: Optional[list[Pet]]

    @classmethod
    def __transformers__(cls):
        yield cls.normalize

    @classmethod
    def normalize(cls, value: Any) -> Any:
        if isinstance(value, str):
            return dict(name=value)
        return value
