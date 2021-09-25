import logging
from time import sleep

import asyncpg
import docker
from docker.errors import APIError, NotFound
from docker.models.containers import Container

from dockerdb.constants import (
    PG_DATABASE,
    PG_HOST,
    PG_IMAGE_NAME,
    PG_PASSWORD,
    PG_PORT,
    PG_USER,
    UNIQUE_CONTAINER_NAME,
)


class PiccoloDockerRepository:
    """
    Manage the life of a piccolo postgres container.
    """

    def __init__(
        self,
        pg_database: str = PG_DATABASE,
        pg_host: str = PG_HOST,
        pg_image_name: str = PG_IMAGE_NAME,
        pg_password: str = PG_PASSWORD,
        pg_port: str = PG_PORT,
        pg_user: str = PG_USER,
        unique_container_name: str = UNIQUE_CONTAINER_NAME,
        auto_remove: bool = False,
    ):
        """
        Parameterised in order to facilitate testing.
        Some of the values are env var/constants that are monkeypatched in the tests
        """
        self.docker_client = docker.from_env()
        self.pg_database = pg_database
        self.pg_host = pg_host
        self.pg_image_name = pg_image_name
        self.pg_password = pg_password
        self.pg_port = pg_port
        self.pg_user = pg_user
        self.unique_container_name = unique_container_name
        self.auto_remove = auto_remove

    @property
    def container_exists(self) -> bool:
        """
        Checks if container exists based on the unique container name
        TODO: Maybe allow more complex identifications later with labels
        :return: True | False
        :rtype: bool
        """
        return (
            self.docker_client.containers.list(
                filters={"name": self.unique_container_name}
            )
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
        return self.unique_container_name

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

        logging.info("Getting %s", self.pg_image_name)
        self.docker_client.images.get(name=self.pg_image_name)

        try:

            logging.info("Starting postgres container")
            self.docker_client.containers.run(
                image=self.pg_image_name,
                ports={f"{self.pg_port}/tcp": f"{self.pg_port}/tcp"},
                name=self.container_name,
                hostname="postgres",
                environment={
                    "POSTGRES_PASSWORD": self.pg_password,
                    "POSTGRES_HOST_AUTH_METHOD": "trust",
                    "PGPORT": self.pg_port,
                },
                detach=True,
                auto_remove=self.auto_remove,
            )
            logging.info("Container %s started", self.unique_container_name)

        except APIError as api_error:

            if api_error.status_code == 409:
                logging.error(
                    "Remove the container before re-creating it. Use 'piccolo dockerdb destroy'"
                )
            if api_error.status_code == 500:
                logging.error(
                    "Port %s is in use. Try 'piccolo dockerdb destroy'",
                    self.pg_port,
                )
            else:
                raise APIError(api_error)

    async def create_database(self) -> str:
        """
        Does some basic checking and creates a new database and tables (if present)
        :return: database_name
        :rtype: str
        """

        # Check if the default database name has been changed
        if self.pg_database in ["postgres", ""]:
            raise ValueError("Did you forget to set a new database name in .env?")

        is_ready_exit_code = 1
        while is_ready_exit_code != 0:
            is_ready_exit_code = self.container.exec_run(cmd="pg_isready").exit_code
            if is_ready_exit_code != 0:
                logging.info("Waiting for postgres to start...")
                sleep(1)

        connection = await asyncpg.connect(
            host=self.pg_host,
            port=self.pg_port,
            user=self.pg_user,
            password=self.pg_password,
        )

        # Check the database name doesn't exist
        result = await connection.fetchrow(
            "select datname from pg_database where datname = $1", self.pg_database
        )
        if not result:
            logging.info("Creating %s database...", self.pg_database)
            await connection.execute(f"create database {self.pg_database}")
            logging.info("Created %s database.", self.unique_container_name)
        elif list(result.values()) == [self.pg_database]:
            logging.info(
                "Database % exists. Nothing to do.", self.unique_container_name
            )

        return self.pg_database

    def destroy(self) -> None:
        """
        Destroys the container. This is not reversible.
        """
        try:
            self.container.remove(force=True)
            logging.info(
                "Container %s is destroyed forever.", self.unique_container_name
            )
        except NotFound as not_found:
            if not_found.status_code == 404:
                logging.warning(
                    "Container %s does not exist. Nothing to destroy.",
                    self.unique_container_name,
                )
            else:
                raise NotFound(not_found)

    def start(self) -> None:
        """
        Starts the container if it exists and is not running
        :return: None
        :rtype: None
        """
        if not self.container_exists:
            logging.warning(
                "Container %s does not exist. Did you mean 'piccolo dockerdb create'?",
                self.unique_container_name,
            )

        if not self.container_is_running:
            self.container.start()
            logging.info("Container %s has started.", self.unique_container_name)
        else:
            logging.info(
                "Container %s is running. Nothing to do.", self.unique_container_name
            )

    def stop(self):
        """
        Stops the container if it exists and is running
        :return: None
        :rtype: None
        """
        if self.container_is_running:
            self.container.stop()
            logging.info("Container %s has stopped.", self.unique_container_name)
        else:
            logging.info(
                "Container %s is not running. Nothing to do.",
                self.unique_container_name,
            )
