# Main API Functions

The reqtracker package provides three main functions for dependency tracking and requirements generation.

## track()

Track dependencies in Python source files using static analysis, dynamic analysis, or both.

### Signature

```python
def track(
    source_paths: Optional[List[Union[str, Path]]] = None,
    mode: str = "hybrid",
    config: Optional[Config] = None,
) -> Set[str]:
```

### Parameters

- **source_paths** (Optional[List[Union[str, Path]]]) - Paths to analyze. Defaults to current directory.
- **mode** (str) - Analysis mode: "static", "dynamic", or "hybrid". Default: "hybrid".
- **config** (Optional[Config]) - Custom configuration object. If not provided, uses defaults.

### Returns

- **Set[str]** - Set of discovered package names (e.g., {"requests", "numpy", "pandas"})

### Examples

```python
import reqtracker

# Track current directory
packages = reqtracker.track()

# Track specific paths
packages = reqtracker.track(["./src", "./lib"])

# Use static analysis only
packages = reqtracker.track(mode="static")

# Use custom configuration
from reqtracker import Config, TrackerMode

config = Config(
    mode=TrackerMode.STATIC,
    exclude_patterns=["test_*.py", "*/tests/*"]
)
packages = reqtracker.track(config=config)
```

### Analysis Modes

1. **static** - Parses Python AST to find import statements
   - Fast and safe (no code execution)
   - May miss dynamic imports
   - Best for CI/CD pipelines

2. **dynamic** - Tracks imports during runtime
   - Catches all imports including dynamic ones
   - Requires code execution
   - Best for complex projects with conditional imports

3. **hybrid** (default) - Combines static and dynamic analysis
   - Most comprehensive results
   - Balances safety and completeness
   - Recommended for most use cases

## generate()

Generate requirements.txt content from a set of packages.

### Signature

```python
def generate(
    packages: Optional[Set[str]] = None,
    output: Optional[Union[str, Path]] = None,
    version_strategy: str = "compatible",
    include_header: bool = True,
    sort_packages: bool = True,
) -> str:
```

### Parameters

- **packages** (Optional[Set[str]]) - Package names to include. If None, tracks current directory first.
- **output** (Optional[Union[str, Path]]) - Output file path. If provided, writes to file.
- **version_strategy** (str) - Version pinning strategy: "exact", "compatible", "minimum", or "none".
- **include_header** (bool) - Include generation timestamp header. Default: True.
- **sort_packages** (bool) - Sort packages alphabetically. Default: True.

### Returns

- **str** - Generated requirements.txt content

### Version Strategies

1. **exact** - Pin exact versions (==1.2.3)
   - Most reproducible
   - May prevent security updates
   - Best for production deployments

2. **compatible** (default) - Compatible versions (~=1.2.3)
   - Allows patch updates
   - Prevents breaking changes
   - Best for most projects

3. **minimum** - Minimum versions (>=1.2.3)
   - Most flexible
   - Allows all updates
   - Best for libraries

4. **none** - No version constraints
   - Only package names
   - Maximum flexibility
   - Best for initial development

### Examples

```python
# Generate from tracked packages
packages = reqtracker.track()
content = reqtracker.generate(packages)

# Write directly to file
reqtracker.generate(packages, output="requirements.txt")

# Use exact versions for production
reqtracker.generate(
    packages,
    output="requirements-prod.txt",
    version_strategy="exact"
)

# Generate without header
content = reqtracker.generate(
    packages,
    include_header=False,
    sort_packages=True
)
```

## analyze()

Complete workflow that combines tracking and generation in a single call.

### Signature

```python
def analyze(
    source_paths: Optional[List[Union[str, Path]]] = None,
    output: Union[str, Path] = "requirements.txt",
    mode: str = "hybrid",
    version_strategy: str = "compatible",
    config: Optional[Config] = None,
    include_header: bool = True,
    sort_packages: bool = True,
) -> Set[str]:
```

### Parameters

Combines parameters from both track() and generate():

- **source_paths** - Paths to analyze
- **output** - Output file path (default: "requirements.txt")
- **mode** - Analysis mode
- **version_strategy** - Version pinning strategy
- **config** - Custom configuration
- **include_header** - Include timestamp header
- **sort_packages** - Sort packages alphabetically

### Returns

- **Set[str]** - Set of discovered package names (same as track())

### Examples

```python
# Basic usage - analyze current directory
packages = reqtracker.analyze()

# Custom output and strategy
packages = reqtracker.analyze(
    source_paths=["./src"],
    output="requirements-dev.txt",
    version_strategy="compatible"
)

# Production deployment
packages = reqtracker.analyze(
    source_paths=["./app"],
    output="requirements-prod.txt",
    mode="static",
    version_strategy="exact"
)

# With custom configuration
from reqtracker import Config, TrackerMode

config = Config(
    mode=TrackerMode.HYBRID,
    exclude_patterns=["tests/**/*", "docs/**/*"]
)

packages = reqtracker.analyze(
    source_paths=["."],
    config=config,
    output="requirements.txt"
)
```

## Deprecated Functions

### scan()

**Deprecated**: Use track() instead.

```python
# Old (deprecated)
packages = reqtracker.scan(["./src"])

# New
packages = reqtracker.track(["./src"])
```

### write_requirements()

**Deprecated**: Use generate() with output parameter instead.

```python
# Old (deprecated)
reqtracker.write_requirements(packages, "requirements.txt")

# New
reqtracker.generate(packages, output="requirements.txt")
```

## Error Handling

All functions may raise the following exceptions:

- **FileNotFoundError** - Source path does not exist
- **ValueError** - Invalid configuration or parameters
- **RuntimeError** - Analysis or generation errors

Example:

```python
try:
    packages = reqtracker.track(["./nonexistent"])
except FileNotFoundError as e:
    print(f"Error: {e}")
```

## Best Practices

1. **Use appropriate mode for your context**
   - CI/CD: Use "static" mode for safety
   - Development: Use "hybrid" for completeness
   - Testing: Use "dynamic" to catch all imports

2. **Choose version strategy based on use case**
   - Production: "exact" for reproducibility
   - Development: "compatible" for flexibility
   - Libraries: "minimum" to avoid conflicts

3. **Configure exclusions properly**
   - Exclude test directories
   - Exclude documentation
   - Exclude build artifacts

4. **Generate multiple requirements files**
   - requirements.txt (base dependencies)
   - requirements-dev.txt (includes test tools)
   - requirements-prod.txt (exact versions)
