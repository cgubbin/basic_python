"""Defines the sessions for Nox."""

import nox
from nox_poetry import Session, session

nox.options.sessions = "lint", "pyre", "tests", "typeguard"

package = "test_environment"


@session(python=["3.9"])
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install("pytest", "pytest-cov")
    session.install(".")
    session.run("pytest", "--cov")


locations = "src", "tests", "noxfile.py", "docs/conf.py"


@session(python=["3.9"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-alphabetize",
        "flake8-annotations",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "darglint",
    )
    session.run("flake8", *args)


@session(python=["3.9"])
def black(session: Session) -> None:
    """Re-format using Black."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=["3.9"])
def pyre(session: Session) -> None:
    """Typecheck statically using Pyre."""
    import site
    import os

    search_path = site.getsitepackages()[0]
    repo_directory = os.getcwd()
    session.install("pyre-check")
    session.run(
        "pyre", "--dot-pyre-directory", repo_directory, "--search-path", search_path
    )


@session(python=["3.9"])
def typeguard(session: Session) -> None:
    """Typecheck at runtime using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    session.install("typeguard", "pytest")
    session.run("pytest", f"--typeguard-packages={package}", *args)


@session(python=["3.9"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    session.install("xdoctest", "pygments")
    session.install(".")
    session.run("python", "-m", "xdoctest", package, *args)


@session(python=["3.9"])
def docs(session: Session) -> None:
    """Build the docs using Sphinx."""
    session.install("sphinx", "sphinx-autodoc-typehints")
    session.run("sphinx-build", "docs", "docs/_build")
