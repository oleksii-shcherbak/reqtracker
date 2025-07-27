# reqtracker CLI Documentation

Comprehensive guide to the reqtracker command-line interface.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Commands](#commands)
- [Options](#options)
- [Configuration](#configuration)
- [Examples](#examples)
- [Workflows](#workflows)
- [Troubleshooting](#troubleshooting)

## Installation



After installation, the  command will be available globally.

## Basic Usage

### Quick Start



### Command Structure



## Commands

### track

Track dependencies in Python source files.



**Arguments:**
-  - Directories or files to analyze (default: current directory)

**Options:**
-  - Analysis mode: static, dynamic, or hybrid (default: hybrid)
-  - Path to configuration file
-  - Enable verbose output
-  - Suppress output

**Examples:**


### generate

Generate requirements.txt from tracked dependencies.



**Options:**
-  - Output file path (default: requirements.txt)
-  - Comma-separated list of packages
-  - Version strategy: exact, compatible, minimum, none
-  - Omit timestamp header
-  - Don't sort packages alphabetically

**Examples:**


### analyze

Complete workflow: track dependencies and generate requirements.



**Arguments:**
-  - Directories or files to analyze

**Options:**
- Combines options from both  and  commands
-  - Analysis mode
-  - Output file path
-  - Version strategy
-  - Configuration file
-  - Verbose output
-  - Quiet mode

**Examples:**


## Global Options

These options can be used with any command:

-  - Show help message
-  - Show version information
-  - Enable debug logging
-  - Disable colored output

## Configuration

### Configuration File

reqtracker looks for configuration in these locations (in order):
1. Path specified with  option
2.  in current directory
3.  (in  section)
4.  in home directory

### Configuration Format

=:                cannot open `=' (No such file or directory)
requirements.txt: cannot open `requirements.txt' (No such file or directory)

### Command-Line Override

Command-line options override configuration file settings:



## Examples

### Basic Workflows



### Production Deployment



### Development Environment



### Excluding Patterns



### CI/CD Integration



### Multiple Requirements Files



## Workflows

### Library Development

For Python libraries, use minimum version constraints:



### Web Applications

For Django/Flask applications:



### Data Science Projects

For Jupyter notebooks and ML projects:



### Monorepo Management

For projects with multiple components:



## Advanced Usage

### Custom Import Mappings



### Verbose Output



### Debugging Issues



## Troubleshooting

### Common Issues

**No dependencies found:**
./tests/test_utils.py
./tests/test_generator.py
./tests/test_static_analyzer.py
./tests/__init__.py
./tests/test_dynamic_tracker.py
./tests/test_tracker.py
./tests/test_config.py
./tests/test_mappings.py
./tests/test_cli.py
./tests/test_init.py

**Missing packages:**


**Version conflicts:**


### Performance Optimization



### Platform-Specific Notes

**Windows:**


**macOS/Linux:**


## Best Practices

1. **Use configuration files** for complex projects
2. **Generate multiple requirements files** for different environments
3. **Use appropriate version strategies**:
   -  for production
   -  for development
   -  for libraries
4. **Exclude unnecessary files** to improve performance
5. **Commit requirements files** to version control
6. **Automate updates** with CI/CD pipelines
7. **Review changes** before committing updated requirements

## Exit Codes

-  - Success
-  - General error
-  - Configuration error
-  - File not found
-  - No dependencies found

## Environment Variables

-  - Default config file path
-  - Default analysis mode
-  - Enable verbose output
-  - Disable colored output

## See Also

- [API Documentation](../api/README.md) - Python API reference
- [Configuration Guide](../guides/configuration.md) - Detailed configuration options
- [Examples](../../examples/README.md) - Example projects and use cases
