# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.6] - 2025-08-05

### Fixed
- Fixed stdlib detection to correctly identify all Python standard library modules
- Added comprehensive list of 200+ stdlib modules including contextvars, ctypes, etc.
- Fixed bug where standard library modules were incorrectly included in requirements.txt

### Added
- Comprehensive test suite for stdlib detection covering all standard library modules
- Real-world scenario tests to prevent regression of stdlib detection bugs

### Changed
- Improved `is_standard_library()` function with complete stdlib module list
- Consolidated stdlib detection tests into test_utils.py for better organization

## [1.0.5] - 2025-07-29

### Fixed
- Critical bug: prevent infinite recursion when analyzing files that import reqtracker
- Filter out local project modules from requirements.txt
- Add tracemalloc to standard library list
- Fix version display in CLI (was showing 1.0.0 instead of actual version)
- Fix unused variable warning in exception handler

### Added
- Add `is_local_module()` function to detect project files
- Add PyCharm-specific warning suppressions for false positives
- Add recursion prevention using environment variable REQTRACKER_ANALYZING

### Changed
- Update tests to match new behavior (silent exception handling)
- Update `_resolve_package_names()` to accept and use source paths

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
- **PyPI Package Publication**: reqtracker is now available on PyPI! Install with `pip install reqtracker`
- Comprehensive package metadata in pyproject.toml for better discoverability
- CLI entry point properly configured for system-wide usage
- Distribution testing workflow to ensure package quality

### Changed
- Updated installation instructions to use pip instead of GitHub clone
- Enhanced package description and keywords for PyPI listing

### Fixed
- Package distribution includes all necessary files
- Entry points correctly set up for CLI commands

## [1.0.0] - 2025-07-27

### Added
- Initial release of reqtracker
- Static analysis using AST for import detection
- Dynamic runtime import tracking with import hooks
- Hybrid analysis mode combining static and dynamic approaches
- Smart package name resolution (e.g., cv2 → opencv-python)
- Standard library detection to exclude built-in modules
- Multiple version strategies (exact, compatible, minimum, none)
- Configurable include/exclude patterns
- TOML configuration file support
- Clean CLI interface with track, generate, and analyze commands
- Comprehensive test suite with 200+ tests
- Full documentation and examples

### Features
- Track Python dependencies by analyzing actual imports
- Generate clean requirements.txt files
- Support for complex import patterns and edge cases
- Intelligent local module detection
- Thread-safe dynamic tracking
- Performance optimized for large codebases

[1.0.6]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.5...v1.0.6
[1.0.5]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/oleksii-shcherbak/reqtracker/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/oleksii-shcherbak/reqtracker/releases/tag/v1.0.0
