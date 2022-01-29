import pytest
from pydantic import ValidationError

from arcenstuff.pydantic.errors import InvalidModule, MissingType, UnknownType
from arcenstuff.pydantic.examples import Job, Person, Pet


def test_job():
    Job.transform({"type": "Engineer", "hours": 40})


def test_job_with_missing_type():
    with pytest.raises(MissingType):
        Job.transform({"hours": 40})


def test_job_with_unknown_type():
    with pytest.raises(UnknownType):
        Job.transform({"type": "Foo", "hours": 40})


def test_pet():
    Pet.transform({"type": "cat", "name": "Boots"})


def test_pet_with_missing_type():
    with pytest.raises(MissingType):
        Pet.transform({"name": "Boots"})


def test_pet_with_invalid_type():
    with pytest.raises(InvalidModule):
        Pet.transform({"type": "parrot", "name": "Boots"})


def test_person_from_str():
    Person.transform("Alice")


def test_person_with_name():
    Person.transform(
        {
            "name": "Alice",
        }
    )


def test_person_with_name_and_job():
    Person.transform(
        {
            "name": "Alice",
            "job": {"type": "Engineer", "hours": 40},
        }
    )


def test_person_with_name_and_pets():
    Person.transform(
        {
            "name": "Bob",
            "pets": [
                {"type": "cat", "name": "Mitts"},
                {"type": "cat", "name": "Boots"},
            ],
        }
    )


def test_person_with_name_and_job_and_pet():
    Person.transform(
        {
            "name": "Carol",
            "job": {"type": "Teacher", "hours": 20},
            "pets": [{"type": "dog", "name": "Spot"}],
        }
    )


def test_person_with_missing_job_type():
    with pytest.raises(ValidationError):
        Person.transform(
            {
                "name": "Alice",
                "job": {"hours": 40},
            }
        )


def test_person_with_unknown_job_type():
    with pytest.raises(ValidationError):
        Person.transform(
            {
                "name": "Alice",
                "job": {"type": "Foo", "hours": 40},
            }
        )


def test_person_with_missing_pet_type():
    with pytest.raises(ValidationError):
        Person.transform(
            {
                "name": "Bob",
                "pets": [
                    {"name": "Mitts"},
                ],
            }
        )


def test_person_with_unknown_pet_type():
    with pytest.raises(ValidationError):
        Person.transform(
            {
                "name": "Bob",
                "pets": [
                    {"type": "parrot", "name": "Polly"},
                ],
            }
        )
