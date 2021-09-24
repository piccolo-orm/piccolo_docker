import nox

versions = [
    "3.8.2",
    "3.8.4",
    "3.8.5",
    "3.8.6",
    "3.8.7",
    "3.8.8",
    "3.8.9",
    "3.9.0",
    "3.9.2",
    "3.9.3",
    "3.9.4",
    "3.9.5",
    "3.9.6",
    "3.9.7",
]


@nox.session(python=versions)
def test(session):
    """Run pytest with the above python versions"""
    session.install("-r", "requirements.txt")
    session.run("pytest", "-vv", "tests")
