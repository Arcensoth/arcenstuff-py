import pytest
from pydantic import ValidationError

from arcenstuff.pydantic.errors import InvalidModule, MissingType, UnknownType
from arcenstuff.pydantic.examples import Job, Person, Pet


def test_job():
    Job.validate({"type": "Engineer", "hours": 40})


def test_job_with_missing_type():
    with pytest.raises(MissingType):
        Job.validate({"hours": 40})


def test_job_with_unknown_type():
    with pytest.raises(UnknownType):
        Job.validate({"type": "Foo", "hours": 40})


def test_pet():
    Pet.validate({"type": "cat", "name": "Boots"})


def test_pet_with_missing_type():
    with pytest.raises(MissingType):
        Pet.validate({"name": "Boots"})


def test_pet_with_invalid_type():
    with pytest.raises(InvalidModule):
        Pet.validate({"type": "parrot", "name": "Boots"})


def test_person_from_str():
    Person.validate("Alice")


def test_person_with_name():
    Person.validate(
        {
            "name": "Alice",
        }
    )


def test_person_with_name_and_job():
    Person.validate(
        {
            "name": "Alice",
            "job": {"type": "Engineer", "hours": 40},
        }
    )


def test_person_with_name_and_pets():
    Person.validate(
        {
            "name": "Bob",
            "pets": [
                {"type": "cat", "name": "Mitts"},
                {"type": "cat", "name": "Boots"},
            ],
        }
    )


def test_person_with_name_and_job_and_pet():
    Person.validate(
        {
            "name": "Carol",
            "job": {"type": "Teacher", "hours": 20},
            "pets": [{"type": "dog", "name": "Spot"}],
        }
    )


def test_person_with_missing_job_type():
    with pytest.raises(ValidationError):
        Person.validate(
            {
                "name": "Alice",
                "job": {"hours": 40},
            }
        )


def test_person_with_unknown_job_type():
    with pytest.raises(ValidationError):
        Person.validate(
            {
                "name": "Alice",
                "job": {"type": "Foo", "hours": 40},
            }
        )


def test_person_with_missing_pet_type():
    with pytest.raises(ValidationError):
        Person.validate(
            {
                "name": "Bob",
                "pets": [
                    {"name": "Mitts"},
                ],
            }
        )


def test_person_with_unknown_pet_type():
    with pytest.raises(ValidationError):
        Person.validate(
            {
                "name": "Bob",
                "pets": [
                    {"type": "parrot", "name": "Polly"},
                ],
            }
        )
