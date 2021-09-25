## piccolo_docker
Easily spin up databases for your Piccolo project using Docker

### Requirements
- [Install poetry](https://python-poetry.org/docs/#installation)
- [Install docker](https://docs.docker.com/get-docker/)

### Setup

- Clone this repo
- Open `.env`
- Add database name
- Add password. If you don't a random password will be generated that can be seen with `docker inspect --format="{{index .Config.Env 0}}" your_container_name`
- Change the unique container name if you don't want to use the default
- To add use this app to your Piccolo project, add it to your `AppRegistry` in `piccolo_conf.py` with: `APP_REGISTRY = AppRegistry(apps=["piccolo_docker.user.piccolo_app"])`


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

For the `nox` tests you'll probably need pyenv and all versions of python that are declared inside `noxfile.py`

### Improvements
- Test against multiple versions of postgres
- Test against more versions of python.


### To Contribute
- Fork the repo
- Have a look around
- Make sure you install [pre-commit](https://pre-commit.com/)
- Do a small PR for early feedback
- Enjoy!
