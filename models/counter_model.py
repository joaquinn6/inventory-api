from pydantic import Field

from models.entity import Entity


class Counter(Entity):
  name: str = Field(...)
  counter: int = Field(default=0)
