import logging
import os

from piccolo.conf.apps import AppConfig

from dockerdb.commands.create import create
from dockerdb.commands.destroy import destroy
from dockerdb.commands.start import start
from dockerdb.commands.stop import stop

logger = logging.getLogger()

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

APP_CONFIG = AppConfig(
    app_name="dockerdb",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "migrations"),
    table_classes=[],
    migration_dependencies=[],
    commands=[create, destroy, start, stop],
)
