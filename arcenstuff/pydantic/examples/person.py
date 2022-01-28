from typing import Optional

from pydantic import BaseModel

from .job import Job
from .pet import Pet

__all__ = ("Person",)


class Person(BaseModel):
    name: str
    job: Optional[Job]
    pets: Optional[list[Pet]]
