## piccolo_docker
Easily spin up databases for your Piccolo project using Docker

### Requirements
- [Install poetry](https://python-poetry.org/docs/#installation)
- [Install docker](https://docs.docker.com/get-docker/)

### Setup

- Clone this repo
- Open `.env`
- Add database name
- Add password

### Usage
- `piccolo dockerdb create`
creates new postgres container with your piccolo database.

- `piccolo dockerdb stop`
stops the docker container.

- `piccolo dockerdb start`
starts the docker container.

- `piccolo dockerdb destroy`
destroys the docker container. This is irreversible.

### Improvements
- Test against multiple versions of postgres
- Test against multiple versions of python
