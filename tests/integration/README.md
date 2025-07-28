# Integration Tests for reqtracker

This directory contains end-to-end integration tests that verify reqtracker works correctly with real Python projects.

## Test Structure
- `test_real_projects.py` - Tests against real Python project structures
- `test_cli_integration.py` - CLI command integration tests
- `test_performance.py` - Performance and scalability tests
- `test_cross_platform.py` - Cross-platform compatibility tests

## Test Scenarios

### Small Projects (< 10 files)
- Basic Python script with few dependencies
- Single module with standard library only
- Small package with common dependencies

### Medium Projects (100+ files)
- Django application structure
- Flask web application
- Data science project with notebooks

### Large Projects (500+ files)
- Complex dependency trees
- Projects with circular imports
- Performance testing scenarios

## Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration -v

# Run specific test category
pytest tests/integration/test_performance.py -v

# Run with performance profiling
pytest tests/integration --profile
```

## Performance Benchmarks

Target performance metrics achieved:
- Small project: < 2 seconds (10 files)
- Medium project: < 10 seconds (100 files)
- Large project: < 30 seconds (500+ files)
- Memory usage: < 100MB for 1000 files

## Test Implementation

All integration tests use **dynamic project generation** rather than static fixtures. This allows for:
- Flexible test scenarios
- Consistent test environments
- Easy maintenance and updates
- Comprehensive edge case coverage

The tests create temporary Python projects programmatically and verify that reqtracker correctly analyzes them across different modes and configurations.
