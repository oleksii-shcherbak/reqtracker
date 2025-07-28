# reqtracker Documentation

Welcome to the comprehensive documentation for reqtracker, a Python dependency tracking and requirements.txt generation tool.

## Documentation Overview

### 📚 [API Documentation](api/README.md)
Complete reference for all modules, classes, and functions:
- Main API functions (track, generate, analyze)
- Core modules (Tracker, Config, Generator)
- Analysis modules (StaticAnalyzer)

### 📖 Guides
- [Configuration Guide](guides/configuration.md) - Detailed configuration options

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
- [PyPI Package](https://pypi.org/project/reqtracker/)
- [Documentation](https://github.com/oleksii-shcherbak/reqtracker#readme)

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
- **Well-Tested**: Comprehensive test suite with 204 tests and >95% coverage

## Test Coverage
The project includes comprehensive testing:
- **Unit Tests**: 200+ tests covering all modules
- **Integration Tests**: Real project testing with various scenarios
- **Performance Tests**: Benchmarks for different project sizes
- **Cross-Platform Tests**: Compatibility across operating systems

## License
reqtracker is released under the MIT License. See [LICENSE](../LICENSE) for details.
