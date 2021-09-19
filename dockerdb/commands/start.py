from dockerdb.repository import PiccoloDockerRepository


def start() -> None:
    """
    Starts the docker container.
    """
    piccolo_docker_repository = PiccoloDockerRepository()
    piccolo_docker_repository.start()
