from datetime import datetime


def divide_list(value):
  if isinstance(value[0], str):
    return value[0].split(",")
  return value


def divide_format_query_dates(value):
  fechas = divide_list(value)
  fechas[0] = datetime.fromisoformat(fechas[0])
  fechas[1] = datetime.fromisoformat(fechas[1])
  return fechas
