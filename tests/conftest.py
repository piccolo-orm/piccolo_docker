import socket
from contextlib import suppress
from typing import Generator

import docker
import pytest
from docker.client import DockerClient
from docker.errors import NotFound
from docker.models.containers import Container
from faker import Faker

fake = Faker()


@pytest.fixture(scope="function")
def docker_client() -> DockerClient:
    """
    Client to share across tests
    """
    return docker.from_env()


@pytest.fixture(scope="function")
def container(docker_client: DockerClient) -> Container:
    # pylint: disable=redefined-outer-name
    """
    The container used in the tests
    """
    from dockerdb.commands.create import create

    container_name, _ = create()
    container = docker_client.containers.get(container_id=container_name)

    yield container

    with suppress(NotFound):
        container.remove(force=True)


@pytest.fixture(scope="function")
def unique_container_name(monkeypatch) -> Generator[str, None, None]:
    """
    Sets the value of UNIQUE_CONTAINER_NAME for the duration of each test
    """
    _unique_container_name = f"piccolo_postgres_{fake.safe_color_name()}"
    monkeypatch.setenv(name="UNIQUE_CONTAINER_NAME", value=_unique_container_name)
    yield _unique_container_name
    monkeypatch.undo()


@pytest.fixture(scope="function")
def pg_database(monkeypatch) -> Generator[str, None, None]:
    """
    Sets the value of PG_DATABASE for the duration of each test
    """
    _pg_database = f"piccolo_{fake.safe_color_name()}"
    monkeypatch.setenv(name="PG_DATABASE", value=_pg_database)
    yield _pg_database
    monkeypatch.undo()


@pytest.fixture(scope="function")
def pg_port(monkeypatch) -> Generator[str, None, None]:
    """
    Sets the value of PG_PORT for the duration of each test
    """
    sock = socket.socket()
    sock.bind(("", 0))
    available_port = sock.getsockname()[1]

    monkeypatch.setenv(name="PG_PORT", value=str(available_port))
    yield str(available_port)
    monkeypatch.undo()


@pytest.fixture(scope="function")
def pg_password(monkeypatch) -> Generator[str, None, None]:
    """
    Sets the value of PG_PASSWORD for the duration of each test
    """
    _pg_password = fake.password()
    monkeypatch.setenv(name="PG_PASSWORD", value=_pg_password)
    yield _pg_password
    monkeypatch.undo()


@pytest.fixture(scope="function")
def set_env(unique_container_name, pg_database, pg_port, pg_password) -> None:
    # pylint: disable=redefined-outer-name
    # pylint: disable=unused-argument
    """
    Collection fixture used for better readability in the tests
    """
    return
