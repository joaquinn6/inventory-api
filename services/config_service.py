from io import BytesIO
from zipfile import ZipFile
from bson import json_util


class ConfigService():
  def __init__(self, database) -> None:
    self._database = database

  def create_backup(self) -> BytesIO:
    try:
      memory_file = BytesIO()

      with ZipFile(memory_file, 'w') as zip_file:
        for collection_name in self._database.list_collection_names():
          collection = self._database[collection_name]
          data = list(collection.find())
          zip_file.writestr(f"{collection_name}.json", json_util.dumps(data))
      memory_file.seek(0)

      return memory_file
    except Exception as exc:
      raise RuntimeError(f"Error al crear el backup: {exc}") from exc
