from abc import ABC, abstractmethod
from typing import Annotated, Any, Literal, Optional, Union

import pytest
from pydantic import BaseModel, Field, ValidationError

from arcenstuff.pydantic.normalizable_model import NormalizableModel

# @@ JOB


class JobBase(NormalizableModel, ABC):
    hours: int = 40

    @abstractmethod
    def get_title(self) -> str:
        ...


class Job(NormalizableModel):
    __root__: Annotated[Union["Engineer", "Teacher"], Field(discriminator="type")]

    @classmethod
    def normalize_input(cls, obj: Any) -> Any:
        if isinstance(obj, str):
            return dict(type=obj)
        return obj


class Engineer(JobBase):
    type: Literal["engineer"]

    # @implements Job
    def get_title(self) -> str:
        return "Engineer"


class Teacher(JobBase):
    type: Literal["teacher"]

    # @implements Job
    def get_title(self) -> str:
        return "Teacher"


Job.update_forward_refs()


# @@ PET


class PetBase(BaseModel, ABC):
    name: str

    @abstractmethod
    def get_noise(self) -> str:
        ...


class Pet(BaseModel):
    __root__: Annotated[Union["Cat", "Dog"], Field(discriminator="type")]


class Cat(PetBase):
    type: Literal["cat"]

    # @implements Pet
    def get_noise(self) -> str:
        return "meow"


class Dog(PetBase):
    type: Literal["dog"]

    # @implements Pet
    def get_noise(self) -> str:
        return "woof"


Pet.update_forward_refs()


# @@ PERSON


class Person(NormalizableModel):
    name: str
    job: Optional[Job]
    pets: Optional[list[Pet]]

    @classmethod
    def normalize_input(cls, obj: Any) -> Any:
        if isinstance(obj, str):
            return dict(name=obj)
        return obj


# @@ TESTS


def test_job():
    Job.parse_obj({"type": "engineer", "hours": 40})


def test_job_with_missing_type():
    with pytest.raises(ValidationError):
        Job.parse_obj({"hours": 40})


def test_job_with_missing_hours():
    Job.parse_obj({"type": "engineer"})


def test_job_with_unknown_type():
    with pytest.raises(ValidationError):
        Job.parse_obj({"type": "foo", "hours": 40})


def test_pet():
    Pet.parse_obj({"type": "cat", "name": "Boots"})


def test_pet_with_missing_type():
    with pytest.raises(ValidationError):
        Pet.parse_obj({"name": "Boots"})


def test_pet_with_invalid_type():
    with pytest.raises(ValidationError):
        Pet.parse_obj({"type": "parrot", "name": "Boots"})


def test_person_from_str():
    Person.parse_obj("Alice")


def test_person_with_name():
    Person.parse_obj(
        {
            "name": "Alice",
        }
    )


def test_person_with_name_and_flat_job():
    Person.parse_obj(
        {
            "name": "Alice",
            "job": "engineer",
        }
    )


def test_person_with_name_and_job():
    Person.parse_obj(
        {
            "name": "Alice",
            "job": {"type": "engineer", "hours": 40},
        }
    )


def test_person_with_name_and_pets():
    Person.parse_obj(
        {
            "name": "Bob",
            "pets": [
                {"type": "cat", "name": "Mitts"},
                {"type": "cat", "name": "Boots"},
            ],
        }
    )


def test_person_with_name_and_job_and_pet():
    Person.parse_obj(
        {
            "name": "Carol",
            "job": {"type": "teacher", "hours": 20},
            "pets": [{"type": "dog", "name": "Spot"}],
        }
    )


def test_person_with_missing_job_type():
    with pytest.raises(ValidationError):
        Person.parse_obj(
            {
                "name": "Alice",
                "job": {"hours": 40},
            }
        )


def test_person_with_unknown_job_type():
    with pytest.raises(ValidationError):
        Person.parse_obj(
            {
                "name": "Alice",
                "job": {"type": "Foo", "hours": 40},
            }
        )


def test_person_with_missing_pet_type():
    with pytest.raises(ValidationError):
        Person.parse_obj(
            {
                "name": "Bob",
                "pets": [
                    {"name": "Mitts"},
                ],
            }
        )


def test_person_with_unknown_pet_type():
    with pytest.raises(ValidationError):
        Person.parse_obj(
            {
                "name": "Bob",
                "pets": [
                    {"type": "parrot", "name": "Polly"},
                ],
            }
        )
