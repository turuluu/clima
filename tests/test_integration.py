def test_version_detection_chain(isolated_cli_env, mock_package_metadata):
    from clima.schema import get_pkg_version
    
    # Should get version from package metadata
    assert get_pkg_version() == "1.0.0"
    
    # Remove package metadata to test fallback
    (isolated_cli_env / "myproject/pyproject.toml").write_text("""
[tool.poetry]
name = "test-cli"
version = "2.0.0"
    """)
    
    # Should get version from pyproject.toml
    assert get_pkg_version() == "2.0.0"