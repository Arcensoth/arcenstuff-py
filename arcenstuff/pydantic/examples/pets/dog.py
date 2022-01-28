from typing import Any

from arcenstuff.pydantic.examples.pet import Pet


class Dog(Pet):
    # @implements Pet
    def get_noise(self) -> str:
        return "woof"


def create(value: Any) -> Pet:
    return Dog.parse_obj(value)
