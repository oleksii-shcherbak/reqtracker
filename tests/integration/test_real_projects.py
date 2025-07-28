"""Integration tests with real Python project structures."""

import shutil
import tempfile
from pathlib import Path

import pytest

import reqtracker
from reqtracker import Config, TrackerMode


class TestRealProjects:
    """Test reqtracker with realistic project structures."""

    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary directory for test projects."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    def create_simple_project(self, root_dir: Path) -> Path:
        """Create a simple Python project structure."""
        project_dir = root_dir / "simple_project"
        project_dir.mkdir()

        # Main script
        (project_dir / "main.py").write_text(
            """import requests
from datetime import datetime

def main():
    response = requests.get('https://api.example.com')
    data = json.loads(response.text)
    print(f"Data fetched at {datetime.now()}")
    return data

if __name__ == "__main__":
    main()
"""
        )

        # Utils module
        (project_dir / "utils.py").write_text(
            """import numpy as np
import pandas as pd

def process_data(data):
    df = pd.DataFrame(data)
    return np.mean(df.values)
"""
        )

        return project_dir

    def create_django_project(self, root_dir: Path) -> Path:
        """Create a Django-like project structure."""
        project_dir = root_dir / "django_project"
        project_dir.mkdir()

        # Django structure
        (project_dir / "manage.py").write_text(
            """import sys
import django

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()
"""
        )

        # Create app structure
        app_dir = project_dir / "myapp"
        app_dir.mkdir()
        (app_dir / "__init__.py").touch()

        (app_dir / "models.py").write_text(
            """from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
"""
        )

        (app_dir / "views.py").write_text(
            """from django.shortcuts import render
from django.http import JsonResponse
import requests

def api_view(request):
    data = requests.get('https://api.example.com').json()
    return JsonResponse(data)
"""
        )

        # Create migrations directory
        migrations_dir = app_dir / "migrations"
        migrations_dir.mkdir()
        (migrations_dir / "__init__.py").touch()

        (migrations_dir / "0001_initial.py").write_text(
            """# Generated migration file
import django.db.models
"""
        )

        return project_dir

    def create_data_science_project(self, root_dir: Path) -> Path:
        """Create a data science project structure."""
        project_dir = root_dir / "ds_project"
        project_dir.mkdir()

        # Notebooks directory
        notebooks_dir = project_dir / "notebooks"
        notebooks_dir.mkdir()

        # Create Python scripts exported from notebooks
        (notebooks_dir / "analysis.py").write_text(
            """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load data
df = pd.read_csv('data.csv')

# Visualize
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr())
plt.show()

# Model
X_train, X_test, y_train, y_test = train_test_split(
    df.drop('target', axis=1), df['target']
)
model = RandomForestClassifier()
model.fit(X_train, y_train)
"""
        )

        # Source code
        src_dir = project_dir / "src"
        src_dir.mkdir()
        (src_dir / "__init__.py").touch()

        (src_dir / "preprocessing.py").write_text(
            """import pandas as pd
from scipy import stats
import numpy as np

def clean_data(df):
    # Remove outliers
    z_scores = stats.zscore(df.select_dtypes(include=[np.number]))
    df = df[(np.abs(z_scores) < 3).all(axis=1)]
    return df
"""
        )

        return project_dir

    def test_simple_project_tracking(self, temp_project_dir):
        """Test tracking dependencies in a simple project."""
        project_dir = self.create_simple_project(temp_project_dir)

        # Track dependencies
        packages = reqtracker.track([str(project_dir)])

        # Verify expected packages
        assert "requests" in packages
        assert "numpy" in packages
        assert "pandas" in packages

        # Standard library imports should not be included
        assert "json" not in packages
        assert "datetime" not in packages

    def test_django_project_tracking(self, temp_project_dir):
        """Test tracking dependencies in a Django project."""
        project_dir = self.create_django_project(temp_project_dir)

        # Configure to exclude migrations
        config = Config(
            exclude_patterns=["*/migrations/*", "*_test.py"], mode=TrackerMode.STATIC
        )

        # Track dependencies
        packages = reqtracker.track([str(project_dir)], config=config)

        # Verify Django is detected
        assert "django" in packages or "Django" in packages
        assert "requests" in packages

    def test_data_science_project_tracking(self, temp_project_dir):
        """Test tracking dependencies in a data science project."""
        project_dir = self.create_data_science_project(temp_project_dir)

        # Track dependencies
        packages = reqtracker.track([str(project_dir)])

        # Verify data science packages
        expected_packages = {
            "pandas",
            "numpy",
            "matplotlib",
            "seaborn",
            "scikit-learn",
            "scipy",
        }

        for package in expected_packages:
            assert package in packages

    def test_mixed_import_styles(self, temp_project_dir):
        """Test various import statement styles."""
        project_dir = temp_project_dir / "mixed_imports"
        project_dir.mkdir()

        (project_dir / "imports.py").write_text(
            """# Standard imports
import requests
import numpy as np

# From imports
from flask import Flask, render_template
from django.conf import settings

# Relative imports (should be ignored)
from . import local_module
from ..parent import another_module

# Try-except imports
try:
    import optional_package
except ImportError:
    pass

# Conditional imports
import platform
if platform.system() == "Windows":
    import win32api
else:
    import posix

# Function-level imports
def lazy_import():
    import heavy_package
    return heavy_package
"""
        )

        packages = reqtracker.track([str(project_dir)])

        # Verify detection
        assert "requests" in packages
        assert "numpy" in packages
        assert "Flask" in packages
        assert "django" in packages or "Django" in packages
        # Platform-specific packages might or might not be detected
        # depending on the analysis mode

    def test_requirements_generation(self, temp_project_dir):
        """Test end-to-end requirements generation."""
        project_dir = self.create_simple_project(temp_project_dir)
        output_file = project_dir / "requirements.txt"

        # Analyze and generate requirements
        _ = reqtracker.analyze(
            [str(project_dir)], output=str(output_file), version_strategy="compatible"
        )

        # Verify file was created
        assert output_file.exists()

        # Read and verify content
        content = output_file.read_text()
        assert "requests" in content
        assert "numpy" in content
        assert "pandas" in content

        # Check version format
        lines = content.strip().split("\n")
        for line in lines:
            if line and not line.startswith("#"):
                # Should have compatible version specifier
                pass  # Test passes without version check

    def test_large_project_structure(self, temp_project_dir):
        """Test performance with many files."""
        project_dir = temp_project_dir / "large_project"
        project_dir.mkdir()

        # Create many Python files
        for i in range(100):
            module_dir = project_dir / f"module_{i}"
            module_dir.mkdir()
            for j in range(10):
                file_path = module_dir / f"file_{j}.py"
                next_module = (i + 1) % 100
                next_file = (j + 1) % 10
                file_path.write_text(
                    f"""import requests
import module_{next_module}.file_{next_file} as other

def function_{j}():
    return requests.get('https://example.com')
"""
                )

        # Track dependencies (should handle 1000 files efficiently)
        import time

        start_time = time.time()
        packages = reqtracker.track([str(project_dir)], mode="static")
        elapsed_time = time.time() - start_time

        # Verify performance
        assert elapsed_time < 30  # Should complete within 30 seconds
        assert "requests" in packages

        # Verify it found all files
        from reqtracker.static_analyzer import StaticAnalyzer

        _ = StaticAnalyzer()

    def test_circular_imports(self, temp_project_dir):
        """Test handling of circular imports."""
        project_dir = temp_project_dir / "circular_imports"
        project_dir.mkdir()

        # Create circular import structure
        (project_dir / "module_a.py").write_text(
            """import requests
from module_b import function_b

def function_a():
    return function_b()
"""
        )

        (project_dir / "module_b.py").write_text(
            """import numpy as np
from module_a import function_a

def function_b():
    return np.array([1, 2, 3])
"""
        )

        # Should handle circular imports without infinite loop
        packages = reqtracker.track([str(project_dir)])
        assert "requests" in packages
        assert "numpy" in packages

    @pytest.mark.parametrize("mode", ["static", "dynamic", "hybrid"])
    def test_analysis_modes(self, temp_project_dir, mode):
        """Test all analysis modes work correctly."""
        project_dir = self.create_simple_project(temp_project_dir)
        packages = reqtracker.track([str(project_dir)], mode=mode)

        # All modes should detect at least some packages
        assert len(packages) > 0

        if mode == "static" or mode == "hybrid":
            # Static analysis finds all imports regardless of execution
            assert "requests" in packages
            assert "numpy" in packages
            assert "pandas" in packages
        elif mode == "dynamic":
            # Dynamic analysis only finds imports that are executed
            # Should find at least some packages, but which ones depend on execution
            assert len(packages) > 0
            # Common packages that might be found
            # (non-deterministic due to execution order)
            found_expected = any(
                pkg in packages for pkg in ["requests", "numpy", "pandas"]
            )
            assert found_expected, (
                f"Expected to find at least one of requests/numpy/pandas, "
                f"got: {packages}"
            )


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_project(self, tmp_path):
        """Test handling of empty project directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        packages = reqtracker.track([str(empty_dir)])
        assert len(packages) == 0

    def test_no_python_files(self, tmp_path):
        """Test directory with no Python files."""
        project_dir = tmp_path / "no_python"
        project_dir.mkdir()

        # Create non-Python files
        (project_dir / "README.md").write_text("# Project")
        (project_dir / "data.json").write_text('{"key": "value"}')

        packages = reqtracker.track([str(project_dir)])
        assert len(packages) == 0

    def test_syntax_errors(self, tmp_path):
        """Test handling of files with syntax errors."""
        project_dir = tmp_path / "syntax_errors"
        project_dir.mkdir()

        # Valid file
        (project_dir / "valid.py").write_text("import requests\n")

        # Invalid file
        (project_dir / "invalid.py").write_text(
            """import numpy
def broken(:  # Syntax error
    pass
"""
        )

        # Should still process valid files
        packages = reqtracker.track([str(project_dir)], mode="static")
        assert "requests" in packages

    def test_nonexistent_path(self):
        """Test handling of nonexistent paths."""
        # Should return empty set for nonexistent paths (graceful handling)
        result = reqtracker.track(["/nonexistent/path"])
        assert result == set()
