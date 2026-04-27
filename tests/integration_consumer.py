"""Integration consumer script for nox.

Run from a temp dir (outside the source tree) with clima installed as a wheel.
Exercises: import, version subcommand, --cwd, and config discovery.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_cli(script_path, args, cwd=None, env=None):
    """Run a clima script and return (returncode, stdout, stderr)."""
    merged_env = {**os.environ, **(env or {})}
    result = subprocess.run(
        [sys.executable, str(script_path)] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=merged_env,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def test_import():
    """clima is importable and core objects exist."""
    from clima import c, Schema
    assert callable(c), "c should be callable"
    assert isinstance(Schema, type), "Schema should be a class"
    print("PASS: import")


def test_version(script_path, tmpdir):
    """version subcommand prints something non-empty."""
    rc, out, err = run_cli(script_path, ["version"], cwd=tmpdir)
    assert rc == 0, f"version failed (rc={rc}): {err}"
    assert out, f"version output is empty"
    print(f"PASS: version -> {out!r}")


def test_config_discovery(tmpdir):
    """Config file in cwd is picked up by clima."""
    # Write a minimal clima script
    script = Path(tmpdir) / "cfgtest.py"
    script.write_text(
        "from clima import c, Schema\n"
        "\n"
        "class C(Schema):\n"
        "    greeting: str = 'default'\n"
        "\n"
        "c: C = c\n"
        "\n"
        "@c\n"
        "class Cli:\n"
        "    def show(self):\n"
        "        print(c.greeting)\n"
    )

    # Write a config that overrides the default
    cfg = Path(tmpdir) / "cfgtest.cfg"
    cfg.write_text("[Clima]\ngreeting = from_config\n")

    rc, out, err = run_cli(script, ["show"], cwd=tmpdir)
    assert rc == 0, f"config discovery failed (rc={rc}): {err}"
    assert "from_config" in out, f"expected 'from_config' in output, got: {out!r}"
    print(f"PASS: config discovery -> {out!r}")


def test_cwd(tmpdir):
    """--cwd points config discovery to a different directory."""
    cfg_dir = Path(tmpdir) / "cfgdir"
    cfg_dir.mkdir()
    script_dir = Path(tmpdir) / "scripts"
    script_dir.mkdir()

    # Write a config in cfg_dir
    cfg = cfg_dir / "cwdtest.cfg"
    cfg.write_text("[Clima]\nmsg = from_cwd\n")

    # Write script in script_dir
    script = script_dir / "cwdtest.py"
    script.write_text(
        "from pathlib import Path\n"
        "from clima import c, Schema\n"
        "\n"
        "class C(Schema):\n"
        "    cwd: Path = Path('.')\n"
        "    msg: str = 'default'\n"
        "\n"
        "c: C = c\n"
        "\n"
        "@c\n"
        "class Cli:\n"
        "    def show(self):\n"
        "        print(c.msg)\n"
    )

    rc, out, err = run_cli(
        script, ["show", "--cwd", str(cfg_dir)], cwd=script_dir
    )
    assert rc == 0, f"--cwd failed (rc={rc}): {err}"
    assert "from_cwd" in out, f"expected 'from_cwd' in output, got: {out!r}"
    print(f"PASS: --cwd -> {out!r}")


def main():
    # Write a minimal script for version testing
    with tempfile.TemporaryDirectory() as tmpdir:
        script = Path(tmpdir) / "vertest.py"
        script.write_text(
            "from clima import c, Schema\n"
            "\n"
            "class C(Schema):\n"
            "    name: str = 'world'\n"
            "\n"
            "@c\n"
            "class Cli:\n"
            "    def greet(self):\n"
            "        print(f'hello {C.name}')\n"
        )

        test_import()
        test_version(script, tmpdir)
        test_config_discovery(tmpdir)
        test_cwd(tmpdir)

    print("\nAll integration checks passed.")


if __name__ == "__main__":
    main()
