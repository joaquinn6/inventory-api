"""Archivo de variables de entorno"""
import os
from dotenv import load_dotenv

load_dotenv(r'.config\.env')

DATABASE = os.getenv('DB_NAME')
MONGO_URI = os.getenv('MONGO_URI')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = os.getenv('SECRET_KEY')
