import nox
from nox_poetry import session

nox.options.sessions = "lint", "tests"


@session(python=["3.9"])
def tests(session):
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov")


locations = "src", "tests", "noxfile.py"


@session(python=["3.9"])
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-alphabetize", "flake8-black", "flake8-bugbear")
    session.run("flake8", *args)


@session(python=["3.9"])
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
