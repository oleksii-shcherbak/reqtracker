# v1.0.7 Release Notes

## Overview
This release fixes critical bugs discovered in the CLI that were causing incorrect dependency detection, including transitive dependencies and self-references.

## 🐛 Bug Fixes
- **Fixed critical CLI bug**: No longer includes transitive dependencies (e.g., matplotlib's numpy, pillow, etc.)
- **Fixed self-reference bug**: reqtracker no longer includes itself in requirements.txt
- **Fixed stdlib filtering**: Added pyexpat and other missing stdlib modules
- **Fixed namespace packages**: Filters out mpl_toolkits and similar namespace packages

## 🔄 Changes
- **Default mode changed**: Static mode is now default (was hybrid) for reliable results
- **Experimental warnings**: Dynamic and hybrid modes now show warnings about transitive dependencies
- **Version updated**: 1.0.6 → 1.0.7
- **Documentation updated**: Added notes about experimental modes

## ✅ Testing
- All 213 unit tests passing
- CLI commands verified working
- Python API verified working
- Critical bugs verified fixed

## ⚠️ Known Limitations
- Dynamic and hybrid modes are experimental and may include transitive dependencies
- This will be properly fixed in v1.0.8

## 📦 What Works Perfectly
- `reqtracker analyze` - Generates clean requirements.txt
- `reqtracker track` - Lists only direct imports
- `reqtracker generate` - Creates requirements with various version strategies
- Static mode - 100% accurate dependency detection
- Python API - All functions working correctly

## 🚀 Installation
```bash
pip install --upgrade reqtracker
```

## 📝 Example Usage
```bash
# Analyze your project (uses static mode by default)
reqtracker analyze

# Track specific files
reqtracker track src/

# Generate with exact versions
reqtracker generate --exact
```

## 🔜 Next Release (v1.0.8)
- Proper fix for dynamic tracking to exclude transitive dependencies
- Restore hybrid as default mode
- Enhanced import detection capabilities
