"""Archivo conexión a base de datos mongodb"""
from core.connection import MongoConnectionProvider
from core.var_env import MONGO_URI

MongoConnectionProvider.connect(MONGO_URI)
db = MongoConnectionProvider.get_instance().get_database_main()
