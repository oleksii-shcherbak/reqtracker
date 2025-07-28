"""Cross-platform compatibility tests for reqtracker."""

import platform
import sys
import tempfile
from pathlib import Path

import pytest

import reqtracker


class TestCrossPlatform:
    """Test reqtracker works correctly across different platforms."""

    def test_platform_info(self):
        """Log current platform information."""
        print("\nPlatform Information:")
        print(f"  System: {platform.system()}")
        print(f"  Python: {sys.version}")
        print(f"  Machine: {platform.machine()}")
        print(f"  Platform: {platform.platform()}")

    def test_path_separators(self):
        """Test handling of different path separators."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested structure
            project_dir = Path(temp_dir) / "project"
            sub_dir = project_dir / "sub" / "module"
            sub_dir.mkdir(parents=True)

            # Create file with mixed path styles in imports
            (sub_dir / "test.py").write_text(
                """
import sys
sys.path.append('..')
sys.path.append(os.path.join('..', '..'))
from pathlib import Path
import requests
"""
            )

            # Track should work regardless of platform
            packages = reqtracker.track([str(project_dir)])
            assert "requests" in packages

    def test_case_sensitivity(self):
        """Test handling of case sensitivity differences."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            # Create files with different cases
            (project_dir / "Main.py").write_text("import requests\n")
            (project_dir / "main.py").write_text("import numpy\n")

            # Track dependencies
            packages = reqtracker.track([str(project_dir)])

            # Should find packages from both files on case-insensitive systems
            # or handle appropriately on case-sensitive systems
            assert len(packages) > 0

    def test_unicode_paths(self):
        """Test handling of Unicode characters in paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create directory with Unicode characters
            unicode_dir = Path(temp_dir) / "프로젝트" / "模块"
            unicode_dir.mkdir(parents=True)

            # Create file
            (unicode_dir / "test.py").write_text("import pandas\n")

            # Should handle Unicode paths
            try:
                packages = reqtracker.track([str(unicode_dir)])
                assert "pandas" in packages
            except UnicodeError:
                pytest.skip("Unicode paths not supported on this system")

    def test_long_paths(self):
        """Test handling of very long path names."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create deeply nested structure
            current = Path(temp_dir)
            for i in range(20):
                current = current / f"very_long_directory_name_number_{i}"

            try:
                current.mkdir(parents=True)
                (current / "test.py").write_text("import flask\n")

                packages = reqtracker.track([str(Path(temp_dir))])
                assert "Flask" in packages
            except OSError as e:
                if "path too long" in str(e).lower():
                    pytest.skip("Long paths not supported on this system")
                raise

    def test_symlinks(self):
        """Test handling of symbolic links."""
        if not hasattr(Path, "symlink_to"):
            pytest.skip("Symbolic links not supported on this system")

        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)

            # Create actual file
            actual_dir = base_dir / "actual"
            actual_dir.mkdir()
            (actual_dir / "module.py").write_text("import requests\n")

            # Create symlink
            link_dir = base_dir / "link"
            try:
                link_dir.symlink_to(actual_dir)

                # Track via symlink
                packages = reqtracker.track([str(link_dir)])
                assert "requests" in packages
            except OSError:
                pytest.skip("Cannot create symbolic links on this system")

    def test_file_permissions(self):
        """Test handling of files with restricted permissions."""
        import os
        import stat

        if platform.system() == "Windows":
            pytest.skip("Permission test not applicable on Windows")

        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            # Create file with restricted permissions
            restricted_file = project_dir / "restricted.py"
            restricted_file.write_text("import numpy\n")

            # Make file read-only
            os.chmod(restricted_file, stat.S_IRUSR)

            try:
                # Should still be able to read and analyze
                packages = reqtracker.track([str(project_dir)])
                assert "numpy" in packages
            finally:
                # Restore permissions for cleanup
                os.chmod(restricted_file, stat.S_IRUSR | stat.S_IWUSR)

    @pytest.mark.parametrize("encoding", ["utf-8", "latin-1", "cp1252"])
    def test_file_encodings(self, encoding):
        """Test handling of files with different encodings."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            # Create file with specific encoding
            file_path = project_dir / f"test_{encoding}.py"
            content = "# -*- coding: {} -*-\nimport requests\n".format(encoding)

            try:
                file_path.write_text(content, encoding=encoding)

                # Should handle different encodings
                packages = reqtracker.track([str(project_dir)])
                assert "requests" in packages
            except UnicodeError:
                pytest.skip(f"Encoding {encoding} not supported on this system")

    def test_line_endings(self):
        """Test handling of different line ending styles."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_dir = Path(temp_dir) / "project"
            project_dir.mkdir()

            # Test different line endings
            line_endings = {"unix": "\n", "windows": "\r\n", "mac": "\r"}

            for name, ending in line_endings.items():
                file_path = project_dir / f"test_{name}.py"
                content = f"import requests{ending}import numpy{ending}"
                file_path.write_bytes(content.encode("utf-8"))

            # Should handle all line ending styles
            packages = reqtracker.track([str(project_dir)])
            assert "requests" in packages
            assert "numpy" in packages
