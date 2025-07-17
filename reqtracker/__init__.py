# reqtracker/__init__.py

import sys
import os
import inspect
from pathlib import Path
import ast

# Internal modules (will be created later)
from . import config
from . import core
from . import output
from . import tracker  # For dynamic tracking

__version__ = "0.0.1"  # Initial version

_tracked_modules = set()  # To store dynamically tracked modules


def track(
        project_root: str = ".",
        output_file: str = "requirements.txt",
        mode: str = "hybrid",
        ignore_paths: list = None,
        exclude_modules: list = None,
        include_dev: bool = False,
        override_config: dict = None
):
    """
    Automatically detects and manages Python dependencies based on actual project usage.

    Args:
        project_root (str): The root directory of your project to scan. Defaults to current directory.
        output_file (str): The name of the requirements file to generate. Defaults to "requirements.txt".
        mode (str): The tracking mode ('static', 'dynamic', 'hybrid'). Defaults to 'hybrid'.
        ignore_paths (list): A list of paths (files or directories) to ignore during scanning.
        exclude_modules (list): A list of module names to explicitly exclude from tracking.
        include_dev (bool): Whether to include development dependencies (e.g., from a 'dev_requirements' section).
                            (Not implemented in initial version, but planned for config)
        override_config (dict): A dictionary to override .reqtracker.toml settings inline.
    """
    print(f"reqtracker: Starting dependency tracking in '{mode}' mode...")

    # Load configuration
    cfg = config.Config(
        project_root=project_root,
        output_file=output_file,
        mode=mode,
        ignore_paths=ignore_paths,
        exclude_modules=exclude_modules,
        include_dev=include_dev,
        inline_overrides=override_config
    )

    detected_dependencies = set()

    if cfg.mode in ["static", "hybrid"]:
        print("reqtracker: Running static analysis...")
        static_deps = core.find_dependencies_static(
            project_root=cfg.project_root,
            ignore_paths=cfg.ignore_paths,
            exclude_modules=cfg.exclude_modules
        )
        detected_dependencies.update(static_deps)
        print(f"reqtracker: Static analysis found {len(static_deps)} dependencies.")

    if cfg.mode in ["dynamic", "hybrid"]:
        print("reqtracker: Running dynamic analysis...")
        # For dynamic mode, we need to capture imports after this point.
        # This part is tricky as reqtracker.track() is called *after* initial imports.
        # A full dynamic mode might require reqtracker to be run as a wrapper for the
        # main script, or for the user to explicitly call track() at the very start.
        # For a simple demo, we'll assume the imports we want to track happen *after* track() is called.
        # A more robust dynamic mode might need a deeper integration or separate CLI.

        # For the demo, we'll just use the _tracked_modules which is populated by the hook
        # if reqtracker.track() enables it *before* other imports happen.
        # This will be more fully developed in the tracker.py

        # This part of the code needs careful design for dynamic tracking.
        # The simplest approach for a library call is to enable the hook, then the user's
        # script continues, and when the script exits (or track() is called at the end),
        # we process the collected modules.

        # However, your example shows `reqtracker.track()` at the end of `main.py`
        # meaning it needs to track imports that happened *before* it was called.
        # This implies a more complex `sys.meta_path` strategy that is always active
        # if reqtracker is installed and `track()` is then called to *report* them.

        # Let's simplify for now: `_tracked_modules` will be populated by the import hook,
        # which `track()` will enable. For *imports that happened before track()* we
        # might need to inspect `sys.modules`.

        # Placeholder for dynamic collection (will be populated by the import hook)
        initial_sys_modules_keys = set(sys.modules.keys())
        tracker.enable_dynamic_tracking(exclude_modules=cfg.exclude_modules)

        # In a real scenario, the user's application code would run here *after* enable_dynamic_tracking()
        # but since track() is called from main.py, we need to consider how to capture previous imports.
        # For simplicity in this first pass, the dynamic tracking will catch imports that occur *after* the hook is enabled.
        # To catch *all* imports, `reqtracker` would need to be run as a separate process or the hook
        # enabled much earlier, perhaps via an entry point script.

        # A practical approach for your example is to look at sys.modules at the end.
        # sys.modules contains all currently loaded modules.
        # We need to filter out built-in, standard library, and current project modules.

        dynamic_deps = tracker.get_tracked_modules()  # Gets modules tracked by the hook

        # Also, consider modules already loaded before the hook was active
        # This is where it gets tricky: how to identify *third-party* modules already loaded?
        # A heuristic: compare sys.modules before and after track() is called, or at least
        # filter out stdlib and local modules.

        # Let's refine this: When `track()` is called, we can look at `sys.modules`.
        # Any module in `sys.modules` that is not a standard library module or part of the project
        # could be considered a dependency.

        # To make this robust, we need a list of standard library modules.
        # sys.stdlib_module_names (Python 3.10+) or a manually curated list for older Python versions.

        # For a truly robust dynamic mode that catches everything including imports *before* track()
        # is called, the hook needs to be active from the start of the Python interpreter,
        # which is typically done by running a script through `python -m reqtracker.runner`
        # or by having an executable.

        # For the simplicity of this library, we will focus on *capturing imports that happen while
        # the hook is active* or by analyzing `sys.modules` at the point `track()` is called,
        # filtering out non-third-party modules.

        # Let's implement a simple `get_current_third_party_modules`
        dynamic_deps.update(core.get_current_third_party_modules(exclude_modules=cfg.exclude_modules))

        detected_dependencies.update(dynamic_deps)
        print(f"reqtracker: Dynamic analysis found {len(dynamic_deps)} dependencies.")

        tracker.disable_dynamic_tracking()  # Clean up hook

    # Filter out excluded modules and standard library modules (again, just in case)
    final_dependencies = core.filter_dependencies(detected_dependencies, cfg.exclude_modules)

    print(f"reqtracker: Total unique dependencies found: {len(final_dependencies)}")

    # Write to output file
    output.write_requirements_file(cfg.output_file, sorted(list(final_dependencies)))
    print(f"reqtracker: Dependencies written to '{cfg.output_file}'.")

# Initialize configuration and core functionality when the module is imported
# This ensures that Config and other internal modules are set up.
# Note: The dynamic tracking hook itself should probably be enabled only when reqtracker.track() is called,
# or for a more "always on" dynamic mode, it would need a different entry point.

# For the dynamic mode as described in your prompt, where `reqtracker.track()` is called
# *after* other imports, we rely on analyzing `sys.modules`.
# The `tracker` module will handle the import hook if we go with the "active during execution" approach.
