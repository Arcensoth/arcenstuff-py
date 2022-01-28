from typing import Any

from arcenstuff.pydantic.examples.pet import Pet


class Cat(Pet):
    # @implements Pet
    def get_noise(self) -> str:
        return "meow"


def create(value: Any) -> Pet:
    return Cat.parse_obj(value)
