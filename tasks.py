import json
import os

import toml
from invoke import task


@task
def install_hooks(c):
    """Install git hooks."""
    c.run("pre-commit install")
    c.run("pre-commit install -t pre-push")


@task(aliases=["format"])
def black(c):
    """Format modules using black."""
    c.run("black cdk_chalice_lite/ tests/ tasks.py app.py cdk_app.py")


@task(aliases=["check-black"])
def check_formatting(c):
    """Check that files conform to black standards."""
    c.run("black --check cdk_chalice_lite/ tests/ tasks.py app.py cdk_app.py")


@task
def unit_tests(c):
    """Run unit tests via pytest."""
    c.run("pytest tests/")


@task(check_formatting, unit_tests)
def publish(c, username=None, password=None):
    """Publish to pypi."""

    username = username or os.getenv("PYPI_USERNAME")

    password = password or os.getenv("PYPI_PASSWORD")

    *_, latest_release = json.loads(
        c.run("qypi releases cdk-chalice-lite", hide=True).stdout
    )["cdk-chalice-lite"]

    latest_release_version = latest_release["version"]

    local_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

    if local_version == latest_release_version:
        print("local and release version are identical -- skipping publish")
    else:
        print(f"publishing chalice_cdk v{local_version}")
        c.run(
            f"poetry publish -u {username} -p '{password}' --build",
            pty=True,
            hide=True,
        )
