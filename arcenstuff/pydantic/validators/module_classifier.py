from dataclasses import dataclass
from typing import Any

from pydantic.errors import DictError
from pydantic.main import BaseModel

from arcenstuff.pydantic.errors import (
    InvalidModule,
    InvalidModuleFunction,
    MissingType,
    UnexpectedInstance,
)
from arcenstuff.pydantic.module_resolver import resolve_module_function

__all__ = [
    "ModuleClassifier",
]


@dataclass
class ModuleClassifier:
    type_class: type[BaseModel]
    type_field: str
    default_module: str
    function_name: str

    def __call__(self, value: Any) -> Any:
        # Make sure we have a dict.
        if not isinstance(value, dict):
            raise DictError()

        # Make sure type was specified.
        type_name = value.pop(self.type_field, None)  # type: ignore
        if not isinstance(type_name, str):
            raise MissingType(type_field=self.type_field)

        # Determine the module name.
        module_name = self.get_module_name(type_name)

        # Attempt to resolve the module function.
        try:
            func = resolve_module_function(module_name, self.function_name)

        # If it fails for any reason, wrap the error.
        except Exception as ex:
            raise InvalidModule(
                module_name=module_name, function_name=self.function_name
            ) from ex

        # Attempt to call the function to create the object.
        try:
            obj = func(value)

        # Allow only a restricted set of errors to propagate to Pydantic.
        except (TypeError, ValueError):
            raise

        # Any other types of errors are wrapped.
        except Exception as ex:
            raise InvalidModuleFunction(
                module_name=module_name, function_name=self.function_name
            ) from ex

        # Raise an error if the object is not of the expected type.
        if not isinstance(obj, self.type_class):
            raise UnexpectedInstance(
                expected_type=self.type_class,
                actual_type=type(obj),
                function_name=self.function_name,
                module_name=module_name,
            )

        return obj

    def get_module_name(self, type_name: str) -> str:
        # If it looks like a relative module, append it to the default module.
        if type_name.startswith("."):
            return f"{self.default_module}{type_name}"

        # Otherwise, if it looks like an absolute module name, use it directly.
        if "." in type_name:
            return type_name

        # Otherwise, use the default module as the parent.
        return f"{self.default_module}.{type_name}"
