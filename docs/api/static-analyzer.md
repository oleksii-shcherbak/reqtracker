# Static Analyzer Module

The static_analyzer module provides AST-based Python import detection.

## Classes

### StaticAnalyzer

Analyzes Python files by parsing their Abstract Syntax Tree (AST) to find import statements.

#### Constructor

```python
class StaticAnalyzer:
    def __init__(self, config: Optional[Config] = None):
        """Initialize analyzer with configuration.

        Args:
            config: Configuration object. Uses defaults if not provided.
        """
```

#### Methods

##### analyze_file()

```python
def analyze_file(self, file_path: Union[str, Path]) -> Set[str]:
    """Analyze a single Python file for imports.

    Args:
        file_path: Path to Python file.

    Returns:
        Set of import names found in the file.

    Raises:
        FileNotFoundError: If file does not exist.
        SyntaxError: If file has invalid Python syntax.
    """
```

##### analyze_directory()

```python
def analyze_directory(self, directory: Union[str, Path]) -> Set[str]:
    """Recursively analyze all Python files in a directory.

    Args:
        directory: Path to directory.

    Returns:
        Set of all import names found.
    """
```

##### discover_files()

```python
def discover_files(self, paths: List[Union[str, Path]]) -> List[Path]:
    """Discover Python files based on include/exclude patterns.

    Args:
        paths: List of paths to search.

    Returns:
        List of Python file paths that match patterns.
    """
```

## How It Works

### AST Parsing

The analyzer uses Python's built-in `ast` module to parse source files:

1. **Read source file** as text
2. **Parse into AST** using `ast.parse()`
3. **Walk the tree** looking for import nodes
4. **Extract import names** from Import and ImportFrom nodes

### Import Detection

Detects all forms of Python imports:

```python
# Simple import
import requests
# Detected: "requests"

# From import
from flask import Flask
# Detected: "flask"

# Aliased import
import numpy as np
# Detected: "numpy"

# Multiple imports
from django.conf import settings, urls
# Detected: "django"

# Relative imports
from . import utils
# Detected: "." (filtered out)
```

### Pattern Matching

Uses glob patterns for file discovery:

```python
analyzer = StaticAnalyzer(Config(
    include_patterns=["*.py", "src/**/*.py"],
    exclude_patterns=["test_*.py", "*/tests/*"]
))
```

## Usage Examples

### Basic File Analysis

```python
from reqtracker.static_analyzer import StaticAnalyzer

analyzer = StaticAnalyzer()

# Analyze single file
imports = analyzer.analyze_file("main.py")
print(f"Imports: {imports}")
```

### Directory Analysis

```python
# Analyze entire directory
imports = analyzer.analyze_directory("./src")

# Analyze multiple directories
all_imports = set()
for directory in ["./src", "./lib", "./scripts"]:
    imports = analyzer.analyze_directory(directory)
    all_imports.update(imports)
```

### Custom Configuration

```python
from reqtracker.config import Config

config = Config(
    include_patterns=["*.py", "!test_*.py"],
    exclude_patterns=[
        "tests/**/*",
        "docs/**/*",
        "build/**/*"
    ]
)

analyzer = StaticAnalyzer(config)
files = analyzer.discover_files(["."])
print(f"Found {len(files)} Python files")
```

### Error Handling

```python
analyzer = StaticAnalyzer()

try:
    imports = analyzer.analyze_file("script.py")
except FileNotFoundError:
    print("File not found")
except SyntaxError as e:
    print(f"Invalid Python syntax: {e}")
```

## AST Node Types

The analyzer handles these AST node types:

### Import

```python
# AST: Import node
import os
import sys, json
import urllib.request

# Extracts: "os", "sys", "json", "urllib"
```

### ImportFrom

```python
# AST: ImportFrom node
from os import path
from urllib.request import urlopen
from . import local_module

# Extracts: "os", "urllib", "."
```

### Nested Imports

The analyzer recursively walks the entire AST:

```python
# Imports inside functions
def main():
    import requests  # Still detected

# Imports inside conditions
if platform.system() == "Windows":
    import win32api  # Still detected

# Imports inside try blocks
try:
    import optional_dependency  # Still detected
except ImportError:
    pass
```

## Filtering

### Standard Library Detection

Filters out Python standard library imports:

```python
# These are filtered out:
import os
import sys
import json
import datetime

# These are kept:
import requests
import numpy
import custom_module
```

### Relative Import Handling

Relative imports are detected but typically filtered:

```python
# Filtered out:
from . import utils
from .. import parent_module
from ...package import module
```

## Performance Considerations

### File Discovery

- Uses `pathlib` for efficient path operations
- Caches compiled patterns for repeated use
- Short-circuits on exclude patterns

### AST Parsing

- Parses each file only once
- Minimal memory usage (doesn't store full AST)
- Handles large files efficiently

### Optimization Tips

```python
# Limit search scope
analyzer.analyze_directory("./src")    # Better
analyzer.analyze_directory(".")        # Slower

# Use specific patterns
config = Config(
    include_patterns=["src/**/*.py"],  # Specific
    exclude_patterns=["**/test_*.py"]  # Efficient
)
```

## Integration with Tracker

The Tracker class uses StaticAnalyzer internally:

```python
# Inside Tracker.track()
if self.config.mode in [TrackerMode.STATIC, TrackerMode.HYBRID]:
    analyzer = StaticAnalyzer(self.config)
    static_imports = analyzer.analyze_directory(path)
```

## Limitations

1. **No execution** - Cannot detect dynamic imports
2. **No resolution** - Cannot follow import chains
3. **Syntax errors** - Cannot analyze files with syntax errors
4. **String imports** - Cannot detect `__import__("module")`

## Advanced Usage

### Custom Import Visitor

```python
import ast
from reqtracker.static_analyzer import StaticAnalyzer

class CustomAnalyzer(StaticAnalyzer):
    def analyze_file(self, file_path):
        # Custom AST analysis
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        # Custom visitor logic
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Custom processing
                pass

        return imports
```

### Parallel Analysis

```python
from concurrent.futures import ProcessPoolExecutor
from reqtracker.static_analyzer import StaticAnalyzer

def analyze_file_parallel(file_path):
    analyzer = StaticAnalyzer()
    return analyzer.analyze_file(file_path)

# Analyze files in parallel
with ProcessPoolExecutor() as executor:
    files = analyzer.discover_files(["."])
    results = executor.map(analyze_file_parallel, files)

all_imports = set()
for imports in results:
    all_imports.update(imports)
```
