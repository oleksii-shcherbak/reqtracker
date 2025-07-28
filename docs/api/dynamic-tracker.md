# Dynamic Tracker API

The `dynamic_tracker` module provides runtime dependency tracking by monitoring import statements during code execution.

## Overview

Dynamic tracking captures dependencies that are actually imported during runtime, providing insights into conditional imports, lazy loading, and runtime-dependent packages that static analysis might miss.

## Classes

### `ImportHook`
Custom import hook that captures module imports during execution.

### `DynamicTracker`
Main class for dynamic dependency tracking.

#### Methods

##### `__init__(exclude_stdlib: bool = True)`
Initialize the dynamic tracker.

##### `start_tracking()`
Begin capturing import statements.

##### `stop_tracking()`
Stop capturing import statements and clean up.

##### `get_imports() -> Set[str]`
Get set of tracked package names.

##### `track_execution(code: str, globals_dict: Optional[Dict] = None) -> Set[str]`
Execute code and track its imports.

### `TrackingSession`
Context manager for convenient dynamic tracking.

## Integration with Main API

Dynamic tracking is automatically used when mode='dynamic' or mode='hybrid'.

## Performance Considerations

- Dynamic tracking adds runtime overhead
- Best suited for smaller scripts or specific modules
- Use hybrid mode for balance of accuracy and performance
