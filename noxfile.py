import nox

@nox.session
def tests(session):
    """Run the test suite."""
    session.run("poetry", "install", "--no-root", "--sync", "--with", "dev", external=True)
    session.run("poetry", "run", "pytest", "tests", "-s", external=True)
