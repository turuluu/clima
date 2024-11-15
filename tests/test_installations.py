import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def isolated_cli_env():
    """Creates an isolated environment with a temporary installation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        old_cwd = Path.cwd()
        tmp_path = Path(tmpdir)
        
        # Create fake project structure
        (tmp_path / "myproject").mkdir()
        (tmp_path / "myproject/pyproject.toml").write_text("""
[tool.poetry]
name = "test-cli"
version = "1.0.0"
        """)
        
        try:
            os.chdir(tmp_path)
            yield tmp_path
        finally:
            os.chdir(old_cwd)

@pytest.fixture
def mock_package_metadata(monkeypatch):
    """Mocks package metadata for version testing"""
    def mock_version(package_name):
        return "1.0.0"
    monkeypatch.setattr('importlib.metadata.version', mock_version)
