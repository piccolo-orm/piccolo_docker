from os import getenv

from dotenv import load_dotenv
from faker import Faker

load_dotenv()

fake = Faker()

PG_DATABASE = getenv(key="PG_DATABASE", default="piccolo_database")
PG_HOST = "localhost"
PG_IMAGE_NAME = getenv(key="POSTGRES_IMAGE_NAME", default="postgres:latest")
PG_PASSWORD = getenv(key="PG_PASSWORD", default=fake.password())
PG_PORT = getenv(key="PG_PORT", default="5432")
PG_USER = "postgres"
UNIQUE_CONTAINER_NAME = getenv(
    key="UNIQUE_CONTAINER_NAME", default="piccolo_postgres_7677f8bd"
)
