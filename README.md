# reqtracker

**Intelligent Python dependency tracking and requirements.txt generation**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

reqtracker automatically detects and manages Python dependencies in your projects using static analysis, dynamic tracking, or hybrid approaches. Unlike traditional tools like `pip freeze`, reqtracker focuses on generating accurate `requirements.txt` files based on *actual project usage*.

---

## ✨ Features

- **🔍 Smart Dependency Detection**: Analyzes your code to find actually used packages
- **⚡ Multiple Analysis Modes**: Static (AST), Dynamic (runtime), or Hybrid (both)
- **🎯 Accurate Package Mapping**: Maps imports like `cv2` to `opencv-python`
- **📦 Flexible Output**: Multiple version strategies and output formats
- **🛠️ Zero Configuration**: Works out of the box with sensible defaults
- **⚙️ Highly Configurable**: Customize analysis via config files or API
- **🚀 CLI & Library**: Use as command-line tool or Python library

---

## 📦 Installation

Install reqtracker using pip:

```bash
pip install reqtracker
```

---

## 🚀 Quick Start

### Command Line Usage

```python
# Analyze current directory and generate requirements.txt
reqtracker analyze

# Track dependencies in specific paths
reqtracker track ./src ./app

# Generate with exact versions
reqtracker generate --version-strategy exact

# Use static analysis only
reqtracker analyze --mode static --output deps.txt

```

### Python Library Usage

```python
import reqtracker

# Simple usage - analyze current directory
packages = reqtracker.track()
print(packages)  # {'requests', 'numpy', 'pandas'}

# Generate requirements.txt
reqtracker.generate()

# Complete workflow
reqtracker.analyze()  # Track dependencies and generate requirements.txt

```

---

## 📚 Detailed Usage

### Analysis Modes

reqtracker supports three analysis modes:

#### 🔍 Static Analysis (AST-based)

Analyzes source code without executing it:

```bash
`reqtracker track --mode static ./src`
```

```python
packages = reqtracker.track(['./src'], mode='static')
```

#### 🏃 Dynamic Analysis (Runtime)

Tracks imports during code execution:

```bash
reqtracker track --mode dynamic ./app.py
```

```python
packages = reqtracker.track(['./app.py'], mode='dynamic')
```

#### ⚡ Hybrid Analysis (Default)

Combines static and dynamic analysis for maximum accuracy:

```bash
reqtracker track --mode hybrid ./src
```

```python
packages = reqtracker.track(['./src'], mode='hybrid')  # Default mode
```

### Version Strategies

Control how package versions are pinned:

```bash
# Exact versions (==1.2.3)
reqtracker generate --version-strategy exact

# Compatible versions (~=1.2.3) - default
reqtracker generate --version-strategy compatible

# Minimum versions (>=1.2.3)
reqtracker generate --version-strategy minimum

# No version constraints
reqtracker generate --version-strategy none
```

```python
# In Python
reqtracker.generate(packages, version_strategy='exact')
```

### Configuration

Create a `.reqtracker.toml` file in your project root:

```toml
[tool.reqtracker]
# Analysis mode: "static", "dynamic", or "hybrid"
mode = "hybrid"

# File patterns to include
include_patterns = ["*.py"]

# File patterns to exclude
exclude_patterns = ["test_*.py", "*_test.py", "tests/**"]

# Directories to exclude
exclude_dirs = ["tests", "docs", ".git", "__pycache__"]

# Custom import mappings
[tool.reqtracker.import_mappings]
cv2 = "opencv-python"
sklearn = "scikit-learn"

[tool.reqtracker.output]
# Output file path
file = "requirements.txt"

# Version strategy
version_strategy = "compatible"

# Include header with generation info
include_header = true

# Sort packages alphabetically
sort_packages = true
```

---

## 🛠️ CLI Reference

### Commands

#### `reqtracker track`

Track dependencies in source files:

```bash
reqtracker track [PATHS...] [OPTIONS]

Options:
  --mode {static,dynamic,hybrid}  Analysis mode (default: hybrid)
  --config PATH                   Configuration file path
  --verbose                       Verbose output
  --quiet                         Quiet mode
```

#### `reqtracker generate`

Generate requirements.txt from tracked packages:

```bash
reqtracker generate [OPTIONS]

Options:
  --output PATH                   Output file (default: requirements.txt)
  --version-strategy {exact,compatible,minimum,none}
  --no-header                     Skip header in output
  --no-sort                       Don't sort packages
  --config PATH                   Configuration file path
```

#### `reqtracker analyze`

Complete workflow - track and generate:

```bash
reqtracker analyze [PATHS...] [OPTIONS]

Options:
  --output PATH                   Output file (default: requirements.txt)
  --mode {static,dynamic,hybrid}  Analysis mode (default: hybrid)
  --version-strategy {exact,compatible,minimum,none}
  --config PATH                   Configuration file path
  --verbose                       Verbose output
```

### Examples

```bash
# Analyze specific directories
reqtracker analyze ./src ./lib --mode static

# Generate with custom output and exact versions
reqtracker generate --output deps.txt --version-strategy exact

# Track with custom config
reqtracker track --config ./custom-config.toml

# Verbose analysis of entire project
reqtracker analyze --verbose --mode hybrid
```

---

## 📖 API Reference

### Main Functions

#### `reqtracker.track()`

```python
def track(
    source_paths: Optional[List[Union[str, Path]]] = None,
    mode: str = "hybrid",
    config: Optional[Config] = None
) -> Set[str]:
    """Track dependencies in source files.
    
    Args:
        source_paths: Paths to analyze. If None, uses current directory.
        mode: Analysis mode - 'static', 'dynamic', or 'hybrid'.
        config: Configuration object.
        
    Returns:
        Set of package names found in the code.
    """
```

#### `reqtracker.generate()`

```python
def generate(
    packages: Optional[Set[str]] = None,
    output: Union[str, Path] = "requirements.txt",
    version_strategy: str = "compatible",
    include_header: bool = True,
    sort_packages: bool = True
) -> str:
    """Generate requirements.txt from packages.
    
    Args:
        packages: Package names. If None, auto-detects from current directory.
        output: Output file path.
        version_strategy: Version pinning strategy.
        include_header: Include generation header.
        sort_packages: Sort packages alphabetically.
        
    Returns:
        Generated requirements.txt content.
    """
```

#### `reqtracker.analyze()`

```python
def analyze(
   source_paths: Optional[List[Union[str, Path]]] = None,
   output: Union[str, Path] = "requirements.txt",
   mode: str = "hybrid",
   version_strategy: str = "compatible",
   include_header: bool = True,
   sort_packages: bool = True,
   config: Optional[Config] = None
) -> Set[str]:
   """Complete workflow: track dependencies and generate requirements.txt.
   
   Returns:
       Set of packages found and included in requirements.txt.
   """
   ```

### Advanced Usage

#### Custom Configuration

```python
from reqtracker import Config, TrackerMode

# Create custom configuration
config = Config(
    mode=TrackerMode.STATIC,
    include_patterns=["*.py"],
    exclude_patterns=["test_*.py"],
    exclude_dirs=["tests", "docs"]
)

# Use with tracking
packages = reqtracker.track(['./src'], config=config)
```

#### Using Core Classes

```python
from reqtracker import Tracker, RequirementsGenerator, VersionStrategy

# Advanced tracking
tracker = Tracker(config)
packages = tracker.track(['./src'], TrackingMode.HYBRID)

# Advanced generation
generator = RequirementsGenerator(VersionStrategy.EXACT)
content = generator.generate(packages, "deps.txt")
```

---

## 🎯 Use Cases

### Web Development

```bash
# Django/Flask project
reqtracker analyze ./myproject --exclude-patterns "*/migrations/*"
```

### Data Science

```bash
# Jupyter notebook environment
reqtracker track ./notebooks --mode dynamic
```

### Package Development

```bash
# Library with examples and tests
reqtracker analyze ./src --exclude-dirs tests examples docs
```

### CI/CD Integration

```bash
# In GitHub Actions
- name: Update requirements
  run: |
    reqtracker analyze
    git add requirements.txt
    git commit -m "Update requirements.txt" || true
```

---

## 🔧 Advanced Configuration

### Import Mappings

Some packages have different import names than their PyPI names:

|Import Name|Package Name|
|---|---|
|`cv2`|`opencv-python`|
|`sklearn`|`scikit-learn`|
|`PIL`|`Pillow`|
|`yaml`|`PyYAML`|

reqtracker includes built-in mappings for common packages and allows custom mappings via configuration.

### File Filtering

Control which files are analyzed:

```toml
[tool.reqtracker]
# Include patterns (glob-style)
include_patterns = ["*.py", "scripts/*.py"]

# Exclude patterns
exclude_patterns = [
    "test_*.py",
    "*_test.py", 
    "tests/**",
    "**/migrations/**"
]

# Exclude directories
exclude_dirs = ["tests", "docs", ".git", "__pycache__", "venv"]
```

---

## 🤝 Contributing

I welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/oleksii-shcherbak/reqtracker.git
cd reqtracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
pre-commit install
```

### Running Tests

```bash
pytest
pytest --cov=src/reqtracker --cov-report=html
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Documentation**: Coming soon
- **PyPI**: Coming soon
- **Issues**: [GitHub Issues](https://github.com/oleksii-shcherbak/reqtracker/issues)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🙏 Acknowledgments

- Inspired by the need for better dependency management in Python projects
- Built with modern Python development practices
- Designed for both individual developers and teams
