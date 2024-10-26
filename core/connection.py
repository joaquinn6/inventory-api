from pymongo import MongoClient
from pymongo.database import Database
from core.var_env import DATABASE


class MongoConnectionProvider:
  """Conexión a la base de datos"""
  __instance = None

  @classmethod
  def connect(cls, uri):
    """
        Establece la conexión con el servidor de mongodb y crea el connection provider
        :param uri: Cadena de conexión al servidor
        :param main_database: Nombre de la base de datos principal
        """
    connection = MongoClient(host=uri)
    cls.__instance = MongoConnectionProvider(connection)

  @classmethod
  def get_instance(cls):
    """
        Devuelve la instancia única del conexión provider
        :type: core.connections.MongoConnectionProvider
        """
    return cls.__instance

  def __init__(self, connection):

    self.__connection = connection

  def __del__(self):
    self.__connection.close()

  def close(self):
    """Cierre de la conexión"""
    self.__connection.close()

  def get_database(self, database_name: str) -> Database:
    """
        Devuelve la instancia a la base de datos
        :return: Base de datos
        :type: pymongo.database.Database
        """
    return self.__connection.get_database(database_name)

  def get_database_main(self) -> Database:
    """Devuelve la instancia de la base de datos"""
    return self.get_database(DATABASE)
