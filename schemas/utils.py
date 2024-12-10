from datetime import datetime


def divide_list(value):
  if isinstance(value[0], str):
    return value[0].split(",")
  return value


def divide_format_query_dates(value):
  fechas = divide_list(value)
  fechas[0] = datetime.strptime(
      fechas[0], "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
  fechas[1] = datetime.strptime(
      fechas[1], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
  return fechas
