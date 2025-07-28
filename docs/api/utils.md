# Utils Module API

The utils module provides utility functions for path handling and standard library detection.

## Functions

### get_package_name(import_name: str) -> str
Get the package name for an import, applying any necessary mappings.

### is_standard_library(module_name: str) -> bool
Check if a module is part of the Python standard library.

### normalize_package_name(package_name: str) -> str
Normalize package names to lowercase with underscores replaced by hyphens.

## Implementation

The module provides core utilities used throughout reqtracker for handling package names and detecting standard library modules.
