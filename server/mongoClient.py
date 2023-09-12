import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_DATABASE")
db_port = os.environ.get("DB_PORT")

# Verifica si todas las variables de entorno necesarias están configuradas
if not all([db_host, db_user, db_password, db_database, db_port]):
    raise Exception("Faltan variables de entorno para la conexión a MongoDB")

# Crea la URI de conexión a MongoDB
mongo_uri = f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource={db_database}&authMechanism=SCRAM-SHA-256"

# Crea un cliente de MongoDB
mongoConnection = MongoClient(mongo_uri)
db = mongoConnection[db_database]