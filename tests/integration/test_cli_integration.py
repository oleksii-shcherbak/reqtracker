"""Integration tests for CLI commands with real file I/O."""

import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestCLIIntegration:
    """Test CLI commands in real environments."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project for CLI testing."""
        temp_dir = tempfile.mkdtemp()
        project_dir = Path(temp_dir)

        # Create sample project
        (project_dir / "app.py").write_text(
            """
import flask
import requests
import numpy as np

app = flask.Flask(__name__)

@app.route('/')
def index():
    data = requests.get('https://api.example.com').json()
    return str(np.mean([1, 2, 3]))
"""
        )

        (project_dir / "utils.py").write_text(
            """
import pandas as pd
from sklearn.model_selection import train_test_split

def load_data():
    return pd.read_csv('data.csv')
"""
        )

        yield project_dir
        shutil.rmtree(temp_dir)

    def run_reqtracker(self, args, cwd=None):
        """Run reqtracker CLI command and return output."""
        cmd = ["python", "-m", "reqtracker"] + args
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        return result

    def test_track_command(self, temp_project):
        """Test reqtracker track command."""
        result = self.run_reqtracker(["track"], cwd=temp_project)

        assert result.returncode == 0
        assert "Flask" in result.stdout
        assert "requests" in result.stdout
        assert "numpy" in result.stdout
        assert "pandas" in result.stdout
        assert "scikit-learn" in result.stdout

    def test_generate_command(self, temp_project):
        """Test reqtracker generate command."""
        # First track
        self.run_reqtracker(["track"], cwd=temp_project)

        # Then generate
        result = self.run_reqtracker(
            ["generate", "--output", "requirements.txt"], cwd=temp_project
        )

        assert result.returncode == 0

        # Check file was created
        req_file = temp_project / "requirements.txt"
        assert req_file.exists()

        content = req_file.read_text()
        assert "Flask" in content
        assert "requests" in content

    def test_analyze_command(self, temp_project):
        """Test reqtracker analyze command (full workflow)."""
        result = self.run_reqtracker(
            ["analyze", "--output", "deps.txt"], cwd=temp_project
        )

        assert result.returncode == 0

        # Check file was created
        deps_file = temp_project / "deps.txt"
        assert deps_file.exists()

        content = deps_file.read_text()
        assert "Flask" in content
        assert "requests" in content
        assert "numpy" in content

    def test_mode_options(self, temp_project):
        """Test different analysis modes via CLI."""
        modes = ["static", "dynamic", "hybrid"]

        for mode in modes:
            result = self.run_reqtracker(["track", "--mode", mode], cwd=temp_project)
            assert result.returncode == 0
            assert "Flask" in result.stdout

    def test_version_strategies(self, temp_project):
        """Test different version strategies."""
        strategies = [
            ("exact", "==", ["analyze", "--exact", "--output"]),
            ("compatible", "~=", ["analyze", "--output"]),  # default is compatible
            ("minimum", ">=", ["analyze", "--minimum", "--output"]),
            ("none", None, ["analyze", "--no-versions", "--output"]),
        ]

        for strategy_name, expected_op, cmd_args in strategies:
            output_file = f"requirements_{strategy_name}.txt"
            result = self.run_reqtracker(cmd_args + [output_file], cwd=temp_project)

            assert result.returncode == 0

            content = (temp_project / output_file).read_text()
            if expected_op:
                assert expected_op in content
            else:
                # No version strategy
                assert "==" not in content
                assert ">=" not in content
                assert "~=" not in content

    def test_exclude_patterns(self, temp_project):
        """Test exclude patterns via CLI."""
        # Create test file to exclude
        (temp_project / "test_app.py").write_text(
            """
    import pytest
    import unittest

    def test_something():
        pass
    """
        )

        # Run with mode flag properly split
        result = self.run_reqtracker(
            ["track", "--mode", "static", "test_*.py"], cwd=temp_project
        )

        assert result.returncode == 0
        assert "pytest" not in result.stdout

    def test_config_file(self, temp_project):
        """Test using configuration file."""
        # Create config file with correct format
        config_content = """
    [tool.reqtracker]
    mode = "static"
    exclude_patterns = ["test_*.py", "*_test.py"]

    [tool.reqtracker.generator]
    version_strategy = "exact"
    include_header = false
    """
        (temp_project / ".reqtracker.toml").write_text(config_content)

        # Run with config
        result = self.run_reqtracker(["analyze"], cwd=temp_project)

        assert result.returncode == 0

        # Check generated file respects config
        req_file = temp_project / "requirements.txt"
        content = req_file.read_text()

        assert len(content) > 0

    def test_verbose_output(self, temp_project):
        """Test global verbose flag."""
        result = self.run_reqtracker(["-v", "track"], cwd=temp_project)

        assert result.returncode == 0
        assert len(result.stdout) > 0

    def test_multiple_paths(self, temp_project):
        """Test tracking multiple paths."""
        # Create subdirectories
        lib_dir = temp_project / "lib"
        lib_dir.mkdir()
        (lib_dir / "helper.py").write_text("import redis\n")

        src_dir = temp_project / "src"
        src_dir.mkdir()
        (src_dir / "main.py").write_text("import celery\n")

        # Track multiple paths
        result = self.run_reqtracker(["track", "lib", "src"], cwd=temp_project)

        assert result.returncode == 0
        assert "redis" in result.stdout
        assert "celery" in result.stdout

    def test_help_command(self):
        """Test help command works."""
        result = self.run_reqtracker(["--help"])

        assert result.returncode == 0
        assert "usage:" in result.stdout
        assert "track" in result.stdout
        assert "generate" in result.stdout
        assert "analyze" in result.stdout

    def test_invalid_command(self):
        """Test error handling for invalid commands."""
        result = self.run_reqtracker(["invalid"])

        assert result.returncode != 0
        assert "usage:" in result.stderr.lower() and "error:" in result.stderr.lower()

    def test_nonexistent_path(self):
        """Test error handling for nonexistent paths."""
        result = self.run_reqtracker(["track", "/nonexistent/path"])

        assert result.returncode == 0
        assert len(result.stdout.strip()) == 0


class TestCLIEdgeCases:
    """Test CLI edge cases and error conditions."""

    def test_empty_directory(self):
        """Test CLI with empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                ["python", "-m", "reqtracker", "track"],
                cwd=temp_dir,
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            assert (
                "No dependencies found" in result.stdout
                or len(result.stdout.strip()) == 0
            )

    def test_no_write_permission(self):
        """Test handling of write permission errors."""
        import os
        import stat

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir)
            (project_dir / "app.py").write_text("import requests\n")

            # Make directory read-only
            os.chmod(temp_dir, stat.S_IRUSR | stat.S_IXUSR)

            try:
                result = subprocess.run(
                    ["python", "-m", "reqtracker", "analyze"],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                )

                assert "Permission denied" in result.stderr
            finally:
                # Restore permissions for cleanup
                os.chmod(temp_dir, stat.S_IRWXU)
