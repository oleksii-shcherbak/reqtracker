# Tracker Module

The tracker module contains the main coordination logic for dependency tracking.

## Classes

### Tracker

Main class that coordinates static and dynamic analysis.

#### Constructor

```python
class Tracker:
    def __init__(self, config: Optional[Config] = None):
        """Initialize tracker with configuration.

        Args:
            config: Configuration object. Uses defaults if not provided.
        """
```

#### Methods

##### track()

```python
def track(
    self,
    source_paths: Optional[List[Union[str, Path]]] = None
) -> Set[str]:
    """Track dependencies in source files.

    Args:
        source_paths: Paths to analyze. Defaults to current directory.

    Returns:
        Set of package names.
    """
```

##### get_imports()

```python
def get_imports(self) -> Set[str]:
    """Get all discovered imports.

    Returns:
        Set of import names (may differ from package names).
    """
```

##### get_packages()

```python
def get_packages(self) -> Set[str]:
    """Get all discovered packages.

    Returns:
        Set of package names suitable for requirements.txt.
    """
```

### TrackingMode

Enum defining available analysis modes.

```python
class TrackingMode(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"
    HYBRID = "hybrid"
```

## Usage Examples

### Basic Usage

```python
from reqtracker.tracker import Tracker

# Create tracker with defaults
tracker = Tracker()

# Track dependencies
packages = tracker.track(["./src"])
print(f"Found packages: {packages}")
```

### Custom Configuration

```python
from reqtracker.tracker import Tracker
from reqtracker.config import Config, TrackerMode

# Configure tracker
config = Config(
    mode=TrackerMode.STATIC,
    exclude_patterns=["test_*.py", "*/tests/*"]
)

# Create tracker with config
tracker = Tracker(config)
packages = tracker.track()
```

### Accessing Raw Imports

```python
tracker = Tracker()
tracker.track(["./myproject"])

# Get import names (e.g., "cv2", "sklearn")
imports = tracker.get_imports()

# Get package names (e.g., "opencv-python", "scikit-learn")
packages = tracker.get_packages()

print(f"Imports: {imports}")
print(f"Packages: {packages}")
```

## How It Works

### Static Analysis Flow

1. Discovers Python files based on include/exclude patterns
2. Parses each file's AST to find import statements
3. Filters out standard library imports
4. Maps import names to package names

### Dynamic Analysis Flow

1. Installs import hooks in Python's import system
2. Executes source files in a controlled environment
3. Records all import events
4. Filters and processes import names

### Hybrid Analysis Flow

1. Performs static analysis first
2. Runs dynamic analysis to catch missed imports
3. Merges results from both approaches
4. Deduplicates and normalizes package names

## Integration with Other Modules

### With StaticAnalyzer

```python
# Tracker internally uses StaticAnalyzer
from reqtracker.static_analyzer import StaticAnalyzer

analyzer = StaticAnalyzer(config)
imports = analyzer.analyze_file("script.py")
```

### With DynamicTracker

```python
# Tracker internally uses DynamicTracker
from reqtracker.dynamic_tracker import DynamicTracker

with DynamicTracker() as tracker:
    # Import tracking is active here
    import some_module
```

### With ImportMapper

```python
# Tracker uses ImportMapper for name resolution
from reqtracker.mappings import ImportMapper

mapper = ImportMapper()
package = mapper.get_package_name("cv2")  # Returns "opencv-python"
```

## Configuration Options

The Tracker respects all configuration options from the Config object:

- **mode** - Analysis mode (static/dynamic/hybrid)
- **include_patterns** - File patterns to include
- **exclude_patterns** - File patterns to exclude
- **ignore_packages** - Packages to ignore
- **custom_mappings** - Custom import-to-package mappings

## Error Handling

```python
from reqtracker.tracker import Tracker

tracker = Tracker()

try:
    packages = tracker.track(["./nonexistent"])
except FileNotFoundError:
    print("Source path not found")
except RuntimeError as e:
    print(f"Tracking error: {e}")
```

## Performance Considerations

1. **Static mode** is fastest - O(n) where n is number of files
2. **Dynamic mode** is slower - depends on import complexity
3. **Hybrid mode** combines both - use when accuracy is critical

### Optimization Tips

- Use static mode in CI/CD for speed
- Exclude unnecessary directories (tests, docs)
- Cache results when analyzing large codebases
- Use specific source paths instead of scanning everything

## Thread Safety

The Tracker class is thread-safe for read operations but not for concurrent track() calls. Use separate instances for parallel processing:

```python
from concurrent.futures import ThreadPoolExecutor
from reqtracker.tracker import Tracker

def analyze_path(path):
    tracker = Tracker()  # Separate instance per thread
    return tracker.track([path])

with ThreadPoolExecutor() as executor:
    results = executor.map(analyze_path, paths)
```
