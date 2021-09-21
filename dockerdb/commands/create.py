import asyncio
from typing import Tuple

from docker.models.containers import Container

from dockerdb.repository import PiccoloDockerRepository


def create(auto_remove: bool = False) -> Tuple[str, str]:
    """
    Creates a database inside a docker container
    :return: container name, database name
    :rtype: Tuple[str, str]
    """
    piccolo_docker_repository = PiccoloDockerRepository(auto_remove=auto_remove)

    piccolo_docker_repository.create_container()

    container: Container = piccolo_docker_repository.container
    database_name: str = ""

    if container:
        loop = asyncio.get_event_loop()
        database_name = loop.run_until_complete(
            piccolo_docker_repository.create_database()
        )

    return container.name, database_name
