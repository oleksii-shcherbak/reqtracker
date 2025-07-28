# reqtracker API Documentation

This directory contains API documentation for the main reqtracker modules.

## Core Documentation

- [Main API Functions](main-api.md) - Core functions (track, generate, analyze)
- [Tracker Module](tracker.md) - Main coordination logic
- [Config Module](config.md) - Configuration management
- [Static Analyzer](static-analyzer.md) - AST-based import detection
- [Generator Module](generator.md) - Requirements file generation

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

## See Also


- [Configuration Guide](../guides/configuration.md) - Detailed configuration options
- [Examples](../../examples/README.md) - Practical usage examples
