# reqtracker Documentation

Welcome to the comprehensive documentation for reqtracker, a Python dependency tracking and requirements.txt generation tool.

## Documentation Overview

### 📚 [API Documentation](api/README.md)
Complete reference for all modules, classes, and functions:
- Main API functions (track, generate, analyze)
- Core modules (Tracker, Config, Generator)
- Analysis modules (StaticAnalyzer, DynamicTracker)
- Utility modules (Mappings, Utils)

### 🖥️ [CLI Documentation](cli/README.md)
Comprehensive command-line interface guide:
- Installation and setup
- Command reference
- Configuration options
- Usage examples
- Troubleshooting

### 📖 Guides
- [Configuration Guide](guides/configuration.md) - Detailed configuration options
- [Integration Guide](guides/integration.md) - CI/CD and tool integration
- [Best Practices](guides/best-practices.md) - Recommended workflows

### 🚀 [Examples](../examples/README.md)
Practical examples and tutorials:
- Basic usage examples
- Web development (Django, Flask)
- Data science (Jupyter, ML)
- Advanced configurations
- CI/CD integration

## Quick Links

- [GitHub Repository](https://github.com/oleksii-shcherbak/reqtracker)
- [Issue Tracker](https://github.com/oleksii-shcherbak/reqtracker/issues)
- [PyPI Package](https://pypi.org/project/reqtracker/) (coming soon)

## Getting Started

### Installation
```bash
pip install reqtracker
```

### Basic Usage
```python
import reqtracker

# Track and generate requirements
reqtracker.analyze()
```

### CLI Usage
```bash
# Track dependencies and generate requirements.txt
reqtracker analyze
```

## Features

- **Multiple Analysis Modes**: Static, dynamic, and hybrid analysis
- **Smart Package Mapping**: Handles import name vs package name differences
- **Flexible Version Strategies**: Exact, compatible, minimum, or no versions
- **Highly Configurable**: TOML-based configuration with extensive options
- **CLI and API**: Both command-line and programmatic interfaces
- **Well-Tested**: Comprehensive test suite with >95% coverage

## License

reqtracker is released under the MIT License. See [LICENSE](../LICENSE) for details.
