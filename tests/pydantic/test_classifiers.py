import pytest
from pydantic import ValidationError

from arcenstuff.pydantic.examples import Person


def test_person_from_str():
    Person.parse_obj("Alice")


def test_person_with_name():
    Person.parse_obj(
        {
            "name": "Alice",
        }
    )


def test_person_with_name_and_job():
    Person.parse_obj(
        {
            "name": "Alice",
            "job": {"type": "Engineer", "hours": 40},
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
            "job": {"type": "Teacher", "hours": 20},
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
