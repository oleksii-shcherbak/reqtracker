"""Performance and scalability tests for reqtracker."""

import tempfile
import time
from pathlib import Path

import pytest

import reqtracker


class TestBasicPerformance:
    """Basic performance tests for reqtracker."""

    def create_simple_project(self, root_dir: Path, num_files: int) -> Path:
        """Create a simple project with multiple Python files."""
        project_dir = root_dir / "test_project"
        project_dir.mkdir()

        # Create Python files
        for i in range(num_files):
            if i % 10 == 0:  # Create subdirectories every 10 files
                sub_dir = project_dir / f"module_{i // 10}"
                sub_dir.mkdir(exist_ok=True)
                file_path = sub_dir / f"file_{i}.py"
            else:
                file_path = project_dir / f"file_{i}.py"

            # Write content with various imports
            content = f"""import requests
import numpy as np
from datetime import datetime

def function_{i}():
    return {i}
"""
            file_path.write_text(content)

        return project_dir

    def test_small_project_performance(self):
        """Test performance on small project (10 files)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = self.create_simple_project(Path(temp_dir), 10)

            start_time = time.time()
            packages = reqtracker.track([str(project_dir)], mode="static")
            elapsed_time = time.time() - start_time

            assert "requests" in packages
            assert "numpy" in packages
            assert elapsed_time < 2.0  # Should complete in under 2 seconds
            print(f"Small project (10 files): {elapsed_time:.2f}s")

    def test_medium_project_performance(self):
        """Test performance on medium project (100 files)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = self.create_simple_project(Path(temp_dir), 100)

            start_time = time.time()
            packages = reqtracker.track([str(project_dir)], mode="static")
            elapsed_time = time.time() - start_time

            assert "requests" in packages
            assert "numpy" in packages
            assert elapsed_time < 10.0  # Should complete in under 10 seconds
            print(f"Medium project (100 files): {elapsed_time:.2f}s")

    @pytest.mark.slow
    def test_large_project_performance(self):
        """Test performance on large project (500 files)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = self.create_simple_project(Path(temp_dir), 500)

            start_time = time.time()
            packages = reqtracker.track([str(project_dir)], mode="static")
            elapsed_time = time.time() - start_time

            assert "requests" in packages
            assert "numpy" in packages
            assert elapsed_time < 30.0  # Should complete in under 30 seconds
            print(f"Large project (500 files): {elapsed_time:.2f}s")
            print(f"  Files per second: {500 / elapsed_time:.1f}")

    def test_mode_comparison(self):
        """Compare performance of different analysis modes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = self.create_simple_project(Path(temp_dir), 20)

            results = {}
            for mode in ["static", "dynamic", "hybrid"]:
                start_time = time.time()
                _ = reqtracker.track([str(project_dir)], mode=mode)
                elapsed_time = time.time() - start_time
                results[mode] = elapsed_time
                print(f"Mode '{mode}': {elapsed_time:.2f}s")

            # Static should generally be fastest
            assert results["static"] <= results["hybrid"]
