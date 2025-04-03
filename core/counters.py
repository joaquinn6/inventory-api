from repositories.counter_repository import CounterRepository


class CounterGenerator:

  def __init__(self):
    self._repo = CounterRepository()

  def generate(self, name: str, prefix: str,  max_digits: int = 8) -> str:
    sequence = self._repo.find_one_and_upsert(
        {"name": name},
        {'$inc': {'counter': 1}},
        'after'
    )
    number = sequence.counter.rjust(max_digits - len(prefix), '0')
    return f"{prefix}{number}"
