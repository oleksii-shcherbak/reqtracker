# Mappings Module API

The mappings module handles the mapping between Python import names and their corresponding PyPI package names.

## Overview

Many Python packages have different import names than their PyPI package names.

## Functions

### resolve_package_name(import_name: str) -> str
Map an import name to its corresponding PyPI package name.

## Built-in Mappings

- cv2 -> opencv-python
- sklearn -> scikit-learn
- PIL -> Pillow
- yaml -> PyYAML
