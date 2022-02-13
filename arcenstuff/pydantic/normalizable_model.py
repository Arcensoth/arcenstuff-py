from typing import Any, Generator, TypeVar

from pydantic import BaseModel
from pydantic.typing import AnyCallable

__all__ = [
    "NormalizableModel",
]


T = TypeVar("T", bound="NormalizableModel")

CallableGenerator = Generator[AnyCallable, None, None]


class NormalizableModel(BaseModel):
    """A model that normalizes input before validation."""

    @classmethod
    def normalize_input(cls, obj: Any) -> Any:
        return obj

    # @overrides BaseModel
    @classmethod
    def _enforce_dict_if_root(cls, obj: Any) -> Any:
        return super()._enforce_dict_if_root(cls.normalize_input(obj))
