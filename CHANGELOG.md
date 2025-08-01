# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.5] – 2025-07-29

### Fixed
- Filtered out local project files from generated requirements.txt
- Excluded standard library modules (e.g., tracemalloc) from dependency listing
- Suppressed false-positive warnings in PyCharm (e.g., unused variable in exception handler)
- Updated _resolve_package_names() to correctly use source paths

## [1.0.4] - 2025-07-29

### Fixed
- Critical bug: prevent infinite recursion when analyzing files that import reqtracker
- Version display in CLI now shows correct version
- Test suite updated to match new exception handling behavior

## [1.0.3] - 2025-07-28

### Fixed
- Replaced relative links in `README.md` with absolute GitHub URLs for proper rendering on PyPI
- Ensured consistent navigation behavior between GitHub and PyPI project pages

## [1.0.2] - 2025-07-28

### Fixed
- CLI version display now shows correct version instead of 1.0.0
- Version consistency between pyproject.toml and __init__.py

## [1.0.1] - 2025-07-28

### Added
- Published to PyPI - package now available via `pip install reqtracker`
- PyPI classifiers and metadata for better discoverability

### Fixed
- Package distribution configuration for proper PyPI installation

## [1.0.0] - 2025-07-28

### Added
- **Core Functionality**: Complete dependency tracking system
  - Static analysis using Python AST for fast, execution-free dependency detection
  - Dynamic tracking using import hooks for runtime dependency capture
  - Hybrid mode combining both approaches for maximum accuracy

- **Smart Package Mapping**: 100+ built-in import-to-package mappings
  - Handles complex cases like `cv2` → `opencv-python`, `sklearn` → `scikit-learn`
  - Extensible mapping system via configuration

- **Professional CLI Interface**:
  - `reqtracker track` - Track dependencies in source files
  - `reqtracker generate` - Generate requirements.txt files
  - `reqtracker analyze` - Complete workflow (track + generate)
  - Multiple analysis modes (static, dynamic, hybrid)
  - Flexible version strategies (exact, compatible, minimum, none)

- **Python API**: Clean programmatic interface
  - `reqtracker.track()` - Track dependencies
  - `reqtracker.generate()` - Generate requirements
  - `reqtracker.analyze()` - Complete workflow

- **Configuration System**:
  - TOML-based configuration files (`.reqtracker.toml`)
  - Include/exclude patterns with glob support
  - Custom import mappings
  - Output formatting options

- **Comprehensive Documentation**:
  - Professional README with usage examples
  - Complete examples directory with real-world use cases
  - Django, Flask, and data science project examples
  - CI/CD integration examples

- **Quality Assurance**:
  - 159 comprehensive tests with >95% coverage
  - Pre-commit hooks with black, isort, flake8, mypy
  - Integration tests for real-world scenarios
  - Performance testing (handles 500+ files in <0.2s)

### Features
- **Zero Configuration**: Works immediately with sensible defaults
- **Cross-Platform**: Supports Windows, macOS, and Linux
- **Python 3.8+ Support**: Compatible with modern Python versions
- **Thread-Safe**: Safe for concurrent usage
- **Type Hints**: Fully typed codebase with mypy validation

### Performance
- **Excellent Performance**: Processes large codebases (500+ files) in under 0.2 seconds
- **Memory Efficient**: Minimal memory footprint during analysis
- **Scalable**: Tested on projects with 1000+ files

[1.0.5]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/oleksii-shcherbak/reqtracker/releases/tag/v1.0.0
