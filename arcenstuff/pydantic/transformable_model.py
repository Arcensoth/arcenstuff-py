from __future__ import annotations

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
    def __get_validators__(cls) -> CallableGenerator:
        yield from cls.__transformers__()
        yield from super().__get_validators__()

    @classmethod
    def transform(cls: type[T], value: Any) -> T:
        for transformer in cls.__transformers__():
            value = transformer(value)
        return cls.validate(value)
