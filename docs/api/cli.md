# CLI Module API

The cli module implements the command-line interface for reqtracker.

## Commands

### reqtracker track
Track dependencies in source files.

### reqtracker generate
Generate requirements.txt from tracked packages.

### reqtracker analyze
Complete workflow - track and generate requirements.

## Implementation

Built using Click framework with support for:
- Multiple subcommands
- Configuration file loading
- Verbose and quiet modes
- Custom output paths

See [CLI Documentation](../cli/README.md) for detailed usage information.
