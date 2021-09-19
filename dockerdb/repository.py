import logging
from time import sleep

import asyncpg
import docker
from docker.client import DockerClient
from docker.errors import APIError, NotFound
from docker.models.containers import Container

from dockerdb.constants import (
    PG_DATABASE,
    PG_HOST,
    PG_IMAGE_NAME,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
    UNIQUE_CONTAINER_LABELS,
    UNIQUE_CONTAINER_NAME,
)


class PiccoloDockerRepository:
    """
    Manage the life of a piccolo postgres container.
    """

    def __init__(self):
        self.docker_client: DockerClient = docker.from_env()

    @property
    def container_exists(self) -> bool:
        """
        Checks if container exists based on the unique container name
        TODO: Maybe allow more complex identifications later with labels
        :return: True | False
        :rtype: bool
        """
        return (
            self.docker_client.containers.list(filters={"name": UNIQUE_CONTAINER_NAME})
            != []
        )

    @property
    def container_is_running(self) -> bool:
        """
        Checks if the container is running
        :return: True | False
        :rtype: bool
        """
        return self.container.status.lower() == "running"

    @property
    def container_name(self) -> str:
        """
        Here for completeness and forward compatibility as we work to support multiple containers.
        If you want to change the value please amend constants.py
        :return: postgres container name
        :rtype: str
        """
        return UNIQUE_CONTAINER_NAME

    @property
    def container(self) -> Container:
        """
        Returns a container object that can be used in container operations
        :return: container object
        :rtype: Container
        """
        return self.docker_client.containers.get(container_id=self.container_name)

    def create_container(self) -> None:
        """
        Creates a new container to host the piccolo database(s)
        :return: None
        :rtype: None
        """

        if self.container_exists and self.container_is_running:
            logging.info("Container %s is running. Nothing to do.", self.container_name)
            return

        logging.info("Getting %s", PG_IMAGE_NAME)
        self.docker_client.images.get(name=PG_IMAGE_NAME)

        try:

            logging.info("Starting postgres container")
            self.docker_client.containers.run(
                image=PG_IMAGE_NAME,
                ports={f"{PG_PORT}/tcp": f"{PG_PORT}/tcp"},
                name=self.container_name,
                hostname="postgres",
                environment={
                    "POSTGRES_PASSWORD": PG_PASSWORD,
                    "POSTGRES_HOST_AUTH_METHOD": "trust",
                },
                detach=True,
                labels=UNIQUE_CONTAINER_LABELS,
            )
            logging.info("Container %s started", UNIQUE_CONTAINER_NAME)

        except APIError as api_error:

            if api_error.status_code == 409:
                logging.error(
                    "Remove the container before re-creating it. Use 'piccolo dockerdb destroy'"
                )
            else:
                raise APIError from api_error

    async def create_database(self) -> str:
        """
        Does some basic checking and creates a new database and tables (if present)
        :return: database_name
        :rtype: str
        """

        # Check if the default database name has been changed
        if PG_DATABASE in ["postgres", ""]:
            raise ValueError("Did you forget to set a new database name in .env?")

        is_ready_exit_code = 1
        while is_ready_exit_code != 0:
            is_ready_exit_code = self.container.exec_run(cmd="pg_isready").exit_code
            if is_ready_exit_code != 0:
                logging.info("Waiting for postgres to start...")
                sleep(1)

        connection = await asyncpg.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
        )

        # Check the database name doesn't exist
        result = await connection.fetchrow(
            "select datname from pg_database where datname = $1", PG_DATABASE
        )
        if not result:
            logging.info("Creating %s database...", PG_DATABASE)
            await connection.execute(f"create database {PG_DATABASE}")
            logging.info("Created %s database.", UNIQUE_CONTAINER_NAME)
        elif list(result.values()) == [PG_DATABASE]:
            logging.info("Database % exists. Nothing to do.", UNIQUE_CONTAINER_NAME)

        return PG_DATABASE

    def destroy(self) -> None:
        """
        Destroys the container. This is not reversible.
        """
        try:
            self.container.remove(force=True)
            logging.info("Container %s is destroyed forever.", UNIQUE_CONTAINER_NAME)
        except NotFound as not_found:
            if not_found.status_code == 404:
                logging.warning(
                    "Container %s does not exist. Nothing to destroy.",
                    UNIQUE_CONTAINER_NAME,
                )
            else:
                raise NotFound from not_found

    def start(self) -> None:
        """
        Starts the container if it exists and is not running
        :return: None
        :rtype: None
        """
        if not self.container_exists:
            logging.warning(
                "Container %s does not exist. Did you mean 'piccolo dockerdb create'?",
                UNIQUE_CONTAINER_NAME,
            )

        if not self.container_is_running:
            self.container.start()
            logging.info("Container %s has started.", UNIQUE_CONTAINER_NAME)
        else:
            logging.info(
                "Container %s is running. Nothing to do.", UNIQUE_CONTAINER_NAME
            )

    def stop(self):
        """
        Stops the container if it exists and is running
        :return: None
        :rtype: None
        """
        if self.container_is_running:
            self.container.stop()
            logging.info("Container %s has stopped.", UNIQUE_CONTAINER_NAME)
        else:
            logging.info(
                "Container %s is not running. Nothing to do.", UNIQUE_CONTAINER_NAME
            )
