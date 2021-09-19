from os import getenv

from dotenv import load_dotenv

load_dotenv()

PG_DATABASE = getenv(key="PG_DATABASE", default="piccolo_database")
PG_HOST = "localhost"
PG_IMAGE_NAME = getenv(key="POSTGRES_IMAGE_NAME", default="postgres:latest")
PG_PASSWORD = getenv(key="PG_PASSWORD")
PG_PORT = getenv(key="PG_PORT", default="5432")
PG_USER = "postgres"
UNIQUE_CONTAINER_NAME = "piccolo_postgres_7677f8bd"
UNIQUE_CONTAINER_LABELS = {"f2c62b9d": "2eb8705fda65"}
