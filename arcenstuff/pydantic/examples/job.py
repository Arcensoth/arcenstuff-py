from abc import ABC, abstractmethod

from arcenstuff.pydantic import SubClassifier, TransformableModel

__all__ = ("Job",)


class Job(TransformableModel, ABC):
    hours: int

    @classmethod
    def __transformers__(cls):
        yield SubClassifier(cls, type_field="type")

    @abstractmethod
    def get_title(self) -> str:
        ...


class Engineer(Job):
    # @implements Job
    def get_title(self) -> str:
        return "Engineer"


class Teacher(Job):
    # @implements Job
    def get_title(self) -> str:
        return "Teacher"
