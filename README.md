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
- Change the unique container name if you don't want to use the default

### Usage
- `piccolo dockerdb create`
creates new postgres container with your piccolo database.

- `piccolo dockerdb stop`
stops the docker container.

- `piccolo dockerdb start`
starts the docker container.

- `piccolo dockerdb destroy`
destroys the docker container. This is irreversible.

### Tests
Simply run:
`pytest -vv tests/`

### Improvements
- Test against multiple versions of postgres
- Test against multiple versions of python

### To Contribute
- Fork the repo
- Have a look around
- Make sure you install [pre-commit](https://pre-commit.com/)
- Do a small PR for early feedback
- Enjoy!
