from models.counter_model import Counter
from repositories.base import RepositoryBase


class CounterRepository(RepositoryBase[Counter]):

  def __init__(self) -> None:
    super().__init__('counters', Counter.from_dict)
