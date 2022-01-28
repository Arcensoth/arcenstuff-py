from abc import ABC, abstractmethod

from pydantic import BaseModel

from arcenstuff.pydantic import SubClassifier

__all__ = ("Job",)


class Job(BaseModel, ABC):
    hours: int

    @classmethod
    def __get_validators__(cls):
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
