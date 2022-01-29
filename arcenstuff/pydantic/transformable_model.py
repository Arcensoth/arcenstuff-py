from typing import Any, Generator, TypeVar

from pydantic import BaseModel
from pydantic.typing import AnyCallable

__all__ = ("TransformableModel",)


T = TypeVar("T", bound="TransformableModel")

CallableGenerator = Generator[AnyCallable, None, None]


class TransformableModel(BaseModel):
    """Model subclass that transforms input before validation."""

    @classmethod
    def __transformers__(cls) -> CallableGenerator:
        yield from ()

    @classmethod
    def validate(cls, value: Any):
        for transformer in cls.__transformers__():
            value = transformer(value)
        return super().validate(value)
