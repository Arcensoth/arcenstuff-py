from abc import ABC, abstractmethod

from pydantic import BaseModel

from arcenstuff.pydantic import ModuleClassifier

__all__ = ("Pet",)


class Pet(BaseModel, ABC):
    name: str

    @classmethod
    def __get_validators__(cls):
        yield ModuleClassifier(
            cls,
            type_field="type",
            default_module="arcenstuff.pydantic.examples.pets",
            function_name="create",
        )

    @abstractmethod
    def get_noise(self) -> str:
        ...
