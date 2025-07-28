# Contributing to reqtracker

Thank you for your interest in contributing to reqtracker! This guide will help you get started with the development workflow and ensure your contributions meet quality standards.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Initial Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/reqtracker.git
   cd reqtracker
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Pre-commit Hooks

This project uses automated code quality tools that run on every commit:

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting and style checking
- **mypy**: Type checking

**Usage:**
```bash
# Hooks run automatically on git commit
git add .
git commit -m "your commit message"

# Run hooks manually on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black
pre-commit run mypy
```

### Code Style Guidelines

#### Formatting Standards
- **Line length**: 88 characters (black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes preferred
- **Import sorting**: Follows isort configuration

#### Type Hints
- All public functions must have type hints
- Use `from typing import` for type annotations
- Return types are required for all functions

#### Docstrings
- Use Google-style docstrings
- Document all parameters, returns, and raises
- Include usage examples for public functions

**Example:**
```python
from typing import Optional, List, Union, Set
from pathlib import Path

from reqtracker import TrackingMode


def track_dependencies(
    source_paths: Optional[List[Union[str, Path]]] = None,
    mode: TrackingMode = TrackingMode.HYBRID
) -> Set[str]:
    """Track dependencies in Python source files.

    Args:
        source_paths: List of paths to analyze. If None, uses current directory.
        mode: Analysis mode for dependency detection.

    Returns:
        Set of package names found in the analyzed code.

    Raises:
        ValueError: If source paths contain invalid directories.

    Examples:
        >>> packages = track_dependencies(["./src"], TrackingMode.STATIC)
        >>> print(packages)
        {"requests", "numpy"}
    """
    pass  # Implementation here
```

### Testing

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/reqtracker --cov-report=html

# Run specific test file
pytest tests/test_tracker.py -v

# Run specific test
pytest tests/test_tracker.py::TestTracker::test_track_default -v
```

#### Test Requirements
- **Coverage target**: >90% for all new code
- **Test types**: Unit tests, integration tests, edge cases
- **Naming**: Test files must start with `test_`
- **Structure**: Use classes to group related tests

#### Writing Tests
```python
from unittest.mock import patch


class TestNewFeature:
    """Test cases for new feature."""

    def test_basic_functionality(self):
        """Test basic functionality works correctly."""
        # Arrange
        input_data = "test_input"
        expected_output = "expected_result"

        # Act
        result = some_function(input_data)

        # Assert
        assert result == expected_output

    @patch("module.dependency")
    def test_with_mock(self, mock_dependency):
        """Test behavior with mocked dependencies."""
        # Arrange
        mock_dependency.return_value = "mocked_result"
        expected_result = "expected_result"

        # Act
        result = some_function()

        # Assert
        assert result == expected_result
        mock_dependency.assert_called_once()
```

### Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(cli): add dry-run mode for preview functionality"
git commit -m "fix(tracker): handle empty directories correctly"
git commit -m "docs(api): update docstrings for track() function"
```

### Branch Naming Conventions

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-topic` - Documentation updates
- `refactor/component-name` - Code refactoring

### Pull Request Process

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation if needed

3. **Ensure quality checks pass:**
   ```bash
   pre-commit run --all-files
   pytest --cov=src/reqtracker
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   git push -u origin feature/your-feature-name
   ```

5. **Create Pull Request:**
   - Use descriptive title following commit format
   - Include detailed description with examples
   - Reference related issues (`Closes #123`)
   - Ensure all CI checks pass

### Pull Request Review Guidelines

#### Before Submitting
- [ ] All tests pass locally
- [ ] Code coverage meets requirements (>90%)
- [ ] Pre-commit hooks pass
- [ ] Documentation updated if needed
- [ ] Manual testing completed

#### Review Checklist
- [ ] Code follows project style guidelines
- [ ] Tests cover new functionality and edge cases
- [ ] Documentation is clear and complete
- [ ] No breaking changes without discussion
- [ ] Performance implications considered

## Code Quality Standards

### Performance Considerations
- Avoid blocking operations in main thread
- Use generators for large data processing
- Profile code for performance bottlenecks
- Consider memory usage for large projects

### Error Handling
- Use specific exception types
- Provide helpful error messages
- Log errors appropriately
- Handle edge cases gracefully

### Security Practices
- Validate all user inputs
- Use safe file operations
- Avoid code execution from strings
- Handle file permissions properly

## Project Structure

```
reqtracker/
├── src/reqtracker/         # Main package code
│   ├── init.py             # Public API and package metadata
│   ├── cli.py              # Command-line interface
│   ├── tracker.py          # Main coordination logic
│   ├── static_analyzer.py  # AST-based analysis
│   ├── dynamic_tracker.py  # Runtime tracking
│   ├── generator.py        # Requirements generation
│   ├── config.py           # Configuration management
│   ├── mappings.py         # Import-to-package mapping
│   └── utils.py            # Utility functions
├── tests/                  # Test suite (204 tests)
├── docs/                   # Documentation
├── examples/               # Usage examples
└── pyproject.toml          # Project configuration and metadata
```

## Getting Help

- **Issues**: Create GitHub issue for bugs or feature requests
- **Questions**: Use GitHub Discussions for general questions
- **Documentation**: Check README.md and inline docstrings
- **Examples**: See examples/ directory for usage patterns

## Release Process

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Create release PR
4. Tag release after merge
5. Publish to PyPI

Thank you for contributing to reqtracker!
