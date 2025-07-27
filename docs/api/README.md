# reqtracker API Documentation

This directory contains comprehensive API documentation for all reqtracker modules, classes, and functions.

## Documentation Structure

- [Main API Functions](main-api.md) - Core functions (track, generate, analyze)
- [Tracker Module](tracker.md) - Main coordination logic
- [Config Module](config.md) - Configuration management
- [Static Analyzer](static-analyzer.md) - AST-based import detection
- [Dynamic Tracker](dynamic-tracker.md) - Runtime import tracking
- [Generator Module](generator.md) - Requirements file generation
- [Mappings Module](mappings.md) - Import-to-package name mappings
- [Utils Module](utils.md) - Utility functions
- [CLI Module](cli.md) - Command-line interface implementation

## Quick Start

The main reqtracker API provides three primary functions:

```python
import reqtracker

# Track dependencies
packages = reqtracker.track(["./src"], mode="hybrid")

# Generate requirements.txt
content = reqtracker.generate(packages, version_strategy="compatible")

# Complete workflow (track + generate)
packages = reqtracker.analyze(["./src"], output="requirements.txt")
```

## Module Overview

### Core Modules

1. **reqtracker** - Main package API
   - track() - Track dependencies in source files
   - generate() - Generate requirements.txt content
   - analyze() - Complete workflow (track + generate)

2. **reqtracker.tracker** - Coordination logic
   - Tracker - Main class that coordinates analysis
   - TrackingMode - Enum for analysis modes

3. **reqtracker.config** - Configuration management
   - Config - Main configuration dataclass
   - OutputConfig - Output-specific settings
   - TrackerMode - Analysis mode enum

### Analysis Modules

4. **reqtracker.static_analyzer** - AST-based analysis
   - StaticAnalyzer - Parses Python AST for imports

5. **reqtracker.dynamic_tracker** - Runtime tracking
   - DynamicTracker - Hooks into Python import system

### Output Modules

6. **reqtracker.generator** - Requirements generation
   - RequirementsGenerator - Creates requirements.txt
   - VersionStrategy - Version pinning strategies

7. **reqtracker.mappings** - Import mappings
   - ImportMapper - Maps import names to packages

### Support Modules

8. **reqtracker.utils** - Utilities
   - File path utilities
   - Standard library detection

9. **reqtracker.cli** - CLI implementation
   - Click-based command interface
   - Command groups and options

## API Design Principles

1. **Simple by Default** - Works with zero configuration
2. **Highly Configurable** - Extensive customization options
3. **Type-Safe** - Full type hints for all public APIs
4. **Well-Tested** - Comprehensive test coverage
5. **Documented** - Detailed docstrings and examples

## Usage Patterns

### Basic Usage
```python
# Track current directory
packages = reqtracker.track()

# Generate with exact versions
reqtracker.generate(packages, version_strategy="exact")
```

### Advanced Usage
```python
from reqtracker import Config, TrackerMode

# Custom configuration
config = Config(
    mode=TrackerMode.STATIC,
    exclude_patterns=["tests/**/*", "docs/**/*"],
    include_patterns=["src/**/*.py"]
)

# Track with custom config
packages = reqtracker.track(config=config)
```

### Integration Examples
```python
# CI/CD Integration
packages = reqtracker.analyze(
    ["./src"],
    output="requirements-prod.txt",
    version_strategy="exact",
    mode="static"
)

# Development workflow
dev_packages = reqtracker.analyze(
    ["."],
    output="requirements-dev.txt",
    version_strategy="compatible",
    mode="hybrid"
)
```

## See Also

- [CLI Documentation](../../cli/README.md) - Command-line interface guide
- [Configuration Guide](../guides/configuration.md) - Detailed configuration options
- [Examples](../../examples/README.md) - Practical usage examples
