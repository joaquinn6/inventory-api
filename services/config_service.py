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

  def restore_db(self, zip_file: BytesIO):
    try:
        # Asegurarse de que el puntero del archivo esté al inicio
      zip_file.seek(0)

      # Abrir el archivo ZIP desde el objeto en memoria
      with ZipFile(zip_file, 'r') as zip_ref:
        # Iterar por cada archivo dentro del ZIP
        for file_name in zip_ref.namelist():
          # Leer el contenido del archivo JSON
          with zip_ref.open(file_name) as json_file:
            data = json_util.loads(json_file.read().decode('utf-8'))

          # Determinar el nombre de la colección a partir del nombre del archivo
          collection_name = file_name.replace('.json', '')

          # Insertar los datos en la colección correspondiente
          collection = self._database[collection_name]
          # Limpiar la colección antes de restaurar los datos
          collection.delete_many({})
          if data:
            collection.insert_many(data)

      return {"status": "success", "message": "Restauración completada exitosamente."}
    except Exception as e:
      raise RuntimeError(f"Error al restaurar la base de datos: {e}") from e
