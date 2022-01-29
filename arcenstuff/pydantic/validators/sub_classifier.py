from dataclasses import dataclass
from typing import Any

from pydantic.errors import DictError
from pydantic.main import BaseModel

from arcenstuff.pydantic.errors import MissingType, UnknownType

__all__ = [
    "SubClassifier",
]


@dataclass
class SubClassifier:
    type_class: type[BaseModel]
    type_field: str

    def __call__(self, value: Any) -> Any:
        if not isinstance(value, dict):
            raise DictError()

        subclasses = self.type_class.__subclasses__()

        subclass_dict: dict[str, type[BaseModel]] = {
            sbc.__name__: sbc for sbc in subclasses
        }

        type_name = value.pop(self.type_field, None)  # type: ignore

        if not isinstance(type_name, str):
            raise MissingType(type_field=self.type_field)

        subclass = subclass_dict.get(type_name)

        if subclass is None:
            raise UnknownType(type_name=type_name)

        obj = subclass.parse_obj(value)

        return obj
