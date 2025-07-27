#!/bin/bash
# reqtracker CLI Examples
#
# This script demonstrates common command-line usage patterns
# for reqtracker in different scenarios.

echo "=== reqtracker CLI Examples ==="
echo

# Basic commands
echo "1. Basic Commands"
echo "================="
echo

echo "# Track dependencies in current directory"
echo "reqtracker track"
echo

echo "# Track dependencies in specific paths"
echo "reqtracker track ./src ./lib"
echo

echo "# Generate requirements.txt"
echo "reqtracker generate"
echo

echo "# Complete workflow (track + generate)"
echo "reqtracker analyze"
echo

# Different modes
echo "2. Analysis Modes"
echo "================="
echo

echo "# Static analysis only (AST-based)"
echo "reqtracker track --mode static"
echo

echo "# Dynamic analysis only (runtime)"
echo "reqtracker track --mode dynamic ./app.py"
echo

echo "# Hybrid analysis (default)"
echo "reqtracker track --mode hybrid"
echo

# Version strategies
echo "3. Version Strategies"
echo "===================="
echo

echo "# Exact versions (==1.2.3)"
echo "reqtracker generate --version-strategy exact"
echo

echo "# Compatible versions (~=1.2.3) - default"
echo "reqtracker generate --version-strategy compatible"
echo

echo "# Minimum versions (>=1.2.3)"
echo "reqtracker generate --version-strategy minimum"
echo

echo "# No version constraints"
echo "reqtracker generate --version-strategy none"
echo

# Output options
echo "4. Output Options"
echo "================="
echo

echo "# Custom output file"
echo "reqtracker generate --output deps.txt"
echo

echo "# Skip header in output"
echo "reqtracker generate --no-header"
echo

echo "# Don't sort packages"
echo "reqtracker generate --no-sort"
echo

# Configuration
echo "5. Configuration"
echo "================"
echo

echo "# Use custom config file"
echo "reqtracker track --config ./custom-config.toml"
echo

echo "# Verbose output"
echo "reqtracker analyze --verbose"
echo

echo "# Quiet mode"
echo "reqtracker track --quiet"
echo

# Real-world examples
echo "6. Real-World Examples"
echo "======================"
echo

echo "# Django project"
echo "reqtracker analyze ./myproject --exclude-patterns '*/migrations/*'"
echo

echo "# Data science project"
echo "reqtracker track ./notebooks --mode dynamic"
echo

echo "# Library development"
echo "reqtracker analyze ./src --exclude-dirs tests examples docs"
echo

echo "# CI/CD pipeline"
echo "reqtracker analyze --output requirements.txt --version-strategy exact"
echo

# Combined examples
echo "7. Combined Usage"
echo "================="
echo

echo "# Advanced Django analysis"
echo "reqtracker analyze ./myapp \\"
echo "  --mode hybrid \\"
echo "  --version-strategy compatible \\"
echo "  --exclude-patterns '*/migrations/*' '*/tests/*' \\"
echo "  --output requirements/base.txt \\"
echo "  --verbose"
echo

echo "# Production deployment preparation"
echo "reqtracker analyze ./src \\"
echo "  --mode static \\"
echo "  --version-strategy exact \\"
echo "  --output requirements/production.txt \\"
echo "  --no-header"
echo

echo "# Development environment"
echo "reqtracker analyze . \\"
echo "  --mode hybrid \\"
echo "  --exclude-dirs tests docs .git __pycache__ venv \\"
echo "  --config .reqtracker.toml"
echo

echo
echo "=== Examples Complete ==="
echo
echo "To run these commands:"
echo "1. Navigate to your project directory"
echo "2. Copy and paste any command above"
echo "3. Modify paths and options as needed"
echo
echo "For more help:"
echo "  reqtracker --help"
echo "  reqtracker track --help"
echo "  reqtracker generate --help"
echo "  reqtracker analyze --help"
