# Configuration Guide

This guide covers all configuration options for reqtracker.

## Configuration File Locations

reqtracker looks for configuration in these locations (in order of precedence):

1. Command-line specified: `--config path/to/config.toml`
2. Project root: `.reqtracker.toml`
3. pyproject.toml: `[tool.reqtracker]` section
4. Home directory: `~/.reqtracker.toml`

## Configuration Format

Configuration uses TOML format:

```toml
[tool.reqtracker]
mode = "hybrid"
include_patterns = ["*.py"]
exclude_patterns = ["tests/**/*"]

[tool.reqtracker.output]
file = "requirements.txt"
version_strategy = "compatible"

[tool.reqtracker.import_mappings]
cv2 = "opencv-python"
```

## Complete Configuration Reference

```toml
[tool.reqtracker]
# Analysis mode: "static", "dynamic", or "hybrid"
mode = "hybrid"

# File patterns to include (glob syntax)
include_patterns = [
    "*.py",           # All .py files in root
    "src/**/*.py",    # All .py files under src/
    "lib/*.py"        # .py files directly in lib/
]

# File patterns to exclude
exclude_patterns = [
    "test_*.py",      # Test files
    "*_test.py",      # Alternative test naming
    "tests/**/*",     # All files in tests/
    "docs/**/*",      # Documentation
    "build/**/*",     # Build artifacts
    "**/__pycache__/**" # Cache directories
]

# Packages to ignore in output
ignore_packages = [
    "internal-package",
    "company-private-lib"
]

# Project root directory (defaults to current directory)
project_root = "/path/to/project"

[tool.reqtracker.output]
# Output file path
file = "requirements.txt"

# Version strategy: "exact", "compatible", "minimum", "none"
version_strategy = "compatible"

# Include timestamp header
include_header = true

# Sort packages alphabetically
sort_packages = true

[tool.reqtracker.import_mappings]
# Map import names to package names
# import_name = "package-name"
cv2 = "opencv-python"
sklearn = "scikit-learn"
skimage = "scikit-image"
PIL = "Pillow"
yaml = "PyYAML"
```

## Configuration Options

### Analysis Mode

Controls how reqtracker analyzes dependencies:

- **static**: Parse Python AST (fast, safe, may miss dynamic imports)
- **dynamic**: Track runtime imports (complete, requires execution)
- **hybrid**: Combine both approaches (default, most accurate)

### Include Patterns

Glob patterns for files to analyze:

```toml
include_patterns = [
    "*.py",                  # Root directory Python files
    "src/**/*.py",           # Recursive under src/
    "app/module/*.py",       # Specific module
    "!test_*.py"             # Exclude pattern (with !)
]
```

### Exclude Patterns

Glob patterns for files to skip:

```toml
exclude_patterns = [
    "tests/**/*",            # Test directories
    "**/test_*.py",          # Test files anywhere
    "**/migrations/**/*",    # Django migrations
    "**/__pycache__/**/*",   # Python cache
    "**/node_modules/**/*"   # JavaScript dependencies
]
```

### Import Mappings

Map import names to PyPI package names:

```toml
[tool.reqtracker.import_mappings]
# Scientific packages
cv2 = "opencv-python"
sklearn = "scikit-learn"

# Web frameworks
flask_sqlalchemy = "Flask-SQLAlchemy"

# Internal packages
mycompany = "mycompany-python"
```

### Output Configuration

Control requirements.txt generation:

```toml
[tool.reqtracker.output]
# Output file name
file = "requirements-prod.txt"

# Version pinning strategy
version_strategy = "exact"  # For production

# Disable header with timestamp
include_header = false

# Keep original order (don't sort)
sort_packages = false
```

## Environment-Specific Configurations

### Development Configuration

`.reqtracker.dev.toml`:
```toml
[tool.reqtracker]
mode = "hybrid"
include_patterns = ["**/*.py"]

[tool.reqtracker.output]
file = "requirements-dev.txt"
version_strategy = "compatible"
```

### Production Configuration

`.reqtracker.prod.toml`:
```toml
[tool.reqtracker]
mode = "static"  # Safe for CI/CD
exclude_patterns = [
    "tests/**/*",
    "docs/**/*",
    "examples/**/*"
]

[tool.reqtracker.output]
file = "requirements-prod.txt"
version_strategy = "exact"  # Reproducible builds
include_header = false
```

### Testing Configuration

`.reqtracker.test.toml`:
```toml
[tool.reqtracker]
mode = "dynamic"
include_patterns = [
    "tests/**/*.py",
    "src/**/*.py"
]

[tool.reqtracker.output]
file = "requirements-test.txt"
version_strategy = "compatible"
```

## Using pyproject.toml

Include reqtracker configuration in your `pyproject.toml`:

```toml
[tool.reqtracker]
mode = "hybrid"
exclude_patterns = ["tests/**/*"]

[tool.reqtracker.output]
version_strategy = "compatible"

[tool.reqtracker.import_mappings]
internal_lib = "company-internal-lib"
```

## Command-Line Override

CLI options override configuration file settings:

```bash
# Config has mode = "static", but CLI uses hybrid
reqtracker track --mode hybrid

# Override output file
reqtracker generate --output requirements-custom.txt

# Override version strategy
reqtracker analyze --version-strategy exact
```

## Best Practices

1. **Use project-specific config files**
   - Keep `.reqtracker.toml` in version control
   - Document custom mappings

2. **Create environment-specific configs**
   - Development: flexible versions
   - Production: exact versions
   - Testing: include test dependencies

3. **Optimize patterns**
   - Be specific with include patterns
   - Exclude build artifacts and caches
   - Test patterns with `--verbose` flag

4. **Maintain import mappings**
   - Add mappings for all non-standard imports
   - Document why each mapping exists
   - Keep mappings sorted for readability

## Examples

### Django Project

```toml
[tool.reqtracker]
mode = "hybrid"
exclude_patterns = [
    "*/migrations/*",
    "*/tests/*",
    "*/static/*",
    "*/media/*",
    "manage.py"
]

[tool.reqtracker.output]
version_strategy = "compatible"

[tool.reqtracker.import_mappings]
rest_framework = "djangorestframework"
django_filters = "django-filter"
```

### Data Science Project

```toml
[tool.reqtracker]
mode = "dynamic"  # For Jupyter notebooks
exclude_patterns = [
    "data/**/*",
    "models/**/*",
    "outputs/**/*",
    "*.ipynb_checkpoints/*"
]

[tool.reqtracker.import_mappings]
cv2 = "opencv-python"
sklearn = "scikit-learn"
```

### Library Development

```toml
[tool.reqtracker]
mode = "static"
include_patterns = ["src/**/*.py"]
exclude_patterns = [
    "tests/**/*",
    "docs/**/*",
    "examples/**/*"
]

[tool.reqtracker.output]
version_strategy = "minimum"  # For libraries
```
