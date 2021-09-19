from dockerdb.repository import PiccoloDockerRepository


def stop() -> None:
    """
    Stops the docker container.
    """
    piccolo_docker_repository = PiccoloDockerRepository()
    piccolo_docker_repository.stop()
