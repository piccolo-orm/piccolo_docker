from dockerdb.repository import PiccoloDockerRepository


def destroy() -> None:
    """
    Destroys the docker container. This is irreversible.
    """
    piccolo_docker_repository = PiccoloDockerRepository()
    piccolo_docker_repository.destroy()
