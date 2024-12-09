from typing import Union, Tuple


def parse_amount_query(item: Union[str, Tuple[int, str], Tuple[int, int]]) -> Union[Tuple[int, str], Tuple[int, int]]:
  if isinstance(item, list):
    parts = item[0].split(",")
    if len(parts) == 2:
      try:
        if parts[1].isdigit():
          return int(parts[0]), int(parts[1])
        return int(parts[0]), parts[1]
      except ValueError as exc:
        raise ValueError(
            "Invalid format for item. Expected 'int,str' or 'int,int'.") from exc
    raise ValueError(
        "Item must be a string in the format 'int,str' or 'int,int'.")
  return item
