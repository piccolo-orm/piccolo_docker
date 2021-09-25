import pytest
from docker.client import DockerClient
from docker.errors import NotFound
from docker.models.containers import Container


def test_create(set_env, container: Container):
    # pylint: disable=unused-argument
    """
    Tests the create command
    """
    assert container
    assert isinstance(container, Container)


def test_destroy(set_env, container: Container, docker_client: DockerClient):
    # pylint: disable=unused-argument
    """
    Tests the destroy command
    """
    assert container

    from dockerdb.commands.destroy import destroy

    destroy()

    with pytest.raises(NotFound):
        docker_client.containers.get(container_id=container.name)


def test_start(set_env, container: Container, docker_client: DockerClient):
    # pylint: disable=unused-argument
    """
    Tests the start command
    """
    assert container
    container.stop()

    from dockerdb.commands.start import start

    start()

    assert container.status == "running"


def test_stop(set_env, container: Container, docker_client: DockerClient):
    # pylint: disable=unused-argument
    """
    Tests the stop command
    """
    assert container

    from dockerdb.commands.stop import stop

    stop()

    # getting the container again in order to assert their status after we stopped it
    _container = docker_client.containers.get(container_id=container.name)
    assert _container.status == "exited"
