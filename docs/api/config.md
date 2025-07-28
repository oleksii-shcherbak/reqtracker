# Config Module

The config module provides configuration management for reqtracker.

## Classes

### Config

Main configuration class using Python dataclasses.

```python
@dataclass
class Config:
    """Main configuration class for reqtracker."""

    mode: TrackerMode = TrackerMode.HYBRID
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "__pycache__/*",
        "*.pyc",
        ".git/*",
        ".tox/*",
        ".venv/*",
        "venv/*",
    ])
    include_patterns: List[str] = field(default_factory=lambda: ["*.py"])
    ignore_packages: List[str] = field(default_factory=list)
    custom_mappings: Dict[str, str] = field(default_factory=dict)
    output: OutputConfig = field(default_factory=OutputConfig)
    project_root: Path = field(default_factory=Path.cwd)
```

### OutputConfig

Configuration for output generation.

```python
@dataclass
class OutputConfig:
    """Configuration for requirements file generation."""

    file: Path = Path("requirements.txt")
    version_strategy: VersionStrategy = VersionStrategy.COMPATIBLE
    include_header: bool = True
    sort_packages: bool = True
```

### TrackerMode

Enum for analysis modes.

```python
class TrackerMode(str, Enum):
    """Available tracking modes."""

    STATIC = "static"
    DYNAMIC = "dynamic"
    HYBRID = "hybrid"
```

### VersionStrategy

Enum for version pinning strategies.

```python
class VersionStrategy(str, Enum):
    """Version pinning strategies for requirements."""

    EXACT = "exact"            # package==1.2.3
    COMPATIBLE = "compatible"  # package~=1.2.3
    MINIMUM = "minimum"        # package>=1.2.3
    NONE = "none"              # package
```

## Loading Configuration

### From TOML File

```python
# Load from .reqtracker.toml
config = Config.from_file(".reqtracker.toml")

# Load from custom path
config = Config.from_file("config/custom.toml")
```

### TOML File Format

```toml
[tool.reqtracker]
mode = "hybrid"
include_patterns = ["*.py", "src/**/*.py"]
exclude_patterns = [
    "test_*.py",
    "*_test.py",
    "tests/**/*",
    "docs/**/*"
]
ignore_packages = ["internal-package"]

[tool.reqtracker.output]
file = "requirements.txt"
version_strategy = "compatible"
include_header = true
sort_packages = true

[tool.reqtracker.import_mappings]
cv2 = "opencv-python"
sklearn = "scikit-learn"
```

## Creating Custom Configuration

### Basic Configuration

```python
from reqtracker.config import Config, TrackerMode

config = Config(
    mode=TrackerMode.STATIC,
    exclude_patterns=["tests/**/*", "docs/**/*"]
)
```

### Advanced Configuration

```python
from reqtracker.config import Config, OutputConfig, TrackerMode, VersionStrategy
from pathlib import Path

# Output configuration
output_config = OutputConfig(
    file=Path("requirements-prod.txt"),
    version_strategy=VersionStrategy.EXACT,
    include_header=False,
    sort_packages=True
)

# Main configuration
config = Config(
    mode=TrackerMode.STATIC,
    include_patterns=["src/**/*.py", "lib/**/*.py"],
    exclude_patterns=[
        "test_*.py",
        "*_test.py",
        "*/tests/*",
        "*/migrations/*"
    ],
    ignore_packages=["mycompany-internal"],
    custom_mappings={
        "cv2": "opencv-python",
        "sklearn": "scikit-learn",
        "custom_lib": "my-custom-package"
    },
    output=output_config,
    project_root=Path("/path/to/project")
)
```

## Pattern Matching

### Include Patterns

Glob patterns for files to analyze:

```python
config = Config(
    include_patterns=[
        "*.py",           # All .py files in root
        "src/**/*.py",    # All .py files under src/
        "lib/*.py",       # .py files directly in lib/
        "!test_*.py"      # Exclude test files (with !)
    ]
)
```

### Exclude Patterns

Glob patterns for files to skip:

```python
config = Config(
    exclude_patterns=[
        "test_*.py",          # Test files
        "*_test.py",          # Alternative test naming
        "*/tests/*",          # Tests directories
        "**/__pycache__/**",  # Cache directories
        "*.pyc",              # Compiled files
        ".git/**/*"           # Git directory
    ]
)
```

## Custom Import Mappings

Map import names to package names:

```python
config = Config(
    custom_mappings={
        # Scientific computing
        "cv2": "opencv-python",
        "sklearn": "scikit-learn",
        "skimage": "scikit-image",

        # Web frameworks
        "flask_sqlalchemy": "Flask-SQLAlchemy",
        "flask_wtf": "Flask-WTF",

        # Company internal
        "company_utils": "company-utils-package",
        "internal_api": "internal-api-client"
    }
)
```

## Configuration Merging

Configurations can be merged with precedence:

```python
# Load base configuration
base_config = Config.from_file(".reqtracker.toml")

# Override for production
prod_config = Config(
    mode=TrackerMode.STATIC,
    output=OutputConfig(
        file=Path("requirements-prod.txt"),
        version_strategy=VersionStrategy.EXACT
    )
)

# Merge configurations (prod_config takes precedence)
final_config = merge_configs(base_config, prod_config)
```

## Environment-Specific Configuration

```python
import os
from reqtracker.config import Config, TrackerMode, VersionStrategy

# Determine environment
env = os.getenv("ENVIRONMENT", "development")

# Environment-specific settings
if env == "production":
    config = Config(
        mode=TrackerMode.STATIC,
        output=OutputConfig(
            version_strategy=VersionStrategy.EXACT
        )
    )
elif env == "development":
    config = Config(
        mode=TrackerMode.HYBRID,
        output=OutputConfig(
            version_strategy=VersionStrategy.COMPATIBLE
        )
    )
else:  # testing
    config = Config(
        mode=TrackerMode.DYNAMIC,
        include_patterns=["tests/**/*.py"],
        output=OutputConfig(
            file=Path("requirements-test.txt")
        )
    )
```

## Validation

Configuration is validated on creation:

```python
try:
    config = Config(
        mode="invalid_mode"  # Will raise ValueError
    )
except ValueError as e:
    print(f"Invalid configuration: {e}")

# Path validation
try:
    config = Config(
        project_root=Path("/nonexistent/path")
    )
except FileNotFoundError:
    print("Project root does not exist")
```

## Default Values

### Default Exclude Patterns
- `__pycache__/*` - Python cache
- `*.pyc` - Compiled Python files
- `.git/*` - Git directory
- `.tox/*` - Tox directory
- `.venv/*`, `venv/*` - Virtual environments

### Default Include Patterns
- `*.py` - All Python files

### Default Output Settings
- File: `requirements.txt`
- Version Strategy: `compatible`
- Include Header: `True`
- Sort Packages: `True`

## Best Practices

1. **Use TOML files for project configuration**
   ```toml
   # .reqtracker.toml in project root
   [tool.reqtracker]
   mode = "hybrid"
   exclude_patterns = ["tests/**/*", "docs/**/*"]
   ```

2. **Create environment-specific configurations**
   ```python
   # config/prod.toml
   # config/dev.toml
   # config/test.toml
   ```

3. **Document custom mappings**
   ```toml
   [tool.reqtracker.import_mappings]
   # Scientific packages
   cv2 = "opencv-python"

   # Internal packages
   mylib = "company-mylib"
   ```

4. **Use appropriate patterns**
   - Be specific with include patterns
   - Exclude test and documentation files
   - Exclude virtual environments
