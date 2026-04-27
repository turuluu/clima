import os
import tempfile

import nox


@nox.session
def tests(session):
    """Run the test suite."""
    session.run("poetry", "install", "--no-root", "--sync", "--with", "dev", external=True)
    session.run("poetry", "run", "pytest", "tests", "-s", external=True)


PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]


@nox.session(python=PYTHON_VERSIONS)
def multi_python(session):
    """Run the test suite across multiple Python versions."""
    session.run("poetry", "install", "--no-root", "--sync", "--with", "dev", external=True)
    session.run("poetry", "run", "pytest", "tests", "-s", external=True)


@nox.session
def integration(session):
    """Build wheel, install into clean venv, run consumer script from temp dir."""
    session.run("poetry", "build", "-f", "wheel", external=True)

    # Find the built wheel
    dist_dir = os.path.join(session.invoked_from, "dist")
    wheels = sorted(
        (f for f in os.listdir(dist_dir) if f.endswith(".whl")),
        key=lambda f: os.path.getmtime(os.path.join(dist_dir, f)),
        reverse=True,
    )
    if not wheels:
        session.error("No wheel found in dist/")
    wheel_path = os.path.join(dist_dir, wheels[0])

    session.install(wheel_path)

    # Run consumer script from a temp dir (outside the source tree)
    consumer = os.path.join(session.invoked_from, "tests", "integration_consumer.py")
    with tempfile.TemporaryDirectory() as tmpdir:
        session.run("python", consumer, env={"HOME": os.environ.get("HOME", "")}, cwd=tmpdir)
