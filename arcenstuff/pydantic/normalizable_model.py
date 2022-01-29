from typing import Any

from pydantic import BaseModel


class NormalizableModel(BaseModel):
    @classmethod
    def __normalize__(cls, value: Any) -> Any:
        return value

    # @overrides BaseModel
    @classmethod
    def _enforce_dict_if_root(cls, obj: Any) -> Any:
        normalized_obj = cls.__normalize__(obj)
        return super()._enforce_dict_if_root(normalized_obj)
