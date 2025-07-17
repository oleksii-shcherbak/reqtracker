# reqtracker/__init__.py

import sys
import os
import inspect
from pathlib import Path
import ast

from . import config
from . import core
from . import output
from . import tracker

__version__ = "0.0.1"

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
        override_config (dict): A dictionary to override .reqtracker.toml settings inline.
    """
    print(f"reqtracker: Starting dependency tracking in '{mode}' mode...")

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
        tracker.enable_dynamic_tracking(exclude_modules=cfg.exclude_modules)

        dynamic_deps = tracker.get_tracked_modules()
        dynamic_deps.update(core.get_current_third_party_modules(exclude_modules=cfg.exclude_modules))

        detected_dependencies.update(dynamic_deps)
        print(f"reqtracker: Dynamic analysis found {len(dynamic_deps)} dependencies.")

        tracker.disable_dynamic_tracking()

    final_dependencies = core.filter_dependencies(detected_dependencies, cfg.exclude_modules)

    print(f"reqtracker: Total unique dependencies found: {len(final_dependencies)}")

    output.write_requirements_file(cfg.output_file, sorted(list(final_dependencies)))
    print(f"reqtracker: Dependencies written to '{cfg.output_file}'.")
