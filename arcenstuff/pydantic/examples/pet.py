from abc import ABC, abstractmethod

from arcenstuff.pydantic import ModuleClassifier, TransformableModel

__all__ = [
    "Pet",
]


class Pet(TransformableModel, ABC):
    name: str

    @classmethod
    def __transformers__(cls):
        yield ModuleClassifier(
            cls,
            type_field="type",
            default_module="arcenstuff.pydantic.examples.pets",
            function_name="create",
        )

    @abstractmethod
    def get_noise(self) -> str:
        ...
