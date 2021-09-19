# piccolo_conf.py
import logging

from asyncpg.exceptions import InvalidCatalogNameError
from piccolo.conf.apps import AppRegistry
from piccolo.engine import PostgresEngine
from piccolo.engine.sqlite import SQLiteEngine

from dockerdb.constants import PG_DATABASE, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER

try:
    DB = PostgresEngine(
        config={
            "database": PG_DATABASE,
            "host": PG_HOST,
            "password": PG_PASSWORD,
            "port": PG_PORT,
            "user": PG_USER,
        }
    )
except ConnectionRefusedError:
    # Warning: Unable to connect to database - [Errno 61] Connection refused
    logging.info(
        msg="Dockerized postgres not yet spun up. Please ignore earlier connection warning."
    )
    DB = SQLiteEngine(path=".ignore.sqlite")
    DB.remove_db_file()
except InvalidCatalogNameError:
    # Warning: Unable to fetch server version: database "my_database" does not exist
    logging.info(
        msg="Creating database in next step. Please ignore earlier piccolo warning."
    )
    PG_DATABASE = "postgres"

APP_REGISTRY = AppRegistry(apps=["dockerdb.app"])
